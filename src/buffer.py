import csv
import queue
import time
import threading

queue_size = 1000 #can be set later

q = queue.Queue(queue_size)
data = "../stroop/meas/fnirs_data.csv"

def push_to_queue(file: str, q: queue.Queue, task_event: threading.Event, task_dat: list[tuple]) -> None:
    c = 0 # line offset
    hits = get_onsets("../stroop/meas/onsets_t.csv")
    miss = get_onsets("../stroop/meas/onsets_f.csv")

    with open(file, 'r') as csvfile:
        numreader = csv.reader(csvfile)
        for row in numreader:
            q.put((c/10, [float(cell) for cell in row]))
            if (c/10 in hits):
                task_dat.append((c/10, True))
                task_event.set()
            elif (c/10 in miss):
                task_dat.append((c/10, False))
                task_event.set()

            if (c % 5 == 0):
                time.sleep(0.46) #put 10 per second
            c += 1
    q.put(None) # signal that data is done

def get_onsets(file: str) -> list[float]:
    with open(file, 'r') as csvfile:
        read = csv.reader(csvfile)
        return [float(row[0]) for row in read]
