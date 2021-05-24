#!/home/yli11/.conda/envs/crispresso2_env/bin/python

from joblib import Parallel, delayed
import matplotlib
import pandas as pd
matplotlib.use('agg')
import os
import glob
import argparse
import seaborn as sns
import gzip
import yaml
import numpy as np
from distance import hamming as hm
import matplotlib.pyplot as plt
def get_parameters(config):

	# return dict
	parameters = {}
	# default parameters
	pre_defined_list = {}

	pre_defined_list["min_read_count"] = 5 
	pre_defined_list["min_aligned"] = 2500 
	for p in pre_defined_list:
		parameters[p] = pre_defined_list[p]
	try:
		# print (config)
		with open(config, 'r') as f:
			manifest_data = yaml.load(f,Loader=yaml.FullLoader)
			# print (manifest_data)
			for p in manifest_data:
				parameters[p] = manifest_data[p]
	except Exception as e:
		print (e)
		print ("Config data is not provided or not parsed successfully, Default parameters were used.")
		

	return parameters

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-m','--manifest',  help="A YAML file specifying inputs and parameters",required=True)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def call_crisprEsso(file_list,ref,gRNA):

	command = "CRISPResso --fastq_output -r1 {fastq_file} --amplicon_seq {ref} --guide_seq {gRNA} --quantification_window_size 3 --quantification_window_center -3 --base_editor_output -o {output}_2 --keep_intermediate --dump --write_detailed_allele_table --plot_window_size 60 --max_rows_alleles_around_cut_to_plot 200 --min_frequency_alleles_around_cut_to_plot 0.001 >/dev/null 2>&1"
	# command = "CRISPResso --fastq_output -r1 {fastq_file} --amplicon_seq {ref} --guide_seq {gRNA} --quantification_window_size 3 --quantification_window_center -3 --base_editor_output -o {output} --keep_intermediate --dump --write_detailed_allele_table --plot_window_size 60 --max_rows_alleles_around_cut_to_plot 200 --min_frequency_alleles_around_cut_to_plot 0.001 "

	command_list = []
	for f in file_list:
		label = f.split("/")[-1].split("_R1")[0].split("_merge")[0]
		current = command.replace("{ref}",ref)
		current = current.replace("{gRNA}",gRNA)
		current = current.replace("{fastq_file}",f)
		current = current.replace("{output}",label+"_crisprEsso_output")
		command_list.append(current)
		# print current

	my_results = Parallel(n_jobs=-1,verbose=10)(delayed(os.system)(c) for c in command_list)



def find_PAM(ref,pam_seq):
	try:
		PAM_index = ref.index(pam_seq)
	except:
		PAM_index = -1
	return PAM_index
	
def find_barcode(ref,barcode_seq):
	try:
		barcode_index = ref.index(barcode_seq)
	except:
		barcode_index = -1
	return barcode_index

def get_PAM_barcode(df,pam_seq,barcode_seq):
	df["PAM_pos"] = df[0].apply(lambda x:find_PAM(x,pam_seq))
	df["Barcode_pos"] = df[0].apply(lambda x:find_barcode(x,barcode_seq))
	df = df[df["PAM_pos"]!=-1]
	df = df[df["Barcode_pos"]!=-1]
	vfunc = np.vectorize(get_PAM_seq)
	df["PAM_seq"] = vfunc(df[1],df["PAM_pos"],pam_seq)
	vfunc = np.vectorize(get_barcode_seq)
	df["Barcode_seq"] = vfunc(df[1],df["Barcode_pos"],barcode_seq)
	return df

def get_PAM_seq(seq,pos,pam_seq):
	if pos == -1:
		return ""
	return seq[pos:pos+len(pam_seq)]
	
def get_barcode_seq(seq,pos,barcode_seq):
	return seq[pos:pos+len(barcode_seq)]

