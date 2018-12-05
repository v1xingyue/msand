#coding=utf-8

import os
import logging
import psutil
import setproctitle
import time 
import random

WORKER_COUNT = 2
WORKER_INTERVAL = 2
TASK_QUEUE_SIZE = 100
HEALTH_CHECK_INTERVAL = 0.3

def random_message():
	messages = "hello world big simple go infomation nothing none gone start stop state".split(" ")
	i = random.randint(0,len(messages) - 1)
	return messages[i]

def worker(interval,task_queue):
	ppid = os.getppid()
	setproctitle.setproctitle("msand worker")	
	while True:
		time.sleep(interval)
		logging.info("worker process : %d , get task data from master : %s , task_queue size : %d ",os.getpid(),task_queue.get(),task_queue.qsize())
		try:
			psutil.Process(ppid)
		except Exception as ex:
			break
	
def put_task_data(task_queue):
	task_queue.put(random_message())
