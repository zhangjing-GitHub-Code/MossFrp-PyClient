import os,requests,sys,platform
frpver="0.46.0"
sysmap={
    "Linux":"linux",
    "Windows":"windows",
    "Darwin":'darwin'
}
fsuffix={
    "zip":"zip",
    "targz":"tar.gz"
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
else:
    data_root="~/.config/mossfrp-pyc"
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
    if not os.path.isfile(execF): # download frpc
        systype=sysmap[platform.platform().split('-')[0]]
        if platform.system()=='Windows':
            arc_fmt="zip"
        else: arc_fmt="targz"
        s_arch=platform.machine().lower()
        dl_uri=f"https://ghproxy.com/https://github.com/fatedier/frp/releases/download/v{frpver}/frp_{frpver}_{systype}_{s_arch}.{fsuffix[arc_fmt]}"
        print(dl_uri)
        os.system("curl -O "+dl_uri)
        
ensureFrpc("test")