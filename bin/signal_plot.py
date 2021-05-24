#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


"""
Every python wrapper is supposed to be similar, since they are using the same convention.

The only thing need to be changed is the guess_input function and the argparser function.

look for ## CHANGE THE FUNCTION HERE FOR DIFFERENT WRAPPER

variable inherents from utils:
myData
myPars
myPipelines
"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="plot bigwiggle signals and heatmaps given a list of bed files")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_%s_"%(addon_string)+str(datetime.date.today()))	
	mainParser.add_argument('--pipeline_type',  help="Not for end-user.", default=current_file_base_name)
	mainParser.add_argument('--figure_type',  help="pdf or png", default="png")
	mainParser.add_argument("--bed",  help="a list of bed files, any number of columns, the first three columns have to be chr, start, end")
	mainParser.add_argument("--computeMatrix_addon_parameters",  help="add user-defined parameters to computeMatrix",default="")
	mainParser.add_argument("--plotHeatmap_addon_parameters",  help="add user-defined parameters to plotHeatmap",default=" --regionsLabel ${COL2}")
	mainParser.add_argument("-u",  help="upstream flanking length",default=5000,type=int)
	mainParser.add_argument("-d",  help="downstream flanking length",default=5000,type=int)
	mainParser.add_argument("-m",'--memory',  help="memory limit, higher the limit, longer the wait time for your job to start",default=4000,type=int)
	mainParser.add_argument("--commands_list",  help="not for end-user")
	mainParser.add_argument("--bw_files",  help="not for end-user")
	mainParser.add_argument("--bed_files",  help="not for end-user")
	mainParser.add_argument("--samplesLabel_list",  help="not for end-user")
	mainParser.add_argument("--regionsLabel_list",  help="not for end-user")
	mainParser.add_argument("--input_list",  help="not for end-user")
	mainParser.add_argument("--max_value",  help="generally it is not used, only if you want to scale all plots into the same range",default=9999,type=float)
	mainParser.add_argument("--min_value",  help="generally it is not used, only if you want to scale all plots into the same range",default=9999,type=float)
	# mainParser.add_argument("--region_plot",  help="By default, only the centers in bed files with extended regions are used. This option enables plotting signals on the given regions plus extended flanking regions",action='store_true')
	mainParser.add_argument("--one_plot_per_bw",  help="Use this option when you want to edit the generated pdf by yourself.",action='store_true')

	
	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument("--multi_bw_to_one_bed",  help="5 columns tsv, path_to_bed, bed_label, path_to_bw, bw_file_label, output_name. Most common usage.",default="None")
	group.add_argument("--one_to_one",  help="5 columns tsv, path_to_bed, bed_label, path_to_bw, bw_file_label, output_name. Most common usage.",default="None")		
	group.add_argument("--multi_to_multi",  help="5 columns tsv, path_to_bed, bed_label, path_to_bw, bw_file_label, output_name. Most common usage.",default="None")		

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def check_input(df,c):
	for f in df[c]:
		if not os.path.isfile(f):
			print (f," not found")
			print ("Exiting..")
			exit()

def multi_bw_to_one_bed_input(args):
	df = pd.read_csv(args.multi_bw_to_one_bed,sep="\t",header=None)
	check_input(df,0)
	check_input(df,2)
	tmp = df.copy()
	tmp = tmp.drop_duplicates(2)
	args.bw_files = " ".join(tmp[2].tolist())
	args.samplesLabel_list = " ".join(tmp[3].tolist())
	
	df = df.drop_duplicates(0)
	df[[0,1,4]].to_csv("%s.input"%(args.jid),sep="\t",index=False,header=False)
	args.input_list = "%s.input"%(args.jid)
	
def multi_to_multi_input(args):
	df = pd.read_csv(args.multi_to_multi,sep="\t",header=None)
	check_input(df,0)
	check_input(df,2)
	tmp = df.copy()
	# tmp = tmp.drop_duplicates(2)
	args.bw_files = " ".join(tmp[2].unique().tolist())
	args.bed_files = " ".join(tmp[0].unique().tolist())
	args.samplesLabel_list = " ".join(tmp[3].unique().tolist())
	args.regionsLabel_list = " ".join(tmp[1].unique().tolist())


def main():

	args = my_args()
	

		
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)		


	## ------------ generate commands -----------------
	
	
	

	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	if args.one_to_one != "None":
		df = pd.read_csv(args.one_to_one,sep="\t",header=None)
		check_input(df,0)
		check_input(df,2)		
		submit_pipeline_jobs(myPipelines["signal_plot_one2one"],args)
	if args.multi_bw_to_one_bed != "None":
		multi_bw_to_one_bed_input(args)
		submit_pipeline_jobs(myPipelines["signal_plot_multile_bw_one_bed"],args)
	if args.multi_to_multi != "None":
		multi_to_multi_input(args)
		submit_pipeline_jobs(myPipelines["signal_plot_multi_bw_multi_bed"],args)
	

# def run_computMatrix(args):

	# if args.region_plot:
		# command = 'computeMatrix scale-regions -R {{bed_files}} -S {{bw_files}} -b {{u}} -a {{d}} -o {{output}}_matrix.gz --samplesLabel {{samplesLabel_list}} --skipZeros'
	# else:
		# command = 'computeMatrix reference-point --referencePoint center -R {{bed_files}} -S {{bw_files}} -b {{u}} -a {{d}} -o {{output}}_matrix.gz --samplesLabel {{samplesLabel_list}} --skipZeros'

	# return command


# def run_plotHeatmap(x,y,i):
	# if args.region_plot:
		# command = """plotHeatmap --missingDataColor 1 --dpi 600 --heatmapHeight 15 --regionsLabel {{regionsLabel_list}} -m {{output}}_matrix.gz -out {{output}}.pdf """
	
		# command = 'plotHeatmap --missingDataColor 1 --yMin 0.5 --yMax 1.75 --dpi 600 --heatmapHeight 15 --whatToShow "plot and heatmap"  --regionsLabel "GUIDE-seq" "CHANGE-seq" "Cas-OFFinder" "Random" -x "" --refPointLabel center -m all{{number}}_'.replace("{{number}}",str(i))+x+'_matrix.gz -out '+x+".random.{{number}}.pdf --colorList 'white,".replace("{{number}}",str(i)) + y +"'" 
	# else:
		# command = 'plotHeatmap --missingDataColor 1 --legendLocation none --yMin 0.5 --yMax 1.75 --dpi 600 --heatmapHeight 15 --whatToShow "plot and heatmap"  --regionsLabel "GUIDE-seq" "CHANGE-seq" "Cas-OFFinder" "Random" -x "" --refPointLabel center -m all{{number}}_'.replace("{{number}}",str(i))+x+'_matrix.gz -out '+x+".random.{{number}}.pdf --colorList 'white,".replace("{{number}}",str(i)) + y +"'" 
	# print command
	# os.system(command)
		
if __name__ == "__main__":
	main()







































