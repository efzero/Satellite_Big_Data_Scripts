#run the whole workflow
from datetime import timedelta, date
from gome_work_flow import *

def main():

	X = np.empty((0,4))
	y = np.array([])
	date_ = datetime.date(2016, 7,1)
	g_flow = Gome_workflow()
	g_flow.preprocess_cdl()
	g_flow.preprocess_par()
	prefix = 'E:\\SIF data\\GOME_2016\\GOME_2016\\'
	min_lon = -89.11086962890625-1.6
	max_lon = -88.69682275390625+1.6
	min_lat = 41.53067026099156 - 0.7
	max_lat = 42.05638178482896 + 0.7

	fp_path = 'data/FPAR_A2016'
	start_fp = 185



	for i in range(30):
		date_ += timedelta(1)
		try:
			print(i%8 == 0)
			if i%8 == 0:
				print('data/FPAR_A2016' + str(start_fp) + '.hdf')
				g_flow.fp_workflow.load_fpar('data/FPAR_A2016' + str(start_fp) + '.hdf')
				start_fp += 8

			g_flow.process_gome(date_, prefix, min_lon, max_lon, min_lat, max_lat)
			# print(g_flow.gome.lons)
			g_flow.build_input_matrix()
			X = np.concatenate((X, g_flow.X), axis= 0)
			y = np.append(y, g_flow.y)
			# print(g_flow.X, g_flow.y)

		except Exception as e:
			print(e)	
			continue

	print(X,y)
	X_ = sm.add_constant(X)
	model = sm.OLS(y, X).fit()
	model2 = sm.OLS(y, X_).fit()
	print(model.summary())
	print(model2.summary())
	return X,y



def sliding_window(min_lon, max_lon, min_lat, max_lat, start_date, timeperiod):

	"""
	run the sliding window algorithm
	
	Args:
	     the bounding box of the window, and the timeperiod of the sliding
	     
	Returns:
	     The input matrix X and labels y for SIF regression

	"""
	X = np.empty((0,4))
	y = np.array([])
	g_flow = Gome_workflow()
	g_flow.preprocess_cdl()
	g_flow.preprocess_par()
	prefix = 'E:\\SIF data\\GOME_2016\\GOME_2016\\'
	fp_path = 'data/FPAR_A2016'
	start_fp = round((start_date - datetime.date(2016,1,1)).days/8)*8 + 1
	offset = start_fp - 1 - (start_date - datetime.date(2016,1,1)).days 
	g_flow.fp_workflow.load_fpar('data/FPAR_A2016' + str(start_fp) + '.hdf')

	for i in range(timeperiod):
		start_date += timedelta(1)
		try:

			if (i + offset) %8 == 0:
				new_fp = round((start_date - datetime.date(2016,1,1)).days/8)*8 + 1
				g_flow.fp_workflow.load_fpar('data/FPAR_A2016' + str(new_fp) + '.hdf')
				print('newfp', new_fp)



			g_flow.process_gome(start_date, prefix, min_lon, max_lon, min_lat, max_lat)
			# print(g_flow.gome.lons)
			g_flow.build_input_matrix()
			X = np.concatenate((X, g_flow.X), axis= 0)
			y = np.append(y, g_flow.y)
			# print(g_flow.X, g_flow.y)

		except Exception as e:
			# print(e)	
			continue

	print(X,y)
	X_ = sm.add_constant(X)
	model = sm.OLS(y, X).fit()
	model2 = sm.OLS(y, X_).fit()
	print(model.summary())
	print(model2.summary())
	return X,y


if __name__ == '__main__':
	main()
