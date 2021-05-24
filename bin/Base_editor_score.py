#!/home/yli11/.conda/envs/py2/bin/python


from os.path import isfile,isdir

import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF #empirical cumulative distribution function
from scipy.special import chdtrc as chi2_cdf
from scipy.stats import pearsonr
import uuid
import sys
import os
import pandas as pd
import glob
import os
import matplotlib
matplotlib.use('agg')
import pandas as pd
import matplotlib.pylab as plt
import argparse
import numpy as np
import sys

import pandas as pd
import numpy as np

from scipy.stats import pearsonr
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from data import *
import datetime
import re
def bdg_to_bw(output,chrom_size):
	os.system("sort -k1,1 -k2,2n %s.bdg > %s.sorted"%(output,output))
	os.system("module load ucsc/041619;bedGraphToBigWig %s.sorted %s %s.bw;rm %s.sorted"%(output,chrom_size,output,output))


## -------- EB----------------

#Input: An m x n data matrix with each of m rows representing a variable and each of n columns representing a sample. Should be of type numpy.array
#       A vector of m P-values to combine. May be a list or of type numpy.array.
#Output: A combined P-value using the Empirical Brown's Method (EBM).
#        If extra_info == True: also returns the p-value from Fisher's method, the scale factor c, and the new degrees of freedom from Brown's Method
def EmpiricalBrownsMethod(data_matrix, p_values, extra_info = False):
    covar_matrix = CalculateCovariances(data_matrix)
    return CombinePValues(covar_matrix, p_values, extra_info)


#Input: raw data vector (of one variable) with no missing samples. May be a list or an array.
#Output Transforemd data vector w.
def TransformData(data_vector):
    m = np.mean(data_vector)
    sd = np.std(data_vector)
    s = [(d-m)/sd for d in data_vector]
    W = lambda x: -2*np.log(ECDF(s)(x))
    return np.array([W(x) for x in s])

#Input: An m x n data matrix with each of m rows representing a variable and each of n columns representing a sample. Should be of type numpy.array.
#       Note: Method does not deal with missing values within the data.
#Output: An m x m matrix of pairwise covariances between transformed raw data vectors
def CalculateCovariances(data_matrix):
    transformed_data_matrix = np.array([TransformData(f) for f in data_matrix])
    covar_matrix = np.cov(transformed_data_matrix)

    return covar_matrix
    
#Input: A m x m numpy array of covariances between transformed data vectors and a vector of m p-values to combine.
#Output: A combined P-value. 
#        If extra_info == True: also returns the p-value from Fisher's method, the scale factor c, and the new degrees of freedom from Brown's Method
def CombinePValues(covar_matrix, p_values, extra_info = False):
    m = int(covar_matrix.shape[0])
    #print "m", m
    df_fisher = 2.0*m
    Expected = 2.0*m
    cov_sum = 0
    for i in range(m):
        for j in range(i+1, m):
            cov_sum += covar_matrix[i, j]
    
    #print "cov sum", cov_sum
    Var = 4.0*m+2*cov_sum
    c = Var/(2.0*Expected)
    df_brown = 2.0*Expected**2/Var
    if df_brown > df_fisher:
        df_brown = df_fisher
        c = 1.0

    x = 2.0*sum([-np.log(p) for p in p_values])
    #print "x", x
    p_brown = chi2_cdf(df_brown, 1.0*x/c)
    p_fisher = chi2_cdf(df_fisher, 1.0*x)
    
    if extra_info:
        return p_brown, p_fisher, c, df_brown
    else:
        return p_brown

#Input: An m x n data matrix with each of m rows representing a variable and each of n columns representing a sample. Should be of type numpy.array
#       A vector of m P-values to combine. May be a list or of type numpy.array.
#Output: A combined P-value using Kost's Method.
#        If extra_info == True: also returns the p-value from Fisher's method, the scale factor c, and the new degrees of freedom from Brown's Method
def KostsMethod(data_matrix, p_values, extra_info = False):
    covar_matrix = CalculateKostCovariance(data_matrix)
    return CombinePValues(covar_matrix, p_values, extra_info = extra_info)
    
#Input correlation between two n x n data vectors.
#Output: Kost's approximation of the covariance between the -log cumulative distributions. This is calculated with a cubic polynomial fit.
def KostPolyFit(cor):
    a1, a2, a3 = 3.263, .710, .027 #Kost cubic coeficients
    return a1*cor+a2*cor**2+a3*cor**3
    
#Input: An m x n data matrix with each of m rows representing a variable and each of n columns representing a sample. Should be of type numpy.array.
#       Note: Method does not deal with missing values within the data.
#Output: An m x m matrix of pairwise covariances between the data vectors calculated using Kost's polynomial fit and numpy's pearson correlation function.
def CalculateKostCovariance(data_matrix):
    m = data_matrix.shape[0]
    covar_matrix = np.zeros((m, m))
    for i in range(m):
        for j in range(i+1, m):
            cor, p_val = pearsonr(data_matrix[i, :], data_matrix[j, :])
            covar = KostPolyFit(cor)
            covar_matrix[i, j] = covar
            covar_matrix[j, i] = covar
    return covar_matrix
    
