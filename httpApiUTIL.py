import json
import urllib.request as ureq
from custlang import *
APIROOTURI="public.ghs.wiki:7001"
from logging import basicConfig,getLogger
import logging
basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] -> %(message)s",level=logging.INFO)
api_log=getLogger(name="API")
#del(dict)
"""
Returns:
return[0]
	-1: http error
	1: no error, request sucess
	other: status code def by MossFrp
return[1]
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

def reqAPI(rtype : str,cargs : dict[str,str]):
    global token
    api_req_uri="http://"+APIROOTURI+"/API?"
    #newargs=cargs.copy()
    newargs=cargs
    newargs["type"]=rtype
    if rtype!="login":
        newargs["token"]=token
    for itm in newargs.keys():
        api_req_uri+=itm
        api_req_uri+="="+newargs[itm]
        api_req_uri+="&"
    api_req_uri=api_req_uri[:-1]
    #api_log.info(api_req_uri)
    req=ureq.urlopen(api_req_uri)
    #print(req.raw)
    if req.getcode()!=200:
        return (-1,"HTTP Protocol Error: "+str(req.getcode()))
    retdat=json.loads(req.read()) # type: ignore
    #api_log.info(retdat)
    resstat=int(retdat["status"])
    if(resstat==200): return (1,retdat)
    if resstat in errmap.keys():
        return_info=errmap[resstat]
    elif resstat in sp_map[rtype].keys():
        return_info=sp_map[rtype][resstat]
    else: return_info=langmap["unknown_stat"] #"Unknown status"
    return (resstat,return_info)

def m_login(loginType:str,acnt:str,passwd:str):
    data={} #dict()
    data["loginType"]=loginType
    data["password"]=passwd
    data["account"]=acnt
    r=reqAPI("login",data) # r[0] return code; r[1] msg or data
    if r[0]==1:
        global token
        token=r[1]["token"] #type:ignore # we love pylance
        api_log.debug(str(r[0])+str(r[1]))
        return True
    else:
        api_log.warning(str(r[0])+": "+r[1])
        return False

def m_logout(): # just simply reset token?
    global token
    token=""

def userCodeList():
    r=reqAPI("userCode",{})
    if r[0]==1:
        api_log.debug(str(r[0])+str(r[1]))
        return True,list(r[1]["codeData"].values())
    else:
        api_log.warning(str(r[0])+": "+r[1])
        return False
