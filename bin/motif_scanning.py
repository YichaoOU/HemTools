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

better to use it for one TF or a group of related TFs

"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--bed_file",  help="bed file",required=True)
	mainParser.add_argument('-m',"--motif_file",  help="bed file",required=True)
	mainParser.add_argument('-o',"--output",  help="output csv",required=True)
	mainParser.add_argument('-p',"--fimo_cutoff",  default=0.0005)
	mainParser.add_argument("--fimo_addon",  default="")
	
	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, mm10, mm9, hg38", default='hg19',type=str)
	genome.add_argument('--genome_fasta',  help="genome version: hs, mm", default=myData['hg19_fasta'],type=str)


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	if args.genome!="custom":
		args.genome_fasta = myData['%s_fasta'%(args.genome)]
	##------- check if jid exist  ----------------------
	# if isdir(args.jid):
		# addon_string = str(uuid.uuid4()).split("-")[-1]
		# logging.warning ("The input job id is not available!")
		# args.jid = args.jid+"_"+addon_string
		# logging.info ("The new job id is: "+args.jid)
	# else:
		# logging.info ("The job id is: "+args.jid)			
	
	##------- add functions below ----------------------
	
	#-------------- run jobs ----------------------
	
	# os.system("mkdir %s"%(args.jid))
	# os.system("mkdir %s/log_files"%(args.jid))
	# run interactive
	df = pd.read_csv(args.bed_file,sep="\t",header=None)
	total=df.shape[0]
	addon_string = str(uuid.uuid4()).split("-")[-1]
	bedtools_command = "module load bedtools;bedtools getfasta -fi {0} -bed {1} -fo {2}.fa".format(args.genome_fasta,args.bed_file,addon_string)
	logging.info (bedtools_command)
	os.system(bedtools_command)
	
	
	# fimo
	command = "module load meme/4.11.2;fimo {0} --text --thresh {1} {2} {3}.fa > {3}.fimo".format(args.fimo_addon,args.fimo_cutoff,args.motif_file,addon_string)
	logging.info (command)
	os.system(command)
	
	# fimo to csv
	df = pd.read_csv("%s.fimo"%(addon_string),sep="\t",skiprows=1,header=None)
	covered = df[1].nunique()
	logging.info("Total covered sequence is: %s,%s,%s"%(covered,total,float(covered)/total))
	df['v'] = [-np.log10(x) for x in df[6]]
	# df = df.sort_values(6,ascending=False)
	print (df.groupby([0,4]).size())
	# df[4] = df[0]+df[1]
	
	# df = df.drop_duplicates(4)
	# df['r'] = df[1]
	# df['m'] = df[0]
	# df2 = df.pivot_table(columns='m', index='r', values='v')
	# df2 = df2.fillna(0)
	# df2.to_csv(args.output)
	os.system("fimo_to_bed.py {0}.fimo;mv {0}.fimo.seq.bed {1}".format(addon_string,args.output))
	os.system("rm %s*"%(addon_string))

if __name__ == "__main__":
	main()

























