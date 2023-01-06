import urllib.request as ureq
import os,requests,sys,platform
from custlang import *
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