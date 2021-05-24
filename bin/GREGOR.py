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
	mainParser.add_argument('-s','--SNP_list', default=myData['blood_variants_VJ01'], help = "Please provide absolute path if you use custom SNP list")
	mainParser.add_argument('-n','--SNP_database_name', default="VJ01", help = "options are custom, hg19_gwas, VJ01_combined, VJ01, VJ025, VJ05, VJ075, VJ00")
	mainParser.add_argument('--config_list',help=argparse.SUPPRESS)
	mainParser.add_argument('-f','--bed_list',  required=True,help = "absolute or relative path")
	mainParser.add_argument('--template_config', default=myData['GREGOR_config'])

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
		
def copy_bed_files(args):
	"""sort bed files, make 4 columns"""
	command  = """for i in `cat %s`;do awk -F "\t" '{print $1"\t"$2"\t"$3"\t."}' $i | sort -k1,1 -k2,2n > %s/bed_files/$(basename $i);done"""%(args.bed_list,args.jid)
	os.system(command)
	print (command)
	myList = read_file_to_list(args.bed_list)
	myList = ["bed_files/%s"%(x.split("/")[-1]) for x in myList]
	write_file("%s/bed.index"%(args.jid),"\n".join(myList))
	print ("copy files done")
	

def prepare_config(args):
	""" create config file for each SNP list file"""
	lines = "".join(open(args.template_config).readlines())
	if not args.SNP_database_name == "custom":
		if args.SNP_database_name == "hg19_gwas":
			args.SNP_list = myData[args.SNP_database_name]
		else:
			args.SNP_list = myData['blood_variants_%s'%(args.SNP_database_name)]
	myList = read_file_to_list(args.SNP_list)
	config_list = []
	for x in myList:
		myDict = {}
		myDict['SNP_feature_file']=x
		myDict['SNP_feature_name']=x.split("/")[-1].replace(".list","")
		new_lines = multireplace(lines, myDict)
		config_file_name = "%s.config"%(myDict['SNP_feature_name'])
		config_list.append(config_file_name)
		write_file("%s/%s"%(args.jid,config_file_name),new_lines)
	write_file("%s.input"%(args.jid),"\n".join(config_list))
	args.config_list = "%s.input"%(args.jid)
	
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
	
	##------- add functions below ----------------------
	
	#-------------- run jobs ----------------------
	
	os.system("mkdir %s"%(args.jid))
	os.system("mkdir %s/log_files"%(args.jid))
	os.system("mkdir %s/bed_files"%(args.jid))
	os.system("mkdir %s/summary_files"%(args.jid))
	prepare_config(args)
	copy_bed_files(args)
	pipeline_name = current_file_base_name
	# exit()
	submit_pipeline_jobs(myPipelines[pipeline_name],args)

	
if __name__ == "__main__":
	main()

























