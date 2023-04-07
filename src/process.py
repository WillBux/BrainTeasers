import queue
from scipy import signal
import numpy as np

def pop_from_queue(q: queue.Queue, output, optodes=104) -> None:
    # create filter
    fs = 10
    len = fs*8+1 # 8 seconds of data
    cutoffs = [0.12, 0.35, 0.7, 2.0, 3]
    taps = signal.firwin(8*fs+1, cutoffs, fs=fs)
    filter_buffer = np.zeros((len,optodes)) 
    filtered = np.zeros((optodes,))
    count = 0
    length = output["length"]
    while True:
        i, data = q.get() 
        if data is None: # all data has been pushed, quit
            break 

        filter_buffer[count%len, :] = data
        filtered = (filter_buffer * taps[:,np.newaxis]).sum(axis=0)
        taps = np.roll(taps, 1)

        output["x"][count%length] = i
        output["y"][count%length] = filtered[3]
        output["y2"][count%length] = data[3]
        output["current"] = count%length
        count += 1
        # print(data)


