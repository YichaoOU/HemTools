#!/hpcf/apps/python/install/2.7.13/bin/python
import pandas as pd
import argparse

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="Given a bed file, create bed files for nearby regions.")
	mainParser.add_argument('-w','--window_size',  help="feature window size, use the center of you input bed file, and create several windows both upstream and downstream, then your input file list will be used to overlap with each of these windows.", default=200,type=int)
	mainParser.add_argument('-s','--step_size',  help="How to create each window (where to set window start site). If step_size >= window_size, then it means no overlap between each window.", default=100,type=int)
	mainParser.add_argument('-n','--number_steps',  help="How many windows to create (i.e., how many steps you want to go). Note that number of bins = n-1. The actual bp to the center is n*s+w", default=5,type=int)
	mainParser.add_argument('--output_file_list',  help="combined with annotate_peaks.py, not for end-user", action='store_true')
	mainParser.add_argument("-f","--input",  help="a bed file with at least 4 columns, additional columns will be kept when output the result. The first 4 columns are chr, start, end, unique name.",required=True)
	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
	


def main():

	args = my_args()
	file_list = []
	df = pd.read_csv(args.input,sep="\t")
	for i in 
	
	

	
if __name__ == "__main__":
	main()







































