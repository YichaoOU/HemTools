#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
from scipy.stats import chi2_contingency


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

"""

given fg and bg fasta, run FIMO to get numbers and run chi-square test for motif enrichment p-value


"""

def chi2_test(FG_count,FG_overlap,BG_count,BG_overlap):
	A = FG_overlap
	B = FG_count - FG_overlap
	C = BG_overlap
	D = BG_count - BG_overlap
	odd,p_value,t1,t2 = chi2_contingency([[A,B],[C,D]])
	return p_value
	
	
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-fg',"--target_fa",  help="fasta file",required=True)
	mainParser.add_argument('-bg',"--background_fa",  help="fasta file",required=True)
	mainParser.add_argument('-m',"--motif_file",  help="motif file",required=True)
	mainParser.add_argument('-o',"--output",  help="output csv",required=True)
	mainParser.add_argument('--label',  help="output label",default=None)
	mainParser.add_argument('-p',"--fimo_cutoff",  default=0.0005)
	mainParser.add_argument("--fimo_addon",  default="")
	

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	
	logging.info ("Reading fasta...")
	target_dict = read_fasta(args.target_fa)
	background_dict = read_fasta(args.background_fa)



	addon_string = str(uuid.uuid4()).split("-")[-1]
	fg_out = addon_string+".fg"
	bg_out = addon_string+".bg"
	logging.info ("Running FIMO...")
	
	# fimo
	command = "module load meme/4.11.2;fimo --verbosity 1 {0} --text --thresh {1} {2} {3} > {4}.fimo".format(args.fimo_addon,args.fimo_cutoff,args.motif_file,args.target_fa,fg_out)
	logging.info (command)
	os.system(command)
	
	command = "module load meme/4.11.2;fimo --verbosity 1 {0} --text --thresh {1} {2} {3} > {4}.fimo".format(args.fimo_addon,args.fimo_cutoff,args.motif_file,args.background_fa,bg_out)
	logging.info (command)
	os.system(command)
	
	# fimo to csv
	dfg = pd.read_csv("%s.fimo"%(fg_out),sep="\t",skiprows=1,header=None)
	covered_fg = dfg[1].nunique()
	
	dbg = pd.read_csv("%s.fimo"%(bg_out),sep="\t",skiprows=1,header=None)
	covered_bg = dbg[1].nunique()
	myList = []
	for motif in list(set(dfg[0].unique().tolist()+dbg[0].unique().tolist())):
		x=p_value_for_motif(dfg,dbg,len(target_dict),len(background_dict),motif)
		myList.append(x)
	df = pd.DataFrame(myList)
	df.columns = ['Motif','P-value','%Target','%Background']
	df['File'] = args.label
	df = df[['File','Motif','P-value','%Target','%Background']]
	df.to_csv(args.output,sep="\t",header=False,index=False)
	# logging.info("%covered sequence is: %s,%s"%(float(covered_fg)/len(target_dict),float(covered_bg)/len(background_dict)))
	os.system("rm %s*"%(addon_string))
	
	
def p_value_for_motif(dfg,dbg,total_fg,total_bg,motif):
	df1 = dfg[dfg[0]==motif]
	df2 = dbg[dbg[0]==motif]
	covered_fg = df1[1].nunique()
	covered_bg = df2[1].nunique()
	
	p = chi2_test(total_fg,covered_fg,total_bg,covered_bg)
	print (motif,p,float(covered_fg)/total_fg,float(covered_bg)/total_bg)
	return [motif,p,float(covered_fg)/total_fg,float(covered_bg)/total_bg]

if __name__ == "__main__":
	main()

























