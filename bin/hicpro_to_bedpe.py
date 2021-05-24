#!/usr/bin/env python


import sys

import pandas as pd

"""
This program is used to convert hicpro sparse matrix to bedpe format

(hicexplorer) [yli11@nodecn125 Jurkat_20copy]$ head iced/20000/Jurkat_20copy_20000_iced.matrix
4	4	128.633202
4	5	108.306118
4	6	111.455314
4	7	98.392661
4	8	61.623737
4	9	50.675832
4	10	42.662543
4	11	35.943330
4	12	33.816256
4	13	20.717739
(hicexplorer) [yli11@nodecn125 Jurkat_20copy]$ head raw/20000/Jurkat_20copy_20000_abs.bed
chr10_paternal	0	20000	1
chr10_paternal	20000	40000	2
chr10_paternal	40000	60000	3
chr10_paternal	60000	80000	4
chr10_paternal	80000	100000	5
chr10_paternal	100000	120000	6
chr10_paternal	120000	140000	7
chr10_paternal	140000	160000	8
chr10_paternal	160000	180000	9
chr10_paternal	180000	200000	10


"""

import glob
import sys

resolution = sys.argv[1]
## takes about 60G memory
bed_file = glob.glob("raw/%s/*%s*abs.bed"%(resolution,resolution))[0]
print ("reading bed file: %s"%(bed_file))
bed = pd.read_csv(bed_file,sep="\t",header=None)
iced_file = glob.glob("iced/%s/*iced.matrix"%(resolution))[0]
print ("reading iced file: %s"%(iced_file))
# iced_file = glob.glob("raw/%s/*.matrix"%(resolution))[0]
# print ("reading raw file: %s"%(iced_file))
df = pd.read_csv(iced_file,sep="\t",header=None)
bed = bed.set_index(3)
df1 = bed.loc[df[0]].reset_index(drop=True)
df2 = bed.loc[df[1]].reset_index(drop=True)
out = pd.concat([df1,df2,df[[2,2]]],axis=1)
print ("saving df")
print (df.shape)
out.to_csv("HiCPro_%s_iced.bedpe"%(resolution),sep="\t",header=False,index=False)
# out.to_csv("HiCPro_%s_raw.bedpe"%(resolution),sep="\t",header=False,index=False)
import os
print ("sorting and gzip")
command = """
module load htslib
sort -k1,1 -k2,2n HiCPro_20000_iced.bedpe > HiCPro_20000_iced.st.bed
bgzip HiCPro_20000_iced.st.bed
tabix -p bed HiCPro_20000_iced.st.bed.gz
""".replace("20000",resolution)
# command = """
# module load htslib
# sort -k1,1 -k2,2n HiCPro_20000_raw.bedpe > HiCPro_20000_raw.st.bed
# bgzip HiCPro_20000_raw.st.bed
# tabix -p bed HiCPro_20000_raw.st.bed.gz
# """.replace("20000",resolution)
os.system(command)

# raw matrix, for replicate QC
'''
bed_file = glob.glob("raw/%s/*%s*abs.bed"%(resolution,resolution))[0]
print ("reading bed file: %s"%(bed_file))
bed = pd.read_csv(bed_file,sep="\t",header=None)
iced_file = glob.glob("raw/%s/*.matrix"%(resolution))[0]
print ("reading raw file: %s"%(iced_file))
df = pd.read_csv(iced_file,sep="\t",header=None)
bed = bed.set_index(3)
df1 = bed.loc[df[0]].reset_index(drop=True)
df2 = bed.loc[df[1]].reset_index(drop=True)
out = pd.concat([df1,df2,df[[2,2]]],axis=1)
print ("saving df")
print (out.head)
# out.to_csv("HiCPro_%s_raw.bedpe"%(resolution),sep="\t",header=False,index=False)
out.columns = [0,1,2,3,4,5,6,7]
contact = out[[0,1,3,4,6]]
contact.to_csv("HiCPro_%s_contact_matrix.repQC.gz"%(resolution),sep="\t",header=False,index=False,compression='gzip')

bed1 = out[[0,1,2,1]]
bed1.columns=[0,1,2,3]
bed1['name'] = bed1[0]+bed1[3].astype(str)
bed1 = bed1.drop_duplicates('name')
bed2 = out[[3,4,5,4]]
bed2.columns=[0,1,2,3]
bed2['name'] = bed2[0]+bed2[3].astype(str)
bed2 = bed2.drop_duplicates('name')
bed = pd.concat([bed1,bed2])
bed = bed.drop_duplicates('name')
bed[[0,1,2,3]].to_csv("HiCPro_%s_bed.repQC.gz"%(resolution),sep="\t",header=False,index=False,compression='gzip')
# import os
# print ("sorting and gzip")
# command = """

# sort -k1,1 -k2,2n HiCPro_20000_iced.bedpe > HiCPro_20000_iced.st.bed
# bgzip HiCPro_20000_iced.st.bed
# tabix -p bed HiCPro_20000_iced.st.bed.gz
# .replace("20000",resolution)
# os.system(command)
'''


