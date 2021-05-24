#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
import csv
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
"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument('-bed',"--chromHMM_bed",  help="chromHMM segments.bed",required=True)
	mainParser.add_argument('-ann',"--annotation_file",  help="chromHMM states annotation ordered",required=True)
	mainParser.add_argument('-o',"--output",  help="chromHMM states ppr tracks",required=True)
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	# given chromHMM segment bed and row_annotation, create a bed file similar to:

	# chr1    13000   13600   {"color":"rgba(254,227,154,0.55)","name":"enhancer","exon":[["13000","13600"]]}
	# chr1    13600   14800   {"color":"rgba(1,114,188,0.67)","name":"quiet (slightly active)","coding":[["13600","14800"]]}
	args = my_args()
	lines = open(args.annotation_file).readlines()
	annot = {}
	for i in range(len(lines)):
		line = lines[i].strip().split("\t")
		annot["E"+str(i+1)] = {}
		annot["E"+str(i+1)]['color'] = '"color":"rgba('+",".join(line[2:5]+["0.8"])+')"'
		annot["E"+str(i+1)]['name'] = '"name":"enhancer"'.replace("enhancer",line[0])
		if "Active" in line[0] or "Strong" in line[0] or "Open" in line[0]:
			annot["E"+str(i+1)]['type'] = 'coding'
		else:
			annot["E"+str(i+1)]['type'] = 'exon'
		

	df = pd.read_csv(args.chromHMM_bed,sep="\t",header=None)

	def row_apply(r):
		state = r[3]
		start = r[1]
		end   = r[2]
		type = '"exon":[["start","end"]]'
		type = type.replace("exon",annot[state]['type'])
		type = type.replace("start",str(start))
		type = type.replace("end",str(end))
		line = '{'+",".join([annot[state]['color'],annot[state]['name'],type])+"}"
		return line

	df[4] = df.apply(row_apply,axis=1)
	print (df[[0,1,2,4]].head())
	df[[0,1,2,4]].to_csv(args.output,sep="\t",index=False,header=False,quoting=csv.QUOTE_NONE)
	os.system("sort -k1,1 -k2,2n {{name}} > {{name}}.sorted;bgzip {{name}}.sorted;tabix -p bed {{name}}.sorted.gz".replace("{{name}}",args.output))
	
	

	args = my_args()
	
	
if __name__ == "__main__":
	main()


