def get_barcode_dict(df,cutoff):
	df4 = df.groupby(["Barcode_seq","PAM_seq"]).size().sort_values(ascending=False)
	df4 = df4.reset_index()
	print ("Number of unique barcode before filter: %s"%(df4.Barcode_seq.nunique()))
	df4 = df4[df4[0]>=cutoff]
	print ("Number of unique barcode after filter: %s"%(df4.Barcode_seq.nunique()))
	df4 = df4.drop_duplicates("Barcode_seq")
	return df4

def get_editing_freq(t,barcode_dict,barcode_seq,pam_seq):
	"""return edit df"""
	label,file = get_Esso_file(t)
	df = calculate_cutting_freq_from_fq(file,barcode_dict,barcode_seq,pam_seq)
	# label = t.split("/")[0].split("_S")[0]
	df['PAM'] = [x[1:3] for x in df.PAM_seq]
	print ("Saving PAM count table for :",label)
	df.to_csv("%s.PAM_count.csv"%(label),index=False)
	total_align = df.shape[0]
	print ("Reads with PAM assigned:")
	print (df.groupby(2).size())
	
	df2 = pd.DataFrame(df.groupby([2,"PAM"]).size())
	# print ("TOTAL mapped"df.groupby(2).sum())
	try:
		edit = df2.loc["Reference_MODIFIED"]/(df2.loc["Reference_MODIFIED"]+df2.loc["Reference_UNMODIFIED"])
	except Exception as e:
		print ("Error:", e)
		print ("replace with zero")
		edit = df2.loc["Reference_UNMODIFIED"]*0
		
	edit.columns = [label]
	edit.index = edit.index.tolist()
	return edit,total_align

def get_dict_from_fq(fn,barcode_seq,pam_seq): 
	n = 4
	out = []
	total_count = 0
	fail_count = 0
	with gzip.open(fn, 'r') as fh:
		lines = []
		for line in fh:
			lines.append(line.rstrip())
			if len(lines) == n:
				total_count+=1
				tmp = lines[2].decode("utf-8").split()

				if tmp[1] == "ALN=NA":
					fail_count += 1
				else:
#					 print (tmp)
					ref = tmp[7].split("=")[-1]
					alt = tmp[8].split("=")[-1]
					out.append([ref,alt])
				lines = []
	out = pd.DataFrame(out)
	contain_deletion = out.shape[0]
	out = get_PAM_barcode(out,pam_seq,barcode_seq)
	out = out[~out.PAM_seq.str.contains("-")]
	out = out[~out.Barcode_seq.str.contains("-")]
	contain_deletion = contain_deletion - out.shape[0]
	fail_count+=contain_deletion
	print ("Fail due to low alignment score %s"%(fail_count/float(total_count)))
	return out

def assign_PAM(q,barcode_dict):
	if q in barcode_dict:
		return barcode_dict[q]
	for b in barcode_dict:
		if hm(q,b)<=1:
			return barcode_dict[b] 
	return ""
def calculate_cutting_freq_from_fq(fn,barcode_dict,barcode_seq,pam_seq): 
	n = 4
	out = []
	total_count = 0
	fail_count = 0
	with gzip.open(fn, 'r') as fh:
		lines = []
		for line in fh:
			lines.append(line.rstrip())
			if len(lines) == n:
				total_count+=1
				tmp = lines[2].decode("utf-8").split()
				# try:
					# tmp[1] == "ALN=NA"
				# except:
					# print lines
					# print tmp
				if tmp[1] == "ALN=NA":
					fail_count += 1
				else:
