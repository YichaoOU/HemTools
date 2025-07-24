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
	mainParser.add_argument('-f',"--input_tsv",  help="tsv file", required=True)
	mainParser.add_argument('-d',"--dir",  help="genome browser HPC dir", required=True)
	mainParser.add_argument("--name",  help="your track name", required=True)
	mainParser.add_argument("--copy",  help="copy data", action='store_true')
	# mainParser.add_argument("--output",  help="your track name", required=True)
	
	# mainParser.add_argument('--interactive',  help="run pipeline interatively", action='store_true')

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def get_unique_sample_name(r,sample_name_list):
	r['file_path'] = r['file_path'].replace(" ","")
	if sample_name_list.count(r['sample'])>1:
		r['sample'] = r['sample']+"_"+r['assay']+"_"+r['level1']+"_"+r['level2']
	return r

def main():

	args = my_args()
	df = pd.read_csv(args.input_tsv,sep="\t")
	df = df.apply(lambda r:get_unique_sample_name(r,df['sample'].tolist()),axis=1)
	out = []
	for i,r in df.iterrows():
		# dir=/home/yli11/dirs/genome_browser/yli11/PRPF19/track_collections
		# copy data
		if args.copy:
			command = f"cp {r['file_path']}* {args.dir}/"
			print (command)
			os.system(command)
			r['file_path'] = str(args.dir).split("genome_browser/")[-1]+"/"+r['file_path'].split("/")[-1]
		# determine type
		ext = r['file_path'].split(".")[-1]
		if  ext=="bw":
			out.append(bw(r))
		elif ext=="hic":
			out.append(hic(r))
		else:
			if "HIC" == str(r['assay']).upper():
				out.append(interaction_matrix(r))
			elif "HICHIP" == str(r['assay']).upper():
				out.append(interaction_arc(r))
			else:
				out.append(bed(r))
	myDict={}
	myDict['track_name']=args.name
	out = [x.replace("'",'"') for x in out]
	myDict['myTracks']= ",\n".join(out)
	output = """
	[
	{
		"isfacet": true,
		"name": "{{track_name}}",
		"tracks": [
		{{myTracks}}
	]
	}
	]
	"""
	
	output = multireplace(output,myDict)
	outFile = f"{args.dir}/{args.name}.json"
	write_file(outFile,output)
	print (f"tracks written to {outFile}")
if __name__ == "__main__":
	main()







