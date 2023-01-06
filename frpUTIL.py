from threading import Thread
import urllib.request as ureq
import os,requests,sys,platform
from custlang import *
import subprocess,time
from logging import basicConfig,getLogger
import logging
basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] -> %(message)s",level=logging.INFO)
frp_log=getLogger(name="FRP UTIL")

frpver="0.46.0"
sysmap={
    "Linux":"linux",
    "Windows":"windows",
    "Darwin":'darwin'
}
fsuffix={
    "zip":".zip",
    "targz":".tar.gz"
}
#alivelist=[]
aliveFrpc={}
# server addr; server port; tunnel code; inst name; local ip; remote ip; remote port
ini_template='''
[common]
server_addr = {}
server_port = {}
token = {}


[{}]
type = tcp
local_ip = {}
local_port = {}
remote_port = {}
'''
#print(platform.architecture())
'''
Config & frpc dir:
for windows: current dir/data
for mac/linux: ~/.config/mossfrp-pyc
'''
data_root=""
if platform.system()=='Windows':
    data_root="./data"
    frp_log.info(langmap["sys_type"]+"Windows")
else:
    data_root="~/.config/mossfrp-pyc"
    frp_log.info(langmap["sys_type"]+"Linux or Mac") # write detail later
frpc_root=data_root+"/frpcs"
#print(data_root)
if not os.path.exists(data_root):
    os.makedirs(data_root,exist_ok=True)
#print(platform.machine())
def ensureFrpc(inst_name:str):
    inst_dir=frpc_root+"/"+inst_name
    if not os.path.exists(inst_dir):
        os.makedirs(inst_dir,exist_ok=True)
    execF=f"{inst_dir}/frpc-{inst_name}"
    if not (os.path.isfile(execF+'.exe') or os.path.isfile(execF)): # download frpc
        systype=sysmap[platform.platform().split('-')[0]]
        if platform.system()=='Windows':
            arc_fmt="zip"
        else: arc_fmt="targz"
        s_arch=platform.machine().lower()
        dl_uri=f"https://ghproxy.com/https://github.com/fatedier/frp/releases/download/v{frpver}/frp_{frpver}_{systype}_{s_arch}{fsuffix[arc_fmt]}"
        #print(dl_uri)
        frp_log.info(langmap["dl_from"]+dl_uri)
        local_arc=execF+fsuffix[arc_fmt]
        #ureq.urlretrieve(dl_uri,local_arc)
        os.system("curl "+dl_uri+" -o "+local_arc)
        #os.system(cmdmap[arc_fmt]+local_arc)
        if arc_fmt=="zip":
            precpfile=""
            import zipfile,shutil
            archive = zipfile.ZipFile(local_arc,mode='r')
            for file in archive.namelist():
                if file.endswith('c.exe'):
                    archive.extract(file, inst_dir)
                    precpfile=inst_dir+"/"+file
            shutil.move(precpfile,execF+'.exe')
        if arc_fmt=="targz":
            precpfile=""
            import shutil
            shutil.unpack_archive(local_arc,inst_dir,"gztar")
            shutil.move(inst_dir+"/*/frpc",execF)
    return execF

#frp_log.info(ensureFrpc("test"))
class FrpcSubProc(Thread):
    def __init__(self,instname:str,frpcF:str,iniF:str):
        Thread.__init__(self)
        self.frpc_exe=frpcF
        self.instname=instname
        self.conf_ini=iniF
    def run(self):
        global aliveFrpc
        if self.instname in aliveFrpc.keys():
            frp_log.error(langmap["duplicate_inst"].format(self.instname,aliveFrpc[self.instname])) #self.frpc_exe))
            return
        proc=subprocess.Popen([self.frpc_exe,'-c',self.conf_ini])
        time.sleep(1)
        if proc.poll()==None:
            frp_log.info(langmap["frpc_start"].format(self.instname,self.frpc_exe))
        else:
            frp_log.warn(langmap["frpc_stop_fast"].format(self.instname,self.frpc_exe))
            return
        #global alivelist
        #alivelist.append(proc.pid)
        while True:
            polstat=proc.poll()
            if polstat!=None:
                frp_log.info(langmap["frpc_exit"].format(self.instname,proc.pid,polstat))
                del(aliveFrpc[self.instname])
                return
            if proc.pid not in aliveFrpc.values():
                frp_log.info(langmap["frpc_mark_not_alive"].format(self.instname))
                proc.terminate()
                return

def writeINIAndStart(inst_name:str,tunnel:dict):
    inst_dir=frpc_root+"/"+inst_name
    execF=f"{inst_dir}/frpc-{inst_name}"
    iniF=f"{inst_dir}/frp-{inst_name}.ini"
    newconf=ini_template.format(
        tunnel["node"]+".mossfrp.cn",
        tunnel["port"],
        tunnel["code"],
        inst_name,
        tunnel["localIP"],
        tunnel["localPort"],
        tunnel["remotePort"]
    )
    with open(iniF,mode="w",encoding='UTF-8') as ini:
        frp_log.debug("Opening and writing conf "+iniF)
        ini.write(newconf)
    FrpcSubProc(inst_name,execF,iniF).start()