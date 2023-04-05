import queue
import threading
import matplotlib.pyplot as plt
from drawnow import drawnow
from buffer import push_to_queue
from process import pop_from_queue
import time

queue_size = 1000
data = "../stroop/meas/stroop_fnirs.csv"
plt.ion() # enable interactive figures
fig = plt.figure()
figdat = {"x": [], "y": [], "y2": []}


q = queue.Queue(queue_size)
push_t = threading.Thread(target=push_to_queue, args=(data, q))
pop_t = threading.Thread(target=pop_from_queue, args=(q,figdat))

push_t.start()
pop_t.start()

def draw_fig():
    plt.plot(figdat["x"][-100:], figdat["y"][-100:])
    plt.plot(figdat["x"][-100:], figdat["y2"][-100:])
    plt.ylim(1,3)

while True:
    time.sleep(1)
    drawnow(draw_fig)

push_t.join()
pop_t.join()



