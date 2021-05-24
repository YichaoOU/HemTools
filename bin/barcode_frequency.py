#!/usr/bin/env python

import sys, gzip
import pandas as pd
b1 = []
b2 = []
read = []

with gzip.open(sys.argv[1]) as fastq:
	for line in fastq:
		if not line.startswith(b'@'): continue
		line = line.strip()
		bc = line.decode("utf-8").split(':')[-1]
		name = line.split()[0]
		# print (bc)
		try:
			bc1,bc2 = bc.split("+")
		except Exception as e:
			tmp = line.split()
			if len(tmp)>1:
				print (e)
				print (bc)
				print (line)
				exit()
		b1.append(bc1)
		b2.append(bc2)
		read.append(name)

df = pd.DataFrame()
df['read'] = read
df['bc1'] = b1
df['bc2'] = b2
print (df.bc1.nunique())
df.to_csv("Barcode_raw_table.csv",index=False)
df = pd.DataFrame(df.groupby(['bc1','bc2']).size())
df[1] = df[0]/df[0].sum()
df = df.sort_values(1,ascending=False)
df.to_csv("Barcode_count_table.csv",index=True)

