#!/usr/bin/python

import thread
import time
import socket 
import json

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print "%s: %s" % ( threadName, time.ctime(time.time()) )


def listener(this):
    host = '' 
    port = 50002
        
    backlog = 5 
    size = 1024 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog) 
    while 1: 
        client, address = s.accept() 
        data = json.loads(client.recv(size).strip())
        
        str = 'Adress: {0}, Action: "{1}", URI: {2}'.format(address, data['action'], data['uri']);
        print str;
        
        if data: 
            client.send(str) 
        client.close()
        
thread.start_new_thread( listener, ('',) )

while 1:
   pass