#!/home/yli11/.conda/envs/py2/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
# from liyc_utils import *
import pandas as pd
import argparse
import getpass
import datetime
import matplotlib
import pandas as pd
matplotlib.use('agg')
import matplotlib.pyplot as plt
import uuid
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def general_df_reader(args):
	if "npz" == args.input.split(".")[-1]:
		npz = np.load('result.npz')
		df = pd.DataFrame(npz['matrix'])
		df.columns = npz['labels']
		return df
	if args.header:
		if args.index:
			df = pd.read_csv(args.input,sep=args.sep,index_col=0)
		else:
			df = pd.read_csv(args.input,sep=args.sep)
	else:
		if args.index:
			df = pd.read_csv(args.input,sep=args.sep,index_col=0,header=None)
		else:
			df = pd.read_csv(args.input,sep=args.sep,header=None)
	return df

def guess_sep(x):
	with open(x) as f:
		for line in f:
			tmp1 = len(line.strip().split(","))
			tmp2 = len(line.strip().split("\t"))
			# print (tmp1,tmp2)
			if tmp1 > tmp2:
				return ","
			if tmp2 > tmp1: 
				return "\t"
			else:
				print ("Can't determine the separator. Please input manually")
				exit()
				
def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="given a dataframe, plot a column as a pie char")

	mainParser.add_argument('-o',"--output",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	

	mainParser.add_argument('-f',"--input",  help="data table input",required=True)
	mainParser.add_argument('-t',"--title",  help="figure title",default=None)
	mainParser.add_argument("--use_col",  help="which color to use for pie chart, if the input file contains column name, please use column name; otherwise, 0 will be the first column, and 1 will be the second column and so on")
	mainParser.add_argument('--index',  help=" index is false", action='store_true')
	mainParser.add_argument("--header",  help="input table has header", action='store_true')
	mainParser.add_argument("--homer",  help="input table is homer", action='store_true')
	mainParser.add_argument("--order",  help="pie chart category order, to keep color assignment consistent", default=None)
	mainParser.add_argument('--just_plot',  help="provide a ready to plot dataframe", action='store_true')
	

	mainParser.add_argument('-s',"--sep",  help="separator",default="auto")
	



	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
	


def pie_chart(char_list,value_list,output,args):
	# from adjustText import adjust_text

	color_set = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']	
	plt.rcParams['font.size'] = '16'
	plt.figure()
	if len(value_list) > len(color_set):
		print ("Too many categories!")
	

	colors = color_set[:len(char_list)]
	df = pd.DataFrame()
	df[0] = char_list
	df[1] = value_list
	df[2] = colors
	df2 = df[df[1]>0]
	df1 = df[df[1]==0] 
	[w,t1,t2] = plt.pie(df2[1], labels=df2[0], autopct='%1.1f%%',shadow=False, startangle=90,colors=df2[2])
	# adjust_text(t1)
	if df1.shape[0] > 0:
		# plt.title()
		print ("These categories are not found: %s"%(", ".join(df1[0].tolist())))
	if args.title:
		plt.title(args.title)
	plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	plt.savefig("%s.pdf"%(output),bbox_inches='tight')

def get_homer_category(x):
	try:
		return x.split()[0]
	except:
		return "NaN"
	if "3' UTR" in x:
		return "3' UTR"
	if "5' UTR" in x:
		return "5' UTR"
	if "non-coding" in x:
		return "Exon (non-coding)"
	if "promoter" in x:
		return "Promoter"
	x = x.split()[0]
	x = list(x)
	x[0] = x[0].upper()
	return "".join(x[0])
	# return x
	



def main():

	args = my_args()
	if args.sep=="auto":
		args.sep = guess_sep(args.input)
	df = general_df_reader(args)
	print (df.head())
	if args.just_plot:
		char_list = df[0].tolist()
		value_list = df[1].tolist()
		pie_chart(char_list,value_list,args.output,args)
	
		exit()
	
	if args.use_col == "-1":
		args.use_col = df.columns.tolist()[-1]
	if args.use_col == "-2":
		args.use_col = df.columns.tolist()[-2]
	if args.homer:
		df[args.use_col] = df[args.use_col].apply(get_homer_category)
	my_cat = df[args.use_col].value_counts(normalize=True).sort_values().to_dict()
	char_list = my_cat.keys()
	if args.order:
		char_list = args.order.split(",")

	value_list = []
	for k in char_list:
		try:
			value_list.append(my_cat[k])
		except:
			value_list.append(0)
	pie_chart(char_list,value_list,args.output,args)
	

if __name__ == "__main__":
	main()

	







