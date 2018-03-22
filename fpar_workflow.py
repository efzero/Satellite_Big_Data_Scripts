#start workflow

from FPAR_utils import *
from CDL_utils import *
from my_functions import *


class Fpar_flow:
	def __init__(self):
		self.cdl_matrix = None
		self.fpar_vals = None
		self.reg_coeffs = None
		self.fpar_ = fpar_utils()
		self.cdl_ = cdl_utils()
		self.fp_ptrs = None

#input a polygon
#return fpar regression result inside that polygon

	def preprocess(self, fpar_path, cdl_path):
		self.fpar_.read_fpar(fpar_path)
		self.cdl_.load_np_cdl(cdl_path)

	def load_fpar(self, fpar_path):
		self.fpar_.read_fpar(fpar_path)


	def get_fpar_vector(self, p1, p2, p3, p4):
		ptrs = self.fpar_.get_fpar_indices_by_box(p1, p2, p3, p4, 0)
		ptrs = np.array(ptrs)
		fp, qc = self.fpar_.get_fpar_by_indices(self.fpar_.fpar, self.fpar_.qc, ptrs)
		ptrs_cleaned, fp_cleaned = clean_data(fp, ptrs, qc)
		assert len(ptrs_cleaned) == len(fp_cleaned)
		self.fpar_vals = fp_cleaned
		self.fp_ptrs = ptrs_cleaned


	def get_cdl_matrix(self):
		assert self.fp_ptrs is not None
		assert self.cdl_.cdl_data is not None

		mat = []

		for point in self.fp_ptrs:
			#lat_ind, lon_ind
			fpar_box = self.fpar_.get_fpar_bound(point[0], point[1])
			cur_cdl_box = self.cdl_.get_cdl_box_data(fpar_box[0],fpar_box[1],fpar_box[2],fpar_box[3])
			proportion = self.cdl_.get_proportion(cur_cdl_box)
			mat.append(proportion)
		mat = np.array(mat)
		# mat = np.append(mat, np.ones((mat.shape[0],1)), axis=1)
		self.cdl_matrix = mat


	def run_regression(self):
		assert self.cdl_matrix != None and self.fpar_vals != None
		result = lstsq(self.cdl_matrix, self.fpar_vals)
		self.reg_coeffs = result[0]
		print(result)
		return result



	def init_workflow(self, fpar_path, cdl_path, p1, p2, p3, p4):
		# p4 = (41.47067026099156,-88.7186962890625)
		# p3 = (41.47067026099156, -87.56082275390625)
		# p2 = (41.81638178482896,-87.56082275390625)
		# p1 = (41.81638178482896, -88.7186962890625)

		# fpar_path = 'FPAR_A2016241.hdf'
		# cdl_path = 'cdl_chicago.npy'
		self.preprocess(fpar_path, cdl_path)
		self.get_fpar_vector(p1, p2, p3, p4)
		self.get_cdl_matrix()
		self.run_regression()

	def continue_workflow(self, fpar_path, p1, p2, p3, p4):
		# p4 = (41.47067026099156,-88.7186962890625)
		# p3 = (41.47067026099156, -87.56082275390625)
		# p2 = (41.81638178482896,-87.56082275390625)
		# p1 = (41.81638178482896, -88.7186962890625)
		self.load_fpar(fpar_path)
		self.get_fpar_vector(p1, p2, p3, p4)
		self.get_cdl_matrix()
		self.run_regression()


