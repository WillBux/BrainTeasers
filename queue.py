import csv
import numpy as np
import queue
import time

queue_size = 1000 #can be set later

q = queue.Queue(queue_size)
c = 0

with open('stroop_fnirs.csv') as csvfile:
	numreader = csv.reader(csvfile)
	for row in numreader:
		q.put(row)
		c += 1
		print(c)
		if (c % 5 == 0):
			time.sleep(1) #put 5 per second
		#maybe a break statement here of some sort?
	#print(q.get()) #function to pull off queue
