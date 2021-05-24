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

def bdg_to_bw(output,chrom_size):
	os.system("sort -k1,1 -k2,2n %s.bdg > %s.sorted"%(output,output))
	os.system("bedGraphToBigWig %s.sorted %s %s.bw;rm %s.sorted"%(output,chrom_size,output,output))

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output",  help="output file name, output_FDR.bw, output_LFC.bw, output_FDR.bdg, output_LFC.bdg", default="output")

	mainParser.add_argument('-f',"--mageck_RRA",  help="mageck_RRA sgRNA summary file",required=True)
	mainParser.add_argument('-b','--gRNA_bed',  help="gRNA bed file, need strand info",required=True)

	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument("--cas9",  help="use cas9 cut site (-3) as gRNA score", action='store_true')
	group.add_argument('--ABE',  help="ABE mode", action='store_true')
	group.add_argument('--CBE',  help="CBE mode", action='store_true')

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def to_bed(df,output):
	df['name'] = df[0]+df[1].astype(str)+df[2].astype(str)
	df = df.sort_values(4)
	shape0 = df.shape[0]
	df1 = df.drop_duplicates('name')
	mean_value = pd.DataFrame(df.groupby('name')[4].mean())
	df1[4] = df['name'].map(mean_value[4].to_dict())
	shape1 = df1.shape[0]
	if shape1<shape0:
		print ("duplicated positions were removed, average values were used")
		print ("There are %s duplicated positions"%(shape0-shape1))
	df1[[0,1,2,4]].to_csv(output,sep="\t",header=False,index=False)

def main():

	args = my_args()
	args.chrom_size = myData['%s_chrom_size'%(args.genome)]


	##------- add functions below ----------------------
	# read Mageck
	
	df = pd.read_csv(args.mageck_RRA,sep="\t",index_col=0)
	
	# read gRNA bed
	
	gRNA = pd.read_csv(args.gRNA_bed,sep="\t",header=None)
	gRNA.index = gRNA[3].tolist()
	
	## re do index
	if len(set(df.index.tolist()).intersection(gRNA.index.tolist()))==0:
		df.index = [re.split('_|-|\.',x)[-1] for x in df.index.tolist()]
	
	## re position
	if args.cas9:
		for i in gRNA.index:
			if gRNA.at[i,5]=="+":
				gRNA.at[i,2] -= 3
			if gRNA.at[i,5]=="-":
				gRNA.at[i,2] = gRNA.at[i,1]+4
		gRNA[1] = gRNA[2]-1		
	else:
		print ("not implemented")
	
	# assign_values
	FDR = gRNA.copy()
	LFC = gRNA.copy()
	
	FDR[4] = df['FDR']
	FDR[4] = [-np.log10(x+1e-300) for x in FDR[4].tolist()]
	LFC[4] = df['LFC']
	FDR = FDR.reset_index(drop=True)
	LFC = LFC.reset_index(drop=True)
	# FDR[[0,1,2,4]].to_csv(args.output+".FDR.bdg",sep="\t",header=False,index=False)
	# LFC[[0,1,2,4]].to_csv(args.output+".LFC.bdg",sep="\t",header=False,index=False)
	to_bed(FDR,args.output+".FDR.bdg")
	to_bed(LFC,args.output+".LFC.bdg")
	bdg_to_bw(args.output+".FDR",args.chrom_size)
	bdg_to_bw(args.output+".LFC",args.chrom_size)
	#-------------- run jobs ----------------------
	
	
if __name__ == "__main__":
	main()

























