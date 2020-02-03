'''
Created on 15. 2. 2018

@author: ja600088
'''

import socket
import logging
import threading

logging.basicConfig(level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)
 
TCP_IP = '127.0.0.1' # use fully qualified name: server will be visible from inet
TCP_PORT = 8062 # ports under 1024 are for privileged applications only
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

def clientThread(conn, addr):
    logging.debug("Entering client thread...")
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        logging.debug("Received data: " + str(data))
        if "quit" in data.decode():
            conn.send("Good bye.".encode())
            break
        conn.send(data.upper())  # echo in capital letters
    logging.debug("Finishing client threadz...")
    conn.close()
 
def multi_server():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # internet, TCP
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # server socket
    serverSocket.bind((TCP_IP, TCP_PORT))
    
    client_threads = []
    
    while True:
        serverSocket.listen(1) # backlog = 1 = maximum queued connections
        logging.debug("Waiting for an incoming connection from a client...")
        conn, addr = serverSocket.accept()
        logging.debug("Connection address: " + str(addr))
        t = threading.Thread(name='client-thread-' + str(addr), target=clientThread, args=(conn, addr,))
        client_threads.append(t)
        t.start()
        
if __name__ == '__main__':
    multi_server()
    
    