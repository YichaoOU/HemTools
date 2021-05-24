#!/home/yli11/.conda/envs/py2/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from liyc_utils import *
from sklearn import preprocessing
"""Plot high dimension data given data frame

in all input data frame, we assume rows are samples and cols are features.

parameters
----------

By default, no header, no index, all content are numeric.

Users can add their own annotation.

--color_by_a_feature

--size_by_a_feature

--text_by_a_col (will remove this column when doing PCA)

--color_by_a_col  (will remove this column when doing PCA)

for this, please use HEX code, e.g., #12efff

--size_by_a_col  (will remove this column when doing PCA)

UMAP, tSNE parameters

process
-------


log2 transform or not
row_norm or not
col_norm or not

PCA
UMAP
sparsePCA
kernelPCA
PCA using randomized SVD
TruncatedSVD 



PCA-100-tSNE
PCA-100-MDS

seaborn.scatterplot or plt.scatter

Each of them have different advantanges

seaborn.scatterplot good for discrete color mapping

https://scikit-learn.org/stable/auto_examples/ensemble/plot_random_forest_embedding.html#sphx-glr-auto-examples-ensemble-plot-random-forest-embedding-py


https://jlmelville.github.io/uwot/abparams.html

https://umap-learn.readthedocs.io/en/latest/parameters.html

"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="plot heatmap given dataframe.")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	

	mainParser.add_argument('--remove_zero',  help="remove all rows or cols that are zero", action='store_true')
	mainParser.add_argument('--index',  help=" index is false", action='store_true')
	mainParser.add_argument('--binarize',  help=" force to binary data", action='store_true')
	mainParser.add_argument('--max',  help=" above this value to determine 1", default=1,type=float)
	mainParser.add_argument('--min',  help=" above this value to determine 0", default=0,type=float)
	mainParser.add_argument('--transpose',  help=" df transpose", action='store_true')
	mainParser.add_argument('--sample_norm',  help=" sample norm by sum", action='store_true')
	mainParser.add_argument('-f',"--input",  help="data table input",required=True)
	mainParser.add_argument("--use_cols",  help="use a subset cols",default=None)
	mainParser.add_argument("--index_using",  help="Sometimes we want to show a different label for the indices, then use this option. For example, gene id is unique, however, gene name can be different, it also has upper or lower case problem, in such case, we want to use gene id for data processing and use gene name for visualization.",default="")
	mainParser.add_argument('-s',"--sep",  help="separator",default="\t")
	
	mainParser.add_argument("--xlabel",default="")
	mainParser.add_argument("--ylabel",default="")
	mainParser.add_argument("--remove_cols",default="")
	mainParser.add_argument("--random_frac",default=None)
	
	group = mainParser.add_mutually_exclusive_group()
	group.add_argument("--color_using",  help="input a file, index should be the same as the input data frame",default="None")
	group.add_argument("--color_by_a_col",default="None",help="input a column name to be used for coloring")
	group.add_argument("--shape_by_str",default="None",help="input a string to match sample name, matched and unmatched names will have different name; used to show our own data vs public data.")
	
	mainParser.add_argument("-n",'--maxPC',default=2,type=int)
	mainParser.add_argument("--UMAP_min_dist",default=0.01,type=float)
	mainParser.add_argument("--UMAP_metric",default="euclidean",type=str)
	mainParser.add_argument("--UMAP_n_neighbors",default=15,type=int)
	mainParser.add_argument("--title",default=username+"_"+str(datetime.date.today()))
	mainParser.add_argument("--label_by_last3_element", action='store_true')
	mainParser.add_argument("--smart_label", action='store_true')
	mainParser.add_argument("--kmeans_label", default=-1,type=int)
	mainParser.add_argument("--dbscan_label", action='store_true')
	mainParser.add_argument("--guess_label", action='store_true')
	mainParser.add_argument("--continous", action='store_true')
	# mainParser.add_argument("--gene_filter", action='store_true')
	mainParser.add_argument("--gene_filter_cutoff", type=float,default=-999)
	# https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0149853
	# mainParser.add_argument("--binarize", action='store_true')
	mainParser.add_argument("--label_by_first_element", action='store_true')
	mainParser.add_argument("--label_by_first4_element", action='store_true')
	mainParser.add_argument("--zero_mean_unit_variance", action='store_true')
	mainParser.add_argument("--label_by_meaningful_name", action='store_true')
	mainParser.add_argument("--nPC_list", default=None)
	mainParser.add_argument("--UMAP", action='store_true')
	mainParser.add_argument("--nPCA_UMAP", default=None,type=int)
	mainParser.add_argument("--text", action='store_true')
	mainParser.add_argument("--save_projection_df", action='store_true')
	mainParser.add_argument("--figure_type",default="png",help="pdf,png,jpeg")
	mainParser.add_argument('-o',"--output",  help="output table name",default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))
	mainParser.add_argument("--header",  help="input table has header", action='store_true')
	mainParser.add_argument("-W", "--width", help="Figure width, by default, w=N_row/4, if given, will replace the default value",type=int,default=500)
	mainParser.add_argument("-H", "--height", help="Figure height, by default, w=N_col/4, if given, will replace the default value",type=int,default=500)
	mainParser.add_argument("--log2_transform",  help="input values will be log2 transformed", action='store_true')


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def do_PCA(df,args,n=2,plot=True):
	print ("Performing PCA...")
	pca = PCA(n_components=n)
	print ("input data frame size:%s"%(df.shape[0]))
	# remove_cols = str(args.remove_cols).split(",")
	tmp_df = df.copy()
	print (tmp_df.head())
	# if len(remove_cols)>0:
		# tmp_df = tmp_df.drop([remove_cols],axis=1)
	# tmp_df = df.select_dtypes(['number'])
	print ("numeric data frame size:%s"%(tmp_df.shape[0]))
	if args.color_by_a_col != "None":
		tmp_df = tmp_df.drop([args.color_by_a_col],axis=1)
	flag_nan = tmp_df.isnull().any().any()
	print ("contain NaN values? %s"%(flag_nan))
	if flag_nan:
		print (tmp_df[tmp_df.isna().any(axis=1)].head())
		print ("Will fill NaN by zero")
		tmp_df = tmp_df.fillna(0)
	print ("Input size for PCA is:%s X %s"%(tmp_df.shape[0],tmp_df.shape[1]))
	transform_df_all = pd.DataFrame(pca.fit_transform(tmp_df))
	transform_df = transform_df_all[[0,1]]
	transform_df.columns=['x','y']
	if args.shape_by_str:
		transform_df['symbol'] = [define_shape(x,args.shape_by_str) for x in df.index.tolist()]	
	if plot:
		xlabel="PC1 ({0:.1%})".format(pca.explained_variance_ratio_[0])
		ylabel="PC2 ({0:.1%})".format(pca.explained_variance_ratio_[1])
		if args.color_by_a_col == "None":
			transform_df['color']="red"
		else:
			transform_df['color']=df[args.color_by_a_col].tolist()
		transform_df['text']=df.index.tolist()
		transform_df_all['color'] = transform_df['color']
		transform_df_all['text'] = df.index.tolist()
		transform_df['size']=5	
		# print (transform_df.head())
		print ("generating figure...")
		if args.save_projection_df:
			transform_df_all.to_csv("%s_projection.csv"%(args.output),index=False)
		plotly_scatter(transform_df,is_discrete=not args.continous,colorscale='Viridis',showlegend=True,xlabel=xlabel,ylabel=ylabel,title="PCA_"+args.title,figure_type=args.figure_type,output=args.output,width=args.width,height=args.height,text=args.text)
	return transform_df

def define_shape(x,q):
	if q in x:
		return "Public"
	else:
		return "Our Own"
	
def do_UMAP(df,args,n=2,plot=True):
	print ("Performing UMAP...")
	args.output += "_minDist_%s_metric_%s_nNeighbor_%s"%(args.UMAP_min_dist,args.UMAP_metric,args.UMAP_n_neighbors)
	try:
		umap_obj = umap.UMAP(n_components=n,random_state=0,min_dist=args.UMAP_min_dist,metric=args.UMAP_metric,n_neighbors=args.UMAP_n_neighbors)
	except:
		print ("Input UMAP parameters invalid, using default")
		umap_obj = umap.UMAP(n_components=n,random_state=0)
	print ("input data frame size:%s"%(df.shape[0]))
	# remove_cols = str(args.remove_cols).split(",")
	tmp_df = df.copy()
	print (tmp_df.head())
	# if len(remove_cols)>0:
		# tmp_df = tmp_df.drop([remove_cols],axis=1)
	# tmp_df = df.select_dtypes(['number'])
	print ("numeric data frame size:%s"%(tmp_df.shape[0]))
	if args.color_by_a_col != "None":
		tmp_df = tmp_df.drop([args.color_by_a_col],axis=1)
	# print (tmp_df.head())
	flag_nan = tmp_df.isnull().any().any()
	print ("contain NaN values? %s"%(flag_nan))
	if flag_nan:
		print (tmp_df[tmp_df.isna().any(axis=1)].head())
		print ("Will fill NaN by zero")
		tmp_df = tmp_df.fillna(0)	
	print ("Input size for UMAP is:%s X %s"%(tmp_df.shape[0],tmp_df.shape[1]))
	transform_df_all = pd.DataFrame(umap_obj.fit_transform(tmp_df.values))
	transform_df = transform_df_all[[0,1]]
	transform_df.columns=['x','y']
	if args.shape_by_str:
		transform_df['symbol'] = [define_shape(x,args.shape_by_str) for x in df.index.tolist()]
	if plot:
		xlabel="UMAP-1"
		ylabel="UMAP-2"
		if args.color_by_a_col == "None":
			transform_df['color']="red"
		else:
			transform_df['color']=df[args.color_by_a_col].tolist()
		transform_df_all['color'] = transform_df['color']
		transform_df_all['text'] = df.index.tolist()
		transform_df['text']=df.index.tolist()
		transform_df['size']=5	
		# print (transform_df.head())
		print ("generating figure...")
		if args.save_projection_df:
			transform_df_all.to_csv("%s_projection.csv"%(args.output),index=False)		
		args.output = args.output.replace("PCA","UMAP")
		plotly_scatter(transform_df,is_discrete=not args.continous,colorscale='Viridis',showlegend=True,xlabel=xlabel,ylabel=ylabel,title="UMAP_"+args.title,figure_type=args.figure_type,output=args.output,width=args.width,height=args.height,text=args.text)
	return transform_df
	
def do_nPCA_UMAP(df,args,n=2,plot=True):
	# print ("Performing UMAP...")
	output = args.output+"_nPCA_%s_minDist_%s_metric_%s_nNeighbor_%s"%(args.nPCA_UMAP,args.UMAP_min_dist,args.UMAP_metric,args.UMAP_n_neighbors)
	try:
		umap_obj = umap.UMAP(n_components=n,random_state=0,min_dist=args.UMAP_min_dist,metric=args.UMAP_metric,n_neighbors=args.UMAP_n_neighbors)
	except:
		print ("Input UMAP parameters invalid, using default")
		umap_obj = umap.UMAP(n_components=n,random_state=0)
	print ("input data frame size:%s"%(df.shape[0]))
	# remove_cols = str(args.remove_cols).split(",")

	print ("Performing PCA...")
	pca = PCA(n_components=args.nPCA_UMAP)
	tmp_df = df.copy()
	print (tmp_df.head())
	print ("numeric data frame size:%s"%(tmp_df.shape[0]))
	if args.color_by_a_col != "None":
		tmp_df = tmp_df.drop([args.color_by_a_col],axis=1)
	flag_nan = tmp_df.isnull().any().any()
	print ("contain NaN values? %s"%(flag_nan))
	if flag_nan:
		print (tmp_df[tmp_df.isna().any(axis=1)].head())
		print ("Will fill NaN by zero")
		tmp_df = tmp_df.fillna(0)
	print ("Input size for PCA is:%s X %s"%(tmp_df.shape[0],tmp_df.shape[1]))
	print (tmp_df.head())
	transform_df_all = pd.DataFrame(pca.fit_transform(tmp_df))
	print ("output size for PCA is: %s X %s"%(transform_df_all.shape[0],transform_df_all.shape[1]))
	
	print ("Performing UMAP...")
	transform_df_all = pd.DataFrame(umap_obj.fit_transform(transform_df_all.values))
	transform_df = transform_df_all[[0,1]]
	transform_df.columns=['x','y']
	print (transform_df.head())
	if args.shape_by_str:
		transform_df['symbol'] = [define_shape(x,args.shape_by_str) for x in df.index.tolist()]
	if plot:
		xlabel="UMAP-1"
		ylabel="UMAP-2"
		if args.color_by_a_col == "None":
			transform_df['color']="red"
		else:
			transform_df['color']=df[args.color_by_a_col].tolist()
		transform_df_all['color'] = transform_df['color']
		transform_df_all['text'] = df.index.tolist()
		transform_df['text']=df.index.tolist()
		transform_df['size']=5	
		# print (transform_df.head())
		print ("generating figure...")
		output = output.replace(".html","html")
		print (output)
		if args.save_projection_df:
			transform_df_all.to_csv("%s_projection.csv"%(output),index=False)		
		
		plotly_scatter(transform_df,is_discrete=not args.continous,colorscale='Viridis',showlegend=True,xlabel=xlabel,ylabel=ylabel,title="UMAP_"+args.title,figure_type=args.figure_type,output=output,width=args.width,height=args.height,text=args.text)
	return transform_df	
	
def contains(query,db):
	for s in db:
		if s in query:
			return True
	return False

def smart_label(x):
	x = x.replace(".tpm","").replace(".gz","")
	out = []
	x = x.upper()
	tabu_list = ['SRR','GSM','GEO']
	for i in re.split('_|-|\.|,',x):
		if contains(i,tabu_list):
			continue
		out.append(i)
	return "_".join(out)


def highlight_genes_UMAP(x,y,gene_ids,myDict,nPC=100):
	df = pd.read_csv(x,index_col=0)
	# df = df.transform(lambda x:np.log2(x+1))	
	df = df.T
	# print (df.values)
	# tmp_df2 = pd.DataFrame(umap.UMAP(repulsion_strength=5).fit_transform(df.values))
	tmp_df2 = pd.DataFrame(umap.UMAP().fit_transform(df.values))
	# print ("tmp_df2.shape",tmp_df2.shape)
	Parallel(n_jobs=10,verbose=10)(delayed(make_plot)(df,tmp_df2,y,g,myDict[g]) for g in gene_ids)

def highlight_genes_UMAP(x,y,gene_ids,myDict,nPC=100):
	df = pd.read_csv(x,index_col=0)
	# df = df.transform(lambda x:np.log2(x+1))	
	df = df.T
	# print (df.values)
	# tmp_df2 = pd.DataFrame(umap.UMAP(repulsion_strength=5).fit_transform(df.values))
	tmp_df2 = pd.DataFrame(umap.UMAP().fit_transform(df.values))
	# print ("tmp_df2.shape",tmp_df2.shape)
	Parallel(n_jobs=10,verbose=10)(delayed(make_plot)(df,tmp_df2,y,g,myDict[g]) for g in gene_ids)

def parse_df(x,y,gene_ids,myDict,nPC=100):
	df = pd.read_csv(x,index_col=0)
	df = df.transform(lambda x:np.log2(x+1))	
	df = df.T
	return df
	
def gene_filter(df,cutoff):
	tmp = df.copy()
	# genes were filtered with TPM value > cutoff in at least 50% of the samples
	# https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0149853
	N = tmp.shape[0]
	tmp[tmp<cutoff]=0
	tmp[tmp>=cutoff]=1
	select_cols = tmp.columns[tmp.sum()>=(N/2.0-0.5)].tolist()
	return df[select_cols]
	
	

def get_meaningful_label(x):
	lines = re.split('_|-|\.|,',x)
	elem_list = []
	for l in lines:
		l = l.lower()
		l = l.replace("rnaseq","")
		try:
			t = l.replace("r","")
			t = t.replace("rep","")
			t = t.replace("s","")
			int(t)
		except:
			if "srr" in l:
				continue
			if "geo" in l:
				continue
			if "gse" in l:
				continue
			l.replace("_","")
			# print (l)
			if l == "":
				continue
			elem_list.append(l)
	return "_".join(elem_list)

def binarize_column(myList,min,max):
	out = []
	for v in myList:
		if v >= max:
			out.append(1)
		elif v <=min:
			out.append(0)
		else:
			out.append(-1)
	return out
def remove_zero(df,cutoff=0):
	col_sum = df.sum()
	col_sum2 = col_sum[col_sum>cutoff]
	row_sum = df.sum(axis=1)
	row_sum2 = row_sum[row_sum>cutoff]
	return col_sum2.index.tolist(),row_sum2.index.tolist()
def main():

	args = my_args()
	"""below is the same for very dataframe scripts
	
	by default our input dataframe is bed format, which is \t separated with no header no index 
	
	"""
	df = general_df_reader(args)
	if args.use_cols != None:
		cols = args.use_cols.split(",")
		df = df[cols]
	if args.random_frac:
		df = df.sample(frac = float(args.random_frac))
		args.save_projection_df = True
	# df = df.sample(frac=1)
	if args.binarize:
		df = df.fillna(0)
		tmp = df[args.color_by_a_col].tolist()
		df[args.color_by_a_col] = binarize_column(tmp,args.min,args.max)
		df = df[df[args.color_by_a_col]>=0]
	remove_cols = str(args.remove_cols).split(",")
	try:
		remove_cols.remove("")
	except:
		pass
	if len(remove_cols)>0:
		print (df.head())
		df = df.drop(remove_cols,axis=1)
	if args.transpose:
		df = df.T

	if args.gene_filter_cutoff != -999:
		print ("Filtering genes with above %s in at least half of samples"%(args.gene_filter_cutoff))
		print ("Before dataframe shape:",df.shape)
		df = gene_filter(df,args.gene_filter_cutoff)
		print ("After dataframe shape:",df.shape)
	if args.zero_mean_unit_variance:
		tmp = pd.DataFrame(preprocessing.scale(df))
		tmp.index = df.index.tolist()
		tmp.columns = df.columns.tolist()
		df = tmp.copy()			
	if args.label_by_first_element:
		df['group'] = [re.split('_|-|\.|,',x)[0] for x in df.index.tolist()]
		args.color_by_a_col = 'group'
	if args.label_by_first4_element:
		df['group'] = ["_".join(re.split('_|-|\.|,',x)[:4]) for x in df.index.tolist()]
		args.color_by_a_col = 'group'
	if args.kmeans_label >= 2:
		df['group'] = group_similar_names(df.index.tolist(),args.kmeans_label)
		args.color_by_a_col = 'group'
	if args.dbscan_label:
		df['group'] = group_similar_names_dbscan(df.index.tolist())
		args.color_by_a_col = 'group'
	if args.guess_label:
		df['group'] = guess_label(df.index.tolist())
		args.color_by_a_col = 'group'
	if args.smart_label:
		df['group'] = [smart_label(x) for x in df.index.tolist()]
		args.color_by_a_col = 'group'
	if args.label_by_last3_element:
		df['group'] = ["_".join(re.split('_|-|\.|,',x)[-3:]) for x in df.index.tolist()]
		args.color_by_a_col = 'group'
	if args.label_by_meaningful_name:
		df['group'] = [get_meaningful_label(x) for x in df.index.tolist()]
		args.color_by_a_col = 'group'
	if not args.color_using == "None":
		args.input = args.color_using
		color_df = general_df_reader(args)
		print (color_df.head())
		df['group'] = color_df[color_df.columns[-1]]
		args.color_by_a_col = 'group'
	##------- check if jid exist  ----------------------
	# if isdir(args.jid):
		# addon_string = str(uuid.uuid4()).split("-")[-1]
		# print ("The input job id is not available!")
		# args.jid = args.jid+"_"+addon_string
		# print ("The new job id is: "+args.jid)
	# else:
		# print ("The job id is: "+args.jid)	
	# os.system("mkdir %s"%(args.jid))

	
	#-------------- pre-processing ----------------------
	print ("Input data size is:%s X %s"%(df.shape[0],df.shape[1]))
	if args.remove_zero:
		# print (df.head())
		print ("removing zero")
		c,r = remove_zero(df.drop([args.color_by_a_col],axis=1))
		df = df.loc[r,c+[args.color_by_a_col]]
		print ("size after remove zero:",df.shape)

	if args.log2_transform:
		# print (df.head())
		if df.shape[1]>100:
			df2 = df.drop([args.color_by_a_col],axis=1).transform(lambda x:np.log2(x+1))
			df2[args.color_by_a_col] = df[args.color_by_a_col]
			df = df2
			del df2
			import gc
			gc.collect()
		else:
			for c in df.columns:
				if c == args.color_by_a_col:
					print ("not doing log2 transformation for %s"%(args.color_by_a_col))
					continue
				try:
					df[c] = df[c].astype(float)
					# print (c)
					df[c] = df[c].apply(lambda x:np.log2(x+1))
				except:
					pass

	if args.sample_norm:
		tmp = df.copy()
		print (df.head())
		sel_col = df.columns.tolist()
		sel_col.remove("group")
		tmp = tmp[sel_col]
		tmp = tmp.div(tmp.sum(axis=1), axis=0)
		tmp['group'] = df['group']
		df = tmp.copy()
		# df = df.transform()
	if args.UMAP:
		do_UMAP(df,args,n=args.maxPC)
	elif args.nPCA_UMAP:
		print (args.nPC_list)
		if args.nPC_list:
			for i in args.nPC_list.split(","):
				print ("trying nPC size",i)
				args.nPCA_UMAP = int(i)
				do_nPCA_UMAP(df,args,n=args.maxPC)
		else:
			do_nPCA_UMAP(df,args,n=args.maxPC)

	else:
		do_PCA(df,args,n=args.maxPC)
	
	
	
	
	
	## additional commands
	# for f in file_list:
		# os.system("mv %s %s/"%(f,args.jid))
	# os.system("cd %s;mkdir others;mv *.png others;cd others;mv *default* ../"%(args.jid))

if __name__ == "__main__":
	main()




