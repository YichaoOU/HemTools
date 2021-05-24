
import pandas as pd

def get_AF_DP(x,pos):
	items = x.split(":")
	values = [int(i) for i in items[pos].split(",")]
	DP = sum(values)
	if DP == 0:
		return -1,0
	AF = 1-float(values[0])/(DP)
	return AF,DP


def parse_vcf(f):
	df = pd.read_csv(f,sep="\t",header=None,comment="#")
	print (df.shape)
	AD_position = df.iat[0,8].split(":").index("AD")
	output_columns = ['AF',"DP"]
	df[output_columns] = df[df.columns[-1]].apply(lambda x:pd.Series(get_AF_DP(x,AD_position)))
	df['name'] = df[0]+"-"+df[1].astype(str)
	df.index = df.name
	print (df.shape)
	return df[[3,4]+output_columns]

def get_control_list(f):
	myList = []
	with open(f) as ff:
		for line in ff:
			line = line.strip().split()
			myList.append(line[0]+"-"+line[1])
	return myList

def ag_rate(df,DP_cutoff):
	tmp_df = df.copy()
	tmp_df = tmp_df[tmp_df['DP']>=DP_cutoff]
	tmp_df1 = tmp_df[(tmp_df[3]=="A")&(tmp_df[4]=="G")]
	tmp_df2 = tmp_df[(tmp_df[3]=="T")&(tmp_df[4]=="C")]
	tmp = pd.concat([tmp_df1,tmp_df2])
	print ("AG conversion rate:")
	print (tmp.describe())
	return tmp
	
def raw_passed_variants(df,DP_cutoff):
	tmp_df = df.copy()
	tmp_df = tmp_df[tmp_df['DP']>=DP_cutoff]
	return tmp_df

def ct_rate(df,DP_cutoff):
	tmp_df = df.copy()
	tmp_df = tmp_df[tmp_df['DP']>=DP_cutoff]
	tmp_df1 = tmp_df[(tmp_df[3]=="C")&(tmp_df[4]=="T")]
	tmp_df2 = tmp_df[(tmp_df[3]=="G")&(tmp_df[4]=="A")]
	tmp = pd.concat([tmp_df1,tmp_df2])
	print ("CT conversion rate:")
	print (tmp.describe())
	return tmp
	
import sys
DP_cutoff=10
treatment_vcf = sys.argv[1]
control_bamCount = sys.argv[2]
output_prefix = sys.argv[3]
# The following is work as expected!
# treatment_vcf = "../H1_H2/rna_seq_variant_call_yli11_2019-12-05/1000001_RFR002_S2_filtered.vcf"
# control_bamCount = "bam_count_yli11_2019-12-31/1000001_RFR002_S2.bam.count.filtered"
vcf = parse_vcf(treatment_vcf)
print (vcf.head())
control = get_control_list(control_bamCount)

vcf2 = vcf.loc[control]
vcf2 = vcf2.dropna()
print ("vcf2 shape: %s"%(vcf2.shape[0]))

df = ag_rate(vcf2,DP_cutoff)
df.to_csv("%s_AG.csv"%(output_prefix))
df = raw_passed_variants(vcf2,DP_cutoff)
df.to_csv("%s_all_passed_variants.csv"%(output_prefix))
df = ct_rate(vcf2,DP_cutoff)
df.to_csv("%s_CT.csv"%(output_prefix))

# >>> treatment_vcf = "../SRR8096314_HepG2_HepG2_filtered.vcf"
# >>> control_bamCount = "SRR8096313_HepG2_nCas9-UGI-NLS-P2A-EGFP.bam.count.filtered"
# work as expected
# python subset_vcf_given_positions.py ../rna_seq_variant_call_yli11_2019-11-15/SRR8096314_HepG2_HepG2_filtered.vcf ../rna_seq_variant_call_yli11_2019-11-15/bam_count_yli11_2019-12-12/SRR8096313_HepG2_nCas9-UGI-NLS-P2A-EGFP.bam.count.filtered

# SRR8908989_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-control-rep1
# SRR8908990_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-ABEmax-rep1
# SRR8908991_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-miniABEmax-rep1
# SRR8908992_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-miniABEmax_variant1-rep1
# SRR8908993_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-miniABEmax_variant2-rep1
# SRR8908994_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-control-rep2
# SRR8908995_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-ABEmax-rep2
# SRR8908996_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-miniABEmax-rep2
# SRR8908997_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-miniABEmax_variant1-rep2
# SRR8908998_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2miniABEmax_variant2-rep2
# SRR8908999_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-control-rep3
# SRR8909000_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-ABEmax-rep3
# SRR8909001_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-miniABEmax-rep3
# SRR8909002_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-miniABEmax_variant1-rep3
# SRR8909003_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-HEKsite2-miniABEmax_variant2-rep3
# SRR8909009_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-GFP-rep1
# SRR8909015_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-GFP-rep2
# SRR8909021_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-GFP-rep3
# SRR8096313_HepG2_HepG2Aligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam	 SRR8096313_HepG2_nCas9-UGI-NLS-P2A-EGFP
# SRR8096314_HepG2_HepG2Aligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam	 SRR8096314_HepG2_BE3-P2A-EGFP
# SRR8096317_HepG2_HepG2Aligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam	 SRR8096317_HepG2_nCas9-UGI-NLS-P2A-EGFP
# SRR8096318_HepG2_HepG2Aligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam	 SRR8096318_HepG2_BE3-P2A-EGFP
# SRR8096321_HepG2_HepG2Aligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam	 SRR8096321_HepG2_nCas9-UGI-NLS-P2A-EGFP
# SRR8096322_HepG2_HepG2Aligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam	 SRR8096322_HepG2_BE3-P2A-EGFP
# SRR8909009_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-GFP-rep1
# SRR8909015_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-GFP-rep2
# SRR8909021_HEK293T_HEK293TAligned.sortedByCoord.rg_added.dedupped.split.IndelRealigner.BQSR.bam HEK293T-GFP-rep3

