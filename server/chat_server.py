'''
Created on 15. 2. 2018

@author: ja600088
'''

import socket
import logging
import threading
import server.server_impl

logging.basicConfig(level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)
 
TCP_IP = '127.0.0.1'  # use fully qualified name: server will be visible from inet
TCP_PORT = 8062  # ports under 1024 are for privileged applications only
BUFFER_SIZE = 20  # Normally 1024, but we want fast response


def clientThread(conn, addr):
    logging.debug("Entering client thread...")
    conn.settimeout(2.0)                    # if there is delay >2s between packets throw exception
    msg = bytearray()
    try:
        while True:
            chunk = conn.recv(BUFFER_SIZE)  # check if there is something in the system buffers
            if not chunk: break             # last packet? get out of here!
            msg.extend(chunk)               # append to already delivered payloads/buffer
            if chunk.endswith(b'\x00'):     # end of command? Protocol says it ends chr(0)
                break                       # do not peek into buffer otherwise you will block!
        text = msg.decode()                 # convert the UTF-8 bytes to string. How do we know it is a UTF_8 string? Protocol says so...
    except Exception as e:
        logging.exception(e, exc_info=True)
    else:
        if text:
            logging.debug("Command from a client: " + text)
            if text.endswith(chr(0)):       # do not bother server implementation
                text = text[:-1]            # with transport details
            conn.sendall(server.server_impl.handleMessage(text).encode())
    finally:
        conn.close()
    logging.debug("Finishing client thread...")
    
 
def multi_server():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # internet, TCP
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # server socket
    serverSocket.bind((TCP_IP, TCP_PORT))
    
    client_threads = []
    
    while True:
        serverSocket.listen(1)  # backlog = 1 = maximum queued connections
        logging.debug("Waiting for an incoming connection from a client...")
        conn, addr = serverSocket.accept()
        t = threading.Thread(name='client-thread-' + str(addr), target=clientThread, args=(conn, addr,))
        client_threads.append(t)
        t.start()
        
if __name__ == '__main__':
    server.server_impl.init()
    multi_server()
    
    
