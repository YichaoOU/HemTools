#!/usr/bin/env python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from liyc_utils import *

"""Plot heatmap given data frame

in all input data frame, we assume rows are samples and cols are features.

Note: this script is intend to plot gene expression or general count data.

Because you can't see the labels when plotting a big dataframe, there are several filters that you can apply.

1. row filters

- top_N_by_row_mean

- row_mean_cutoff

- row_mean_percent_col_cutoff

2. col filters




"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="plot heatmap given dataframe.")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	

	mainParser.add_argument('--remove_zero',  help="remove all rows or cols that are zero", action='store_true')
	# mainParser.add_argument('--row',  help="results on rows. This is to the opposite of pandas row and col, which is operations on rows or cols. For example, operations (e.g., find zeros) on cols will result in removing rows.", action='store_true')
	# mainParser.add_argument('--col',  help="results on cols", action='store_true')
	mainParser.add_argument('--index',  help=" index is false", action='store_true')
	mainParser.add_argument('-f',"--input",  help="data table input",required=True)
	# mainParser.add_argument("--label",  help="dataframe name")
	mainParser.add_argument("--index_using",  help="Sometimes we want to show a different label for the indices, then use this option. For example, gene id is unique, however, gene name can be different, it also has upper or lower case problem, in such case, we want to use gene id for data processing and use gene name for visualization.",default="")
	mainParser.add_argument('-s',"--sep",  help="separator",default="\t")
	mainParser.add_argument("--xlabel",default="")
	mainParser.add_argument("--ylabel",default="")
	mainParser.add_argument("--title",default="")
	mainParser.add_argument("--figure_type",default="png",help="pdf,png,jpeg")
	mainParser.add_argument("--remove_cols",default="")
	# mainParser.add_argument("--z_score",default=None,help="None, 0, 1")
	# mainParser.add_argument("--standard_scale",default=None,help="None, 0, 1")
	# mainParser.add_argument("--clustering_method",default="average")
	# mainParser.add_argument("--clustering_distance",default="euclidean")
	mainParser.add_argument('-o',"--output",  help="output table name",default=username+"_"+str(datetime.date.today()))
	mainParser.add_argument("--header",  help="input table has header", action='store_true')
	mainParser.add_argument("--no_col_names",  help="Don't show column names in the heatmap", action='store_true')
	mainParser.add_argument("--no_row_names",  help="Don't show row names in the heatmap", action='store_true')
	mainParser.add_argument("-W", "--width", help="Figure width, by default, w=N_row/4, if given, will replace the default value",type=str,default="")
	mainParser.add_argument("-H", "--height", help="Figure height, by default, w=N_col/4, if given, will replace the default value",type=str,default="")
	# mainParser.add_argument("--no_row_names",  help="Don't show row names in the heatmap", action='store_true')
	mainParser.add_argument("--just_default",  help="just plot using default seaborn parameters", action='store_true')
	mainParser.add_argument("--log2_transform",  help="input values will be log2 transformed", action='store_true')
	mainParser.add_argument("--just_plot",  help="with this option, no filters will be applied. This program will just plot a heatmap based on the input dataframe", action='store_true')

	row_filters=mainParser.add_argument_group(title='Applying row filters to your dataframe, heatmaps will be generated for each of the following filters.')
	row_filters.add_argument('--top_N_by_row_mean',  help="plot the top N rows", default=50,type=int)
	row_filters.add_argument('--row_mean_cutoff',  help="plot the rows with a minimal mean value", default=5,type=float)
	row_filters.add_argument('--row_mean_percent_col_cutoff',  nargs='+',help="row mean cutoff, col fraction cutoff, space separated", default=[5, 0.1],type=float)


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def plot_row_filters(df,args):
	file_list = []


	print ("Processing %s"%(args.input))
	
	##
	N=args.top_N_by_row_mean
	filter_df = top_row_mean(df,n=N)
	# file_list.append(plot_clustermap(filter_df,"top_row_mean",args))
	file_list += parameter_combinatorial(filter_df,"top_row_mean",args)
	
	##
	c=args.row_mean_cutoff
	filter_df = row_mean_cutoff(df,c)
	print ("There are %s rows with at least mean value of %s"%(filter_df.shape[0],c))
	print ("These rows are:")
	print ("\n".join(filter_df.index.tolist()))
	# file_list.append(plot_clustermap(filter_df,"row_mean_cutoff",args))
	file_list += parameter_combinatorial(filter_df,"row_mean_cutoff",args)
	
	##
	frac=args.row_mean_percent_col_cutoff[1]
	c=args.row_mean_percent_col_cutoff[0]
	filter_df = row_mean_percent_col_cutoff(df,frac,c)
	print ("There are %s rows that the top %s fraction of cols have a mean value of at least %s"%(filter_df.shape[0],frac,c))
	print ("These rows are:")
	print ("\n".join(filter_df.index.tolist()))
	# file_list.append(plot_clustermap(filter_df,"row_mean_percent_col_cutoff",args))
	file_list += parameter_combinatorial(filter_df,"row_mean_percent_col_cutoff",args)
	
	return file_list
	
def plot_col_filters(df,args):
	file_list = []
	
	
	
	
	return file_list

def parameter_combinatorial(df,name,args):
	file_list = []
	file_list.append(plot_clustermap(df,name+".default",args,method='average', metric='euclidean', z_score=None, standard_scale=None))
	if args.just_default:
		return file_list
	metric_list = ["euclidean","cosine","correlation"]
	# metric_list = ["average","median","single","complete","ward"]
	method_list= ["average","ward"]
	z_score = [0,1]
	standard_scale = [0,1]
	for method in method_list:
		for metric in metric_list:
			if method == "ward" and metric != "euclidean":
				continue
			for z in z_score:
				try:
					file_list.append(plot_clustermap(df,name+".%s.%s.%s.%s"%(method,metric,z,None),args,method=method, metric=metric, z_score=z, standard_scale=None))
				except:
					continue
			for s in standard_scale:
				try:
					file_list.append(plot_clustermap(df,name+".%s.%s.%s.%s"%(method,metric,None,s),args,method=method, metric=metric, z_score=None, standard_scale=s))
				except:
					continue					
	return file_list


# def plot_clustermap(df,name,args,**kwargs):
def plot_clustermap(df,name,args,xlabel="",ylabel="",title="",reIndexDict="",show_x=True,show_y=True,figure_type="png",method='average', metric='euclidean', z_score=None, standard_scale=None):
	return clustermap(df,"%s_%s"%(args.output,name),\
	xlabel=args.xlabel,ylabel=args.ylabel,\
	title=args.title,reIndexDict=args.index_using,\
	## when plotting heatmaps, data row is show as yticks
	show_x=not args.no_col_names,show_y=not args.no_row_names,\
	W=args.width,H=args.height,figure_type=args.figure_type,\
	method=method, metric=metric, z_score=z_score, standard_scale=standard_scale)

def main():

	args = my_args()
	"""below is the same for very dataframe scripts
	
	by default our input dataframe is bed format, which is \t separated with no header no index 
	
	"""
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


	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		print ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		print ("The new job id is: "+args.jid)
	else:
		print ("The job id is: "+args.jid)	
	os.system("mkdir %s"%(args.jid))

	
	#-------------- pre-processing ----------------------
	remove_cols = str(args.remove_cols).split(",")
	try:
		remove_cols.remove("")
	except:
		pass
	if len(remove_cols)>0:
		df = df.drop(remove_cols,axis=1)
	if args.log2_transform:
		df = df.transform(lambda x:np.log2(x+1))
	
	if args.index_using != "":
		row_names = pd.read_csv(args.index_using,index_col=0,sep="\t",header=None,dtype=str)
		args.index_using = row_names[1].to_dict()
	
	
	
	
	#-------------- plot heatmap ----------------------
	file_list=[]
	
	###-------------- just plot ---------------------- 
	if args.just_plot:
		file_list += parameter_combinatorial(df,"just-plot",args)
		
	
	###-------------- plot heatmap for each filter ---------------------- 
	
	else:
		file_list += plot_row_filters(df,args)
	
	
		file_list += plot_col_filters(df,args)
	
	
	
	
	## additional commands
	for f in file_list:
		os.system("mv %s %s/"%(f,args.jid))
	os.system("cd %s;mkdir others;mv *.png others;cd others;mv *default* ../"%(args.jid))

if __name__ == "__main__":
	main()




