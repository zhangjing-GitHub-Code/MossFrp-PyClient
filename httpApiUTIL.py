import requests,json
from custlang import *
APIROOTURI="public.ghs.wiki:7001"
del(dict)
"""
Returns:
return[0]
	-1: http error
	1: no error, request sucess
	other: status code def by MossFrp
return[1:]
	if success, the returned dict
	if error, the err msg mapping
"""
token=""
errmap={
	400: langmap["argv_miss_wrong"],
	401: langmap["token_err"],
	423: langmap["blacklisted"]
}

sp_map={
	"login":{ 404: langmap["user_login_fail"] },
	"usercode": {},
	"nodelist": {},
	"rmcode": {},
	"createcode": {},
	"verifycode": {},
	"reg": {},
	"infoupdate": {},
	"userinfo": {},
	"coderenewal": {},
	"codeaddband": {}
}

def reqAPI(string:type,dict:cargs):
    global token
    api_req_root="http://"+APIROOTURI+"/API"
    newargs=cargs.copy()
    newargs["type"]=type
    if type!="login":
        newargs["token"]=token
    req=requests.get(api_req_root,data=newargs)
    if req.status_code!=200:
        return -1,"HTTP Protocol Error"
    retdat=json.loads(req.text)
    resstat=retdat["status"]
    if(resstat==200): return (1,resstat)
    if resstat in errmap.keys():
        return_info=errmap[resstat]
    elif resstat in sp_map[type].keys():
        return_info=sp_map[type][resstat]
    return (resstat,return_info)

def m_login(loginType,acnt,passwd):
    data=dict()
    data["loginType"]=loginType
    data["password"]=passwd
    data["account"]=acnt
    r=reqAPI("login",data)