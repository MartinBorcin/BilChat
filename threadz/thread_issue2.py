import threading

lockForAccountA = threading.Lock()
lockForAccountB = threading.Lock()
accountA = 100
accountB = 100

MAX = 100000

def transferMoneyFromAtoB(amount):
    global lockForAccountA, lockForAccountB, accountA, accountB    
    lockForAccountA.acquire()
    accountA = accountA - amount
    lockForAccountB.acquire()
    accountB = accountB + amount
    lockForAccountB.release()
    lockForAccountA.release()

def transferMoneyFromBtoA(amount):
    global lockForAccountA, lockForAccountB, accountA, accountB
    lockForAccountB.acquire()
    accountB = accountB - amount
    lockForAccountA.acquire()
    accountA = accountA + amount
    lockForAccountA.release()
    lockForAccountB.release()    

def doTransfersFromAtoB():
    for i in range(1, MAX):
        transferMoneyFromAtoB(1)
    
def doTransfersFromBtoA():
    for i in range(1, MAX):
        transferMoneyFromBtoA(1)
    
if __name__ == '__main__':
    t1 = threading.Thread(target=doTransfersFromAtoB)
    t2 = threading.Thread(target=doTransfersFromBtoA)
    t1.start()
    t2.start()    
    t1.join()
    t2.join()
    print ("Transfers finished: ", accountA, "=", accountB)
    