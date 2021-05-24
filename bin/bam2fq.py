#!/hpcf/apps/python/install/2.7.13/bin/python
import pandas as pd
import argparse
import os
import uuid

"""

samtools bedtools

only work for pair end


"""

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--bam_file",  help="bam_file",required=True)
	mainParser.add_argument('-b',"--bed_file",  help="bed_file",default="None")
	mainParser.add_argument('-o',"--output",  help="output fastq",default="bam2fq.output")
	mainParser.add_argument("--use_in_silico_PCR_result",  help="use_in_silico_PCR_result",default="None")
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	
	tmp_file = str(uuid.uuid4()).split("-")[-1]
	
	if args.use_in_silico_PCR_result != "None":
		args.bed_file = str(uuid.uuid4()).split("-")[-1]
		df = pd.read_csv(args.use_in_silico_PCR_result,sep="\t")
		print (df)
		df["PositionInSequence"] = df["PositionInSequence"].astype(int)
		df["Length"] = df["Length"].astype(int)
		df['start'] = df["PositionInSequence"]-df["Length"]-100
		df['end'] = df["PositionInSequence"]+df["Length"]+100
		df[['SequenceId','start','end']].to_csv(args.bed_file,sep="\t",index=False,header=False)
	
	filter_bam = "samtools view -b -L %s %s > %s"%(args.bed_file,args.bam_file,tmp_file)
	os.system(filter_bam)
	
	sortbam = "samtools sort -@ 4 -n %s -o %s.qsort"%(tmp_file,tmp_file)
	os.system(filter_bam)
	
	bamtofastq = "bedtools bamtofastq -i %s -fq %s.R1.fastq -fq2 %s.R2.fastq"%(tmp_file,args.output,args.output)
	os.system(bamtofastq)
	
	os.system("rm %s*"%(tmp_file))
	
	os.system("gzip %s.R1.fastq"%(args.output))
	os.system("gzip %s.R2.fastq"%(args.output))
	if args.use_in_silico_PCR_result != "None":
		os.system("rm %s"%(args.bed_file))
	
if __name__ == "__main__":
	main()











