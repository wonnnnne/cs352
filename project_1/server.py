import numpy as mypy
import threading
import time
import random
import sys

import socket as mysoc


def server():
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',50007)
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)
# send a intro  message to the client.  
    msg="Welcome to CS 352"
    csockid.send(msg.encode('utf-8'))

# receive data from client and reverse it
    buf=csockid.recv(100)
    print("[S]: Data received from client::  ",buf.decode('utf-8'))
    csockid.send((buf.decode('utf-8')[::-1]).encode('utf-8'))
    print("[S]: Data reversed and sent to client \n ")
# get data from server, reverse and send it
    get = csockid.recv(1024)
    print("[S]: Data received from client:: \n ",get.decode('utf-8'))
    print("[S]: Data reversed and sent to client \n ")
    csockid.send((get.decode('utf-8')[::-1]).encode('utf-8'))


# Close the server socket
    ss.close() 
    exit()

t1 = threading.Thread(name='server', target=server)
t1.start()
time.sleep(random.random()*5)
