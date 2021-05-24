#!/hpcf/apps/python/install/2.7.13/bin/python
import os
import argparse
from utils import *
import subprocess
import glob
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
cwd = os.getcwd()
def arg_report_bug(parser):
	cmd=parser.add_parser('report_bug',help='Email the log files to the developer.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	cmd.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='{{subcmd}}_'+username+"_"+str(datetime.date.today()))	
	

def run_report_bug(args,rootLogger):
	if str(args.subcmd).lower() != "report_bug":
		return 0
	if not os.path.isdir("log_files"):
		rootLogger.error("The log_files folder can't be found!")
		rootLogger.error("Your current dir is: ",cwd)
		os.system("rm "+args.jid+".log")
	if not os.path.isfile("log_files.zip"):
		command1 = "zip -r log_files.zip log_files"
		subprocess.Popen(command1, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()
	files_list_upper = glob.glob("../*")
	cur_files = glob.glob("*")
	command2 = 'echo "{{content}}" | mailx -a "log_files.zip" -s "report_bug" -- yli11@stjude.org'
	content = "files list:\n"+"\n".join(files_list_upper)+"\n"+"\n".join(cur_files)
	command2 = command2.replace("{{content}}",content)
	subprocess.Popen(command2, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()
	rootLogger.info("log files are sent to the developer! Bye!")








