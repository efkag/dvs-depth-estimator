from dv import AedatFile
import os 
import cv2
import numpy as np

def load_dvs_data(path):
    print('loading from: ', path)
    with AedatFile(path) as f:
        # list all the names of streams in the file
        print(f.names)
        # events['timestamp'], events['x'], events['y'], events['polarity']
        events = np.hstack([packet for packet in f['events'].numpy()])
    return events
