#   write flow file

#   According to the matlab code of Deqing Sun and c++ source code of Daniel Scharstein  
#   Contact: dqsun@cs.brown.edu
#   Contact: schar@middlebury.edu

#   Author: Johannes Oswald, Technical University Munich
#   Contact: johannes.oswald@tum.de
#   Date: 26/04/2017

#	For more information, check http://vision.middlebury.edu/flow/ 

import numpy as np
import os

#TAG_STRING = 'PIEH'
TAG_CHAR = np.array([202021.25], np.float32)
TAG_FLOAT = 202021.25

def read(file):

	assert type(file) is str, "file is not str %r" % str(file)
	assert os.path.isfile(file) is True, "file does not exist %r" % str(file)
	assert file[-4:] == '.flo', "file ending is not .flo %r" % file[-4:]
	f = open(file,'rb')
	flo_number = np.fromfile(f, np.float32, count=1)[0]
	assert flo_number == TAG_FLOAT, 'Flow number %r incorrect. Invalid .flo file' % flo_number
	w = np.fromfile(f, np.int32, count=1)
	h = np.fromfile(f, np.int32, count=1)
	#if error try: data = np.fromfile(f, np.float32, count=2*w[0]*h[0])
	#data = np.fromfile(f, np.float32, count=2*w*h)

	#raft version
	data = np.fromfile(f, np.float32, count=2 * int(w) * int(h))
	# Reshape data into 3D array (columns, rows, bands)
	flow = np.resize(data, (int(h), int(w), 2))	
	f.close()

	return flow

def write(flow, filename):

	assert type(filename) is str, "file is not str %r" % str(filename)
	assert filename[-4:] == '.flo', "file ending is not .flo %r" % file[-4:]

	height, width, nBands = flow.shape
	assert nBands == 2, "Number of bands = %r != 2" % nBands
	u = flow[: , : , 0]
	v = flow[: , : , 1]	
	assert u.shape == v.shape, "Invalid flow shape"
	height, width = u.shape

	f = open(filename,'wb')
	#f.write(TAG_STRING)
	f.write(TAG_CHAR)
	np.array(width).astype(np.int32).tofile(f)
	np.array(height).astype(np.int32).tofile(f)
	tmp = np.zeros((height, width*nBands))
	tmp[:,np.arange(width)*2] = u
	tmp[:,np.arange(width)*2 + 1] = v
	tmp.astype(np.float32).tofile(f)

	f.close()
    
if __name__=="__main__":
    #flow = read(r'D:\华理(new)\组会实验\flyingchairs_test2021-12-16\flow\00003_flow.flo')
    flow = read(r'D:\华理(new)\组会实验\scalarFlow_dataset\test1\result4\velocity_000100_wavr_axis0.flo')
    