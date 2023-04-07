import csv
import queue
import time

queue_size = 1000 #can be set later

q = queue.Queue(queue_size)
data = "../stroop/meas/fnirs_data.csv"

def push_to_queue(file: str, q: queue.Queue) -> None:
    c = 0 # line offset
    with open(file, 'r') as csvfile:
        numreader = csv.reader(csvfile)
        for row in numreader:
            q.put((c/10, [float(cell) for cell in row]))
            if (c % 5 == 0):
                time.sleep(0.46) #put 10 per second
            c += 1
    q.put(None) # signal that data is done
