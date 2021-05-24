#!/usr/bin/env python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from liyc_utils import *


"""

module load conda3 
source activate py2
module load bedtools





"""

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="plot number of overlaps as venn diagram given multiple (2 or 3) bed files.")
	
	mainParser.add_argument('-f',"--input",  help="a list of bed files, separated by ,",required=True)
	mainParser.add_argument('-s',"--names",  help="Default is filenames. Sample names, separated by ,",default="None")
	mainParser.add_argument('--show_percent',  help="Show percent instead of numbers", action='store_true')
	mainParser.add_argument('--set_total',  help="for 3 bed files, use the overlaps with the last one as the total", action='store_true')
	mainParser.add_argument('-o',"--output",  help="output figure name",default="bed_venn.png")

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def rename_bed(f,name,output):
	df = pd.read_csv(f,sep="\t",header=None)
	df[3] = name
	df[[0,1,2,3]].to_csv(output,sep="\t",index=False,header=False)
	
def to_venn_diagram(merged_bed_file,names,output):
	df = pd.read_csv(merged_bed_file,sep="\t",header=None)
	df['name'] = df[0]+":"+df[1].astype(str)+"-"+df[2].astype(str)
	# df = df[df[3].str.contains(names[-1])]
	df.to_csv("test.csv")
	my_list = []
	for n in names:
		my_list.append(set(df[df[3].str.contains(n)]['name'].to_list()))
	total=float(df.shape[0])
	plt.figure()
	if len(my_list) == 3:
		# venn3(my_list,names,subset_label_formatter=lambda x: '%0.1f%%'%(x/total*100))
		venn3(my_list,names)
	if len(my_list) == 2:
		# venn2(my_list,names,subset_label_formatter=lambda x: '%0.1f%%'%(x/total*100))	
		venn2(my_list,names)	
	plt.title("Venn diagram")
	plt.savefig(output)


def main():

	args = my_args()
	input_files = args.input.split(",")
	if args.names == "None":
		names = [".".join(x.split(".")[:-1]).replace(".markdup","").replace(".rmchrM_peaks","").replace(".rmblck","").replace(".rmdup","") for x in input_files]
	else:
		names = args.names.split(",")
	renamed_files = [str(uuid.uuid4()).split("-")[-1] for i in range(len(input_files))]
	[rename_bed(input_files[i],names[i],renamed_files[i]) for i in range(len(input_files))]
	combine_files = "cat %s > combined_files.bed"%(" ".join(renamed_files))
	os.system(combine_files)
	[os.system('rm %s'%(x)) for x in renamed_files]
	
	bedtools = "module load bedtools;sort -k1,1 -k2,2n combined_files.bed > combined_files.sorted; bedtools merge -c 4 -o collapse -i combined_files.sorted > merged_files.bed"
	os.system(bedtools)
	to_venn_diagram("merged_files.bed",names,args.output)
if __name__ == "__main__":
	main()


















