#!/home/yli11/.conda/envs/captureC/bin/python


import pandas as pd


from simplesam import Reader, Writer
import simplesam
import sys
file=sys.argv[1]
out=sys.argv[2]
final_talon_read_annot = sys.argv[3]

# file="/research_jude/rgs01_jude/groups/chenggrp/projects/blood_regulome/chenggrp/Sequencing_runs/IsoSeq_256066_RNA/first_second_merged_run/talon_abundance/merged.final_talon_read_annot.tsv"
df = pd.read_csv(final_talon_read_annot,sep="\t",index_col=0)
# df.head()


in_file = open(file, 'r')
in_sam = Reader(in_file)
out_sam = Writer(open(out, 'w'), in_sam.header)
# {"annot_gene_name":df.at[read.qname,"annot_gene_name"],"annot_transcript_name":df.at[read.qname,"annot_transcript_name"]}
# print (df.at["m64304e_220525_180752/6817092/ccs","annot_gene_name"])
for read in in_sam:
    try:
        new_read_name = f"{read.qname}_{df.at[read.qname,'annot_gene_name']}_{df.at[read.qname,'annot_transcript_name']}"
        tmp = simplesam.Sam(
        rname=read.rname,
        qname=new_read_name,
        flag=read.flag,
        pos=read.pos,
        mapq=read.mapq,
        cigar=read.cigar,
        tlen=read.tlen,
        seq=read.seq,
        qual=read.qual
        )
        out_sam.write(tmp)
    except:
        continue
out_sam.close()

