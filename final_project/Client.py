import sys
import socket as mysoc
import re
import hmac
import pickle
import time

#[first socket]
try:
    cli = mysoc.socket(mysoc.AF_INET,mysoc.SOCK_STREAM)
    print('[C] client socket created')
except mysoc.error as err:
    print('{} \n'.format("socketopen error ",err))

#First Connect to RS server
rsport = 51111
sa_sameas_myaddr =mysoc.gethostbyname(mysoc.gethostname())
server_binding=(sa_sameas_myaddr,rsport)
cli.connect(server_binding)    

Key = ""
chal = ""
dom = ""

#set default output text file
with open('RESOLVED.txt','w') as w:
    w.write("")

with open("PRO3-HNS.txt", 'r') as f:
      
    while True:
        Domain = f.readline().splitlines()
        if not Domain:
            break
        #print(Domain)
        Str = "".join(Domain)
        List = Str.split(" ")
        key = List[0]
        chal = List[1]
        dom = List[2]
        
        cli.send(chal.encode('utf-8'))
        answer = cli.recv(1024).decode('utf-8') 
       # print(answer)

       # print(List)
       # print(key)
       # print(chal)

        d1 = hmac.new(key.encode('utf-8'), chal.encode('utf-8'))
        sendData = pickle.dumps(d1.hexdigest())
        cli.send(sendData)
       # print(d1.hexdigest())
        answer = cli.recv(1024).decode('utf-8') 
        #print(answer)
   
        choose = cli.recv(1024).decode('utf-8')
        print(choose)
        time.sleep(1)
       
#############################################################################
        #to connect to tlds1 and tlds2
        try:
            tlds = mysoc.socket(mysoc.AF_INET,mysoc.SOCK_STREAM)
           # print('[C] client socket created')
        except mysoc.error as err:
            print('{} \n'.format("socketopen error ",err))
        tldsport = 51112
        sa_sameas_myaddr1 ="cpp.cs.rutgers.edu"
        server_binding1=(sa_sameas_myaddr1,tldsport)
        tlds.connect(server_binding1)
        #print("req to TLDS")
        #tlds.send("got connect request".encode('utf-8'))
        try:
            tlds2 = mysoc.socket(mysoc.AF_INET,mysoc.SOCK_STREAM)
           # print('[C] client socket created')
        except mysoc.error as err:
            print('{} \n'.format("socketopen error ",err))
        tldsport2 = 51113
        sa_sameas_myaddr2 = "java.cs.rutgers.edu"
        server_binding2=(sa_sameas_myaddr2,tldsport2)
        tlds2.connect(server_binding2)
        #print("req to TLDS2")
        #tlds2.send("got connect request".encode('utf-8'))
#############################################################################

       # print(key +" " + chal + " " + dom)
        if choose == "TLDS1":
            tlds.send(dom.encode('utf-8'))
            get = tlds.recv(50).decode('utf-8')
            print(get)
            with open('RESOLVED.txt', 'a') as w:
                w.write(get)
                w.write('\n')
            w.close()
        elif choose == "TLDS2":
            tlds2.send(dom.encode('utf-8'))
            get1 = tlds2.recv(1024).decode('utf-8')
            print(get1)
            with open('RESOLVED.txt', 'a') as w:
                w.write(get1)
                w.write('\n')
            w.close()
        
        tlds2.close()
        tlds.close()


f.close()

cli.close()
exit()
