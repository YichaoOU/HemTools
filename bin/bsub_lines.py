#!/usr/bin/env python

import sys
import os
import argparse


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output", help="output file", default="my_table.json")

	mainParser.add_argument('-f',"--input",  help="lines of commands")
	mainParser.add_argument('-q',"--queue",  help="submit queue",default="standard")
	mainParser.add_argument('-l',"--label",  help="label",default="USR")
	mainParser.add_argument('-n',"--ncore",  help="number of cores",default=1,type=int)
	mainParser.add_argument('-m',"--mem",  help="memory MB",default=4000,type=int)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	count = 1
	for line in open(args.input).readlines():
		line = line.strip()
		command = f'bsub -R "rusage[mem={args.mem}] span[hosts=1]" -n {args.ncore} -P {args.label} -J {args.label} -q {args.queue} -oo {args.label}.{count}.log -eo {args.label}.{count}.err {line}'
		print (command)
		count += 1


if __name__ == "__main__":
	main()


















