from netCDF4 import Dataset
import numpy as np
import datetime
from datetime import timedelta, date
from shapely.geometry import Polygon
from helper import *

class par_utils:

	def __init__(self):
		
		self.filepath = 'PAR2016.nc'
		data = {}
		ds = Dataset(self.filepath, mode='r')
		for var in list(ds.variables):
			data[var] = ds[var][:]

		data['total_par'] = data['sfc_comp_par_direct_all_3h'] + data['sfc_comp_par_diffuse_all_3h']
		self.par = data
		self.min_date = min(data['time'])

#given 4 lon and lat corners, find the according weighted average pars
	def get_weighted_par(self, lon_corners, lat_corners, time_ind):

		ret_= 0
		swap_mat = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
		gome_box = Polygon(np.vstack((lon_corners@swap_mat, lat_corners@swap_mat)).T)
		min_lon, max_lon = min(lon_corners), max(lon_corners)
		min_lat, max_lat = min(lat_corners), max(lat_corners)
		bounding_box = find_nearest_border(min_lon, max_lon, min_lat, max_lat)
		left, right = bounding_box[0], bounding_box[1]
		down, up = bounding_box[2], bounding_box[3]
		assert right > left and up > down
		print(gome_box.centroid)
		for lon in range(left, right, 1):
			for lat in range(down, up, 1):
				lon_ind = self.get_par_lon_ind(lon)
				lat_ind = self.get_par_lat_ind(lat)

				par_box = Polygon([[lon,lat],[lon+1, lat], [lon+1, lat+1], [lon, lat+1]])
				weight = gome_box.intersection(par_box).area/gome_box.area
				# print('lon', lon, 'lat', lat, 'weight', weight)
				ret_ += weight * self.par['total_par'][time_ind][lat_ind, lon_ind]
		return ret_


    #input integer values of lon and lat, representing the left, down corner of a par grid
	def get_par_lon_ind(self, lon):
		return lon + 360 - 263

	def get_par_lat_ind(self, lat):
		return lat -37

	def get_time_ind(self, cur_date, hour):

		base_date = datetime.date(2016, 1, 1)
		date_ind = int((cur_date-base_date).days*8 + hour//3)
		return date_ind