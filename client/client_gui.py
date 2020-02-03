'''
Created on 20. 2. 2018

@author: ja600088
http://tkinter.programujte.com/grid.htm
'''


from tkinter import *
from tkinter import messagebox
import client.chat_client
import logging

logging.basicConfig(level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

REFRESH_TIME = 5000 # in milliseconds

class Application(Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.goodName = "unknown"
        self.create_widgets()
        
                
    def updateText(self, txt):
        self.chatText.config(state=NORMAL)
        self.chatText.delete(1.0, END)
        self.chatText.insert(END, txt)
        self.chatText.config(state=DISABLED) 
        
    def onChatroomSelected(self, val):
        logging.debug("Selected value is:" + val)
        self.updateText(client.chat_client.getChatFromRoom(val))
        
    def onMessageEntered(self, event):
        logging.debug ("Message: " + self.nameEntry.get() + " / " + self.messageEntry.get())
        client.chat_client.sendMessage(self.nameEntry.get(), self.selectedChatroom.get(), self.messageEntry.get())
        self.msg.set("")
        self.onRefresh()
        
    def onNameEntered(self, event):
        logging.debug ("Name: " + self.nameEntry.get())
        if " " in self.nameEntry.get() or self.nameEntry.get() == "":
            messagebox.showinfo("Error", "Name cannot contain spaces or be empty")
            self.name.set(self.goodName)
        else:
            self.goodName = self.nameEntry.get()
             
        
    def onRefresh(self):
        self.updateText(client.chat_client.getChatFromRoom(self.selectedChatroom.get()))
        
    def periodicRefresh(self):
        logging.debug ("Periodic refresh called...")
        self.onRefresh()
        self.master.after(REFRESH_TIME, self.periodicRefresh)

    def create_widgets(self):
        
        self.selectedChatroom = StringVar()  
        rooms = client.chat_client.getChatroomList()
        self.selectedChatroom.set(rooms[0])      # initial value
        chatroomOption = OptionMenu(self.master, self.selectedChatroom, *rooms, command=self.onChatroomSelected)
        chatroomOption.grid(row=0, column=0, padx=5, pady=5, sticky=W+E)
        
        nameLabel = Label(text="Your name:")
        nameLabel.grid(row=0, column=1, padx=5, pady=5)
        
        self.name = StringVar()
        self.name.set(self.goodName)
        self.nameEntry = Entry(textvariable=self.name)
        self.nameEntry.grid(row=0, column=2, padx=5, pady=5, sticky=W+E)
        self.nameEntry.bind('<Return>', self.onNameEntered)
        
        msgLabel = Label(text="Message to the group: (ENTER to send)")
        msgLabel.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=W)
        
        self.msg = StringVar()
        self.msg.set('no message')
        self.messageEntry = Entry(textvariable=self.msg)
        self.messageEntry.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=W+E)
        self.messageEntry.bind('<Return>', self.onMessageEntered)
        
        self.chatText = Text()
        self.chatText.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=W+E+N+S)
        self.updateText("txt")
        
        refreshButton = Button(text="Refresh", command=self.onRefresh)
        refreshButton.grid(row=4, column=1, padx=5, pady=5)
        

if __name__ == '__main__':
    root = Tk()
    root.title("Chat client GUI v1.0")
    app = Application(master=root)
    app.periodicRefresh()
    app.mainloop()
