#!/usr/bin/env python
import sys
import glob
import pandas as pd
def parse_log(x):
    with open(x) as f:
        for line in f:
            # print (line)
            if "Finished reads;" in line:
                line = line.split()
                
                total = int(line[3])
                part1 = int(line[5])
                part2 = int(line[7])
                mapped = part1+part2
                rate = float(mapped)/total
                return [mapped,total,rate]
    return [-1,-1,-1]

files = glob.glob("*/*/CRISPResso_RUNNING_LOG.txt")
print (len(files))
# print (files)
# exit()
lines = [parse_log(x) for x in files]
df = pd.DataFrame(lines)
df.index = [x.split("/")[0] for x in files]
df = df.sort_values(2)
df.columns = ['N_align','N_total','mapping_rate']
df.to_csv("mapping_rate.tsv",sep="\t")


