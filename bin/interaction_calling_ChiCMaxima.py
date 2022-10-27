#!/home/yli11/.conda/envs/py2/bin/python

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import numpy as np
import datetime
import getpass
import uuid
import argparse
import glob
import scipy
import pandas as pd
"""

only good for 20copy projects

"""

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-bdg',  help="bdg file, containing the interaction frequency",required=True)
	mainParser.add_argument('-bed',  help="bait bed file",required=True)

	mainParser.add_argument('-o',"--output",  help="output prefix",default="lineplot_"+username+"_"+str(datetime.date.today()))
	
	##------- add parameters above ---------------------
	# args = mainParser.parse_args()	
	args,unknown = mainParser.parse_known_args()
	known_pDict = vars(args)
	for i in range(0,len(unknown),2):
		mainParser.add_argument(unknown[i],default=unknown[i+1])
	args = mainParser.parse_args()
	user_pDict  = {k:v for k,v in vars(args).items() if k not in known_pDict or v != known_pDict[k]}

	return args,known_pDict,user_pDict


def main():


	args,known_pDict,user_pDict = my_args()
	# print (args)
	print (known_pDict)
	print (user_pDict)
	

	bdg = pd.read_csv(args.bdg,sep="\t",header=None,comment="#")
	bed = pd.read_csv(args.bed,sep="\t",header=None,comment="#")
	bed[3] = bed[0]+"_"+bed[1].astype(str)+"_"+bed[2].astype(str)
	bed[4] = bed.index.tolist()
	bdg[4] = bdg[0]+"_"+bdg[1].astype(str)+"_"+bdg[2].astype(str)
	bdg[5] = bdg.index.tolist()
	## ID has to be int
	df_list= []
	for chr,start,end,name,id in bed.values:

		tmp =bdg[bdg[0]==chr]

		tmp['ID_Bait'] = id
		tmp['chr_Bait'] = chr
		tmp['start_Bait'] = start
		tmp['end_Bait'] = end
		tmp['Bait_name'] = name
		tmp['ID_OE'] = tmp[5]
		tmp['chr_OE'] = tmp[0]
		tmp['start_OE'] = tmp[1]
		tmp['end_OE'] = tmp[2]
		tmp['OE_name'] = tmp[4]
		tmp['N'] = tmp[3]
		tmp = tmp.drop([0,1,2,3,4,5],axis=1)

		df_list.append(tmp)
	df = pd.concat(df_list)
	tmp_out = args.output+"tmp"
	df.to_csv(tmp_out,sep="\t",index=False)
	command = "module load R/3.4.0;ChiCMaxima_v0.9.R -i %s -o %s.ibed -w 20 -s 0.01 -c 2000000"%(tmp_out,args.output)
	os.system(command)
	df = pd.read_csv("%s.ibed"%(args.output),sep="\t",index_col=0)
	df = df[df[' Enrichment ']>=1]
	print (df.shape)
	os.system("rm %stmp"%(args.output))
	# os.system("rm %s.ibed"%(args.output))
	df.columns = [x.replace(" ","") for x in df.columns]
	mango_columns = ["chr_Bait","start_Bait","end_Bait","chr_OE","start_OE","end_OE","Enrichment"]
	df.to_csv("%s.tsv"%(args.output),sep="\t")
	df[mango_columns].to_csv("%s.mango"%(args.output),sep="\t",header=False,index=False)



if __name__ == "__main__":
	main()
















