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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))

	mainParser.add_argument('-f',"--input", help="input list",required=True)
	mainParser.add_argument("--SE_input_list", help="input list")
	mainParser.add_argument("--PE_input_list", help="input list")
	mainParser.add_argument("-s", help="input list",default=0)
	mainParser.add_argument("-q", help="input list",default=0)


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
	args.jid += "_s%s_q%s"%(args.s,args.q)
	args.SE_input_list = args.jid+".se.input"
	args.PE_input_list = args.jid+".pe.input"	
	##------- add functions below ----------------------
	df = pd.read_csv(args.input,sep="\t",names = [0,1,2,3,4])
	# print (df.head())
	pe = df.dropna()
	se = df[~df.index.isin(pe.index)]
	# print (se.head())
	# print (pe.head())
	if df.shape[1]==4:
		se=df
		pe=pd.DataFrame()
	se.to_csv(args.SE_input_list,sep="\t",header=False,index=False)
	pe.to_csv(args.PE_input_list,sep="\t",header=False,index=False)
	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))

	submit_pipeline_jobs(myPipelines[current_file_base_name],args)


	
if __name__ == "__main__":
	main()

























