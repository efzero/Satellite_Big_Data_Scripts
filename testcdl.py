#testcdl

from CDL_utils import *
import cv2
def test_cdl_box():
	cd = cdl_utils()
	cd.load_np_cdl('cdl_chicago.npy')
	min_lon = -89
	max_lon = -88
	min_lat = 41
	max_lat = 42
	dat = cd.get_cdl_box_data(min_lon, max_lon, min_lat, max_lat)
	img = np.zeros((int(-1/cd.x_step) + 5, int(1/cd.y_step) +5, 3))
	dict_ = {1: [0.0,255.0,255.0],5: [0.0,255.0,0.0],3: [0.0,0.0,0.0]}
	for i in range(dat.shape[0]):
		for j in range(dat.shape[1]):
			if dat[i,j] in dict_:
				img[i,j] = dict_[dat[i,j]]

	cv2.imwrite("cdl41428889.png", img)

	print(dat.shape)
	print(img.shape)
	return img

def test_cdl_proportion():
	cd = cdl_utils()
	cd.load_np_cdl('cdl_chicago.npy')
	min_lon = -89.0
	max_lon = -88.92
	min_lat = 41.89
	max_lat = 42
	dat = cd.get_cdl_box_data(min_lon, max_lon, min_lat, max_lat)
	unique_elements, counts_elements = np.unique(dat, return_counts=True)
	proportion = cd.get_proportion(dat)
	return proportion


def test_cdl_indices_geo():
	cd = cdl_utils()
	cd.load_np_cdl('cdl_chicago.npy')
	p1 = (41.5, -88)
	p2 = (41.7, -87.5)
	p3 = (40.7, -87.6)
	p4 = (40.6, -88.1)
	ind = cd.get_cdl_indices_geo(p1, p2, p3, p4)
	vals = cd.get_cdl_by_indices(ind, cd.cdl_data)

	proportion = cd.get_proportion(np.array(vals))
	print(len(ind), proportion)

	return


test_cdl_indices_geo()