from pyhdf.SD import SD, SDC
from netCDF4 import Dataset
import numpy as np
import datetime

class GNOME_utils:

	def __init__(self, cdl_util):
		self.GOME_sif = []
		self.lat_corners = []
		self.lon_corners = []
		self.clouds = []
		self.time = []
		self.date = []
		self.lons = []
		self.lats = []
		self.min_lon = cdl_util.min_lon	
		self.max_lon = cdl_util.max_lon
		self.min_lat = cdl_util.min_lat
		self.max_lat = cdl_util.max_lat
		#08\\ret_f_nr5_nsvd12_v26_waves734_nolog.20160801_v27_all.nc


	def load_gnome(self, path, date_):
		prefix = 'E:\\SIF data\\GOME_2016\\GOME_2016\\'
		self.date = date_
		path = prefix + path
		dat = Dataset(path)
		data_lons = dat.variables['longitude'][:]
		data_lats = dat.variables['latitude'][:]
		data_lat_corners = dat.variables['Latitude_corners'][:]
		data_lon_corners = dat.variables['Longitude_corners'][:]
		data_clouds = dat.variables['cloud_fraction'][:]
		data_sifs = dat.variables['Daily_averaged_SIF']
		data_time = dat.variables['time']
		filtered_lon_ind = np.where((data_lons >= self.min_lon + 1.6)&(data_lons <= self.max_lon - 1.6))
		filtered_lat_ind = np.where((data_lats >= self.min_lat + 0.7)&(data_lats <= self.max_lat - 0.7))
		indices = np.intersect1d(filtered_lon_ind, filtered_lat_ind)

		if len(indices) == 0:
			return False

		self.time = np.array(data_time[indices])
		self.clouds = np.array(data_clouds[indices])
		self.lat_corners =  np.array(data_lat_corners[indices])
		self.lon_corners = np.array(data_lon_corners[indices])
		self.lons = np.array(data_lons[indices])
		self.lats = np.array(data_lats[indices])
		self.GOME_sif = np.array(data_sifs[indices])
		return True

#clean gmone data by cloud fractions		
	def get_clean_gmone_data(self):

		good_indices = np.where(np.array(self.clouds) < 0.20)
		if len(good_indices[0]) <= 4:
			# raise Exception('no valid gnome data found!')
			self.time = []
			self.clouds = []
			self.lat_corners = []
			self.lon_corners = []
			self.lons = []
			self.lats = []
			self.GOME_sif = []
			return False

			#np.where returns a tuple
		# good_indices = good_indices[0]
		good_indices = good_indices[0]
		self.time = self.time[good_indices]
		self.clouds = self.clouds[good_indices]
		self.lat_corners = self.lat_corners[good_indices]
		self.lon_corners = self.lon_corners[good_indices]
		self.lons = self.lons[good_indices]
		self.lats = self.lats[good_indices]
		self.GOME_sif = self.GOME_sif[good_indices]
		return True


#we do not need the minutes and seconds
	def convert_time_data(self, time):
		time = np.array([int(i[0])*10 + int(i[1]) for i in time])
		self.time = time
		return True