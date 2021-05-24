#!/usr/bin/env python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
import datetime
import uuid
import matplotlib
import pandas as pd
matplotlib.use('agg')
import seaborn as sns
import numpy as np
import scipy
import glob
import sys
import matplotlib.pyplot as plt
import os
from joblib import Parallel, delayed
from os.path import isfile,isdir
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
import matplotlib
import numpy as np
import scipy
import glob
import sys
import matplotlib.pyplot as plt
import os
import numpy as np
import getpass
import argparse
from matplotlib_venn import venn3,venn2
import uuid
import subprocess
from matplotlib_venn import venn2, venn2_circles
import scipy.stats as ss
"""Plot venn diagram for 2 sets and calculate p-value


https://github.com/brentp/poverlap

http://www.pangloss.com/wiki/VennSignificance

https://www.gungorbudak.com/blog/2016/05/25/computing-significance-of-overlap/





"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="Plot venn diagram for 2 sets and calculate p-value. If inputs are bed files, make sure there is not redundant regions inside each file.")
	mainParser.add_argument("-l1",  help="input list 1",required=True)
	mainParser.add_argument("-l2",  help="input list 2",required=True)
	mainParser.add_argument("--label1",  help="label for list 1",default="List1")
	mainParser.add_argument("--label2",  help="label for list 2",default="List2")
	mainParser.add_argument("--bedtools",  help="with this option, the inputs are parsed as bed files", action='store_true')


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
def wccount(filename):
	out = subprocess.Popen(['wc', '-l', filename],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
	return int(out.partition(b' ')[0])

def run_bedtools(args):
	output = str(uuid.uuid4())
	print (output)
	command = "bedtools intersect -a %s -b %s -wa > %s"%(args.l1,args.l2,output)
	os.system(command)
	a = wccount(args.l1)
	b = wccount(args.l2)
	df = pd.read_csv(output,sep="\t",header=None)
	df['name'] = df[0]+df[1].astype(str)+df[2].astype(str)
	df = df.drop_duplicates('name')
	overlap = df.shape[0]
	os.system("rm %s"%(output))
	print (overlap)
	print ("Percentage of {0:.1%} in {1} overlapped with {2}".format(float(overlap)/a,args.label1,args.label2))
	return a,b,overlap

def main():

	args = my_args()
	if args.bedtools:
		a,b,overlap = run_bedtools(args)
		
	
	

if __name__ == "__main__":
	main()




