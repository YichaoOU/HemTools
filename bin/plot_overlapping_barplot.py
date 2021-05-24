#!/hpcf/apps/python/install/2.7.13/bin/python

import pandas as pd
import sys
import os
import numpy as np
import argparse
import datetime
import getpass
import uuid
import re, string

"""
This is a wrapper to call R ggplot

Input
------

Groups,Total_count_each,Condition,Intersection
25,903,Case1,512
25,817,Case2,512
20,722,Case1,400
20,644,Case2,400
15,543,Case1,332
15,469,Case2,332
10,357,Case1,172
10,287,Case2,172
5,184,Case1,65
5,125,Case2,65




"""



def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		myString = str(myString).replace("{{"+str(k)+"}}",str(myDict[k]))
	return myString


def send_email(attachments):
	username = getpass.getuser()
	command = ' echo "{{message}}" | mailx {{attachments}} -s "{{subject}}" -- User_name@stjude.org '
	command = command.replace("{{message}}","plot overlapping barplot"+"\n\nYour result is located at:\n"+os.getcwd())
	command = command.replace("{{subject}}","plot overlapping barplot")
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
	default = "95%"
	
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--input",help="correlation matrix with index and header",required=True)	
	mainParser.add_argument('-s',"--sep",  help="this program can infer separator automatically, but it may fail. Use auto if the input tables contain different separators.",default="auto")
	mainParser.add_argument('--skiprows',  help="Pandas read_csv parameter to skip first N rows", default=0,type=int)
	mainParser.add_argument('-o',"--output",  help="output file name",default=username+"_"+str(datetime.date.today())+"_overlapping_barplot")
	args = mainParser.parse_args()	
	return args

def guess_sep(x):
	with open(x) as f:
		for line in f:
			tmp1 = len(line.strip().split(","))
			tmp2 = len(line.strip().split("\t"))
			# print (tmp1,tmp2)
			if tmp1 > tmp2:
				return ","
			if tmp2 > tmp1: 
				return "\t"
			else:
				print ("Can't determine the separator. Please input manually")
				exit()
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

R_script = """
library(ggplot2)
mydf = read.csv("{{file_name}}.csv")
pdf(file="{{output}}.pdf",width={{width}},height={{height}})
ggplot(mydf, aes(fill=Condition, y=Total_count_each, x=Groups)) +        
  geom_bar(position="dodge", stat="identity", color="black", width={{bar_width}},size=1) + 
  geom_bar(data=mydf[!duplicated(mydf$Groups), ], stat="identity", 
           aes(Groups, Intersection), fill="yellow", width={{bar_width_yellow}},size=3,alpha=0.8) +
  geom_text(data=mydf[!duplicated(mydf$Groups), ], 
            aes(label=Intersection, y=Intersection - {{text_adjust}}), color="black", size=3.5) +       
  scale_fill_brewer(palette="Set1")+ theme_bw()+ theme(axis.text.x = element_text(angle = 90,hjust = 1))
dev.off()
pdf(file="{{output}}_half_count.pdf",width={{width}},height={{height}})
ggplot(mydf, aes(fill=Condition, y=Total_count_each, x=Groups)) +        
  geom_bar(position="dodge", stat="identity", color="black", width={{bar_width}},size=1) + 
  geom_bar(data=mydf[!duplicated(mydf$Groups), ], stat="identity", 
           aes(Groups, Intersection), fill="yellow", width={{bar_width_yellow}},size=3,alpha=0.8) +
  geom_text(data=mydf[!duplicated(mydf$Groups), ], 
            aes(label=Intersection, y=Intersection - {{text_adjust}}), color="black", size=3.5) +       
  scale_fill_brewer(palette="Set1")+ theme_bw()+ theme(axis.text.x = element_text(angle = 90,hjust = 1))+ coord_cartesian(ylim = c(0, {{half_count}}))
dev.off()
"""

def main():
	## init
	args = my_args()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	if args.sep =="auto":
		args.sep=guess_sep(args.input)
	df = pd.read_csv(args.input,sep=args.sep,skiprows=args.skiprows,index_col=0)
	df.to_csv("%s.csv"%(addon_string))
	
	Rscript_dict= {}
	Rscript_dict['output']=args.output
	Rscript_dict['file_name']=addon_string
	Rscript_dict['width']=int(df.shape[0]/2)
	# print (df['Total_count_each'].max())
	Rscript_dict['height']=int(Rscript_dict['width']*0.8)
	if Rscript_dict['width'] > 8:
		Rscript_dict['bar_width_yellow']=0.77
		Rscript_dict['bar_width']=0.8
	else:
		Rscript_dict['bar_width_yellow']=3
		Rscript_dict['bar_width']=2.85
	Rscript_dict['half_count']=int(df['Total_count_each'].max()/2.0)
	Rscript_dict['text_adjust']=int(df['Total_count_each'].max()*0.017)
	
	
	write_file("%s.R"%(addon_string),multireplace(R_script, Rscript_dict))
	R_command = "module load R/3.5.1;Rscript %s.R;rm %s.R;rm %s.csv"
	# R_command = "module load R/3.5.1;Rscript %s.R;mv Rplots.pdf %s.pdf"
	# os.system(R_command%(addon_string,args.output))
	os.system(R_command%(addon_string,addon_string,addon_string))
	send_email(['%s.pdf'%(args.output),'%s_half_count.pdf'%(args.output)])

if __name__ == "__main__":
	main()



