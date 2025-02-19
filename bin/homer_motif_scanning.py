#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


"""
Every python wrapper is supposed to be similar, since they are using the same convention.

The only thing need to be changed is the guess_input function and the argparser function.


"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--peak_list",  help="peak_list relative or abs path",required=True)
	mainParser.add_argument('-m',"--motif_file",  help="homer motif file",default="/home/yli11/Data/Motif_database/Human/homer_format_all.motifs")
	mainParser.add_argument('-sub',"--motif_subset",  help="subset motifs to annotate",default=None)


	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. currently, only hg19 is available", default='hg19',type=str)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def subset_homer(f,myList):
	myList = myList.split(",")
	out = []
	write_flag=False
	with open(f) as ff:
		for line in ff:
			line = line.strip()
			if ">" == line[0]:
				write_flag=False
				for m in myList:
					if m in line:
						write_flag = True
						name = line
						# out[name]=[]
						out.append(name)
			else:
				if write_flag:
					line = [float(x) for x in line.split()]
					mySum = sum(line)
					out.append("\t".join([str(x/mySum) for x in line]))
	write_file("subset_motif.homer","\n".join(out))
	return "subset_motif.homer"

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


	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	
	## additional commands
	if args.motif_subset != None:
		args.motif_file = subset_homer(args.motif_file,args.motif_subset)
		# exit()
	

	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)
	
	
	
if __name__ == "__main__":
	main()







































