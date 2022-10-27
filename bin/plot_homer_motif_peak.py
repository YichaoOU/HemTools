#!/hpcf/apps/python/install/2.7.13/bin/python
import os
import matplotlib
matplotlib.use('agg')
import pandas as pd
import matplotlib.pylab as plt
import argparse
"""make motif peak plot same to the figure shown below in the url

http://homer.ucsd.edu/homer/ngs/peakMotifs.html

Usage
-----

Run this program inside the homer motif folder!

module load homer/4.10
module load python/2.7.13

plot.py

Output
------

homer_motif_density_peak

In this folder, we have individual png files for each motif and a list of absolute path to the figures.


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

def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		myString = str(myString).replace("{{"+str(k)+"}}",str(myDict[k]))
	return myString
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

command = """
mkdir homer_all_motifs
cd homer_all_motifs
cp ../homerResults/*.motif .
cp ../knownResults/*.motif .
rm *similar*
rm *RV*
cat *.motif > all.motifs
rm *.motif
annotatePeaks.pl {{bed_file}} {{genome}} -m all.motifs -size {{flanking_size}} -hist {{bin_size}} > motif_density.tsv

"""

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
import subprocess
def main(command):
	args = my_args()
	args.flanking_size = args.flanking_size*2
	# bed_file = args.bed_file.split("/")[-1]
	args.bed_file = os.path.abspath(args.bed_file)
	# print os.path.dirname(os.path.abspath(args.bed_file))
	# os.path.abspath(os.path.join(directory, file))
	# print (args.bed_file)
	# exit()
	argsDict = vars(args)
	command = multireplace(command, argsDict)
	write_file("tmp.sh",command)
	print ("Running homer")
	# os.system("bash tmp.sh")
	subprocess.call("bash tmp.sh",shell=True)
	df = pd.read_csv("homer_all_motifs/motif_density.tsv",sep="\t",index_col=0)
	sel_cols = []
	for x in df.columns.tolist():
		if "total sites" in x:
			sel_cols.append(x)
	df = df[sel_cols]
	sel_cols = [x.split()[0] for x in df.columns.tolist()]
	df.columns = sel_cols
	df['Dist. To Motif'] = df.index.tolist()
	my_list={}
	cwd = os.getcwd()
	for s in sel_cols:
		file_name = lineplot(s,df)
		my_list[s] = "%s/%s"%(cwd,file_name)
	write_file("homer_all_motifs/file.list","\n".join("%s\t%s"%(x,my_list[x]) for x in my_list))
	os.system("rm tmp.sh")
	

if __name__ == "__main__":
	main(command)




























