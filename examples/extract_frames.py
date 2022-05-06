from ctypes import util
import sys
import os
path = os.path.join(os.path.dirname(__file__), os.pardir)
fwd = os.path.dirname(__file__)
sys.path.append(path)


import utils

path = os.path.join('/', 'home', 'efkag', 'dvs-depth-estimator', 'test.aedat4')
data = utils.load_dvs_data(path)

frames = utils.get_frames(data)
