from dv import AedatFile
import os 
import cv2
import numpy as np

path = os.path.join('/', 'home', 'efkag', 'capocaccia', 'dvsproj', 'test.aedat4')
print('loading: ', path)
with AedatFile(path) as f:
    # list all the names of streams in the file
    print(f.names)
    height, width = f['events'].size 
    # events['timestamp'], events['x'], events['y'], events['polarity']
    events = np.hstack([packet for packet in f['events'].numpy()])

    print(events[:10])

    # for frame in f['frames']:
    #     print(frame.timestamp)
    #     cv2.imshow('out', frame.image)
    #     cv2.waitKey(1)

