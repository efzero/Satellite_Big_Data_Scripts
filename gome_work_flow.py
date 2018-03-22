#start gome workflow
from Par_util import *
from gnone_utils import *
from fpar_workflow import *
from CDL_utils import *
import statsmodels.api as sm

class Gome_workflow:

	def __init__(self):
		self.X = None
		self.y = None
		self.par = None
		self.gome = None
		self.date = None
		self.fp_workflow = None

	def build_input_matrix(self):
		mat = []
		for i in range(len(self.y)):
			lat_corner = self.gome.lat_corners[i]
			lon_corner = self.gome.lon_corners[i]
			print(lat_corner, lon_corner)
			cdl_proportion = self.get_cdl_proportion_gome(lat_corner, lon_corner)
			time_ind = self.par.get_time_ind(self.date, self.gome.time[i])
			par_val = self.par.get_weighted_par(lon_corner, lat_corner, time_ind)
			fpari = self.get_fpari(lat_corner, lon_corner)

			# print(cdl_proportion, fpari, par_val, fpari * cdl_proportion * par_val)
			mat.append(fpari * cdl_proportion * par_val)

		self.X = np.array(mat)
		return np.array(mat)


	def preprocess_gome(self):
		prefix = 'E:\\SIF data\\GOME_2016\\GOME_2016\\'
		gome_path = '07\\ret_f_nr5_nsvd12_v26_waves734_nolog.20160708_v27_all.nc'
		date_ = datetime.date(2016, 7, 8)
		self.date = date_
		cd = cdl_utils()
		my_par = par_utils()
		gome = GNOME_utils(cd)
		gome.load_gnome(gome_path, date_)
		gome.get_clean_gmone_data()
		t = gome.convert_time_data(gome.time)
		self.y = gome.GOME_sif
		self.gome = gome
		self.par = my_par

	def preprocess_cdl(self):
		fpar_path = 'FPAR_A2016185.hdf'
		cdl_path = 'cdl_chicago.npy'
		self.fp_workflow = Fpar_flow()
		self.fp_workflow.preprocess(fpar_path, cdl_path)

	def get_cdl_proportion_gome(self, lat_corner, lon_corner):
		#rb ru lb lu
		rb = (lat_corner[0], lon_corner[0])
		ru = (lat_corner[1], lon_corner[1])
		lb = (lat_corner[2], lon_corner[2])
		lu = (lat_corner[3], lon_corner[3])
		ind = self.fp_workflow.cdl_.get_cdl_indices_geo(lu, ru, rb, lb)
		vals = self.fp_workflow.cdl_.get_cdl_by_indices(ind, self.fp_workflow.cdl_.cdl_data)
		proportion = self.fp_workflow.cdl_.get_proportion(np.array(vals))
		return proportion

	def get_fpari(self, lat_corner, lon_corner):
		rb = (lat_corner[0], lon_corner[0])
		ru = (lat_corner[1], lon_corner[1])
		lb = (lat_corner[2], lon_corner[2])
		lu = (lat_corner[3], lon_corner[3])
		self.fp_workflow.get_fpar_vector(lu, ru, rb, lb)
		self.fp_workflow.get_cdl_matrix()
		self.fp_workflow.run_regression()
		return self.fp_workflow.reg_coeffs


	def run_gome_regression(self):
		assert self.X != None and self.y != None
		result = lstsq(self.X, self.y)
		model = sm.OLS(self.y, self.X).fit()
		print(model.summary())
		coeffs = result[0]
		return coeffs








