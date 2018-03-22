#run the whole workflow

from gome_work_flow import *
def main():
	g_flow = Gome_workflow()
	g_flow.preprocess_gome()
	g_flow.preprocess_cdl()
	g_flow.build_input_matrix()
	g_flow.run_gome_regression()



if __name__ == '__main__':
	main()