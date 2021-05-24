#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


"""
Every python wrapper is supposed to be similar, since they are using the same convention.

The only thing need to be changed is the guess_input function and the argparser function.

look for ## CHANGE THE FUNCTION HERE FOR DIFFERENT WRAPPER

variable inherents from utils:
myData
myPars
myPipelines
"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="Heatmap for exon level expression")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--bait_bed",  help="bait bed file", required=True)
	mainParser.add_argument('--bdg',  help="bdg file from hicpro, 4 columns", required=True)
	mainParser.add_argument('--ctcf_peak',  help="bdg file from hicpro, 4 columns", default=None)
	mainParser.add_argument('--ctcf_motif',  help="bdg file from hicpro, 4 columns", default=None)
	mainParser.add_argument('-w',  help="ChiCmaxima parameter, window size, default 50kb", default=50,type=int)
	mainParser.add_argument('-c',  help="ChiCmaxima parameter, cis window, default 5MB, Chicmaxima default is 1.5MB", default=5000000,type=int)
	mainParser.add_argument('-s',  help="ChiCmaxima parameter, loess_span", default=0.05,type=float)
	mainParser.add_argument('-e',  help="ChiCmaxima enrichment score cutoff, only applied when biological evidence is not found, this default =2 is very stringent", default=2,type=float)
	mainParser.add_argument('-n',  help="number of reads cutoff, called interactions with less than this count is removed, depends on sequencing depth", default=5,type=int)
	mainParser.add_argument('-d1',  help="distance to nearest CTCF peak cutoff, 5kb", default=5000,type=int)
	mainParser.add_argument('-d2',  help="distance to nearest TSS cutoff, 10kb", default=10000,type=int)
	mainParser.add_argument('--gene_exp',  help="will match gene name in our tss bed file, and append all columns in this user provided file", default=None)
	mainParser.add_argument('--logFC',  help="gene logFC cutoff, make sure you have a column called logFC. If provided, further filter out interactions", default=None)
	# mainParser.add_argument("--remove_first_line",  help="bdg file list", default=None)
	mainParser.add_argument("--filter",  help="filter using the criteria based on our 20copy project", action='store_true' )
	mainParser.add_argument('-o',"--output",  help="output prefix",default="captureC_ChiCMaxima_"+username+"_"+str(datetime.date.today()))


	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('--gene',  help="gene body", default=myData['hg19_ensembl_gene_body'])

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def to_ibed(bed_file,bdg_file,output):

	"""bdg+bed to ibed

	bed file 4 columns, bdg 4 colmns


	output format
	--------

	ID_Bait	chr_Bait	start_Bait	end_Bait	Bait_name	ID_OE	chr_OE	start_OE	end_OE	OE_name	N
	30	chr1	3090913	3092556	U6.149	590	chr1	4592259	4592779	.	0
	30	chr1	3090913	3092556	U6.149	593	chr1	4595997	4596467	.	1
	30	chr1	3090913	3092556	U6.149	596	chr1	4605050	4610398	.	2

	for runnning https://github.com/yousra291987/ChiCMaxima





	"""

	bdg = pd.read_csv(bdg_file,sep="\t",header=None,comment="#")
	bed = pd.read_csv(bed_file,sep="\t",header=None,comment="#")
	bed[4] = bed[0]+"_"+bed[1].astype(str)+"_"+bed[2].astype(str)
	bed[5] = bed.index.tolist()
	bdg[4] = bdg[0]+"_"+bdg[1].astype(str)+"_"+bdg[2].astype(str)
	bdg[5] = bdg.index.tolist()
	## ID has to be int
	df_list= []
	for chr,start,end,name,id in bed.values:
		# print (chr,start,end,name)
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
	ChiCMaxima_input = "%s.ibed"%(output)
	df.to_csv(ChiCMaxima_input,sep="\t",index=False)
	return ChiCMaxima_input

def call_ChiCMaxima(bed_file,bdg_file,output,w,s,c):

	# get input
	input = to_ibed(bed_file,bdg_file,output)
	ChiCMaxima_output = "%s.ChiC_output.ibed"
	command = "module load R/3.5.1;ChiCMaxima_v0.9.R -i %s -o %s -w %s -s %s -c %s"%(input,ChiCMaxima_output,w,s,c)
	os.system(command)
	return ChiCMaxima_output
	
	



def main():

	args = my_args()
	args.gene = myData['%s_ensembl_gene_body'%(args.genome)]
	call_ChiCMaxima(args.bait_bed,args.bdg,args.output,args.w,args.s,args.c)
	
if __name__ == "__main__":
	main()







































