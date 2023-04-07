import queue
import threading
import numpy as np
import matplotlib.pyplot as plt
from drawnow import drawnow
from buffer import push_to_queue
from process import pop_from_queue
import time

queue_size = 1000
data = "../stroop/meas/fnirs_data.csv"
plt.ion() # enable interactive figures
fig = plt.figure()
length = 600 # 60 seconds
optodes = 52*2
figdat = {"x": np.zeros((length,)), 
          "y": np.zeros((length, optodes)),
          "y2": np.zeros((length,optodes)),
          "current": 0,
          "length": length}


q = queue.Queue(queue_size)
push_t = threading.Thread(target=push_to_queue, args=(data, q))
pop_t = threading.Thread(target=pop_from_queue, args=(q,figdat))

push_t.start()
pop_t.start()

def draw_fig():
    rot = -figdat["current"]-1
    plt.plot(np.roll(figdat["x"], rot), np.roll(figdat["y"], rot, axis=0)[:,2])
    plt.plot(np.roll(figdat["x"], rot), np.roll(figdat["y2"], rot, axis=0)[:,2])
    # plt.ylim(1,3)

while True:
    time.sleep(1)
    drawnow(draw_fig)

push_t.join()
pop_t.join()



