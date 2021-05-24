#!/hpcf/apps/python/install/2.7.13/bin/python
import os
import argparse
import subprocess
import glob
import pandas as pd
from utils import *
import uuid
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
cwd = os.getcwd()
def arg_my_dir(parser):
	cmd=parser.add_parser('my_dir',help='CD, search, and list my dirs',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	cmd.add_argument('-j',"--jid",  help="A dummy parameter. No log file will be generated for this subcmd.", default='{{subcmd}}_'+username+"_"+str(datetime.date.today()))	
	group = cmd.add_mutually_exclusive_group(required=True)
	group.add_argument('-l',"--list",  help="list all dirs (max display = 50 entries) that have been logged in your profile. Your profile is stored in ~/.hemtools_meta/my_dir.csv",action='store_true')
	group.add_argument('-a',"--add",  help="add a new dir manually",type=str)
	group.add_argument('-s',"--search",  help="search for a string in your profile",type=str)
	group.add_argument('-d',"--delete",  help="delete a dir in your profile. Please use the index to delete an entry.",type=int)
	group.add_argument('--cd',  help="cd to the dir. This option uses a fuzzy string match; even if your input does not match exactly to the database, it will find the best matched dir and cd to that dir.",type=str)


def run_my_dir(args,rootLogger):
	if str(args.subcmd).lower() != "my_dir":
		return 0
	rootLogger.info("Reading user's my_dir.csv")
	file = "~/.hemtools_meta/my_dir.csv"
	df = pd.read_csv(file)
	save_flag = False
	pd.set_option('display.max_colwidth', 0)
	current = os.getcwd()
	if args.list:
		# print df.head(50).to_string()
		pass
	if args.add:
		rootLogger.info("Adding entry "+str(args.add))
		n = df.shape[0]
		try:
			myList = args.add.split(",")
			if len(myList) == 2:
				myList.append(".")
			df.loc[n] = myList
			save_flag=True
		except:
			rootLogger.error("could not add this entry: "+args.add)
	if args.delete:
		rootLogger.info("Deleting index "+str(args.delete))
		df = df.drop(args.delete)
		save_flag=True
	if args.search:
		df['match'] = map(lambda x:similar(x,args.search),df['keyword'])
		# print df.sort_values('match',ascending=False)[['keyword','dir','subcmd']].head(3).to_string()
	if args.cd:
		df['match'] = map(lambda x:similar(x,args.cd),df['keyword'])
		rootLogger.info("The top 3 matches are shown below. Will CD to the first match.")
		tmp = df.sort_values('match',ascending=False)[['keyword','dir','subcmd']].head(3)
		# print tmp.to_string()
		content = """
dir="{{dir}}"
cd $dir
exec bash
		"""
		content = content.replace("{{dir}}",tmp['dir'].tolist()[0])
		bash_file = "/tmp/"+str(uuid.uuid4()).split("-")[-1]+".sh"
		write_file(bash_file,content)
		dos2unix(bash_file)
		os.system("bash "+bash_file)
		os.system("rm "+bash_file)
	if save_flag:
		rootLogger.info("Saving profile!")
		df[['keyword','dir','subcmd']].to_csv(file,index=False)
	rootLogger.info("Bye!")
	os.system("rm "+current+"/"+args.jid+".log")







