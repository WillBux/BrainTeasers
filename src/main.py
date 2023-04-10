import queue
import threading
import numpy as np
import matplotlib.pyplot as plt
from drawnow import drawnow
from argparse import ArgumentParser 

from buffer import push_to_queue
from process import pop_from_queue
from lsl import lsl_push_to_queue


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
    pop_t = threading.Thread(target=pop_from_queue, args=(q, figdat, output_updated), kwargs={'optodes': optodes})

    push_t.start()
    pop_t.start()

    def draw_fig():
        rot = -figdat["current"]-1
        plt.plot(np.roll(figdat["x"], rot), np.roll(figdat["y"], rot, axis=0)[:,2])
        plt.plot(np.roll(figdat["x"], rot), np.roll(figdat["y2"], rot, axis=0)[:,2])
        for task in task_dat:
            plt.axvline(x = task[0], color = 'b' if task[1] else 'r')
        # plt.ylim(1,3)

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
    print(f"Starting, with {args.test}")
    main(args.test)



