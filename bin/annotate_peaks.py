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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="annotate your bed files given a list of bed files, bedGraph files, or narrowPeak files. The input list can't contain a mix of types.")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('--pipeline_type',  help="Not for end-user.", default=current_file_base_name)
	mainParser.add_argument('-w','--window_size',  help="feature window size, use the center of you input bed file, and create several windows both upstream and downstream, then your input file list will be used to overlap with each of these windows.", default=200,type=int)
	mainParser.add_argument('-s','--step_size',  help="How to create each window (where to set window start site). If step_size >= window_size, then it means no overlap between each window.", default=100,type=int)
	mainParser.add_argument('-n','--number_steps',  help="How many windows to create (i.e., how many steps you want to go). Note that number of bins = n-1. The actual bp to the center is n*s+w", default=5,type=int)
	mainParser.add_argument('-l',"--feature_list",  help="a tsv file containing 2 columns, feature name & feature file (with path)",required=True)
	mainParser.add_argument('-t',"--feature_type",  help="can be bed, bedGraph, or narrowPeak. Case insensitive. Currently, only bedGraph or narrowPeak is implemented.",default="narrowPeak")
	mainParser.add_argument("--bed_list",  help="NOT FOR END-USER")
	mainParser.add_argument('-g',"--genome",  help="homer genome, hg18, hg19, mm9, mm10. Case sensitive!",default="hg19")
	mainParser.add_argument("-f","--input",  help="a bed file with at least 4 columns, additional columns will be kept when output the result. The first 4 columns are chr, start, end, unique name. This file should be in the same dir where you run this command.",required=True)
	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def extend_bed(args):

	file_list = []
	bed_name = args.input.split("/")[-1].split(".")
	bed_name = ".".join(bed_name[:-1])
	df = pd.read_csv(args.input,sep="\t",header=None)
	df['c'] = (df[1]+df[2])/2
	df["c"] = df['c'].astype(int)
	# further_site = 0
	# closer_site = 0
	# print df.head()
	for i in range(args.number_steps):
		# further_site = (i+1)*args.step_size
		start_site = i*args.step_size
		u = df.copy() ## upstream extending
		d = df.copy() ## downstream extending
		# u['start'] = u['c']-(start+1)*args.window_size
		# u['end'] = u['c']-(start)*args.window_size
		# d['start'] = d['c']+(start)*args.window_size
		# d['end'] = d['c']+(start+1)*args.window_size
		# u['start'] = u['c']-(further_site+args.window_size)
		# u['end'] = u['c']-(closer_site+args.window_size)
		# d['start'] = d['c']+(closer_site+args.window_size)
		# d['end'] = d['c']+(further_site+args.window_size)
		u['start'] = u['c']-(start_site+args.window_size)
		u['end'] = u['c']-(start_site)
		d['start'] = d['c']+(start_site)
		d['end'] = d['c']+(start_site+args.window_size)
		u_name = "%s_upstream_%s_%s.bed"%(bed_name,(start_site),(start_site+args.window_size))
		d_name = "%s_downstream_%s_%s.bed"%(bed_name,(start_site),(start_site+args.window_size))
		u[[0,'start','end',3]].to_csv(u_name,sep="\t",index=False,header=False)
		d[[0,'start','end',3]].to_csv(d_name,sep="\t",index=False,header=False)
		file_list.append(u_name)
		file_list.append(d_name)
	os.system("cp %s %s.center.bed"%(args.input,bed_name))
	file_list.append("%s.center.bed"%(bed_name))
	outFile = "%s.homer.input"%(args.jid)
	write_file(outFile,"\n".join(file_list))
	return file_list,outFile
	
def convert_to_bdg(args):
	with open(args.feature_list) as f:
		for line in f:
			if len(line) < 2:
				continue
			line = line.strip().split()
			if args.feature_type == "narrowPeak":
				command = "cut -f 1,2,3,9 %s > %s/%s.bdg"%(line[-1],args.jid,line[0])
				os.system(command)
			if args.feature_type == "bedGraph":
				command = "cut -f 1,2,3,4 %s > %s/%s.bdg"%(line[-1],args.jid,line[0])
				os.system(command)

			
def redefine_header(args):
	
	python_script="""
	
import pandas as pd
import sys

def parse_df(f):
	df = pd.read_csv(f,sep="\\t")
	df.columns = [x.replace(".bdg bedGraph avg over given bp","").split(" (cmd=annotatePeaks.pl")[0] for x in df.columns]
	df = df.fillna(0)
	df.to_csv(f,index=False,sep="\\t")	

parse_df(sys.argv[1])	
	
	"""
	write_file(args.jid+"/tmp.py",python_script)
	

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

	##------- check inputs exist  ----------------------
	logging.info("checking input files...")
	input_error=False
	if not isfile(args.input):
		logging.error("%s not found"%(args.input))
		input_error=True
	dos2unix(args.feature_list)
	with open(args.feature_list) as f:
		for line in f:
			if len(line) < 2:
				continue
			line = line.strip().split()
			if not isfile(line[-1]):
				logging.error("%s not found"%(line[-1]))
				input_error=True
	if input_error:
		logging.error("Please check your input. See above message.")
		logging.error("Program exiting...")
		sys.exit(1)
	else:
		logging.info("All input files are found. Submitting jobs...")
				
			

	## ------------ generate commands -----------------
	
	
	

	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	
	## additional commands
	convert_to_bdg(args)
	file_list,outFile = extend_bed(args)
	args.bed_list = outFile
	redefine_header(args)
	
	if args.feature_type != "bed":
		pipeline_name = current_file_base_name+"_bdg"
		submit_pipeline_jobs(myPipelines[pipeline_name],args)
	
	## additional commands
	for f in file_list:
		os.system("mv %s %s/"%(f,args.jid))
if __name__ == "__main__":
	main()







































