import numpy as np
from numpy.linalg import lstsq
from my_functions import *
from osgeo import gdal

import sifutil

class cdl_utils:



	def __init__(self):
		self.llon = 349785
		self.rlon = self.llon + 15590*30
		self.lon_steps = 15590
		self.ulat = 2087295
		self.lat_steps = 15749
		self.blat = self.ulat - 15749*30
		self.cdl_data = None


	def load_cdl(self, path):
		data = gdal.Open(path)
		data = data.ReadAsArray()
		self.cdl_data = data
		return data


	def save_cdl(self):
		np.save('cdl.npy', self.cdl_data)
		return

	def getCDLprojection(self, lon,lat):
		return sifutil.convertProjection(lon, lat, sifutil.WGS84, sifutil.CONUS_ALBERS)


	def proj_to_ind(self, projection):
		return (int((self.ulat - projection[1])/30), -int((self.llon - projection[0])/30))


	#input a 2d matrix consist of cdl labels
	#return the proportion of each type of crops in that matrix

	def get_proportion(self, submat, cdl_data):
		row = np.array([0,0,0,0])


		for j in submat:
			if cdl_data[j] == 1:
				row[0] += 1

			elif cdl_data[j] == 5:
				row[0] += 1

			elif cdl_data[j] == 64:
				row[0] += 1

			elif cdl_data[j] == 176:
				row[0] += 1


		if np.max(row) != 0:
			row = row/np.sum(row)


		return row


	#input a bounding box which is a polygon of latitude and longitude
	#return cdl datas inside that bounding box
	def get_cdl_indices(self, lu, ru, rb, lb):
		
		#cdl projection returns (lon_projection, lat_projection)
		ul = self.proj_to_ind(self.getCDLprojection(lu[1], lu[0]))
		bl = self.proj_to_ind(self.getCDLprojection(lb[1], lb[0]))
		ur = self.proj_to_ind(self.getCDLprojection(ru[1], ru[0]))
		br = self.proj_to_ind(self.getCDLprojection(rb[1], rb[0]))


		box = polygon([ul, ur, br, bl])

		indices = points_inside_polygon(box, ul, ur, br, bl)

		return np.array(indices)















