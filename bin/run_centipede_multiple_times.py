#!/usr/bin/env python
import os
import matplotlib
matplotlib.use('agg')
import pandas as pd
import matplotlib.pylab as plt
import argparse
import numpy as np
import glob
"""draw footprint figure

combine two strands and draw footprint figure

filter sites by posterior probability

given CENTIPEDE output

module load R/3.5.1

module load conda3/5.1.0
source activate /home/yli11/.conda/envs/cutruntools/


"""

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)


	mainParser.add_argument('-f',"--bed_file",  help="bed or peak file",required=True)

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, mm10, mm9", default='hg19',type=str)

	motif=mainParser.add_argument_group(title='Plot Info')
	motif.add_argument('--flanking_size',  help="extend this size to left and right", default=1000,type=int)
	motif.add_argument('--bin_size',  help="bin size for plot density, use minimal 10 maximal 50, motif size can affect the figure a little bit, if you want to make the peak stronger, change this parameter", default=20)


	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def get_motif_length():
	lines = open("fimo.txt").readlines()
	return lines[1].strip().split()[0],len(lines[1].strip().split()[-1])
	
def get_significant_sites(threshold=0.99):
	file1 = open("fimo.postpr.txt").readlines()
	file2 = open("fimo.cuts.freq.txt").readlines()
	file3 = open("fimo.bed").readlines()
	selected_cuts = []
	selected_annots = []
	random_cuts = []
	random_annots = []
	for i in range(len(file1)):
		prob = float(file1[i].strip())
		if prob>=threshold:
			selected_cuts.append(file2[i].strip())
			selected_annots.append(file3[i].strip())
		if prob<=0.4:
			random_cuts.append(file2[i].strip())
			random_annots.append(file3[i].strip())

	write_file("selected_cuts.txt","\n".join(selected_cuts))
	write_file("selected_fimo.bed","\n".join(selected_annots))
	write_file("random_cuts.txt","\n".join(random_cuts))
	write_file("random_fimo.bed","\n".join(random_annots))

def run_CENTIPEDE(l):
	command = "run_centipede_parker.R selected_cuts.txt selected_fimo.bed footprint.png %s"%(l)
	os.system(command)
	command = "run_centipede_parker.R random_cuts.txt random_fimo.bed random.png %s"%(l)
	os.system(command)

def run_CENTIPEDE_raw(n,motif_length):
	command = "run_centipede_parker.R fimo.cuts.freq.txt fimo.bed fimo.png %s"%(motif_length)
	os.system(command)
	os.system("mv fimo.postpr.txt %s.rep_postpr.txt"%(n))

def abline2(val):
	"""Plot a line from slope and intercept"""
	axes = plt.gca()
	y_vals = np.array(axes.get_ylim())
	x_vals = [val]*len(y_vals)
	plt.plot(x_vals, y_vals, '--',alpha=0.6,c="grey")

def draw_combined_figure(motif_name,file_name,mlen):
	df = pd.read_csv(file_name,header=None)
	cut = df.shape[0]/2
	df1 = df.loc[list(range(df.shape[0]))[0:int(cut)]]
	df2 = df.loc[list(range(df.shape[0]))[int(cut):df.shape[0]]]
	df3 = pd.DataFrame([(g + h) / 2 for g, h in zip(df1[0], df2[0])])
	plt.figure()
	plt.plot(np.arange(-cut/2,cut/2),df3[0])
	plt.xlim(-cut/2,cut/2)
	abline2(-mlen/2)
	abline2(mlen/2)
	# print df3.shape
	
	plt.ylim(df3.min()[0],df3.max()[0])
	num_sites = len(open(file_name.replace("lambda.txt",'postpr.txt')).readlines())
	plt.title(file_name.replace(".lambda.txt","")+" | Num sites: %s"%(num_sites))
	plt.ylabel("cut-site probability")
	plt.xlabel("Dist. to motif")
	plt.savefig(file_name.replace(".txt",".strand_combined.png"))

	
	
def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		myString = str(myString).replace("{{"+str(k)+"}}",str(myDict[k]))
	return myString
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

def lineplot(s,df):
	plt.figure()
	plt.plot(df['Dist. To Motif'], df[s], label='')
	plt.title(s)
	plt.ylabel("sites per bp per peak")
	plt.xlabel("Dist. To Motif")
	file_name = "homer_all_motifs/%s.png"%(s.replace("Homer","").replace("/","-").replace("(","|").replace(")","|").replace(",","-").replace("?",""))
	plt.savefig(file_name)
	plt.close()
	return file_name

def combine_postpr():
	files = glob.glob("*.rep_postpr.txt")
	df_list = [pd.read_csv(x,header=None)[0] for x in files]
	df = pd.concat(df_list,axis=1,columns=list(range(len(df_list))))
	return df

def get_significant_sites2(threshold=0.9):
	# file1 = open("fimo.postpr.txt").readlines()
	# file2 = open("fimo.cuts.freq.txt").readlines()
	# file3 = open("fimo.bed").readlines()
	df = combine_postpr()
	prob_list  = df.mean(axis=1).tolist()
	selected_cuts = []
	selected_annots = []
	random_cuts = []
	random_annots = []
	for i in range(len(file1)):
		prob = prob_list[i]
		if prob>=threshold:
			selected_cuts.append(file2[i].strip())
			selected_annots.append(file3[i].strip())
		if prob<=0.4:
			random_cuts.append(file2[i].strip())
			random_annots.append(file3[i].strip())

	write_file("selected_cuts.txt","\n".join(selected_cuts))
	write_file("selected_fimo.bed","\n".join(selected_annots))
	write_file("random_cuts.txt","\n".join(random_cuts))
	write_file("random_fimo.bed","\n".join(random_annots))
	

def main():
	# args = my_args()
	
	
	
	motif_name,motif_length = get_motif_length()
	[run_CENTIPEDE_raw(x,motif_length) for x in range(10)]
	
	get_significant_sites2(threshold=0.8)
	run_CENTIPEDE(motif_length)
	draw_combined_figure(motif_name,"fimo.lambda.txt",motif_length)
	draw_combined_figure(motif_name,"footprint.lambda.txt",motif_length)
	draw_combined_figure(motif_name,"random.lambda.txt",motif_length)
	
	

if __name__ == "__main__":
	main()















































