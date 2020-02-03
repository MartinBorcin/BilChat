'''
Created on 17. 2. 2018

@author: ja600088
'''
import threading
import time
import random
import logging

logging.basicConfig(level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

def bitcoinMiner():
    logging.debug("Started.")
    time.sleep(random.randint(2, 5))
    logging.debug("Finished.")
    
if __name__ == '__main__':
    threads = []
    for i in range(5):
        t = threading.Thread(name='Miner-' + str(i), target=bitcoinMiner)
        threads.append(t)
        t.start()
        
    logging.debug(" --- Finish ---")
        
    for t in threads:
        logging.debug("Joining thread " + str(t))
        t.join(2)
