#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


"""
Given motif.pwm and a user-bed file, perform motif scanning and generate bed file (bedjs) for each motif


"""

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--input",  help="a list of consensus sequence",required=True)
	mainParser.add_argument('-o',"--output", default="consensus.meme",help="output file name")
	


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

	
def to_meme(kmer_list):

	header="""
MEME version 4.4
ALPHABET= ACGT
strands: + -
Background letter frequencies (from web form):
A 0.25000 C 0.25000 G 0.25000 T 0.25000
	
	"""
	
	motif = """
MOTIF {{motif_id}}

letter-probability matrix: alength= 4 w= {{motif_width}} nsites= 1 E= 0	
{{motif_matrix}}
	"""
	
	motif_pwm = []
	for k in kmer_list:
		tmp = motif.replace("{{motif_id}}",k)
		tmp = tmp.replace("{{motif_width}}",str(len(k)))
		tmp = tmp.replace("{{motif_matrix}}",kmer_to_matrix(k))
		motif_pwm.append(tmp)
	return header+"\n".join(motif_pwm)
	
def kmer_to_matrix(s):
	myDict = {}
	myDict["A"]=[1,0,0,0]
	myDict["C"]=[0,1,0,0]
	myDict["G"]=[0,0,1,0]
	myDict["T"]=[0,0,0,1]
	output = []
	for i in s:
		output.append("\t".join([str(x) for x in myDict[i]]))
	return "\n".join(output)
	
def main():

	args = my_args()
	
	write_file(args.output,to_meme(read_file_to_list(args.input)))
		
if __name__ == "__main__":
	main()