# python subset_vcf_given_positions.py ../rna_seq_variant_call_yli11_2019-11-15/final_results/SRR8909015_HEK293T_HEK293T.GTAK.bcftools.final.vcf ../rna_seq_variant_call_yli11_2019-11-15/bam_count_yli11_2019-12-12/HEK293T-HEKsite2-control-rep2.bam.count.relaex




# /home/yli11/dirs/Base_editor_RNA_seq/down_sampled_fastq_files/analysis2

# python subset_vcf_given_positions.py ../rna_seq_variant_call_yli11_2019-11-15/final_results/SRR8909015_HEK293T_HEK293T.GTAK.bcftools.final.vcf ../rna_seq_variant_call_yli11_2019-11-15/bam_count_yli11_2019-12-12/HEK293T-HEKsite2-control-rep2.bam.count.relaex
# (40811, 10)
# (40811, 13)
			# 3  4		AF	DP
# name
# chr1-14653  C  T  0.684211  38.0
# chr1-14677  G  A  0.465517  58.0
# chr1-14907  A  G  0.307692  13.0
# chr1-14930  A  G  0.428571  14.0
# chr1-16378  T  C  0.700000  10.0
# subset_vcf_given_positions.py:64: FutureWarning:
# Passing list-likes to .loc or [] with any missing label will raise
# KeyError in the future, you can use .reindex() as an alternative.

# See the documentation here:
# http://pandas.pydata.org/pandas-docs/stable/indexing.html#deprecate-loc-reindex-listlike
  # vcf2 = vcf.loc[control]
# vcf2 shape: 3158
# AG conversion rate:
			   # AF		  DP
# count  385.000000  385.000000
# mean	 0.225811   18.864935
# std	  0.094224   12.411665
# min	  0.076923   10.000000
# 25%	  0.166667   11.000000
# 50%	  0.200000   14.000000
# 75%	  0.272727   22.000000
# max	  0.846154  116.000000
# CT conversion rate:
			  # AF		  DP
# count  89.000000   89.000000
# mean	0.249354   29.977528
# std	 0.176370   42.592140
# min	 0.081081   10.000000
# 25%	 0.142857   12.000000
# 50%	 0.192308   18.000000
# 75%	 0.285714   27.000000
# max	 1.000000  294.000000


# [yli11@nodegpu118 analysis2]$ python subset_vcf_given_positions.py ../rna_seq_variant_call_yli11_2019-11-15/final_results/SRR8908995_HEK293T_HEK293T.GTAK.bcftools.final.vcf ../rna_seq_variant_call_yli11_2019-11-15/bam_count_yli11_2019-12-12/HEK293T-HEKsite2-control-rep2.bam.count.relaex
# (75417, 10)
# (75417, 13)
			# 3  4		AF	DP
# name
# chr1-14653  C  T  0.593750  32.0
# chr1-14677  G  A  0.400000  40.0
# chr1-15015  G  C  0.400000  10.0
# chr1-15211  T  G  0.727273  11.0
# chr1-15214  T  C  0.181818  11.0
# subset_vcf_given_positions.py:64: FutureWarning:
# Passing list-likes to .loc or [] with any missing label will raise
# KeyError in the future, you can use .reindex() as an alternative.

# See the documentation here:
# http://pandas.pydata.org/pandas-docs/stable/indexing.html#deprecate-loc-reindex-listlike
  # vcf2 = vcf.loc[control]
# vcf2 shape: 30555
# AG conversion rate:
				 # AF			DP
# count  27640.000000  27640.000000
# mean	   0.236581	 98.919935
# std		0.134600	164.195491
# min		0.058824	 10.000000
# 25%		0.155556	 28.000000
# 50%		0.194444	 55.000000
# 75%		0.266667	110.000000
# max		1.000000   3914.000000
# CT conversion rate:
			   # AF		  DP
# count  139.000000  139.000000
# mean	 0.241442   43.928058
# std	  0.161409   78.184902
# min	  0.075000   10.000000
# 25%	  0.152022   13.000000
# 50%	  0.181818   19.000000
# 75%	  0.275253   32.000000
# max	  1.000000  516.000000