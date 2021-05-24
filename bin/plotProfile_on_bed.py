#!/home/yli11/.conda/envs/py2/bin/python
import pandas as pd
import sys
import matplotlib
matplotlib.use('agg')
import os
import matplotlib as mpl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import argparse
import datetime
import getpass
import uuid
from scipy.interpolate import interp1d
import re, string
from matplotlib_venn import venn2
import subprocess
import pandas as pd
import seaborn as sns
# %matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import scipy
import seaborn as sns
import glob
from scipy.stats import gaussian_kde
import json


def send_email(attachments):
	username = getpass.getuser()
	command = ' echo "{{message}}" | mailx {{attachments}} -s "{{subject}}" -- User_name@stjude.org '
	command = command.replace("{{message}}","average signal plot"+"\n\nYour result is located at:\n"+os.getcwd())
	command = command.replace("{{subject}}","%s scatter correlation density plot"%(attachments[0]))
	command = command.replace("User_name",username)
	real_attachments = []
	for item in attachments:
		if os.path.isfile(item):
			real_attachments.append(item)
	attachments_string = map(lambda x: '-a "'+x+'" ',real_attachments)
	command = command.replace("{{attachments}}","".join(attachments_string))
	os.system(command)
	# print command
	
def my_args():
	username = getpass.getuser()
	
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument("-f",help="data table, from computeMatrix deeptools",required=True)	
	mainParser.add_argument("--yMin",help="yMin",default=None,type=float)	
	mainParser.add_argument("--yMax",help="yMax",default=None,type=float)	
	mainParser.add_argument('--smooth',  help="Not for end-user.", action='store_true')
	mainParser.add_argument("-c",help="colors, seperated by comma, hex color is OK",default="red,green,blue,yellow,grey,purple,darkgreen,darkred,pink,orange")	

	mainParser.add_argument('-o',"--output",  help="output file name",default=username+"_"+str(datetime.date.today())+".average_signal.pdf")

	## https://stackoverflow.com/questions/21168120/python-argparse-errors-with-in-help-string
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
from scipy.ndimage.filters import gaussian_filter1d


def plot(f,colors,output,yMin=None,yMax=None,smooth=False):

	label = open(f).readlines()[0].strip()[1:]
	label = json.loads(label)
	df = pd.read_csv(f,sep="\t",header=None,skiprows=1).fillna(0)
	df2 = df[df.columns[6:]].mean()
	fig, ax = plt.subplots()
	myList = label['sample_boundaries']
	samples = label['sample_labels']
	# colors = ['red','green','blue']
	for i in range(len(myList)-1):
		s = myList[i]
		e = myList[i+1]
		if smooth:
			ysmoothed = gaussian_filter1d(df2[s:e], sigma=50)
			plt.plot(range(e-s), ysmoothed , color=colors[i], label=samples[i], alpha=0.9)
		else:
			plt.plot(range(e-s), df2[s:e] , color=colors[i], label=samples[i], alpha=0.9)
	plt.legend()
	plt.xlim(0, e-s)
	
	if yMin==None:
		yMin = df2.min()
	if yMax==None:
		yMax = int(df2.max()+0.7)
	plt.ylim(yMin, yMax)
	ax.set_xticks([0,int((e-s)/2),e-s])
	ax.set_xticklabels(['-%skb'%(label['upstream'][0]/1000),'center','-%skb'%(label['downstream'][0]/1000)])
	plt.savefig(output,bbox_inches='tight')




def main():
	args = my_args()
	colors = args.c.split(",")
	plot(args.f,colors,args.output,yMin=args.yMin,yMax=args.yMax,smooth=args.smooth)
	send_email([args.output])

	


if __name__ == "__main__":
	main()



