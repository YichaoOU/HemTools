#!/usr/bin/env python
import pandas as pd

def find_13nt_deletion(x,y):
	seed = "CAATA"
	seed_rev = "TATTG"
	
	repeat = "GCCTTGAC"
	repeat_rev = "GTCAAGGC"
	## x is aligned_sequence
	## y is ref seq
	delete_seq = ""
	delete_seq_list = []
	for i in range(len(x)):
		if x[i]!="-":
			if delete_seq != "":
				if len(delete_seq) == 13:
					delete_seq_list.append(delete_seq)
				delete_seq=""
		else:
			delete_seq+=y[i]
	for s in delete_seq_list:
		if seed in s:
			tmp = s.split(seed)
			if len(tmp)==2:
				check_seq = tmp[1]+tmp[0]
				if check_seq == repeat:
					return 1
				else:
					print ("The deletion sequence %s%s doesn't match CAATAGCCTTGAC"%(seed,check_seq))
			else:
				print ("The deletion sequence %s doesn't match CAATAGCCTTGAC"%(s))
		elif seed_rev in s:
			tmp = s.split(seed_rev)
			if len(tmp)==2:
				check_seq = tmp[0]+tmp[1]
				if check_seq == repeat_rev:
					return 1
				else:
					print ("The deletion sequence %s%s doesn't match GTCAAGGCTATTG"%(seed_rev,check_seq))
			else:
				print ("The deletion sequence %s doesn't match GTCAAGGCTATTG"%(s))			
		else:
			print ("The deletion sequence %s doesn't match CAATAGCCTTGAC or GTCAAGGCTATTG"%(s))
		
	return 0
	
def row_apply(r):
	return 	find_13nt_deletion(r['Aligned_Sequence'],r['Reference_Sequence'])
	
def parse_file(x):
	df = pd.read_csv(x,sep="\t")
	df['is_correct_deletion'] = df.apply(row_apply,axis=1)
	df = df[df['is_correct_deletion']==1]
	if df.shape[0] == 0:
		return [0,0]
	else:
		return [df['#Reads'].sum(),df['%Reads'].sum()]
	


import os
import os.path
result = []
for dirpath, dirnames, filenames in os.walk("."):
	for filename in [f for f in filenames if "Alleles_frequency_table_around_sgRNA" in f and f.endswith(".txt")]:
		filename = os.path.join(dirpath, filename)
		id = filename.split("/Alleles_frequency_table_around_sgRNA")[0].replace("./","").replace("/","_").replace("CRISPResso_","")
		line = [id]
		line += parse_file(filename)
		result.append(line)

df = pd.DataFrame(result)
df.columns = ['Filename','#Reads','%Reads']
df.to_csv("13nt_deletion_summary.txt",index=False,sep="\t")

