#!/usr/bin/env python
import sys
def all_motif_features(file1):
	motif_list = []
	with open(file1, 'rb') as handler:
		for line in handler:
			if "MOTIF" in line:
				line = line.strip().split()
				motif_list.append("\t".join(line[1:]))
	return motif_list


pwm_files = [sys.argv[1]]
out_file=sys.argv[2]
for pwm in pwm_files:
	motif_list = all_motif_features(pwm)
	# print motif_list
	f = open(out_file,"wb")
	print >>f,"\n".join(motif_list)
	f.close()