def parse_dataframe(x):
	df = pd.read_csv(x,sep=guess_sep(x),index_col=0)
	myCols = df.columns.tolist()
	df['myChr'] = [re.split('_|-|\.|:',i)[0] for i in df.index.tolist()]
	df['myStart'] = [re.split('_|-|\.|:',i)[1] for i in df.index.tolist()]
	# print df.head()
	df['myEnd'] = [re.split('_|-|\.|:',i)[2] for i in df.index.tolist()]
	myBed = ['myChr','myStart','myEnd']
	return df,myBed,myCols
	
def dataframe_to_bed(args):
	df,myBed,myCols = parse_dataframe(args.bdg_files)
	myList = []
	for c in myCols:
		output = "%s/%s.bdg"%(args.jid,c)
		df[myBed+[c]].to_csv(output,sep="\t",index=False,header=False)
		myList.append("%s.bdg"%(c))
	args.bdg_files = "%s/%s.input"%(args.jid,args.jid)
	write_file(args.bdg_files,"\n".join(myList))

"""workflow

1. given sgRNA bed file, generate all A or C bases

chr19	13215425	13215426	CTATGCGCAAGCCCGTGGCC	2	+
chr19	13215431	13215432	CTATGCGCAAGCCCGTGGCC	8	+
chr19	13215432	13215433	CTATGCGCAAGCCCGTGGCC	9	+
chr6	135501701	135501702	GACATGTGACAATACGACGG	1	+
chr6	135501703	135501704	GACATGTGACAATACGACGG	3	+
chr6	135501708	135501709	GACATGTGACAATACGACGG	8	+
chr6	135501710	135501711	GACATGTGACAATACGACGG	10	+
chr6	135501711	135501712	GACATGTGACAATACGACGG	11	+

the 5th column is the A position on the sgRNA sequence, zero index

2. run the EBM method


3. generate bw files



"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	# mainParser.add_argument('-o',"--output",  help="output file name for FDR bw", default="base_editor_score")
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f1',"--mageck_RRA",  help="mageck_RRA sgRNA summary file",required=True)
	mainParser.add_argument('-f2',"--mageck_norm_count",  help="mageck sgRNA normalized count file",required=True)
	mainParser.add_argument('-b','--gRNA_bed',  help="gRNA bed file, need strand info",required=True)
	mainParser.add_argument('-e','--edit_base',  help="A for ABE and C for CBE",required=True)
	mainParser.add_argument('--edit_freq',  help="known editing frequency to adjust position effect",default="/home/yli11/HemTools/share/misc/editing_frequency.list")



	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg19',type=str)
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=myData['hg19_chrom_size'])


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


## main function ##
def main():

	args = my_args()
	args.chrom_size = myData['%s_chrom_size'%(args.genome)]
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		print  ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		print ("The new job id is: "+args.jid)
	else:
		print ("The job id is: "+args.jid)			
	os.system("mkdir %s"%(args.jid))
	
	## filter out gRNAs not found in any of the input files
	gRNA = pd.read_csv(args.gRNA_bed,sep="\t",header=None)
	gRNA.index = gRNA[3].tolist()
	gRNA_list = gRNA[3].tolist()
	abe = pd.read_csv(args.mageck_RRA,sep="\t")
	abe.index = [re.split("-|_|\||:|\.",x)[-1] for x in abe.sgrna]
	ABE_count = pd.read_csv(args.mageck_norm_count,sep="\t")
	ABE_count.index = [re.split("-|_|\||:|\.",x)[-1] for x in ABE_count.sgRNA]
	use_gRNA_list = list(set(gRNA_list).intersection(abe.index))
	use_gRNA_list = list(set(use_gRNA_list).intersection(ABE_count.index))
	ABE_count = ABE_count.loc[use_gRNA_list]
	abe = abe.loc[use_gRNA_list]
	gRNA = gRNA.loc[use_gRNA_list]
	# step 1: given sgRNA bed file, generate all A or C bases
	step1_out = "%s/gRNA_all_%s.pos"%(args.jid,args.edit_base)
	gRNA.to_csv("%s/overlaped_gRNA"%(args.jid),sep="\t",header=False,index=False)
	
	command = "get_editable_base.py %s/overlaped_gRNA %s %s"%(args.jid,args.edit_base,step1_out)
	os.system(command)
	df = pd.read_csv(step1_out,sep="\t",header=None)
	print ("-----------A pos per gRNA------------------")
	print (df.head())
	df['name'] = df[0]+":"+df[1].astype(str)+"-"+df[2].astype(str)+df[5].astype(str)
	A_by_gRNA = pd.DataFrame(df.groupby('name')[3].agg(', '.join))
	A_by_gRNA.columns = ['gRNAs']
	
	
	# abe.index = [x.split("-")[-1] for x in abe.sgrna]
	
	myFDR = abe['FDR'].to_dict()
	df[3] = df[3].map(myFDR)
	df[3] = df[3].astype(str)
	df[4] = df[4].astype(str)
	A_by_FDR = pd.DataFrame(df.groupby('name')[3].agg(', '.join))
	A_by_gRNA['FDRs'] = A_by_FDR[3]
	A_by_pos = pd.DataFrame(df.groupby('name')[4].agg(', '.join))
	A_by_gRNA['pos'] = A_by_pos[4]
	A_by_gRNA.head()
	A_by_gRNA['coord'] = A_by_gRNA.index.tolist()
	A_by_gRNA.index = [x[:-1] for x in A_by_gRNA.index]
	# print (A_by_gRNA.head())
	A_by_gRNA[['filtered_gRNAs','filtered_FDRs',"filtered_pos","length"]] = A_by_gRNA.apply(row_apply, axis=1).apply(pd.Series)

	A_by_gRNA = A_by_gRNA[A_by_gRNA['length']>0]

	freq = pd.read_csv(args.edit_freq,header=None)
	freq = freq[0].tolist()
	# A_by_gRNA['new_FDR'] = A_by_gRNA.apply(new_FDR,axis=1)
	A_by_gRNA['new_FDR'] = A_by_gRNA.apply(lambda x:new_FDR(x,freq),axis=1)

	ABE_count = ABE_count.drop(['sgRNA','Gene'],axis=1)
	ABE_count.columns = list(range(ABE_count.shape[1]))
	print ("-----------MAGECK count table------------------")
	print (ABE_count.head())
	# A_by_gRNA['EBM_FDR']=A_by_gRNA.apply(combine_p_value,axis=1)    
	A_by_gRNA['EBM_FDR']=A_by_gRNA.apply(lambda x:combine_p_value(x,ABE_count),axis=1)    
	A_by_gRNA['BaseEditorScore'] = [-np.log10(x) for x in A_by_gRNA['EBM_FDR']]
	A_by_gRNA.to_csv("%s/Editable_scores.tsv"%(args.jid),sep="\t")
	# print (A_by_gRNA.head())
	# step3, convert to bw
	df = A_by_gRNA[['BaseEditorScore']]
	df[0] = [re.split('_|-|\.|:',i)[0] for i in df.index.tolist()]
	df[1] = [re.split('_|-|\.|:',i)[1] for i in df.index.tolist()]
	# print df.head()
	df[2] = [re.split('_|-|\.|:',i)[2] for i in df.index.tolist()]
	df[3] = df['BaseEditorScore']
	df[[0,1,2,3]].to_csv("%s/Editable_scores.bdg"%(args.jid),sep="\t",header=False,index=False)
	bdg_to_bw("%s/Editable_scores"%(args.jid),args.chrom_size)
	command = "cp %s %s/gRNA.bed;module load python/2.7.13;module load htslib;cd %s;create_tracks.py --current_dir -g %s"%(args.gRNA_bed,args.jid,args.jid,args.genome)
	os.system(command)


def row_apply(r):
    gRNA_list = r["gRNAs"].split(", ")
    FDR_list = r['FDRs'].split(", ")
    pos_list = r['pos'].split(", ")
    new_gRNA_list = []
    new_FDR_list = []
    new_pos_list = []
    for i in range(len(pos_list)):
        if 0<=int(pos_list[i])<=12: ## from 0 to 12 positions are observed editing events
            new_gRNA_list.append(gRNA_list[i])
            new_FDR_list.append(FDR_list[i])            
            new_pos_list.append(pos_list[i])   
    return [", ".join(new_gRNA_list),", ".join(new_FDR_list),", ".join(new_pos_list),len(new_gRNA_list)]


def new_FDR(x,freq):
    FDRs= [float(y) for y in x['filtered_FDRs'].split(", ")]
    new_FDRs = []
    pos_list = [int(y) for y in x['filtered_pos'].split(", ")]
    for i in range(len(pos_list)):
        pos = pos_list[i]
        FDR = FDRs[i]+1e-300
        new_FDRs.append(min(FDR/freq[pos],1))
    return ", ".join([str(f) for f in new_FDRs])    

# EmpiricalBrownsMethod(DataMatrix, Pvalues, extra_info = True)
def combine_p_value(x,ABE_count):
    """row apply for A_by_gRNA"""
    ## get count matrix
    if len(x['filtered_gRNAs'].split(", "))==1:
        return float(x['new_FDR'])
    # myCount = get_count_matrix(x['filtered_gRNAs'].split(", ")).values
    myCount = ABE_count.loc[x['filtered_gRNAs'].split(", ")].values
    ## get p-value vector
    p_value_vector = np.array([float(y) for y in x['new_FDR'].split(", ")])
    result = EmpiricalBrownsMethod(myCount, p_value_vector, extra_info = True)
    return result[0]
    
def get_count_matrix(gRNA_list):
    return ABE_count.loc[gRNA_list]
















if __name__ == "__main__":
	main()









