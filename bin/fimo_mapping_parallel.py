#!/usr/bin/env python
from joblib import Parallel, delayed

import sys
import os
import pandas as pd
"""

Given motif meme, output motif_mapping for every motif

meme opsbed

"""
def fimo(command,motif):
	os.system(command.replace("{{motif_id}}",motif))


motif_file = sys.argv[1]
fimo_cutoff = sys.argv[2]
input_fasta = sys.argv[3]

print ("getting motif list")
os.system("pwm_to_list.py %s all.motifs.list"%(motif_file))

motif_list = pd.read_csv("all.motifs.list",header=None)
motif_list = motif_list[0].tolist()

fimo_dir = "FIMO_motif_mapping"
os.system("mkdir %s"%(fimo_dir))

fimo_command = """fimo --verbosity 1 --motif {{motif_id}} --thresh %s --parse-genomic-coord -oc {{FIMO_dir}}/{{motif_id}} %s %s; gff2bed < {{FIMO_dir}}/{{motif_id}}/fimo.gff | awk 'BEGIN {IFS="\t"; OFS="\t";} {print $1,$2,$3,$4,$5,$6}' > {{FIMO_dir}}/{{motif_id}}/fimo.bed"""%(fimo_cutoff,motif_file,input_fasta)
fimo_command = fimo_command.replace("{{FIMO_dir}}",fimo_dir)
Parallel(n_jobs=10,verbose=10)(delayed(fimo)(fimo_command,m) for m in motif_list)



