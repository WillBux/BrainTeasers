#! /usr/bin/env python3
import queue
import threading
import numpy as np
import matplotlib.pyplot as plt
from drawnow import drawnow
from argparse import ArgumentParser 
import pickle

from buffer import push_to_queue
from process import pop_from_queue
# from lsl import lsl_push_to_queue


def main(test: bool) -> None:
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
    task_dat = []

    task_event = threading.Event()
    output_updated = threading.Event()


    q = queue.Queue(queue_size)
    optodes = 104 if test else 48
    if test:
        push_t = threading.Thread(target=push_to_queue, args=(data, q, task_event, task_dat))
    else:
        push_t = threading.Thread(target=lsl_push_to_queue, args=(q,))
    pop_t = threading.Thread(target=pop_from_queue, args=(q, figdat, output_updated), kwargs={'optodes': optodes, 'log': True})

    push_t.start()
    pop_t.start()

    model = pickle.load(open("glm_model.pkl", 'rb'))

    def draw_fig():
        rot = -figdat["current"]-1
        x = np.roll(figdat["x"], rot)[1:-1]
        y = np.roll(figdat["y"], rot, axis=0)[1:-1,:]
        for i in range(optodes//2):
            plt.plot(x, i/10000+y[:,2*i], color="b")
            plt.plot(x, i/10000+y[:,2*i+1], color="r")
        for task in task_dat:
            if task[0] > x[0] and task[0] < x[-1]:
                if task[0] + 9.2 < x[-1] and task[0] - 1 > x[0]:
                    start = np.where(x == task[0]-1)[0][0]
                    end = np.where(x == task[0]+9)[0][0]
                    dat = y[start:end,:]
                    dat = dat.flatten()
                    pred = model.predict([dat])
                    plt.axvline(x = task[0], color = 'b' if pred[0] else 'r')
                else: 
                    plt.axvline(x = task[0], color = 'k')


        plt.xlim(x[0], x[-1])

    while True:
        output_updated.wait()
        output_updated.clear()
        drawnow(draw_fig)

    push_t.join()
    pop_t.join()


if __name__ == "__main__":
    parser = ArgumentParser(prog="BrainTeasers")
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()
    print("Testing Mode" if args.test else "Doin it live")
    main(args.test)



