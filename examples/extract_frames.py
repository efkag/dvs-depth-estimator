from ctypes import util
import sys
import os
path = os.path.join(os.path.dirname(__file__), os.pardir)
fwd = os.path.dirname(__file__)
sys.path.append(path)

from matplotlib import pyplot as plt
import utils

path = os.path.join('/', 'home', 'efkag', 'dvs-depth-estimator', 'test.aedat4')
data = utils.load_dvs_data(path)

frame_gen  = utils.gen_frames(data)
plt.imshow(next(frame_gen))
plt.show()
