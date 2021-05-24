#!/home/yli11/.conda/envs/py2/bin/python
from joblib import Parallel, delayed

import os
import sys
import uuid
import argparse




def my_args():
	
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="bw operations")
	mainParser.add_argument('-b1',help="bigwiggle file 1",required=True)	
	mainParser.add_argument('-b2',help="bigwiggle file 2",required=True)	
	mainParser.add_argument('-o',help="output name",required=True)	
	mainParser.add_argument('-op',help="operation: log2,ratio,subtract,add,mean,reciprocal_ratio,first,second, diff_mean_log2",default="diff_mean_log2")	
	mainParser.add_argument('-pc',help="pseudocount",default=1,type=float)	
	mainParser.add_argument('-bs',help="bin size",default=10,type=int)	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	if args.op != "diff_mean_log2":
		command = f"bigwigCompare -b1 {args.b1} -b2 {args.b2} --operation {args.op} --pseudocount {args.pc} -bs {args.bs} -p 8 -o {args.o}"
		print (command)
		os.system(command)
	else:
		diff_out = addon_string+".diff"
		mean_out = addon_string+".mean"
		command1 = f"bigwigCompare -b1 {args.b1} -b2 {args.b2} --operation subtract -bs {args.bs} -p 8 -o {diff_out}"
		command2 = f"bigwigCompare -b1 {args.b1} -b2 {args.b2} --operation mean -bs {args.bs} -p 8 -o {mean_out}"
		Parallel(n_jobs=2,verbose=10)(delayed(os.system)(m) for m in [command1,command2])
		command3 = f"bigwigCompare -b1 {diff_out} -b2 {mean_out} --operation log2 --pseudocount {args.pc} -bs {args.bs} -p 8 -o {args.o}"
		# command3 = f"bigwigCompare -b1 {diff_out} -b2 {args.b2} --operation log2 --pseudocount {args.pc} -bs {args.bs} -p 8 -o {args.o}"
		os.system(command3)



if __name__ == "__main__":
	main()







