#!/hpcf/apps/python/install/2.7.13/bin/python

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

def send_email(attachments):
	username = getpass.getuser()
	command = ' echo "{{message}}" | mailx {{attachments}} -s "{{subject}}" -- User_name@stjude.org '
	command = command.replace("{{message}}","plot blood lineage"+"\n\nYour result is located at:\n"+os.getcwd())
	command = command.replace("{{subject}}","plot blood lineage")
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
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--input",help="2 column tsv, no header, the values for each cell type",required=True)	
	mainParser.add_argument("--min",help="set min value, otherwise infered from data",default="None")	
	mainParser.add_argument("--custom_color_scale",help="You can define your own color scheme (linear from lowest to highest) using hex color, separated by comma",default="#ffffff,#ff8000,#660000")	
	mainParser.add_argument("--svg_template",default="/home/yli11/HemTools/share/misc/blood_lineage_Hchang_13cells.svg")	
	mainParser.add_argument('-o',"--output",  help="output file name",default=username+"_"+str(datetime.date.today())+"_"+addon_string)
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args



def replace2(lines,name,color):
	search = 'id="%s"'%(name)
	for i in range(len(lines)):
		if search in lines[i]:
			lines[i] = lines[i].replace(search,'%s fill="%s"'%(search,color))
	return lines

def replace(lines,name,color):
	search = 'id="%s"'%(name)
	search2 = '%s_fill'%(name)
	for i in range(len(lines)):
		if search in lines[i]:
			lines[i] = lines[i].replace(search,'%s fill="%s"'%(search,color))
		if search2 in lines[i]:
			lines[i] = lines[i].replace(search2,color)
	return lines
def draw_color_bar(vmin,vmax,output,cmap):
	fig, ax = plt.subplots(figsize=(1, 5))
	norm = mpl.colors.Normalize(vmin = vmin, vmax = vmax)  
	cbar = mpl.colorbar.ColorbarBase(ax, cmap=cmap,norm=norm,ticks=[vmin,vmax])
	plt.savefig("%s_colorbar.pdf"%(output), bbox_inches='tight')
def to_hex(input):
	return '#%02x%02x%02x%02x' % tuple(int(x*255) for x in input)
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()	
def main():
	## init
	args = my_args()
	template = open(args.svg_template).readlines()
	df = pd.read_csv(args.input,sep="\t",header=None,index_col=0)
	if args.min != "None":
		vmin = float(args.min)
	else:
		vmin = df[1].min()
	vmax = df[1].max()
	color_bar = clr.LinearSegmentedColormap.from_list('custom',args.custom_color_scale.split(","),N=256)
	m = interp1d([vmin,vmax],[1,256])

	## process
	df['colors'] = df[1].apply(lambda x:to_hex(color_bar(int(m(x)))))
	print (df.head())
	my_dict = df['colors'].to_dict()
	for n in my_dict:
		template = replace(template,n,my_dict[n])
	write_file("%s.svg"%(args.output),"".join(template))
	draw_color_bar(vmin,vmax,args.output,color_bar)
	send_email(["%s.svg"%(args.output),"%s_colorbar.pdf"%(args.output)])



if __name__ == "__main__":
	main()



