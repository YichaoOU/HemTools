#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *

"""

myBaseName=$(basename -- ${COL1})

sort -k1,1 -k2,2n ${COL1} > {{jid}}/${myBaseName}.sorted
cd {{jid}}
module load ucsc/041619
bedGraphToBigWig ${myBaseName}.sorted {{chrom_size}} ${myBaseName%.sorted}.bw

"""

def bdg_to_bw(bed,output,chrom_size):
	temp_file = str(uuid.uuid4())
	bed = bed.sort_values([0,1])
	bed[[0,1,2,'value']].to_csv(temp_file,sep="\t",header=False,index=False)
	# os.system("sort -k1,1 -k2,2n %s > %s.sorted"%(temp_file,temp_file))
	os.system("bedGraphToBigWig %s %s %s.bw"%(temp_file,chrom_size,output))
	os.system("rm %s"%(temp_file))

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
				
				
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output",  help="output file name", default="output.bw")

	mainParser.add_argument('-f',"--input",  help="data frame, header required",required=True)
	mainParser.add_argument("--sep",  help="this program can infer separator automatically, but it may fail. Use auto if the input tables contain different separators.",default="auto")
	mainParser.add_argument('-c',"--bw_col",  help="which col to convert to bw",required=True)
	mainParser.add_argument('-i',"--index_col",  help="which col to convert to bw",default=0,type=int)
	mainParser.add_argument("--split_index",  help="specifically designed, not generic",default=-999,type=int)
	mainParser.add_argument('-b','--bed',  help="gRNA bed file, need strand info",required=True)

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	args.chrom_size = myData['%s_chrom_size'%(args.genome)]


	##------- add functions below ----------------------

	df = pd.read_csv(args.input,sep=guess_sep(args.input),index_col=args.index_col)
	
	if args.split_index != -999:
		import re
		df.index = [re.split("\.|-|_|:",x)[args.split_index] for x in df.index]
	# print (df.head())
	# read bed
	bed = pd.read_csv(args.bed,sep="\t",header=None,index_col=3)
	# print (bed.head())
	
	bed['value'] = df[args.bw_col]
	bed['name'] = bed[0]+bed[1].astype(str)+bed[2].astype(str)
	# print (bed.head())
	
	# https://stackoverflow.com/questions/35401691/groupby-and-calculate-mean-but-keeping-all-columns
	metric_cols = ['value']
	group_cols=['name']
	aggs = bed.groupby(group_cols)[metric_cols].mean()
	# remove the metric_cols from df because we are going to replace them
	# with the means in aggs
	bed.drop(metric_cols, axis=1, inplace=True)
	# dedupe to leave only one row with each combination of group_cols
	# in df
	bed.drop_duplicates(subset=group_cols, keep='last', inplace=True)
	# add the mean columns from aggs into df
	bed = bed.merge(right=aggs, right_index=True, left_on=group_cols, how='right')

	bed = bed.dropna()
	print (bed.head())
	
	bdg_to_bw(bed,args.output,args.chrom_size)


if __name__ == "__main__":
	main()

























