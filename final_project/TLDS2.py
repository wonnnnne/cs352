import sys
import socket as mysoc
import re
import hmac
import pickle
import json

try:
    tlds2 = mysoc.socket(mysoc.AF_INET,mysoc.SOCK_STREAM)
    print("[TLDS2]: TLDS2 server socket created")
except mysoc.error as err:
    print('[TLDS2]{} \n'.format("TLDS2server socket open error ", err))

server_binding = ('',51113)
tlds2.bind(server_binding)
tlds2.listen(2)
crsd,addr=tlds2.accept()

cmpStr = ""
with open("PRO3-KEY2.txt", 'r') as f:
    Str = f.read().strip().split()
    cmpStr = "".join(Str)
f.close()



# name will be compared with cnct variable which is come from Client
name = ""
ip = ""
flag = ""
temp = ""
tempList = []

with open("PRO3-TLDS2.txt", 'r') as f:
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
    tlds2digest = hmac.new(cmpStr.encode('utf-8'), chal.encode('utf-8')) 
    sendData = pickle.dumps(tlds2digest.hexdigest())
    #print(tlds2digest.hexdigest())
    crsd.send(sendData)
     
    tl,addr=tlds2.accept()
    _cnct = tl.recv(50).decode('utf-8')
    #print(_cnct)
   # tl.send("one".encode('utf-8'))
   
    List = _cnct.split(" ")
    cnct = "".join(List)
    #print(cnct)

    
    for a,b,c in tempList:
        if cnct == a:
          #  print("find")
            name = a
            ip = b
            flag = c
            temp = name+"  "+ip+" "+flag
            break
        else:
            temp = "Error: HOST NOT FOUND"
    tl.send(temp.encode('utf-8'))


tlds2.close()
exit()
