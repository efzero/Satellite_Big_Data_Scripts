from pyhdf.SD import SD, SDC
from netCDF4 import Dataset
import numpy as np

class GNOME_utils:

	def __init__(self, cdl_util):
		self.GOME_sif = None
		self.lat_corners = None
		self.lon_corners = None
		self.clouds = None
		self.time = None
		self.min_lon = cdl_util.min_lon
		self.max_lon = cdl_util.max_lon
		self.min_lat = cdl_util.min_lat
		self.max_lat = cdl_util.max_lat
		#08\\ret_f_nr5_nsvd12_v26_waves734_nolog.20160801_v27_all.nc


	def load_gnome(self, path):
		prefix = 'E:\\SIF data\\GOME_2016\\GOME_2016\\'
		path = prefix + path
		dat = Dataset(path)
		data_lons = dat.variables['longitude'][:]
		data_lats = dat.variables['latitude'][:]
		data_lat_corners = dat.variables['Latitude_corners'][:]
		data_lon_corners = dat.variables['Longitude_corners'][:]
		data_clouds = dat.variables['cloud_fraction'][:]
		data_sifs = dat.variables['Daily_averaged_SIF']
		data_time = dat.variables['time']
		filtered_lon_ind = np.where((data_lons >= self.min_lon)&(data_lons <= self.max_lon))
		filtered_lat_ind = np.where((data_lats >= self.min_lat)&(data_lats <= self.max_lat))
		indices = np.intersect1d(filtered_lon_ind, filtered_lat_ind)
		
		if len(indices) <= 4:
			raise Exception('no valid gnome data found!')
			return False
		self.time = data_time[indices]
		self.clouds = data_clouds[indices]
		self.lat_corners =  data_lat_corners[indices]
		self.lon_corners = data_lon_corners[indices]
		return True
		
	def get_clean_gmone_data(self, path):

		good_indices = np.where(self.clouds < 0.20)
		if len(good_indices[0]) <= 4:
			raise Exception('no valid gnome data found!')
			return False
		self.time = self.time[good_indices]
		self.clouds = self.clouds[good_indices]
		self.lat_corners = self.lat_corners[good_indices]
		self.lon_corners = self.lon_corners[good_indices]
		return True


#we do not need the minutes and seconds
	def convert_time_data(self, time):
		time = [int(i[0])*10 + int(i[1]) for i in time]
		return time
		 

		








