#!/usr/bin/env python

import pandas as pd
import glob
## must be python3

def get_ref(df):
    tmp = df[df.n_deleted==0]
    tmp = df[df.n_inserted==0]
    return tmp.Reference_Sequence.tolist()[0]
def get_mutation_positions(ref,var_tsv):
    var = pd.read_csv(var_tsv,sep="\t",header=None)
    var = var.transform(lambda x:x.str.upper())
    mutation_pos_list = {} # 0-index
    for i,j in var.values:
        init_pos = ref.index(i)
        for base_index in range(len(i)):
            if i[base_index] != j[base_index]:
                mutation_pos_list[init_pos+base_index] = j[base_index]
    return mutation_pos_list
def get_mutation_type(alt_seq,mut_dict):
    for i in mut_dict:
        if alt_seq[i]!=mut_dict[i]:
            return False
    return True


# get all files
files = glob.glob("**/Alleles_frequency_table_around_sgRNA*txt",recursive=True)
import sys
var_tsv = sys.argv[1]
out = []
for f in files:
	label = f.split("/")[0]
	try:
		df = pd.read_csv(f,sep="\t")
		ref = get_ref(df)
		mut_dict = get_mutation_positions(ref,var_tsv)
		df['is_expected_edit'] = df.Aligned_Sequence.apply(lambda x:get_mutation_type(x,mut_dict))
		edited_reads = df[df.is_expected_edit==True]['#Reads'].sum()
		total_reads = df['#Reads'].sum()
	except:
		edited_reads=-1
		total_reads=-1
	out.append([label,edited_reads,total_reads])
out = pd.DataFrame(out)
out.columns = ['label','edited_reads','total_reads']
out['editing_freq'] = out.edited_reads / out.total_reads
out.to_csv("custom_edit_freq.csv",index=False)
print (out)