#					 print (tmp)
					ref = tmp[7].split("=")[-1]
					alt = tmp[8].split("=")[-1]
					status = tmp[2].split("=")[-1]
					out.append([ref,alt,status])
				lines = []
	df = pd.DataFrame(out)
	print (df.groupby(2).size())
	Total_M = df[df[2]=="Reference_MODIFIED"].shape[0]
	Total_U = df[df[2]=="Reference_UNMODIFIED"].shape[0]
	df["PAM_pos"] = df[0].apply(lambda x:find_PAM(x,pam_seq))
	df["Barcode_pos"] = df[0].apply(lambda x:find_barcode(x,barcode_seq))
	barcode_fail = df[df.Barcode_pos==-1].shape[0]

	df = df[df["Barcode_pos"]!=-1]
	vfunc = np.vectorize(get_barcode_seq)
	df["Barcode_seq"] = vfunc(df[1],df["Barcode_pos"],barcode_seq)

	fail_count+=barcode_fail
	print ("Alignment Fail %s"%(fail_count/float(total_count)))

	df['PAM_seq'] = df['Barcode_seq'].map(barcode_dict) # barcode pam
	
	df = df.fillna("")

	vfunc = np.vectorize(get_PAM_seq)
	df["PAM_seq2"] = vfunc(df[1],df["PAM_pos"],pam_seq) # actual pam

	final_pam_list = Parallel(n_jobs=-1,verbose=0,prefer="threads")(delayed(parallel_pam_finding)(i,j,x,barcode_dict) for i,j,x in df[['PAM_seq','PAM_seq2','Barcode_seq']].values)
	# print (df.head())
	# for i,j,x in df[['PAM_seq','PAM_seq2','Barcode_seq']].values:
	# parallel_pam_finding
	df.PAM_seq = final_pam_list
	df = df[df.PAM_seq!=""]
	try:
		Total_M1 = df[df[2]=="Reference_MODIFIED"].shape[0]
		Total_U1 = df[df[2]=="Reference_UNMODIFIED"].shape[0]
	
		print ("PAM assignment success rate in Modified %s"%(Total_M1/float(Total_M)))
		print ("PAM assignment success rate in Un-modified %s"%(Total_U1/float(Total_U)))
	except Exception as e:
		print (e)
	return df

def parallel_pam_finding(i,j,x,barcode_dict):
	if i=="":
		if j == "":
			return assign_PAM(x,barcode_dict)
		elif "-" in j or "N" in j:
			return assign_PAM(x,barcode_dict)
		else:
			return j
	elif "-" in i:
		if j == "":
			return ""
		elif "-" in j or "N" in j:
			return ""
		else:
			return j	
	else:
		if j == "":
			return i
		elif "-" in j or "N" in j:
			return i
		else:
			return j	 
def get_Esso_file(x):
	label = x.split("/")[-1].split("_R1")[0].split("_merge")[0].split(".extendedFrags")[0]
	return label,glob.glob("%s*/*/CRISPResso_output.fastq.gz"%(label))[0]

