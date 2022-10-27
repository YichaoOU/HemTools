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
	mainParser.add_argument('-f',"--input",  help="a list of gRNA sequences",required=True)
	mainParser.add_argument('-n',"--num_mismatches",  help="Number of allowed mis-matches in the gRNA, excluding PAM sequence",default=2)
	mainParser.add_argument('-l',"--gRNA_length",  help="infer from input",default=20,type=int)
	mainParser.add_argument('--add_PAM', help="if PAM sequence is not included in your gRNA, please add this option.",action='store_true')
	mainParser.add_argument('--remove_first_G', help="remove first letter G in the input gRNA list",action='store_true')
	mainParser.add_argument('--allow_PAM_mis', help="allowing mismatch in the PAM sequence",action='store_true')
	mainParser.add_argument('--PAM_seq', help="specify the PAM sequence, e.g., NGG.",default="NGG")
	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. currently, only hg19 is available", default='hg19',type=str)
	genome.add_argument('--chr_fa',  help="This will be automatically changed with -g option", default=myData['hg19_chr_fa'])
	genome.add_argument('--genome_fasta',  help="genome fasta file", default=myData['hg19_fasta'])
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def to_casOffinder_input(args):

	df = pd.read_csv(args.input,header=None)
	gRNA = df[0].tolist()
	gRNA_length = args.gRNA_length
	if args.remove_first_G:
		gRNA = [x[1:] for x in gRNA]
		gRNA_length = args.gRNA_length - 1
	# gRNA_length = len(gRNA[0])
	# args.gRNA_length = gRNA_length
	
	out = []
	out.append(myData['%s_fasta'%(args.genome)])
	example_N_seq = ["N"]*gRNA_length
	# for i in range(gRNA_length):
		# print (gRNA[0])
		# if gRNA[0][i] in ["","","",""]:
			# example_N_seq[i] = gRNA[0][i]
	example_N_seq = "".join(example_N_seq)
	if args.add_PAM:	
		if args.allow_PAM_mis:
			out.append(example_N_seq+"N"*len(args.PAM_seq))
		else:
			out.append(example_N_seq+args.PAM_seq)
		for g in gRNA:
			# if args.allow_PAM_mis:
				# out.append(g+"N"*len(args.PAM_seq)+" "+str(args.num_mismatches))
			# else:
				# out.append(g+args.PAM_seq+" "+str(args.num_mismatches))
			out.append(g+args.PAM_seq+" "+str(args.num_mismatches))
			
	else:
		# out.append("".join(["N"]*(gRNA_length-3))+args.PAM_seq)
		if args.allow_PAM_mis:
			out.append(example_N_seq+"N"*len(args.PAM_seq))
		else:
			out.append(example_N_seq+args.PAM_seq)
		for g in gRNA:
			g = list(g)
			# g[-3] = "N"
			g = "".join(g)
			out.append(g+" "+str(args.num_mismatches))

			
	write_file("%s/input.list"%(args.jid),"\n".join(out))
	
def main():

	args = my_args()
	args.genome_fasta = myData['%s_fasta'%(args.genome)]
		
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
	to_casOffinder_input(args)
	

	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)
	
	
	
if __name__ == "__main__":
	main()







































