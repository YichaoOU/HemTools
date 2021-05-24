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
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output",  help="outputname", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today())+".tsv")
	mainParser.add_argument("--capC",  help="captureC bed file", default=None)
	requiredNamed = mainParser.add_argument_group('required named arguments')
	requiredNamed.add_argument('-tad',"--TAD_file",  help="bed file, at least 4 columns",required=True)
	requiredNamed.add_argument('-peak',"--peak_file",  help="bed file, at least 4 columns",required=True)

	# gene_name, gene_id column order
	mainParser.add_argument("--gene_name",  help="captureC bed file", type=int,default=4)
	mainParser.add_argument("--gene_id",  help="captureC bed file", type=int,default=5)

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update chrom size.", default='hg19',type=str)
	genome.add_argument('--gene_file',  help="genome version: hs, mm", default=myData['mm10_gene_bed'],type=str)
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def get_N_cols(f):
	df = pd.read_csv(f,sep="\t",header=None,nrows=3)
	return df.shape[1]

def main():

	args = my_args()
	if args.genome!="custom":
		args.gene_file = myData['%s_gene_bed'%(args.genome)]

	try:
		capC = myData[args.capC]
		flagC=True
	except:
		flagC=False
		
	N_cols_peak = get_N_cols(args.peak_file)
	N_cols_tad = get_N_cols(args.TAD_file)
	
	# step 1
	# tad genes
	os.system("module load bedtools/2.29.2;bedtools intersect -a %s -b %s -wao > tad_with_genes.bed"%(args.TAD_file,args.gene_file))
	# step 2
	# subset tad
	os.system("module load bedtools/2.29.2;bedtools intersect -a %s -b tad_with_genes.bed -wao > peaks_with_tad_with_genes.bed"%(args.peak_file))

	
	if flagC:
		os.system("module load bedtools/2.29.2;bedtools intersect -a %s -b %s -wao > tmp.bed"%(args.peak_file,capC))
	
	df = pd.read_csv("peaks_with_tad_with_genes.bed",sep="\t",header=None)
	
	df['name'] = df[0]+"_"+df[1].astype(str)+"_"+df[2].astype(str)
	# 3+9+4
	gene_name_col = N_cols_peak+N_cols_tad+args.gene_name-1
	gene_id_col = N_cols_peak+N_cols_tad+args.gene_id-1
	df = df.fillna("")
	# print (df[gene_name_col].unique())
	# print (df[gene_id_col].unique())
	gene_name = df.groupby('name')[gene_name_col].apply(",".join)
	gene_id = df.groupby('name')[gene_id_col].apply(",".join)
	columns = []
	if flagC:
		df2 = pd.read_csv("tmp.bed",sep="\t",header=None)
		df2['name'] = df2[0]+"_"+df2[1].astype(str)+"_"+df2[2].astype(str)
		df2 = df2.fillna("")
		gene_id_capC = df2.groupby('name')[N_cols_peak+args.gene_name-1].apply(",".join)
		gene_name_capC = df2.groupby('name')[N_cols_peak+args.gene_id-1].apply(",".join)
		out = pd.concat([gene_name,gene_id,gene_name_capC,gene_id_capC],axis=1).reset_index()
		out.columns = ['name',"gene_name_in_same_TAD","gene_id_in_same_TAD","gene_name_captureC","gene_id_captureC"]
	else:
		out = pd.concat([gene_name,gene_id],axis=1).reset_index()
		out.columns = ['name',"gene_name_in_same_TAD","gene_id_in_same_TAD"]
	columns += out.columns.tolist()[1:]
	out.to_csv("test.csv")
	out = rmdup(out)
	out[['chr','start','end']] = out.name.apply(lambda x:pd.Series(x.split("_")))
	out[['chr','start','end']+columns].to_csv(args.output,sep="\t",header=True,index=False)
def rmdup(out):
	for c in out.columns:
		out[c] = out[c].apply(lambda x:",".join(list(set(x.split(",")))))
	return out



if __name__ == "__main__":
	main()

























