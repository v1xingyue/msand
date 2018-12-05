#coding=utf-8

import setproctitle
import multiprocessing
import time
import logging
import os
import psutil
import random

try:
	from config import *
except Exception as ex:
	logging.error("no config.py found current dir")
	print(ex)
	exit()

#WORKER_COUNT = 2
#WORKER_INTERVAL = 2
#TASK_QUEUE_SIZE = 100
#HEALTH_CHECK_INTERVAL = 0.3
#def worker(interval,task_queue):
#	ppid = os.getppid()
#	setproctitle.setproctitle("msand worker")	
#	while True:
#		time.sleep(interval)
#		logging.info("worker process : %d , get task data from master : %s , task_queue size : %d ",os.getpid(),task_queue.get(),task_queue.qsize())
#		try:
#			psutil.Process(ppid)
#		except Exception as ex:
#			break
			
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

def newWorker(q):
	return multiprocessing.Process(target = worker ,args=(WORKER_INTERVAL,q,))

if __name__ == '__main__':
	task_queue = multiprocessing.Queue(TASK_QUEUE_SIZE)
	worker_count = WORKER_COUNT
	workers = []
	setproctitle.setproctitle("msand master")	
	for i in range(0,worker_count):
		p = newWorker(task_queue) 
		workers.append(p)
		p.start()
	
	while True:
		#task_queue.put(random_message())
		put_task_data(task_queue)
		n_worker = 0
		for w in workers:
			if not w.is_alive():
				workers.remove(w)
				logging.info("one worker die! remove it. worker_count  %d " % (len(workers)))
				n_worker += 1
		for i in range(0,n_worker):
			p = newWorker(task_queue) 
			workers.append(p)
			p.start()
			logging.info("one worker born!  worker_count  %d " % (len(workers)))
				
		time.sleep(HEALTH_CHECK_INTERVAL)

