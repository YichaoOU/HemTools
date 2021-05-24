#!/hpcf/apps/python/install/2.7.13/bin/python

import sys
import os
import uuid
import glob

tmp = str(uuid.uuid4()).split("-")[-1]

bam=sys.argv[1]
peak=sys.argv[2]
label=sys.argv[3]
bam = glob.glob("%s"%(bam))[0]
print (bam)
print (peak)
# sort -k1,1 -k2,2n {peak} > {tmp}.bed

bed2saf = """

module load bedtools

tail -n +2 {peak} | sort -k1,1 -k2,2n  |   cut -f 1,2,3,4 - > {tmp}.bed

bedtools merge -c 4 -o collapse -i {tmp}.bed > {tmp}.bedtools.bed

awk 'BEGIN{FS=OFS="\t"; print "GeneID\tChr\tStart\tEnd\tStrand"}{print $4, $1, $2+1, $3, "."}' {tmp}.bedtools.bed > {tmp}.saf

""".replace("{peak}",peak).replace("{tmp}",tmp)


os.system(bed2saf)

feature_count = """

module load subread

featureCounts -p -T 4 -a {0}.saf -F SAF -o {0}.out {1} > /dev/null 2>&1


""".format(tmp,bam)
os.system(feature_count)
import pandas as pd
df = pd.read_csv("%s.out.summary"%(tmp),sep="\t",index_col=0)
df = df.loc['Assigned']/df[df.columns[0]].sum()
df = pd.DataFrame(df)
df = df.reset_index()
df.columns = ['Name','FRIP_%s'%(label)]
print (df)
os.system("rm %s*"%(tmp))
out = "%s.FRiP.tsv"%(bam)
f = open(out,'wb')
header="""
# description: 'The fraction of reads in called peak regions'
# plot_type: 'table'
# section_name: 'FRIP'
"""
f.write(header.encode())
f.close()
f = open(out,'a')

df.to_csv(f,header=True,index=False,sep="\t")

# df.to_csv(,sep="\t")
