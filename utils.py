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

def infer_img_dim(data):
    x_max = 0
    y_max = 0
    for event in data:
        if event[1] > x_max:
            x_max = event[1]
        if event[2] > y_max:
            y_max = event[2]
    return (x_max,y_max)

def get_integrated_img(data,idx0,idx1,x_max,y_max):
    X_DIM = 1
    Y_DIM = 2
    POLARITY_DIM = 3

    # note: Numpy array dim are transpose of image dim
    img = np.zeros((y_max+1,x_max+1))
    for event in data[idx0:idx1]:
        if event[POLARITY_DIM] ==1:
            img[event[Y_DIM],event[X_DIM]] = 1
        elif event[POLARITY_DIM]==0:
            img[event[Y_DIM],event[X_DIM]] = -1         
        else:
            print("hallo")
            
    return img    
    





    
