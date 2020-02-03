'''
Created on 15. 2. 2018

@author: ja600088
https://pythonspot.com/python-network-sockets-programming-tutorial/
https://docs.python.org/3/howto/sockets.html
'''

import socket
 
TCP_IP = '127.0.0.1' # use fully qualified name: server will be visible from inet
TCP_PORT = 8063 # ports under 1024 are for privileged applications only
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
 
def simple_server():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # internet, TCP
    serverSocket.bind((TCP_IP, TCP_PORT))
    serverSocket.listen(1) # backlog = 1 = maximum queued connections
 
    conn, addr = serverSocket.accept()

    print ("Connection address: ", addr)
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print ("Received data:", data)
        conn.send(data.upper())  # echo in capital letters
    conn.close()

if __name__ == '__main__':
    simple_server()
    
    
