#!/home/yli11/.conda/envs/py2/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from liyc_utils import *
from sklearn import preprocessing
"""Plot scatter by color and shape



"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="Scatter plot given dataframe.")

	mainParser.add_argument('--index',  help=" index is false", action='store_true')
	mainParser.add_argument('-f',"--input",  help="data table input",required=True)
	mainParser.add_argument('-x',  help="X-axis",required=True)
	mainParser.add_argument('-y',  help="Y-axis",required=True)
	mainParser.add_argument('-s',"--sep",  help="separator",default="\t")
	mainParser.add_argument('--log2',  help="force to draw a dignal line", action='store_true')
	mainParser.add_argument("--xlabel",default="")
	mainParser.add_argument("--ylabel",default="")
	mainParser.add_argument("--title",default="")
	
	mainParser.add_argument("--color_using",  help="input a file, index should be the same as the input data frame",default=None)
	mainParser.add_argument("--size_using",  help="by size",default=None)
	mainParser.add_argument("--shape_using",default=None,help="by shape")
	
	# mainParser.add_argument("--figure_type",default="png",help="pdf,png,jpeg")
	mainParser.add_argument('-o',"--output",  help="output figure (html format)",default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))
	mainParser.add_argument("--header",  help="input table has header", action='store_true')

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	"""below is the same for very dataframe scripts
	
	by default our input dataframe is bed format, which is \t separated with no header no index 
	
	"""
	df = general_df_reader(args)
	plot_df = pd.DataFrame()
	plot_df['x'] = df[args.x].tolist()
	plot_df['y'] = df[args.y].tolist()
	if args.log2:
		plot_df = plot_df.transform(lambda x:np.log2(x+1))
	if args.color_using:
		plot_df['color'] = df[args.color_using].tolist()
	else:
		plot_df['color'] = 'red'
	if args.shape_using:
		plot_df['symbol'] = df[args.shape_using].tolist()
	else:
		plot_df['symbol'] = 'red'
	if args.size_using:
		plot_df['size'] = df[args.size_using].tolist()
	else:
		plot_df['size'] = 3
	if args.index:
		plot_df['text'] = df.index.tolist()
	else:
		plot_df['text'] = ""
	
	#-------------- pre-processing ----------------------
	fig = plotly_scatter(plot_df,is_discrete=True,colorscale='Viridis',showlegend=True,xlabel=args.xlabel,ylabel=args.ylabel,title=args.title,output=args.output)
	for s,d in plot_df.groupby("color"):
		x = d.x.mean()
		y = d.y.mean()
		fig.add_annotation(x=x, y=y,
				text=s,
				showarrow=False)
	fig.write_html('%s.with_text.html'%(args.output), include_plotlyjs=True,auto_open=False)
if __name__ == "__main__":
	main()




