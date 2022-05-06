from dv import AedatFile
import os 
import cv2
import numpy as np
from PIL import Image 

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
    
def transform_to_frames(data,f_name,ev_per_frame=120,x_max=640, y_max=480,fps=60):
    # calcaulate how many blocks you can form
    n_events = len(data)
    n_frames = int(np.floor(n_events/ev_per_frame))
    #fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(f_name,fourcc, fps, (x_max,y_max))
    # setup
    idx0 = 0
    idx1 = idx0+ev_per_frame
    # for each block
    for i in range(n_frames):
        # get integrated image
        np_img = get_integrated_img(data, idx0, idx1, x_max=x_max-1, y_max=y_max-1)
        # create rgb channel version
        r_channel = ((np_img == -1).astype(int))*255
        g_channel = ((np_img == 1).astype(int))*255
        b_channel = ((np_img == 1).astype(int))*0
        cv_img = np.stack([r_channel,g_channel,b_channel],axis=2)
        cv_img = cv_img.astype('uint8')
        video.write(cv_img)
        # attach to video
        idx0 = idx1
        idx1 = idx1+ev_per_frame
        if i%fps ==0:
            print("Seconds processed: {}".format(i/fps))
    video.release()
    print("Video has been saved as {}".format(f_name))

def get_frames(data, ev_per_frame=120, x_max=640, y_max=480,fps=60):
    frames = []    
    # calcaulate how many blocks you can form
    n_events = len(data)
    n_frames = int(np.floor(n_events/ev_per_frame))
    # setup
    idx0 = 0
    idx1 = idx0+ev_per_frame
    # for each block
    for i in range(n_frames):
        # get integrated image
        np_img = get_integrated_img(data, idx0, idx1, x_max=x_max-1, y_max=y_max-1)
        # create rgb channel version
        r_channel = ((np_img == -1).astype(int))*255
        g_channel = ((np_img == 1).astype(int))*255
        b_channel = ((np_img == 1).astype(int))*0
        cv_img = np.stack([r_channel,g_channel,b_channel],axis=2)
        cv_img = cv_img.astype('uint8')
        frames.append(cv_img)
        # attach to video
        idx0 = idx1
        idx1 = idx1+ev_per_frame
        if i%fps ==0:
            print("Seconds processed: {}".format(i/fps))
    return frames