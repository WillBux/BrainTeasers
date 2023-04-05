import csv
import queue
import time

queue_size = 1000 #can be set later

q = queue.Queue(queue_size)
data = "../stroop/meas/stroop_fnirs.csv"

def push_to_queue(file: str, q: queue.Queue) -> None:
    c = -40 # line offset
    with open(file, 'r') as csvfile:
        numreader = csv.reader(csvfile)
        for row in numreader:
            if c > 0: # goto first row of data
                q.put((int(row[0]), [float(cell) for i, cell in enumerate(row) if i !=0 and i < 105]))
                if (c % 5 == 0):
                    time.sleep(0.46) #put 10 per second
            c += 1
    q.put(None) # signal that data is done
