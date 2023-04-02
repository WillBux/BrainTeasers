import csv
import numpy as np
import random as r

buffer_size = 100 #unsure

buffer = np.empty(buffer_size) #default type is float64
c = 0

with open('numbers.csv') as csvfile:
	numreader = csv.reader(csvfile, delimiter = ' ')
	for row in numreader:
		buffer[c] = row[0]
		c += 1
		sleep(r.uniform(.1,.5)) #sleep for random amount of time between 0.1 and 0.5 seconds for 2-10 samples per second 
