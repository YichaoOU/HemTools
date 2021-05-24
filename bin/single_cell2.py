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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="perform 10X single-cell RNA-seq analysis or CITE-seq")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument("--input_list",  help=argparse.SUPPRESS,default=None)

	mainParser.add_argument("-f","--library_csv",  help="A list of group name (fastq file prefix).",required=True)
	mainParser.add_argument("-a","--antibody_barcode",  help="antibody barcodes see: https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/feature-bc-analysis",default=None)
	mainParser.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm10.", default='hg38',type=str)
	mainParser.add_argument('--genes',  help="Genes to inspect, use Ensembl ID, separated by ,.", default='ENSG00000213934,ENSG00000196565',type=str)
	mainParser.add_argument('--cellranger_refdata',  help="Not for end-user", default=myData['hg38_cellranger'],type=str)


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def make_input2(args):
	df = pd.read_csv(args.library_csv)
	out = []
	for s,d in df.groupby('sample'):
		s = s.replace(" ","")
		d.to_csv("%s/%s.library.csv"%(args.jid,s),index=False)
		if d['library_type'].tolist()[0]=="Antibody Capture":
			out.append([s,"--feature-ref=%s"%(args.antibody_barcode)])
			os.system("cp %s %s/"%(args.antibody_barcode,args.jid))
		else:
			out.append([s,""])
	df = pd.DataFrame(out)
	df.to_csv("%s.input"%(args.jid),sep="\t",header=False,index=False)
	args.input_list = "%s.input"%(args.jid)

def rename_sample(x):
	L00 = glob.glob("%s*_L00*gz"%(x))[0]
	tmp = L00.split("/")[-1]
	return re.split("_S\d+_",tmp)[0]



def make_input(args):
	df = pd.read_csv(args.library_csv)
	os.system("cp %s %s/"%(args.antibody_barcode,args.jid))
	out = []
	for s,d in df.groupby('sample'):
		s = s.replace(" ","")
		d['sample'] = d['fastqs'].apply(rename_sample)
		d.to_csv("%s/%s.library.csv"%(args.jid,s),index=False)
		out.append(s)
	df = pd.DataFrame(out)
	df.to_csv("%s.input"%(args.jid),sep="\t",header=False,index=False)
	args.input_list = "%s.input"%(args.jid)


def main():

	args = my_args()
	args.cellranger_refdata = myData['%s_cellranger'%(args.genome)]

		
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
	make_input(args)
	

	pipeline_name = current_file_base_name
	submit_pipeline_jobs(myPipelines[pipeline_name],args)


if __name__ == "__main__":
	main()







































