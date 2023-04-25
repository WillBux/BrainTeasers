import queue
from scipy import signal
import numpy as np
import threading
import csv

def pop_from_queue(q: queue.Queue, output, output_updated: threading.Event, optodes=104, log=False) -> None:
    # create filter
    fs = 25
    len = fs*8+1 # 8 seconds of data
    cutoffs = [0.12, 0.35, 0.7, 2.0, 3]
    cutoffs = [0.01, 0.2]
    taps = signal.firwin(8*fs+1, cutoffs, fs=fs, pass_zero=False)
    filter_buffer = np.zeros((len,optodes)) 
    filtered = np.zeros((optodes,))
    count = 0
    length = output["length"]
    csv_writer = None
    if log:
        dump_file = open("processed.csv", 'w', newline='')
        csv_writer = csv.writer(dump_file)

    while True:
        q_data = q.get()
        if q_data is None: # all data has been pushed, quit
            break 

        i, data = q_data

        filter_buffer[count%len, :] = data
        filtered = (filter_buffer * taps[:,np.newaxis]).sum(axis=0)
        taps = np.roll(taps, 1)

        output["x"][count%length] = i
        output["y"][count%length] = filtered[3]
        output["y2"][count%length] = data[3]
        output["current"] = count%length
        output_updated.set()

        if csv_writer is not None:
            csv_writer.writerow(np.insert(filtered, 0, i))

        count += 1
        # print(data)


