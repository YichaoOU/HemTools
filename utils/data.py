
import getpass
import os
def parse_config(x):
	myDict = {}
	with open(x) as f:
		for line in f:
			line = line.strip()
			if len(line) < 2:
				continue
			if line[0] == "#":
				continue
			line = line.split()
			## make sure it is case-insensitive
			myDict[line[0].lower()] = line[1]
			myDict[line[0]] = line[1]
	return myDict
	
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
username = getpass.getuser()
myData = parse_config(p_dir+"../config/data.config")
myPars = parse_config(p_dir+"../config/parameters.config")
myPipelines = parse_config(p_dir+"../config/pipeline.config")
