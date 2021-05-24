#!/usr/bin/env python


import sys



lines =[]

capture = ["gene_id","transcript_id","gene_name",'gene_type']

with open(sys.argv[1]) as f:
    for line in f:
        flag = True
        for c in capture:
            if not c in line:
                flag = False
        if flag:
            line = line.strip().split()
            gene_id = None
            transcript_id = None
            gene_name = None
            gene_type = None
            for i in range(len(line)):
                if line[i] == "gene_id":
                    gene_id = line[i+1][:-1].replace('"', '')
                
                if line[i] == "transcript_id":
                    transcript_id = line[i+1][:-1].replace('"', '')
                
                if line[i] == "gene_name":
                    gene_name = line[i+1][:-1].replace('"', '')
                
                if line[i] == "gene_type":
                    gene_type = line[i+1][:-1].replace('"', '')
            lines.append([gene_id,transcript_id,gene_name,gene_type])




import pandas as pd
df = pd.DataFrame(lines)
df.columns = capture
df[0] = df[capture[0]]+df[capture[1]]+df[capture[2]]+df[capture[3]]
df = df.drop_duplicates(0)
df = df.drop([0],axis=1)
df.to_csv("%s.names.list"%(sys.argv[1]),index=False)