## main function ##
def main():

	args = my_args()
	config = get_parameters(args.manifest)
	# print (config)
	file_list = glob.glob("*.fastq.gz")+glob.glob("*.fq.gz")+glob.glob("*.fastq")+glob.glob("*.fq")
	# run crisprEsso
	call_crisprEsso(file_list,config['amplicon_seq'],config['gRNA_seq'])
	

	# calculate barcode
	# output barcode raw
	#input
	label1,file1 = get_Esso_file(config['input'])
	print ("Generating barcode dictionary for %s"%(label1))
	out1 = get_dict_from_fq(file1,config['barcode_seq'],config['PAM_seq'])
	print ("Saving raw barcode/PAM count to %s.raw_barcode_PAM.count.csv"%(label1))
	out1.to_csv("%s.raw_barcode_PAM.count.csv"%(label1),index=False)
	barcode_dict1 = get_barcode_dict(out1,config['min_read_count'])
	barcode_dict1 = barcode_dict1.set_index("Barcode_seq")
	print ("Saving filtered barcode/PAM assignment to %s.barcode_PAM.filter.csv"%(label1))
	barcode_dict1.to_csv("%s.barcode_PAM.filter.csv"%(label1))
	barcode_dict1 = barcode_dict1.PAM_seq.to_dict()
	
	
	# rep1
	label1,file1 = get_Esso_file(config['control_rep1'])
	print ("Generating barcode dictionary for %s"%(label1))
	out1 = get_dict_from_fq(file1,config['barcode_seq'],config['PAM_seq'])
	print ("Saving raw barcode/PAM count to %s.raw_barcode_PAM.count.csv"%(label1))
	out1.to_csv("%s.raw_barcode_PAM.count.csv"%(label1),index=False)
	barcode_dict1 = get_barcode_dict(out1,config['min_read_count'])
	barcode_dict1 = barcode_dict1.set_index("Barcode_seq")
	print ("Saving filtered barcode/PAM assignment to %s.barcode_PAM.filter.csv"%(label1))
	barcode_dict1.to_csv("%s.barcode_PAM.filter.csv"%(label1))
	barcode_dict1 = barcode_dict1.PAM_seq.to_dict()

	# rep2
	label2,file2 = get_Esso_file(config['control_rep2'])
	print ("Generating barcode dictionary for %s"%(label2))
	out2 = get_dict_from_fq(file2,config['barcode_seq'],config['PAM_seq'])
	print ("Saving raw barcode/PAM count to %s.raw_barcode_PAM.count.csv"%(label2))
	out2.to_csv("%s.raw_barcode_PAM.count.csv"%(label2),index=False)
	barcode_dict2 = get_barcode_dict(out2,config['min_read_count'])
	barcode_dict2 = barcode_dict2.set_index("Barcode_seq")
	print ("Saving filtered barcode/PAM assignment to %s.barcode_PAM.filter.csv"%(label2))
	barcode_dict2.to_csv("%s.barcode_PAM.filter.csv"%(label2))
	barcode_dict2 = barcode_dict2.PAM_seq.to_dict()
	

	# calculate cutting efficiency
	# df_list1 = [get_editing_freq(t,barcode_dict1,config['barcode_seq'],config['PAM_seq']) for t in [config['cas9_rep1'],config['cas9sso7d_rep1']]]
	# df_list2 = [get_editing_freq(t,barcode_dict2,config['barcode_seq'],config['PAM_seq']) for t in [config['cas9_rep2'],config['cas9sso7d_rep2']]]
	rep1_list = []
	rep2_list = []
	rename_names = {}
	for k in config:
		if "rep1" in k:
			rep1_list.append(config[k])
			rename_names[get_Esso_file(config[k])] = k
		if "rep2" in k:
			rep2_list.append(config[k])
			rename_names[get_Esso_file(config[k])] = k
	df_list1 = [get_editing_freq(t,barcode_dict1,config['barcode_seq'],config['PAM_seq']) for t in rep1_list]
	df_list2 = [get_editing_freq(t,barcode_dict2,config['barcode_seq'],config['PAM_seq']) for t in rep2_list]
	
	
	filter_df_list = []
	for i,j in df_list1:
		# print (i,j)
		if j >= config['min_aligned']:
			filter_df_list.append(i)
	for i,j in df_list2:
		if j >= config['min_aligned']:
			filter_df_list.append(i)
	df = pd.concat(filter_df_list,axis=1)
	print ("saving editing frequency table to edit.freq.csv")
	df = df.fillna(0)
	df = df.sort_index()
	try:
		df.columns = [rename_names[x] for x in df.columns]
	except Exception as e:
		print ("failed to replace names")
		print (e)
	df.to_csv("edit.freq.csv")
	
	## generate figure
	g=sns.clustermap(df,annot=True,figsize=(df.shape[0],10),row_cluster=False,cmap="RdBu_r",linewidth=0.2,fmt=".2f")
	plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
	plt.setp(g.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
	plt.savefig("%s.pdf"%("cutting_freq_heatmap"),bbox_inches='tight')
	










if __name__ == "__main__":
	main()


