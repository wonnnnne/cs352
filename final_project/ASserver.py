import sys
import socket as mysoc
import re
import hmac
import pickle
import json
try:
    assd = mysoc.socket(mysoc.AF_INET,mysoc.SOCK_STREAM)
    print("[AS]: AS server socket created")
except mysoc.error as err:
    print('[AS]{} \n'.format("ASserver socket open error ", err))

server_binding = ('',51111)
assd.bind(server_binding)
assd.listen(1)
crsd,addr=assd.accept()

try:
    tlds = mysoc.socket(mysoc.AF_INET,mysoc.SOCK_STREAM)
    print("[TLDS]: TLDS server socket created")
except mysoc.error as err:
    print('[TLDS]{} \n'.format("TLDSserver socket open error ", err))

tlport = 51112
myaddr = "cpp.cs.rutgers.edu"
server_binding2 = (myaddr, tlport)
tlds.connect(server_binding2)

try:
    tlds2 = mysoc.socket(mysoc.AF_INET,mysoc.SOCK_STREAM)
    print("[TLDS2]: TLDS2 server socket created")
except mysoc.error as err:
    print('[TLDS2]{} \n'.format("TLDS2server socket open error ", err))

tlport2 = 51113
myaddr2 = "java.cs.rutgers.edu"
server_binding3 = (myaddr2, tlport2)
tlds2.connect(server_binding3)

keepDataForTLDS = []
tempList = []
while True:
    chal = crsd.recv(1024).decode('utf-8')
   # print(chal)
    if not chal:
        break
    
    crsd.send("got chal".encode('utf-8'))

    h = crsd.recv(1024)
    hexdig = pickle.loads(h)
    #print(hexdig)
    crsd.send("got hexdigest".encode('utf-8'))
    
    tlds.send(chal.encode('utf-8'))
    tlds2.send(chal.encode('utf-8'))

    ListCmp = []
    tl_h = tlds.recv(1024)
    tlHexdig = pickle.loads(tl_h)
    ListCmp.append(tlHexdig)
   # print(tlHexdig)
    #print(hexdig == tlHexdig)
    
    tl_h2 = tlds2.recv(1024)
    tlHexdig2 = pickle.loads(tl_h2)
    ListCmp.append(tlHexdig2)
   # print(tlHexdig2)
    #print(hexdig == tlHexdig2)

    if hexdig == ListCmp[0]:
        crsd.send("TLDS1".encode('utf-8'))
    elif hexdig == ListCmp[1]:
        crsd.send("TLDS2".encode('utf-8'))
    else:
        crsd.send("Error: HOST NOT FOUND".encode('utf-8'))

   # print(ListCmp)
   # keepDataForTLDS.extend([chal,hexdig])
   # tempList.extend([[chal,hexdig]])



tlds.close()
assd.close()
tlds2.close()
exit()
