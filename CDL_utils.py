import numpy as np
from numpy.linalg import lstsq
from my_functions import *
# from osgeo import gdal
from helper import *
import sifutil

class cdl_utils:

	def __init__(self):
		# self.llon = 349785
		# self.rlon = self.llon + 15590*30
		# self.lon_steps = 15590
		# self.ulat = 2087295
		# self.lat_steps = 15749
		# self.blat = self.ulat - 15749*30
		self.cdl_data = None
		self.min_lon = -91.4210280
		self.max_lon = -87.3981700
		self.min_lat = 40.3271460
		self.max_lat = 42.5235010
		self.x_size = 6739
		self.y_size = 12344
		self.x_step = -0.000325917050007
		self.y_step = 0.000325895819831

 
	def load_cdl(self, path):
		data = gdal.Open(path)
		data = data.ReadAsArray()
		self.cdl_data = data
		return data


	def load_np_cdl(self, path):
		self.cdl_data = np.load(path)
		return np.load(path)

	def save_cdl(self):
		np.save('cdl_chicago.npy', self.cdl_data)
		return

	def getCDLprojection(self, lon,lat):
		return sifutil.convertProjection(lon, lat, sifutil.WGS84, sifutil.CONUS_ALBERS)


	def proj_to_ind(self, projection):
		print(projection)
		return (int((self.ulat - projection[1])/30), -int((self.llon - projection[0])/30))


	#input a 2d matrix consist of cdl labels
	#return the proportion of each type of crops in that matrix

	def get_proportion(self, submat, cdl_data):


		row = np.array([0,0,0,0], dtype=float)


		unique_elements, counts_elements = np.unique(submat, return_counts=True)
		indices_map = {1:0, 5:1, 176:2}
		for num, count in zip(unique_elements, counts_elements):
			if num == 1 or num == 5 or num == 176:
				row[indices_map[num]] = count
			else:
				row[3] += count
		
		if np.sum(row) == 0:
			return row

		row = row/(submat.shape[0]*submat.shape[1])
		return row


	#input a bounding box which is a polygon of latitude and longitude
	#return cdl datas inside that bounding box
	def get_cdl_box_data(self, min_lon, max_lon, min_lat, max_lat):

		start_col = int((min_lon - self.min_lon)/self.y_step)
		end_col = int((max_lon - self.min_lon)/self.y_step)
		start_row = int((max_lat - self.max_lat)/self.x_step)
		end_row = int((min_lat - self.max_lat)/self.x_step)
		# print(start_row, end_row, start_col, end_col)
		assert start_col <= end_col and start_row <= end_row and start_row >= 0 and start_col >= 0
		assert end_col < self.cdl_data.shape[1] and end_row < self.cdl_data.shape[0]
		cdl_data = self.cdl_data[start_row: end_row+1, start_col: end_col+1]
		# print(cdl_data.shape)
		return np.array(cdl_data) 


	#input the four lu, ru, rb, lb points
	#return according indices in cdl data
	def get_cdl_indices(self, lu, ru, rb, lb):

		#cdl projection returns (lon_projection, lat_projection)
		ul = self.proj_to_ind(self.getCDLprojection(lu[0], lu[1]))
		ur = self.proj_to_ind(self.getCDLprojection(ru[0], ru[1]))
		br = self.proj_to_ind(self.getCDLprojection(rb[0], rb[1]))
		bl = self.proj_to_ind(self.getCDLprojection(lb[0], lb[1]))
		box = Polygon([ul, ur, br, bl])
		indices = points_inside_polygon(box, ul, ur, br, bl)
		return np.array(indices)