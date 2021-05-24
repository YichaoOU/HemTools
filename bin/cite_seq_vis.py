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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="cite-seq visualization pipeline")

	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('--current_dir',  help="run in current dir, suppose cellRanger is finished correctly", action='store_true')
	group.add_argument('--input_csv',  help="manually input csv")

	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	# mainParser.add_argument('-f','--input_csv',  help="Need at least 2 columns with column names, Sample,Location, see: https://pegasus.readthedocs.io/en/stable/usage.html", required=True)
	mainParser.add_argument('--MT_prefix',  help=argparse.SUPPRESS)
	mainParser.add_argument('--MT_percent',  help="MT_percent, default is 20, sometimes I use 10 or 5", default=20,type=float)
	mainParser.add_argument('--max_genes',  help="max_genes", default=6000,type=int)
	mainParser.add_argument('-o',"--output",  help="output prefix",default="sc_integration_"+username+"_"+str(datetime.date.today()))

	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

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

	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	
	if "hg" in args.genome:
		args.MT_prefix = "MT-"
	if "mm" in args.genome:
		args.MT_prefix = "mm-"
	if args.current_dir:
		## get input
		files = glob.glob("*/outs/filtered_feature_bc_matrix.h5")
		if len(files) == 0:
			print ("can't find h5 files. Please check */outs/filtered_feature_bc_matrix.h5")
			exit()
		out = "%s.input.csv"%(args.output)
		lines = []
		for f in files:
			label = f.split("/")[0]
			lines.append([label,f,args.genome])
		df = pd.DataFrame(lines,columns = ['Sample','Location','Genome'])
		df.to_csv(out,index=False)
		args.input_csv = out
	submit_pipeline_jobs(myPipelines[current_file_base_name],args)

		
if __name__ == "__main__":
	main()







































