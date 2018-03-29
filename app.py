#run the whole workflow
from datetime import timedelta, date
from gome_work_flow import *

def main():


	X = np.empty((0,4))
	y = np.array([])
	date_ = datetime.date(2016, 6,15)
	g_flow = Gome_workflow()
	g_flow.preprocess_cdl()
	g_flow.preprocess_par()
	prefix = 'E:\\SIF data\\GOME_2016\\GOME_2016\\'

	for i in range(10):
		date_ += timedelta(1)
		try:
			if i == 7:
				g_flow.fp_workflow.load_fpar('FPAR_A2016177.hdf')
			g_flow.process_gome(date_, prefix)
			g_flow.build_input_matrix()
			X = np.concatenate((X, g_flow.X), axis= 0)
			y = np.append(y, g_flow.y)
			print(g_flow.X, g_flow.y)

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

		# g_flow.run_gome_regression()




if __name__ == '__main__':
	main()