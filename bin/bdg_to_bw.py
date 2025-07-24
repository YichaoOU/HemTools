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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="bdg to bw")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--bdg_files",  help="bdg file list", required=True)
	mainParser.add_argument("--remove_first_line",  help="bdg file list", default=None)
	mainParser.add_argument("--binSize",  help="bdg file list", default=None,type=int)
	mainParser.add_argument("--data_frame",  help="The input is a table, not bdg file list, index and header are required in this data frame", action='store_true' )
	
	mainParser.add_argument('--interactive',  help="run pipeline interatively", action='store_true')

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])
	genome.add_argument('-sb','--chrom_size_bed',  help="chrome size", default=myData['hg19_chrom_size_bed'])


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
	
def parse_dataframe(x,binSize=None):
	df = pd.read_csv(x,sep=guess_sep(x),index_col=0)
	myCols = df.columns.tolist()
	df['myChr'] = [re.split('_|-|\.|:',i)[0] for i in df.index.tolist()]
	df['myStart'] = [re.split('_|-|\.|:',i)[1] for i in df.index.tolist()]
	def check_is_valid(x):
		try:
			x = int(x)
			return True
		except:
			return False
		
	df['is_valid'] = df.myStart.apply(check_is_valid)
	print (df.head())
	df = df[df.is_valid==True]
	df['myStart'] = df['myStart'].astype(int)
	# print df.head()
	df['myEnd'] = [int(re.split('_|-|\.|:',i)[2]) for i in df.index.tolist()]
	if binSize:
		df['myEnd'] = df['myStart']+binSize
	myBed = ['myChr','myStart','myEnd']
	for c in df.columns:
		# if c in ['pvalue','padj']:
		if "pval" in c or "padj" in c:
			df[c] = [-np.log10(x) for x in df[c]]
			df[c] = df[c].fillna(0)
	return df,myBed,myCols
	
def dataframe_to_bed(args):
	df,myBed,myCols = parse_dataframe(args.bdg_files,args.binSize)
	myList = []
	for c in myCols:
		output = "%s/%s.bdg"%(args.jid,c)
		df[myBed+[c]].to_csv(output,sep="\t",index=False,header=False)
		myList.append("%s/%s.bdg"%(args.jid,c))
	args.bdg_files = "%s/%s.input"%(args.jid,args.jid)
	write_file(args.bdg_files,"\n".join(myList))

def main():

	args = my_args()
	if args.genome != "custom":
		args.chrom_size = myData['%s_chrom_size'%(args.genome)]
		args.chrom_size_bed = myData['%s_chrom_size_bed'%(args.genome)]

		
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
	if args.data_frame:
		dataframe_to_bed(args)	
	if args.remove_first_line != None:
		args.remove_first_line = "sed -i '1d' ${COL1}"
		print ("removing first line in bdg file")
	#-------------- run jobs ----------------------


	if args.interactive:
		run_interative_jobs(myPipelines[current_file_base_name],args)
		exit()
	submit_pipeline_jobs(myPipelines[current_file_base_name],args)

	
if __name__ == "__main__":
	main()







































