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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="NGS read counts normalization")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--input",  help="TSV file, 1 or 2 columns. If the 2nd col is available, it will be used as control.",required=True)
	mainParser.add_argument("--S3norm_input", help=argparse.SUPPRESS)
	mainParser.add_argument("--converter_input", help=argparse.SUPPRESS)
	mainParser.add_argument("--bdg_to_bw_files", help=argparse.SUPPRESS)

	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-bam',  help="input files are bam, bam need index",action='store_true')
	group.add_argument("-bw",  help="input files are bigwig",action='store_true')	
	group.add_argument("-bdg",  help="input files are bedgraph",action='store_true')	

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def create_converter_input(args):
	df = pd.read_csv(args.input,sep="\t",header=None)
	files=[]
	for c in df.columns:
		files += df[c].tolist()
	files = list(set(files))
	labels = [".".join(x.split(".")[:-1])+".s3norm.bdg" for x in files]
	out = pd.DataFrame()
	out[0] = files
	out[1] = labels
	outfile = args.jid+".converter.input"
	out.to_csv(outfile,sep="\t",header=False,index=False)
	args.converter_input=outfile
	out.index = out[0]
	for c in df.columns:
		df[c] = df[c].map(out[1].to_dict())	
	# df = df.map()
	outfile = args.jid+".S3norm.input"
	df.to_csv(outfile,sep="\t",header=False,index=False)
	args.S3norm_input=outfile
	
	## bdg to bw input
	# .s3norm.bdg.s3norm.bedgraph
	# .s3norm.bdg.NBP.s3norm.bedgraph
	labels_col1 = [x+".NBP.s3norm.bedgraph" for x in labels] + [x+".s3norm.bedgraph" for x in labels]
	labels2 = [".".join(x.split(".")[:-1])+".bw" for x in labels_col1]
	out = pd.DataFrame()
	out[0] = labels_col1
	out[1] = labels2
	outfile = args.jid+".bdg_to_bw_files.input"
	out.to_csv(outfile,sep="\t",header=False,index=False)
	args.bdg_to_bw_files=outfile
	
def main():

	args = my_args()
	args.chrom_size = myData['%s_chrom_size'%(args.genome)]

		
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			

	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	pipeline_name = current_file_base_name
	if args.bam:
		pipeline_name+="_bam"
	if args.bw:
		pipeline_name+="_bw"
	if args.bdg:
		pipeline_name+="_bdg"
		
		
	create_converter_input(args)
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()






































