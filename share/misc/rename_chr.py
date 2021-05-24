import sys
input = sys.argv[1]
output = sys.argv[2]

out = open(output,"wb")
with open(input) as f:
	for line in f:
		line = line.strip()
		if ">" in line:
			line = line.split("_")[0]
		print >>out,line
