'''
Created on 17. 2. 2018

@author: ja600088
'''
import socket
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

TCP_IP = "127.0.0.1"
TCP_PORT = 8062
BUFFER_SIZE = 24

def send_command_and_return_reply(command):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.sendall((command + chr(0)).encode())
    logging.debug("-- Sent command to the server: '" + command + "'")
    text = ''
    while True:
        chunk = s.recv(BUFFER_SIZE)
        if not chunk: break
        text += chunk.decode()
    s.close()
    logging.debug("-- Got response: " + text)    
    return text

def getChatroomList():
    response = send_command_and_return_reply("GETROOMS") # OK boys girls singles_only chamber_of_secrets
    if response.startswith("OK"):
        rooms = response.split(" ")
        return rooms[1:]
    else:
        logging.error("Rooms not defined?" + response)
        return ["None"]

def sendMessage(author, room, message):
    command = "POST " + room + ' ' + author + ': ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S ') + message
    response = send_command_and_return_reply(command)
    if response.startswith("OK"):
        logging.debug("[" + response + "] to: " + command)
    else:
        logging.error("[" + response + "] to: " + command)
 

def getChatFromRoom(room):
    command = "GET " + room
    response = send_command_and_return_reply(command)
    if response.startswith("OK"):
        logging.debug("[" + response + "] to: " + command)
    else:
        logging.error("[" + response + "] to: " + command)
    return response[3:]

if __name__ == '__main__':
    response = send_command_and_return_reply("GETROOMS")
    response = send_command_and_return_reply("GET boys")
    response = send_command_and_return_reply("POST boys jan: the first post in the boys room")
    response = send_command_and_return_reply("GET boys")
    response = send_command_and_return_reply("POST boys jan: the second post in the boys room")
    response = send_command_and_return_reply("GET boys")
    response = send_command_and_return_reply("GET xxx")
    response = send_command_and_return_reply("GETROOMS")
    
    print(getChatroomList())
    sendMessage("jva", "boys", "test msg")
    print(getChatFromRoom("boys"))