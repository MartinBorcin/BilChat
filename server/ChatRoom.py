'''
Created on 19. 2. 2018

@author: ja600088
'''
class ChatRoom(object):

    def __init__(self, roomName):
        self.roomName = roomName
        self.roomChat = []

    def getRoomName(self):
        return self.roomName
    
    def appendPost(self, postText):
        self.roomChat.append(postText)
        
    def getLastTexts(self):
        return '\n'.join(self.roomChat)