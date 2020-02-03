'''
Created on 17. 2. 2018

@author: ja600088
'''
import socket
import time

TCP_IP = "109.246.243.198"
TCP_PORT = 8063
BUFFER_SIZE = 24
MESSAGE = "uppercase me" + '\r\n'

def simple_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE.encode())
    print("Send", MESSAGE.encode())
    while True:
        data = s.recv(BUFFER_SIZE)
        if not data: break
        print ("Received data:", data)
    s.close()
    
MESSAGES = ['Fr', 'agmented m', 'essage. ', 
            '123456789012345678901234567890 ', 'Finished by chr(0)' + chr(0)]

def simple_chat_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    for MESSAGE in MESSAGES:
        s.send(MESSAGE.encode())
        print("Send", MESSAGE.encode())
        while True:
            data = s.recv(BUFFER_SIZE)
            if not data: break
            print ("Received data:", data)
            if '\r\n' in data.decode(): break    # test for end of message
    s.close()

if __name__ == '__main__':
    simple_client()
    # simple_chat_client()
