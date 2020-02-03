'''
Created on 19. 2. 2018

@author: ja600088
'''
from server.ChatRoom import ChatRoom
import logging

logging.basicConfig(level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)


names = ['boys', 'girls', 'singles_only', 'chamber_of_secrets']
rooms = []

def init():
    for n in names:
        rooms.append(ChatRoom(n))
        
def getRoomWithName(name):
    try:
        index = names.index(name)   # what is the number of the chatroom?
    except Exception as e:
        logging.exception(e)        # Unknown name
        return None
    else:
        return rooms[index]
    
def handleMessage(message):
    response = 'ERROR Unknown command'
    
    if message.startswith('GETROOMS'):
        response = 'OK'
        for room in names:
            response = response + ' ' + room
    
    message_words = message.split(" ")
    
    if message_words[0] == 'GET':  # e.g. GET boys
        logging.debug("Arriving command: " + message)
        room = getRoomWithName(message_words[1])
        logging.debug("Selected room: " + message_words[1] + " is " + room.getRoomName())
        if room == None:
            response = 'ERR Room "' + message_words[1] + '" does not exist.'
        else:
            response = 'OK ' + room.getLastTexts()

    if message_words[0] == 'POST':
        room = getRoomWithName(message_words[1])
        if room == None:
            response = 'ERR Room "' + message_words[1] + '" does not exist.'
        else:
            room.appendPost(message[5:])
            response = 'OK'
        
    return response

if __name__ == '__main__':
    init()
    print (handleMessage('GETROOMS'))
    print(getRoomWithName('boys').getRoomName())
    print(handleMessage('POST boys Jan: Hello.'))
    print(handleMessage('POST boys Jan: Hello2.'))
    print(handleMessage('GET boys'))
    print(handleMessage('GET xxx'))
    print('------- End of test -------------')