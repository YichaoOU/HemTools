
# exec(open("/home/yli11/HemTools/bin/motif_pair_direction.py").read())
import pandas as pd
import os

motif_bed = "/home/yli11/Data/Human/hg19/motif_mapping/JASPA_MA0139.1_CTCF.hg19.fimo.bed"

output = "20copy_hg19.CTCF_pairs.tsv"

anchor_motif_direction = "/home/yli11/dirs/20copy_project/captureC/new_data/captureC_analysis/CTCF_direction/anchor.bed"
anchor = pd.read_csv(anchor_motif_direction,sep="\t",header=None)
anchor.index = anchor[0]+"_"+anchor[1].astype(str)+"_"+anchor[2].astype(str)
flip = True
print (anchor)
if flip:
	anchor[4] = anchor[4].map({"-":"+","+":"-","o":"o"})
print (anchor)
peak_file = "/research/rgs01/project_space/chenggrp/blood_regulome/chenggrp/Projects/hgcOPT_insulator/Data/ChIP/chenggrp_201110/chip_seq_pair_qqi_2020-10-01_hg19/peak_files/2036257_Jurkat_20copy_ChIP_CTCF_300_700bp_2_S7.vs.2036259_Jurkat_20copy_input_300_700bp_S9.rmdup.uq.rmchrM_summits.bed"

# chr1	235493349	235493353	GGPS1	-
# chr2	61687564	61687568	USP34	+
# chr3	15118929	15118933	RBSN	-
# chr4	32635317	32635318	PCDH7	o
# chr4	133875585	133875589	PCDH10	+
# type o is specific for 20copy data

interaction_ibed = "/home/yli11/dirs/20copy_project/captureC/new_data/captureC_analysis/20copy_hg19.called_interactions.tsv"
df = pd.read_csv(interaction_ibed,sep="\t")



# for the 20copy project, CTCF is on the reverse strand to the inserted gene


# 1. other end bed
tmp = df[['chr_OE','start_OE','end_OE','OE_name']].sort_values(['chr_OE','start_OE'])
tmp = tmp.drop_duplicates("OE_name")
tmp.to_csv("other_end.bed",sep="\t",header=False,index=False)

# overlap peak
# assign best motif
# best motif is determined as the one closest to peak center

os.system("module load bedtools/2.29.2;bedtools closest -a %s -b %s -t first > peak_motif_assignment.bed"%(peak_file,motif_bed))
# chr1    10124   10125   2036257_Jurkat_20copy_ChIP_CTCF_300_700bp_2_S7.vs.2036259_Jurkat_20copy_input_300_700bp_S9.rmdup.uq.rmchrM_peak_1       24.82383        chr1    10470   10489   JASPA_MA0139.1_CTCF_chr1_10471  9.90164 -

# get nearest peak
os.system("module load bedtools/2.29.2;bedtools closest -a other_end.bed -b peak_motif_assignment.bed -t first -d > other_end_peak_motif_assignment.bed")

annot = pd.read_csv("other_end_peak_motif_assignment.bed",sep="\t",header=None)
annot.index = annot[3].tolist()

# annotate interaction with peak and motif
df['OE_nearest_peak_distance'] = df['OE_name'].map(annot[annot.columns[-1]].to_dict())
df['OE_nearest_peak_name'] = df['OE_name'].map(annot[7].to_dict())
df['OE_motif_direction_in_peak'] = df['OE_name'].map(annot[annot.columns[-2]].to_dict())


# get Bait_motif_direction
df['Bait_motif_direction'] = df['Bait_name'].map(anchor[4].to_dict())

# define motif pair

def row_apply(r):
	# OE position
	OE_bait_distance = r['start_OE'] - r['start_Bait']
	if OE_bait_distance>0:
		# downstream
		if r['Bait_motif_direction'] == "o":
			if r['OE_motif_direction_in_peak'] == "-":
				return "convergent or tandem"
			else:
				return "tandem or divergent"
		if r['Bait_motif_direction'] == "-":
			if r['OE_motif_direction_in_peak'] == "-":
				return "tandem"
			else:
				return "divergent"
		if r['Bait_motif_direction'] == "+":
			if r['OE_motif_direction_in_peak'] == "-":
				return "convergent"
			else:
				return "tandem"
		
	
	elif OE_bait_distance<0:
		# upstream
		if r['Bait_motif_direction'] == "o":
			if r['OE_motif_direction_in_peak'] == "+":
				return "convergent or tandem"
			else:
				return "tandem or divergent"
		if r['Bait_motif_direction'] == "-":
			if r['OE_motif_direction_in_peak'] == "-":
				return "tandem"
			else:
				return "convergent"
		if r['Bait_motif_direction'] == "+":
			if r['OE_motif_direction_in_peak'] == "-":
				return "divergent"
			else:
				return "tandem"
		
	else:
		print ("soimething is wrong")
		return "Wrong"

df['CTCF_pair'] = df.apply(row_apply,axis=1)
df.to_csv(output,sep="\t",index=False)


