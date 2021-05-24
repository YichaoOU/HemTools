#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


"""
Every python wrapper is supposed to be similar, since they are using the same convention.

The only thing need to be changed is the guess_input function and the argparser function.

look for ## CHANGE THE FUNCTION HERE FOR DIFFERENT WRAPPER

variable inherents from utils:
myData
myPars
myPipelines

TODO, overwrite genome index
"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)


	
	mainParser.add_argument('-o',"--output",  help="output file for liftover",default="liftover.bed")
	mainParser.add_argument('-p',"--match_percent",  help="minMatch for liftover",default=0.95)

	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument("--bed",  help="input bed file")		
	group.add_argument("--bw",  help="Input bw file")
	group.add_argument("--bedpe",  help="Input bedpe file, 7 columns")


	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="Target genome version: hg19, mm10, mm9, hg38, or custom", default='mm9',type=str)
	genome.add_argument('-s','--chrom_size',  help="chrome size", default=None)
	genome.add_argument('-c','--chain_file',  help="genome version: hg19, mm10, mm9, hg38", default=None,type=str)

	

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	if args.genome != "custom":
		try:
			args.chain_file = myData[args.genome]
			args.chrom_size = myData['%s_all_chrom_size'%(args.genome.split("_")[0])]
		except:
			args.chain_file = myData['%s_liftover'%(args.genome)]
			args.chrom_size = myData['%s_all_chrom_size'%(args.genome)]
	if "custom" in args.genome:
		try:
			args.chrom_size = myData[args.chrom_size]
		except:
			print ("Using user provided chrom size %s"%(args.chrom_size))

		
	
		
	print ("Using the following chain file")
	print (args.chain_file)
	args.output = args.output.replace(".bed","").replace(".bw","")
	if args.bed:
		temp_output1 = str(uuid.uuid4()).split("-")[-1]
		temp_output2 = str(uuid.uuid4()).split("-")[-1]
		## extract first 3 column
		command = """dos2unix %s;awk NF %s|awk  -F "\t" '{print $1"\t"$2"\t"$3"\t"$1":"$2"-"$3}' > %s"""%(args.bed,args.bed,temp_output1)
		os.system(command)
		# command = "module load ucsc/041619;liftOver %s %s %s.bed unMapped"%(args.bed,args.chain_file,args.output)
		command = "module load ucsc/041619;liftOver -minMatch=%s %s %s %s.bed unMapped"%(args.match_percent,temp_output1,args.chain_file,temp_output2)
	if args.bedpe:
		temp_output1 = str(uuid.uuid4()).split("-")[-1]
		temp_output2 = str(uuid.uuid4()).split("-")[-1]
		## extract first 3 column
		command = """awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$1":"$2"-"$3}' %s > %s.part1"""%(args.bedpe,temp_output1)
		os.system(command)
		command = """awk -F "\t" '{print $4"\t"$5"\t"$6"\t"$4":"$5"-"$6}' %s > %s.part2"""%(args.bedpe,temp_output1)
		os.system(command)
		# command = "module load ucsc/041619;liftOver %s %s %s.bed unMapped"%(args.bed,args.chain_file,args.output)
		command = "module load ucsc/041619;liftOver -minMatch={0} {1}.part1 {2} {3}.bed1 unMapped;liftOver -minMatch={0} {1}.part2 {2} {3}.bed2 unMapped".format(args.match_percent,temp_output1,args.chain_file,temp_output2)
	if args.bw:
		command = "module load ucsc/041619;bigWigToBedGraph %s {{output_bdg}};liftOver -minMatch=%s {{output_bdg}} %s {{output_bdg_liftover}} unMapped;module load conda3;source activate /home/yli11/.conda/envs/py2;sort -k1,1 -k2,2n {{output_bdg_liftover}} > {{output_bdg_liftover}}.sorted;pybigwig.py {{output_bdg_liftover}}.sorted %s.bw %s;rm {{output_bdg}}*;rm {{output_bdg_liftover}}*"%(args.bw,args.match_percent,args.chain_file,args.output,args.chrom_size)
		tmp1 = str(uuid.uuid4()).split("-")[-1]
		tmp2 = str(uuid.uuid4()).split("-")[-1]
		command = command.replace("{{output_bdg}}",tmp1)
		command = command.replace("{{output_bdg_liftover}}",tmp2)
		
	print ("The command is: %s"%(command))
	os.system(command)
	if args.bedpe:
		df1 = pd.read_csv("%s.bed1"%(temp_output2),sep="\t",header=None)
		df1 = df1.drop_duplicates(3)
		df1.index = df1[3].tolist()
		df2 = pd.read_csv("%s.bed2"%(temp_output2),sep="\t",header=None)
		df2 = df2.drop_duplicates(3)
		df2.index = df2[3].tolist()
		df = pd.read_csv(args.bedpe,sep="\t",header=None)
		df["p1"] = df[0]+":"+df[1].astype(str)+"-"+df[2].astype(str)
		df["p2"] = df[3]+":"+df[4].astype(str)+"-"+df[5].astype(str)
		df.index = df['p1'].tolist()
		df[['chr1','start1','end1']] = df1.loc[df.index.tolist()][[0,1,2]]
		df.index = df['p2'].tolist()
		df[['chr2','start2','end2']] = df2.loc[df.index.tolist()][[0,1,2]]
		df[['chr1','start1','end1','chr2','start2','end2',6]].to_csv(args.output+".bed",index=False,header=False,sep="\t")
		print (df.sample(n=5))
		command = "module load htslib;bgzip %s.bed;tabix -p bed %s.bed.gz"%(args.output,args.output)
		os.system(command)
		
	if args.bed:
		os.system("rm %s"%(temp_output1))
		df2 = pd.read_csv(temp_output2+".bed",sep="\t",header=None)
		# df2 = pd.read_csv("ce798991c2bc.bed",sep="\t",header=None)
		df = pd.read_csv(args.bed,sep="\t",header=None)
		# print (df.head())
		# print (df2.head())
		df.index = df[0]+":"+df[1].astype(str)+"-"+df[2].astype(str)
		df2.index = df2[3].tolist()
		df2 = df2.drop([3],axis=1)
		df2.index = df2.index + df2.groupby(level=0).cumcount().astype(str)
		df.index = df.index + df.groupby(level=0).cumcount().astype(str)
		for c in df.columns[3:]:
			# print (c)
			df2[c] = df.loc[df2.index.tolist()][c].tolist()
		mapped = float(df2.shape[0])
		total = float(df.shape[0])
		print ("%s mapped, %s total, %s successfully converted"%(mapped,total,mapped/total))
		
		df2.to_csv(args.output+".bed",index=False,header=False,sep="\t")
		os.system("rm %s.bed"%(temp_output2))

	
if __name__ == "__main__":
	main()



































