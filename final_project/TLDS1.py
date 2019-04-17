import sys
import socket as mysoc
import re
import hmac
import pickle
import json

try:
    tlds1 = mysoc.socket(mysoc.AF_INET,mysoc.SOCK_STREAM)
    print("[TLDS]: TLDS server socket created")
except mysoc.error as err:
    print('[TLDS]{} \n'.format("TLDSserver socket open error ", err))

server_binding = ('',51112)
tlds1.bind(server_binding)
tlds1.listen(2)
crsd,addr=tlds1.accept()

cmpStr = ""
with open("PRO3-KEY1.txt", 'r') as f:
    Str = f.read().strip().split()
    cmpStr = "".join(Str)
f.close()

# name will be compared with cnct variable which is come from Client
name = ""
ip = ""
flag = ""
temp = ""
tempList = []

with open("PRO3-TLDS1.txt", 'r') as f:
    while True:
        Domain = f.readline().splitlines()
        if not Domain:
            break
        Str = "".join(Domain)
        List = Str.split()
        tempList.append(List)
f.close()

#print(tempList)
#print(tempList[0][0])
# 0 name 1 ip 2 flag

while True:
    chal = crsd.recv(1024).decode('utf-8')
    #print(chal)
    if not chal:
        break
    
    #print(cmpStr) 
    TLDS1digest = hmac.new(cmpStr.encode('utf-8'), chal.encode('utf-8')) 
    sendData = pickle.dumps(TLDS1digest.hexdigest())
    #print(TLDS1digest.hexdigest())
    crsd.send(sendData)
     
    tl,addr=tlds1.accept()
    _cnct = tl.recv(50).decode('utf-8')
    #print(_cnct)
   # tl.send("one".encode('utf-8'))
   
    List = _cnct.split(" ")
    cnct = "".join(List)
   # print(cnct)

    
    for a,b,c in tempList:
        if cnct == a:
    #        print("find")
            name = a
            ip = b
            flag = c
            temp = name+"  "+ip+" "+flag
            break
        else:
            temp = "Error: HOST NOT FOUND"
    tl.send(temp.encode('utf-8'))


tlds1.close()
exit()
