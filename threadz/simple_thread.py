'''
Created on 17. 2. 2018

@author: ja600088
'''
import threading
import time
import random

def bitcoinMiner(thread_id):
    print("Miner", thread_id,"started.")
    time.sleep(random.randint(1,4))
    print("Miner", thread_id,"finished.")
    
if __name__ == '__main__':
    threads = []
    for i in range(5):
        t = threading.Thread(target=bitcoinMiner, args=(i,))
        threads.append(t)
        t.start()