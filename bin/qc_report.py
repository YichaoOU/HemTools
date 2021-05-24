#!/usr/bin/env python

"""
this code is intended to parse HemTools results and 
output two qc files for nr reporting summary

1. mapping statistics (for sequencing depth section)
2. data quality for (data quality section)

python3

"""
# exec(open("qc_report.py").read())
from joblib import Parallel, delayed
import pandas as pd
import glob
from pathlib import Path
import numpy as np
import sys

fastq_tsv = sys.argv[1]
sample_df = pd.read_csv(fastq_tsv,sep="\t",header=None)


def parse_complexity_file(f):
    try:
        df = pd.read_csv(f,sep="\t",header=None)
        df.columns = ["Total Reads","Distinct Reads","One Read","Two Reads","NRF = Distinct/Total","PBC1 = OneRead/Distinct","PBC2 = OneRead/TwoReads"]
        df.index = [f.split("/")[-1].replace(".lib.complexity","")]
        return df
    except:
        return pd.DataFrame()



def parse_flagstat_file(f):
	# 118108564 + 0 in total (QC-passed reads + QC-failed reads)
	# 0 + 0 secondary
	# 2198 + 0 supplementary
	# 16232835 + 0 duplicates
	# 117233029 + 0 mapped (99.26% : N/A)
	# 118106366 + 0 paired in sequencing
	# 59053183 + 0 read1
	# 59053183 + 0 read2
	# 115853764 + 0 properly paired (98.09% : N/A)
	# 116852516 + 0 with itself and mate mapped
	# 378315 + 0 singletons (0.32% : N/A)
	# 852774 + 0 with mate mapped to a different chr
	# 590700 + 0 with mate mapped to a different chr (mapQ>=5)

	total = 0
	properly_mapped = 0
	mapped = 0
	PE_flag = False
	with open(f) as xx:
		for line in xx:
			line = line.strip()
			if "total (QC-passed reads + QC-failed reads)" in line:
				total = int(line.split()[0])
			if "properly paired" in line:
				properly_mapped = int(line.split()[0])
			if "0 mapped" in line:
				mapped = int(line.split()[0])
	if properly_mapped == 0:
		properly_mapped = mapped
		# properly_mapped = properly_mapped/2
	df = pd.DataFrame([total,properly_mapped]).T
	# print (df.head())
	df.columns = ['total_reads',"properly_mapped_reads"]
	df.index = [f.split("/")[-1].replace(".markdup.report","").replace(".report","")]
	return df

	pass
	
	
	
def parse_peak_file(f):

	# 7th: fold-change at peak summit
	# 8th: -log10pvalue at peak summit
	# 9th: -log10qvalue at peak summit
	# 10th: relative summit position to peak start
	df = pd.read_csv(f,sep="\t",header=None)
	FDR_cutoff = -np.log10(0.05)
	# print (df.head(),FDR_cutoff)
	df = df[df[8]>=FDR_cutoff]
	df = df[df[7].abs()>=5]
	df = pd.DataFrame([df.shape[0]]).T
	df.columns = ['FDR5_FC5_peaks']
	df.index = [f.split("/")[-1].replace(".rmdup.uq.rmchrM_peaks.narrowPeak","")]
	return df
	pass


ENCODE_qc_files = list(Path('./').rglob('*.lib.complexity'))
print (ENCODE_qc_files)
# samtools_flagstat_files = list(Path('./').rglob('*.markdup.report'))
samtools_flagstat_files = list(Path('./').rglob('*.report'))
peak_files = list(Path('./').rglob("*.rmdup.uq.rmchrM_peaks.narrowPeak"))
# peak_files = list(Path('./').rglob("*peaks.narrowPeak"))

# df_list = [parse_complexity_file(f) for f in ENCODE_qc_files]
df_list = Parallel(n_jobs=-1,verbose=10)(delayed(parse_complexity_file)(str(f)) for f in ENCODE_qc_files)
df = pd.concat(df_list)
df1 = df.T
print (df1.head())
# df_list = [parse_flagstat_file(f) for f in samtools_flagstat_files]
df_list = Parallel(n_jobs=-1,verbose=10)(delayed(parse_flagstat_file)(str(f)) for f in samtools_flagstat_files)
df = pd.concat(df_list)
df2 = df.T
print (df2.head())


# df_list = [parse_peak_file(f) for f in peak_files]
df_list = Parallel(n_jobs=-1,verbose=10)(delayed(parse_peak_file)(str(f)) for f in peak_files)
df = pd.concat(df_list)
df3 = df.T
df3.columns = [x.split(".vs.")[0] for x in df3.columns]
print (df3.head())

# sample_list = ["GATA1_WT_input","GATA1_WT","GATA1_13nt_rep1","GATA1_113G_rep1","GATA1_110C_rep1","GATA1_13nt_input_rep1","GATA1_13nt_rep2","GATA1_186T_13nt_rep1","GATA1_113G_2","GATA1_186T_113G","GATA1_110C_rep2","GATA1_186T_110C","NFYB_WT_input","NFYB_WT","NFYB_13nt_rep1","NFYB_113G","NFYB_110C","GATA1_13nt_input_rep2","GATA1_13nt_rep3","GATA1_186T_13nt_rep2","GATA1_13nt_dp","GATA1_186T_13nt_dp","NFYB_13nt_input","NFYB_13nt_rep2","NFYB_186T_13nt","NFYB_13nt_dp","NFYB_186T_13nt_dp"]
sample_list = sample_df[sample_df.columns[-1]].tolist()
# overlap_columns = list(set(df1.columns).intersection(df2.columns))
df = pd.concat([df1[sample_list],df2[sample_list]])
df = df.loc[:,~df.columns.duplicated()]

select_cols = []
used_s = []
for c in df3.columns:
	tmp = c.split("_vs_")
	if "input" in tmp[0]:
		continue
	for s in sample_list:
		if "input" in s:
			continue
		if s in tmp[0]:
			if s in used_s:
				continue
			else:
				used_s.append(s)
				select_cols.append(c)
df4 = df3[select_cols]
df4.columns = [x.split("_vs_")[0] for x in df4.columns]
df5 = pd.concat([df4,df[df4.columns]])

## output 1

df.loc[['Total Reads','Distinct Reads']].to_csv("sequencing_depth.csv")

## output2
df5.loc[['NRF = Distinct/Total','PBC1 = OneRead/Distinct','PBC2 = OneRead/TwoReads','FDR5_FC5_peaks']].to_csv("data_quality.csv")

