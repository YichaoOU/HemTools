import sys
cutoff = 10
AF_cutoff = 0.99
myDict = {}
myDict['A']=5
myDict['C']=6
myDict['G']=7
myDict['T']=8
with open(sys.argv[1]) as f:
	for c in f:
		line = c.strip().split()
		count = int(line[3])
		if line[2] == "N":
			continue
		if count <= cutoff:
			continue
		id = "%s-%s-%s"%(line[0],line[1],line[2])
		ref_count = int(line[myDict[line[2]]].split(":")[1])
		if ref_count <= cutoff:
			continue
		if float(ref_count)/count < AF_cutoff:
			continue
		print (c.strip())
		
