import numpy as np
from numpy.linalg import lstsq
from my_functions import *
# from osgeo import gdal
from helper import *
import sifutil
import re
from dbfread import DBF

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
		self.get_crop_label()
		data = gdal.Open(path)
		data = data.ReadAsArray()
		self.cdl_data = data
		return data



	def get_crop_label(self):


		"""
		get the accordingly corn labels in the cdl data
		build a hashtable which takes a number as an input and returns the according crop label
		e.g. self.crop_label[1] = 'corn'
				 self.crop_label[5] = 'soybeans'

		"""
		data = DBF('configuration/cdl.dbf')
		dataset = []
		for i in data:
			if i['CLASS_NAME'] != '':
				dataset.append(i)
		pattern = re.compile(r'\bWater\b|Undefined|Developed|Clouds|Background|Aquaculture')
		non_empty = set()
		non_veg = set()
		forest = set()
		corns = set()
		soybeans = set()
		for i, obj in enumerate(dataset):
			if obj['CLASS_NAME'] != '':
				non_empty.add(obj['VALUE'])

			if re.findall(pattern, obj['CLASS_NAME']) != []:
				non_veg.add(obj['VALUE'])

			if re.findall(r'forest|Forest', obj['CLASS_NAME']) != []:
				forest.add(obj['VALUE'])

			if re.findall(r'corn|Corn', obj['CLASS_NAME']) != []:
				corns.add(obj['VALUE'])

			if re.findall(r'soybean|Soybean', obj['CLASS_NAME']) != []:
				soybeans.add(obj['VALUE'])

		grass = non_empty - non_veg - corns - forest - soybeans
		crop_label = ['' for i in range(256)]
		
		for i in grass:
			crop_label[i] = 'grass'
		for i in corns:
			crop_label[i] = 'corn'
		for i in soybeans:
			crop_label[i] = 'soybeans'
		for i in forest:
			crop_label[i] = 'forest'

		self.crop_label = crop_label


	def load_np_cdl(self, path):
		self.get_crop_label()
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


	def get_proportion(self, submat):


		"""
		input a 2d matrix consist of cdl labels
		return the proportion of each type of crops in that matrix
		The order of proportion matrix is 'corn':0, 'soybeans':1, 'grass':2, 'forest':3
		
		"""

		row = np.array([0,0,0,0], dtype=float)

		unique_elements, counts_elements = np.unique(submat, return_counts=True)

		indices_map = {'corn':0, 'soybeans':1, 'grass':2, 'forest':3}

		for num, count in zip(unique_elements, counts_elements):
			if self.crop_label[num] != '':
				row[indices_map[self.crop_label[num]]] += count

		if np.sum(row) == 0:
			return row

		row = row/np.sum(counts_elements)
		return row


	#input a bounding box which is a polygon of latitude and longitude
	#return cdl datas inside that bounding box
	def get_cdl_box_data(self, min_lon, max_lon, min_lat, max_lat):

		start_col = int((min_lon - self.min_lon)/self.y_step)
		end_col = int((max_lon - self.min_lon)/self.y_step)
		start_row = int((max_lat - self.max_lat)/self.x_step)
		end_row = int((min_lat - self.max_lat)/self.x_step)
		if start_row < 0 or start_col < 0:
			print(min_lon, max_lat) 
		# print(start_row, end_row, start_col, end_col)
		assert start_col <= end_col and start_row <= end_row and start_row >= 0 and start_col >= 0
		assert end_col < self.cdl_data.shape[1] and end_row < self.cdl_data.shape[0]
		cdl_data = self.cdl_data[start_row: end_row+1, start_col: end_col+1]
		# print(cdl_data.shape)
		return np.array(cdl_data) 



	#input the four lu, ru, rb, lb points with albert projection
	#return according indices in cdl data
	def get_cdl_indices_albert(self, lu, ru, rb, lb):

		#cdl projection returns (lon_projection, lat_projection)
		ul = self.proj_to_ind(self.getCDLprojection(lu[0], lu[1]))
		ur = self.proj_to_ind(self.getCDLprojection(ru[0], ru[1]))
		br = self.proj_to_ind(self.getCDLprojection(rb[0], rb[1]))
		bl = self.proj_to_ind(self.getCDLprojection(lb[0], lb[1]))
		box = Polygon([ul, ur, br, bl])
		indices = points_inside_polygon(box, ul, ur, br, bl)
		return np.array(indices)


	#input the four points (polygon) with geographical projection
	#return according indices in cdl data
	def get_cdl_indices_geo(self, lu, ru, rb, lb):
		p1 = self.convert_to_ind(lu)
		p2 = self.convert_to_ind(ru)
		p3 = self.convert_to_ind(rb)
		p4 = self.convert_to_ind(lb)
		box = Polygon([p1, p2, p3, p4])
		indices = points_inside_polygon(box, p1, p2, p3, p4)
		return np.array(indices)


	#input the latitude and longitude (lat, lon)
	#return according indices in cdl data
	def convert_to_ind(self,point):
		lat, lon = point[0], point[1]
		col = int((lon - self.min_lon)/self.y_step)
		row = int((lat - self.max_lat)/self.x_step)
		return (row,col)


	#input the cdl_array and indices
	#return the cdl value
	def get_cdl_by_indices(self, indices, cdl_array):
		cdl_values = []
		for i in range(len(indices)):
			row, col = indices[i, 0], indices[i, 1]
			cdl_data = cdl_array[row, col]
			cdl_values.append(cdl_data)

		return cdl_values
