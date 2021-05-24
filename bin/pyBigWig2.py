#!/home/yli11/.conda/envs/py2/bin/python

import sys
import pyBigWig
# print (pyBigWig.__version__)

input = sys.argv[1]
output = sys.argv[2]
chrom_size = sys.argv[3]
# print (output)

# print (dir(pyBigWig))
bw = pyBigWig.open(output, "w")

myList = []

with open(chrom_size) as f:
	for line in f:
		line = line.strip().split()
		if len(line) == 0:
			continue
		myList.append((line[0], int(line[1])))
# print (myList)
bw.addHeader(myList)
chr_list = []
with open(input) as f:
	for line in f:
		line = line.strip().split()
		try:
			bw.addEntries([line[0]], [int(line[1])], ends=[int(line[2])], values=[float(line[3])])
			if not line[0] in chr_list:
				chr_list.append(line[0])
				print (line[0])
		except:
			
			print ("Error adding this line:",line)
			exit()
bw.close()

