import threading

warehouseAmount = 0
MAX = 1000000

def producer():
    global warehouseAmount
    for i in range(1, MAX):
        warehouseAmount = warehouseAmount + 1
    print ("producer finished", warehouseAmount)
    
def consumer():
    global warehouseAmount
    for i in range(1, MAX):
        warehouseAmount = warehouseAmount - 1
    print ("consumer finished", warehouseAmount)

    
if __name__ == '__main__':
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()    
    t1.join()
    t2.join()
    print ("Final warehouseAmount =", warehouseAmount)
    