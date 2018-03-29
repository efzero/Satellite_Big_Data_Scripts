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


		"""
		this function must be run after preprocessing gome has run
		
		"""

		mat = []
		print(self.date)
		print('building gome input matrix')
		print('y',self.y)
		with open(str(self.date) + '.txt', 'w') as f:
		#loop through all the bounding box in gome array
			for i in range(len(self.y)):
				lat_corner = self.gome.lat_corners[i]
				lon_corner = self.gome.lon_corners[i]
				print(lat_corner, lon_corner, file = f)

				cdl_proportion = self.get_cdl_proportion_gome(lat_corner, lon_corner)
				#get the time index in par data
				time_ind = self.par.get_time_ind(self.date, self.gome.time[i])
				#get the weighted par for gome regression
				par_val = self.par.get_weighted_par(lon_corner, lat_corner, time_ind)
				#get the according fpari in the gome bounding box
				fpari = self.get_fpari(lat_corner, lon_corner)
				print('time', self.gome.time[i], file = f)
				print('cdl','fpari', 'parval', cdl_proportion, fpari, par_val, file = f)
				mat.append(fpari * cdl_proportion * par_val)

			self.X = np.array(mat)
		return np.array(mat)


	def preprocess_par(self):

		"""
		preprocess the par object which is needed in the workflow
		
		"""
		print('preprocessing par')
		my_par = par_utils()
		self.par = my_par


		#the gome object must be cleared after processing
	def process_gome(self, gome_date, prefix):

		"""
		gome_dates is a datetime object

		"""

		
		gome = GNOME_utils(self.fp_workflow.cdl_)
		self.gome = gome
		gome_path = convertGOMEDate(gome_date, prefix)
		print('gome_path', gome_path)
		self.gome.load_gnome(gome_path, gome_date)
		self.gome.get_clean_gmone_data()
		self.gome.convert_time_data(self.gome.time)
		self.y = self.gome.GOME_sif
		self.date = gome_date


	def preprocess_cdl(self):

		print('preprocessing cdl')
		fpar_path = 'FPAR_A2016169.hdf'
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
		# print(model.summary())
		coeffs = result[0]
		return coeffs











