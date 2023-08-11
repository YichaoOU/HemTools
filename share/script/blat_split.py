
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

def read_fasta(f):
	my_dict = {}
	for r in SeqIO.parse(f, "fasta"):
		my_dict[r.id] = str(r.seq).upper()
	return my_dict	
def read_psl(f):
    df = pd.read_csv(f,sep="\t",header=None,skiprows=6)
    df = df.sort_values(0,ascending=False)
    df = df.drop_duplicates(9)
    df.index = df[9].tolist()
    return df
def write_fasta(file_name,myDict):
    out = open(file_name,"wt")
    for k in myDict:
        if len(myDict[k])<=1:
            myDict[k]="NN"
        out.write(">"+k+"\n")
        out.write(myDict[k]+"\n")

seq = read_fasta("step3.filtered.R2.fa")
df = read_psl("step4.psl")
pd.set_option('display.max_columns', None)
df['seq'] = [seq[x] for x in df[9]]
df['match_seq'] = df.apply(lambda r:r.seq[r[11]:r[12]],axis=1)
df['filter_seq'] = df.apply(lambda r:r.seq[r[12]:],axis=1)
write_fasta("step3.filtered.R2_matched.fa",df.match_seq.to_dict())
write_fasta("step3.filtered.R2_unmatched.fa",df.filter_seq.to_dict())

