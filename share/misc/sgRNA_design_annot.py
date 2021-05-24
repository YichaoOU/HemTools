

# exec(open("get_pos.py").read())

import pandas as pd
import glob
import sys
# df = pd.read_csv("WGATAR_25_gRNA.annote.bed",sep="\t",header=None)

all_gRNA_annotate_bed_file=sys.argv[1]
position_anchor=int(sys.argv[2])
off_target_file = sys.argv[3]

try:
	editable_base=sys.argv[4]
except:
	editable_base="A"


df = pd.read_csv(all_gRNA_annotate_bed_file,sep="\t",header=None)

old_columns = df.columns.tolist()

def get_edit_pos(r,editable_pos,editable_base):
	seq = r[3]
	out = []
	if r[5] == "-":
		start = r[2]
		for i in editable_pos:
			if seq[i] == editable_base:
				out.append(start-i)
	if r[5] == "+":
		start = r[1] + 1
		for i in editable_pos:
			if seq[i] == editable_base:
				out.append(start+i)		
	return out

editable_pos=[2,3,4,5,6,7]
df['edit_pos'] = df.apply(lambda r:get_edit_pos(r,editable_pos,editable_base),axis=1)


# print (df.head())

def get_rel_distance_to_WGATAR(r,position_anchor):
	"""
	118230764  118230770  WGATAR   0  +
	179048682  179048688  WGATAR   0  -
	
	if seq is +, pos wgAtar is +3
	if seq is -, pos is +4
	"""
	if r[11] == "+":
		gata_pos = r[7]+position_anchor
	if r[11] == "-":
		gata_pos = r[7]+position_anchor+1
	out = []
	for i in r.edit_pos:
		value = i - gata_pos
		if r[11] == "-":
			value = -value
		if value <= 0:
			value -= 1
		out.append(value)
	return out
df['rel_pos'] = df.apply(lambda r:get_rel_distance_to_WGATAR(r,position_anchor),axis=1)



df = df[old_columns+['rel_pos']]
df = df.drop_duplicates(3)
df.to_csv(all_gRNA_annotate_bed_file+".rel_edit_pos.bed",sep="\t",header=False,index=False)
df2 = df.copy()

def is_within_10bp(x):
	flag = False
	for i in x:
		if abs(i)<=8:
			return True
	return False
df = df2.copy()
def rmdup_name(x):
	x = x.split(",")
	x = list(set(x))
	return ",".join(x)

df[17] = [rmdup_name(x) for x in df[17]]
df3 = pd.read_csv(off_target_file,sep="\t",header=None,index_col=0)
df3.index = [x[:20] for x in df3.index.tolist()]
# filter

df['N_edit_bases'] = [len(x) for x in df.rel_pos]
df = df[df.N_edit_bases >0]
df = df[df[4].between(0.2,0.8)]

df.index = df[3].tolist()

# df['off-target'] = df3[1]
df['off-target'] = df.index.to_series().map(df3[1].to_dict())
df['off-target'] = df['off-target'].fillna(-1)
df = df[df['off-target']<=1] 
# print (df.sample(n=5).head())
print (df.shape)
df.to_csv(all_gRNA_annotate_bed_file+".rel_edit_pos.filter.bed",sep="\t",header=True,index=False)
'''
## get gene rank
## rank genes based on number of occurrences

## tableS8 has higher weight
w1 = 1
w2 = 2
my_genes = {}
files = glob.glob("ranked_gene_list/*.list")
for f in files:
	if "tableS8" in f:
		w = w2
	else:
		w = w1
	try:
		tmp = pd.read_csv(f,header=None)[0]
	except:
		continue
	for i in pd.read_csv(f,header=None)[0].tolist():
		if i in my_genes:
			my_genes[i]+=w
		else:
			my_genes[i] = w


gene_ranks = pd.DataFrame.from_dict(my_genes,orient="index")
gene_ranks = gene_ranks.sort_values(0,ascending=False)
gene_ranks.to_csv("gene_ranks.tsv",sep="\t",header=False)

df.to_csv("WGATAR_25_gRNA.rel_edit_pos.filter.gene_rank.bed",sep="\t",header=True,index=False)

def match_gene(x):
	max_rank = 1
	for i in x.split(","):
		if my_genes[i] > max_rank:
			max_rank = my_genes[i]
	return max_rank

df['rank'] = df[17].apply(match_gene)
df = df.sort_values("rank",ascending=False)
print (df.groupby("rank").size())
df = df[df['rank']>=3]
print (df.shape)
print (get_number_genes(df[17]))
df['WGATAR'] = df[6]+"_"+df[7].astype(str)+"_"+df[8].astype(str)
df.groupby("WGATAR").size().sort_values(ascending=False).head(n=20)
sgRNA_per_WGATAR_count = df.groupby("WGATAR").size().sort_values(ascending=False)

## generate two sets for rank >=3

df3 = df[df['rank']==3]
df3.groupby(17).size().sort_values(ascending=False)
df[df[17].isin(selected_genes)].shape[0]+df[df['rank']>3].shape[0]

selected_genes = ["VPS39,TMEM87A","SFPQ,ZMYM4","ATF5,MED25,AP2A1,NUP62","ARID2,SCAF11","TAF1","MAX","BRCA2","DNAJC24,ELP4,EIF3M","NFYC",'HUWE1,TSR2,GNL3L','SRRT,PPP1R35,POP7','GFI1B','NEDD1','YEATS4']

batch1 = df[df['rank']>3][17].tolist()+selected_genes
batch2 = set(df[df['rank']==3][17].tolist())-set(selected_genes)
batch2 = list(batch2)
column_names = ['#chr','start','end','sgRNA_seq','GC_content','strand','WGATAR_chr','WGATAR_start','WGATAR_end','WGATAR_name','WGATAR_value','WGATAR_strand','GATA1_peak_chr','GATA1_peak_start','GATA1_peak_end','GATA1_peak_id','GATA1_peak_name','root_gene_name','relative_distance_to_WGATAR','Number_editable_bases','off-target','gene_rank','asd']
df.columns = column_names
df = df.drop(['asd'],axis=1)
b1 = df[df["root_gene_name"].isin(batch1)]
b2 = df[df["root_gene_name"].isin(batch2)]
print (b1.shape)
print (b2.shape)
b1.to_csv("WGATAR_25_gRNA.batch1.tsv",sep="\t",header=True,index=False)
b2.to_csv("WGATAR_25_gRNA.batch2.tsv",sep="\t",header=True,index=False)
# df.groupby(17).size().sort_values(ascending=False)

# df = df[df['off-target']<2] # 149980
# df = df[df.N_edit_bases >1] # 96922

def get_number_genes(x):
	count = {}
	for i in x:
		for j in i.split(","):
			count[j]=0
	return len(count)
	

# df['is_10bp'] = [is_within_10bp(x) for x in df.rel_pos]

# df = df[df.is_10bp==True]
'''