#!/hpcf/apps/python/install/2.7.13/bin/python
import pandas as pd
import argparse
import numpy as np
import os
"""

Minimal example of vcf for protein paint

##fileformat=VCFv4.2
##INFO=<ID=numTFBS,Number=1,Type=Integer,Description="sum of gain or loss TFBSs">
##INFO=<ID=isGATA1,Number=1,Type=Integer,Description="is GATA1, 1 or 0">
##INFO=<ID=isTAL1,Number=1,Type=Integer,Description="is TAL1, 1 or 0">
##INFO=<ID=isBCL11A,Number=1,Type=Integer,Description="is BCL11A, 1 or 0">
##INFO=<ID=isKLF1,Number=1,Type=Integer,Description="is KLF1, 1 or 0">
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT
chr11   4167378 chr11.4167378   A       G       100.0   PASS    numTFBS=26;isBCL11A=0;isKLF1=0;isGATA1=0;isTAL1=1       .
chr11   4167381 chr11.4167381   A       G       100.0   PASS    numTFBS=26;isBCL11A=0;isKLF1=0;isGATA1=0;isTAL1=1       .

"""

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument('-f',"--tsv",  help="input tsv file", required=True)
	mainParser.add_argument("--required_cols",  help="input the chr, pos, ID, ref, alt col names in order", required=True)
	mainParser.add_argument("--info_cols",  help="input col names (please make sure no spaces in the col names) to be put in the info column", required=True)
	mainParser.add_argument("--info_types",  help="input col types for the info columns, should match info cols in order. choose from Integer, Float, String", required=True)
	mainParser.add_argument('-o',"--output",  help="output file name", default="bed2vcf.vcf")
	mainParser.add_argument("--column_number",  help="if no header, then columns will be named as numbers, start from 0", default=None)
	mainParser.add_argument('--add_chr',  help="add string chr to the chrom column", action='store_true')
	mainParser.add_argument("--remove_cols",  help="remove columns not used in the vcf file", default=None)
	mainParser.add_argument("--log10_cols",  help="convert a col to -np.log10", default=None)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def get_info_def(x,t):
	# print (x,t)
	return '##INFO=<ID={0},Number=.,Type={1},Description="{0}">\n'.format(x,t)

def populate_info_col(r,names,types):
	out = []
	for i in range(len(names)):
		n = names[i]
		t = types[i]
		# print (r,n,t,r[n])
		# if t != "String"
		content = r[n]
		if t == "String":
			# print (r,n,t,r[n])
			content = str(content).replace(";",",")
		out.append("%s=%s"%(n,content))
	return ";".join(out)
	

def main():

	
	args = my_args()

	vcf_header="##fileformat=VCFv4.2\n"
	
	info_cols = args.info_cols.split(",")

		
	info_types = args.info_types.split(",")
	info_def_list = []
	for i in range(len(info_cols)):
		info_def_list.append(get_info_def(info_cols[i],info_types[i]))
	vcf_col_names = "#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT\n"
	vcf_header += "".join(info_def_list) + vcf_col_names
	if args.column_number !=None:
		df = pd.read_csv(args.tsv,sep="\t",header=None)
	else:
		df = pd.read_csv(args.tsv,sep="\t")
	df = df.fillna(0)
	if args.remove_cols != None:
		if args.column_number !=None:
			for x in args.remove_cols.split(","):
				print ("removing ",x)
				df = df.drop([int(x)],axis=1)
		else:
			for x in args.remove_cols.split(","):
				df = df.drop([x],axis=1)
	if args.log10_cols != None:
		if args.column_number !=None:
			for x in args.log10_cols.split(","):
				df[int(x)] = df[int(x)].apply(lambda i:-np.log10(i))
		else:
			for x in args.log10_cols.split(","):
				df[x] = df[x].apply(lambda i:-np.log10(i))

	if args.column_number !=None:
		chr,pos,ID,ref,alt = [int(x) for x in args.required_cols.split(",")]
	else:
		chr,pos,ID,ref,alt = args.required_cols.split(",")
	if args.add_chr:
		df[chr] = "chr"+df[chr].astype(str)
	out = df[[chr,pos,ID,ref,alt]]
	out['QUAL'] = 100.0
	out['FILTER'] = "PASS"
	if args.column_number !=None:
		column_number_list = args.column_number.split(",")
		for i in range(len(column_number_list)):
			c = int(column_number_list[i])
			df[info_cols[i]] = df[c]
	print (df.head())
	print (out.head())
	df['INFO'] = df.apply(lambda x:populate_info_col(x,info_cols,info_types),axis=1)
	out['INFO'] = df['INFO']
	
	
	
	
	
	out['FORMAT'] = "."


	# vcf_file = "%s.vcf"%(jid)
	# os.system("rm %s*"%(args.output))
	f = open(args.output,'wb')
	f.write(vcf_header)
	f.close()
	f = open(args.output,'a')
	out[pos] = out[pos].astype(int)
	out = out.sort_values([chr,pos])
	out.to_csv(f,header=False,index=False,sep="\t")
	f.close()	
	
	command = "module load htslib;bgzip %s ; tabix -p vcf %s.gz"%(args.output,args.output)
	os.system(command)

	
if __name__ == "__main__":
	main()

























