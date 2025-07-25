#!/home/yli11/.conda/envs/captureC/bin/python
from joblib import Parallel, delayed

import sys
import os

def read_file_to_list(x):
	myList = []
	with open(x) as f:
		for line in f:
			line = line.strip()
			if len(line)>1:
				myList.append(line)
	return myList

myList = read_file_to_list(sys.argv[1])
Parallel(n_jobs=20,verbose=10)(delayed(os.system)(m) for m in myList)
# Parallel(n_jobs=5,verbose=10)(delayed(os.system)(m) for m in myList)



