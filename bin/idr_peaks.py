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

TODO, overwrite genome index
"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	

	mainParser.add_argument('-r1',"--R1_input",  help="TSV file, 2 columns, treatment, control files for replicate 1",required=True)
	mainParser.add_argument('-r2',"--R2_input",  help="TSV file, 2 columns, treatment, control files for replicate 2",required=True)
	mainParser.add_argument("--merged_input",  help="Not for end-user anymore")
	mainParser.add_argument("--macs2_addon_parameters", default="")
	mainParser.add_argument("--half_width", default=-1,type=int,help="half.width: -1 if using the reported peak width,  a numerical value to truncate the peaks to +- half_width")

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, mm10, mm9", default='hg19',type=str)
	genome.add_argument('--macs_genome',  help="genome version: hs, mm", default='hs',type=str)
	genome.add_argument('-b','--black_list',  help="Blacklist file", default=myData['hg19_black_list'])

	

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
def find_unique_input(x,y,output):
	line1 = open(x).readlines()[0].strip().split("\t")
	print line1
	line2 = open(y).readlines()[0].strip().split("\t")
	print line2
	if line1[-1] == line2[-1]:
		out = line1+[line2[0]]
	else:
		out = line1+line2
	write_file(output,"\t".join(out))
def main():

	args = my_args()
	args.black_list = myData['%s_black_list'%(args.genome)]

	
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			
	
	##------- add functions below ----------------------

	#-------------- run jobs ----------------------
	
	dos2unix(args.R1_input)
	dos2unix(args.R2_input)
	merge_input_name = args.jid + ".merged_input"
	# os.system("paste %s %s > %s"%(args.R1_input,args.R2_input,merge_input_name))
	args.merged_input = merge_input_name
	find_unique_input(args.R1_input,args.R2_input,merge_input_name)
	
	dos2unix(args.merged_input)
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	if args.half_width <=0:
		if args.half_width == -1:
			pipeline_name = current_file_base_name
		else:
			print ("Error: half widht should >0 or = -1")
			exit()
	else:
		pipeline_name = current_file_base_name+"_half_width"
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























