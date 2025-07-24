#!/usr/bin/env python
## python3
import pandas as pd
import argparse
import os
def interaction_arc(r):
	return f"{{'assay':'{r['assay']}','sample':'{r['sample']}','level1':'{r['level1']}','type':'hicstraw','name':'{r['sample']}','mode_arc':true,'mode_hm':false,'bedfile':'{r['file_path']}','enzyme':'MboI','color':'{r['color']}'}}"
def interaction_matrix(r):
	return f"{{'assay':'{r['assay']}','sample':'{r['sample']}','level1':'{r['level1']}','type':'hicstraw','name':'{r['sample']}','mode_arc':false,'mode_hm':true,'bedfile':'{r['file_path']}','enzyme':'MboI','color':'{r['color']}'}}"
def hic(r):
	return f"{{'assay':'{r['assay']}','sample':'{r['sample']}','level1':'{r['level1']}','type':'hicstraw','name':'{r['sample']}','mode_arc':false,'mode_hm':true,'file':'{r['file_path']}','enzyme':'MboI','color':'{r['color']}'}}"

def bw(r):
	return f"{{'assay':'{r['assay']}','sample':'{r['sample']}','level1':'{r['level1']}','type':'bigwig','scale':{{'auto': 1}},'file': '{r['file_path']}','stackheight':20,'stackspace':1,'onerow':1,'name':'{r['sample']}','pcolor':'{r['color']}'}}"

def bed(r):
	return f"{{'assay':'{r['assay']}','sample':'{r['sample']}','level1':'{r['level1']}','type':'bedj','name':'{r['sample']}','file':'{r['file_path']}','stackheight':10,'stackspace':1}}"


def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		if myDict[k] == None:
			value = ""
		else:
			value = myDict[k]
		myString = str(myString).replace("{{"+str(k)+"}}",str(value))
	return myString

def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="create tracks")
	mainParser.add_argument('-f',"--input",  help="a list of files", required=True)
	mainParser.add_argument('-d',"--dir",  help="genome browser HPC dir", required=True)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def get_unique_sample_name(r,sample_name_list):
	if sample_name_list.count(r['sample'])>1:
		r['sample'] = r['sample']+"_"+r['assay']+"_"+r['level1']
	return r

def main():

	args = my_args()
	df = pd.read_csv(args.input,header=None)
	# df = df.apply(lambda r:get_unique_sample_name(r,df['sample'].tolist()),axis=1)
	out = []
	for i,r in df.iterrows():
		command = f"cp {r[0]}* {args.dir}/"
		os.system(command)
		template={}
		template['file_path'] = str(args.dir).split("genome_browser/")[-1]+"/"+r[0].split("/")[-1]
		ext = r[0].split(".")[-1]
		template['assay'] = "ChIP"
		template['sample'] = r[0].split(".")[0]
		template['level1'] = "level1"
		template['color'] = "red"
		if ext=="bw":
			out.append(bw(template))
		elif ext=="hic":
			out.append(hic(template))
		else:
			if "HIC" == str(template['assay']).upper():
				out.append(interaction_matrix(template))
			elif "HICHIP" == str(template['assay']).upper():
				out.append(interaction_arc(template))
			else:
				out.append(bed(template))
	out = [x.replace("'",'"') for x in out]
	print (",\n".join(out))

if __name__ == "__main__":
	main()







