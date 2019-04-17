import numpy as mypy
import threading
import time
import random
import sys

import socket as mysoc

def client():
    try:
        cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
        
# Define the port on which you want to connect to the server
    port = 50007                
    sa_sameas_myaddr =mysoc.gethostbyname(mysoc.gethostname())
# connect to the server on local machine
    server_binding=(sa_sameas_myaddr,port)
    cs.connect(server_binding)
# receive data from the server
    data_from_server=cs.recv(100)
    print("[C]: Data received from server::  ",data_from_server.decode('utf-8'))
# send message to server
    buf="Hello, This is client"
    cs.send(buf.encode('utf-8'))
    print("[C]: Data sent to server\n")
# receive reversed data from server
    revbuf=cs.recv(100)
    print("[C]: Data received from server::  ",revbuf.decode('utf-8'))
# open and read file   
    with open('HW1test.txt','r') as fi:
        temp=fi.read()
# send to server 
    cs.send(temp.encode('utf-8'))
    print("[C]: Data sent to server::\n")
    print(temp)
# receive reversed data from server
    getfrom = cs.recv(1024)
    print("[C]: Data received from server::\n",getfrom.decode('utf-8'))
# write new file with reversed data    
    with open('HW1out.txt','w') as newfi:
        newfi.write(getfrom.decode('utf-8'))
    print("\n\n[C]: Data saved as ::  HW1out.txt ")

# close the cclient socket 
    cs.close() 
    exit()
   
t2 = threading.Thread(name='client', target=client)
t2.start()
input("Hit ENTER  to exit\n")
exit()

