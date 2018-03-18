from pyhdf.SD import SD, SDC
from netCDF4 import Dataset


class GNOME_utils:

	def __init__():
		self.GOME_sif = None
		self.lat_corners = None
		self.lon_corners = None
		self.clouds = None
		#08\\ret_f_nr5_nsvd12_v26_waves734_nolog.20160801_v27_all.nc


	def load_gnome(path):
		prefix = 'E:\\SIF data\\GOME_2016\\GOME_2016\\'
		path = prefix + path
		dat = Dataset(path)
		self.GOME_sif = dat.variables['Daily_averaged_SIF'][:]
		self.lat_corners = dat.variables['Latitude_corners'][:]
		self.lon_corners = dat.variables['Longitude_corners'][:]
		self.clouds = dat.variables['cloud_fraction'][:]
		return 
		
	def clean_gmone_data(data):
		








