def get_distance(x,lst,edist):
    for i in lst:
        if i==x:
            continue
        if distance(x,i)<=edist:
            return True
    return False
def self_overlap_check(s,seq_list,myDict):
    """
    myDict is a seq:[seq1,seq2,...]

    that means all these seq are self overlapping

    """

    for i in seq_list:
        if i in myDict:
            if s in myDict[i]:
                return True
    return False

position_distance_cutoff=5
N_per_gene = 5
max_per_gene = 30
edist = 7
# Azusa specific format table
dd = pd.read_csv("design2_input.tsv",sep="\t")

# gene rank, input should be a gene rank sorted, the top is the most important gene to add
gene_rank = dd.Gene.tolist()

# NgRNA dict, important, but because user input format is not generic, the specific code to get this may change
dd['Nnull'] = dd.isnull().sum(axis=1)
dd['NgRNA'] = 3-dd.Nnull
NgRNA = dd.set_index("Gene").NgRNA.to_dict()


# Extract user gRNA
# user input sgRNA list
myList = list(set(dd.pool1_hit1.fillna("").tolist()+dd.pool1_hit2.fillna("").tolist()+dd.crispick.fillna("").tolist()))
myList = [item for item in myList if item]


#----------------- important --------------------
# user also need to have a gRNA bed file
user_gRNA_bed = gRNA_candidate2[gRNA_candidate2.target.isin(myList)]



# extract user's gene list, and extract candidate gRNA
# candidate sgRNAs
# df2 is `hg38.Gene_KO.candidateg_RNA.bed.gz` in my github
candidate_gRNA = pd.concat([df2[df2.Gene.isin(dd.Gene.tolist())],df[(df.Gene=="UBE2L3")&(df['CDS%']!=-1)]])

candidate_gRNA.seq = candidate_gRNA.target
candidate_gRNA = candidate_gRNA[candidate_gRNA.columns[:6]]
user_gRNA_bed = user_gRNA_bed[user_gRNA_bed.columns[:6]]
candidate_gRNA.columns = list(range(6))
user_gRNA_bed.columns = list(range(6))
candidate_bed = pd.concat([candidate_gRNA,user_gRNA_bed])
candidate_bed = candidate_bed.drop_duplicates([0,1,2,3])
candidate_bed.to_csv("pooled_design.candidate.bed",sep="\t",header=False,index=False)
print (candidate_bed.shape)
# self overlap
os.system(f"bedtools slop -i pooled_design.candidate.bed -b {position_distance_cutoff} -g ~/Data/Human/hg38/annotations/hg38.chrom.sizes > pooled_design.candidate.slop5.bed")
!bedtools intersect -a pooled_design.candidate.slop5.bed -b pooled_design.candidate.slop5.bed -wao > pooled_design.candidate.slop5.selfoverlap.bed
candidate_gRNA = pd.concat([df2[df2.Gene.isin(dd.Gene.tolist())],df[(df.Gene=="UBE2L3")&(df['CDS%']!=-1)]])




self_overlap_list={}
sdf = pd.read_csv("pooled_design.candidate.slop5.selfoverlap.bed",sep="\t",header=None)
for i,r in sdf.iterrows():
    if r[3]==r[9]:
        continue
    if r[3] in self_overlap_list:
        self_overlap_list[r[3]].append(r[9])
    else:
        self_overlap_list[r[3]]=[r[9]]

# first search, to satisfy min sgRNA per gene
# existing list
myList = user_gRNA_bed[3].tolist()

for g in gene_rank:
    # print (g,NgRNA[g])
    if NgRNA[g]>=N_per_gene:
        continue
    candidate_sgRNA_list_current_gene =  candidate_gRNA[candidate_gRNA.Gene==g]
    if candidate_sgRNA_list_current_gene.shape[0]<=1:
        print (f"Gene {g} has less than 2 sgRNA candidates")

    for sgRNA_seq in candidate_sgRNA_list_current_gene.sort_values(['#chr','start']).target.tolist():
        if sgRNA_seq in myList:
            continue
        # edist cutoff
        if not get_distance(sgRNA_seq,myList,edist):
            if not self_overlap_check(sgRNA_seq,myList,self_overlap_list):
                myList.append(sgRNA_seq)
                NgRNA[g]+=1
        #     else:
        #         print (g,sgRNA_seq,"overlap")
        # else:
        #     print (g,sgRNA_seq,"not edist")
        if NgRNA[g]>=N_per_gene:
            break
dd['final_count'] = dd.Gene.map(NgRNA)
dd[dd.final_count<N_per_gene]



# second search, to continue add more sgRNA if possible
for g in gene_rank:
    # print (g,NgRNA[g])
    if NgRNA[g]>=max_per_gene:
        continue
    candidate_sgRNA_list_current_gene =  candidate_gRNA[candidate_gRNA.Gene==g]
    if candidate_sgRNA_list_current_gene.shape[0]<=1:
        print (f"Gene {g} has less than 2 sgRNA candidates")

    for sgRNA_seq in candidate_sgRNA_list_current_gene.sort_values(['#chr','start']).target.tolist():
        if sgRNA_seq in myList:
            continue
        # edist cutoff
        if not get_distance(sgRNA_seq,myList,edist):
            if not self_overlap_check(sgRNA_seq,myList,self_overlap_list):
                myList.append(sgRNA_seq)
                NgRNA[g]+=1
            # else:
                # print (g,sgRNA_seq,"overlap")
        # else:
            # print (g,sgRNA_seq,"not edist")
        if NgRNA[g]>=max_per_gene:
            break



dd['final_count'] = dd.Gene.map(NgRNA)
dd[dd.final_count<N_per_gene]


gRNA_in = df[df.target.isin(myList)]
gRNA_in=gRNA_in[gRNA_in.Gene.isin(list(gene_rank))][["#chr","start","end","target","CDS%","strand","Gene"]].drop_duplicates(['#chr','start','end','target'])
gRNA_not=gRNA_candidate2[gRNA_candidate2.target.isin(myList)].drop_duplicates(['#chr','start','end','target'])
final = pd.concat([gRNA_in,gRNA_not]).drop_duplicates(['#chr','start','end','target'])
# double check 
# for s,d in final.groupby("Gene"):
#     d = d.sort_values("start")
#     d['diff'] = d['start'].shift(-1) - d['start']
#     d['diff'] = d['diff'].abs()    
#     display(d[d['diff']<30])

# def get_distance2(x,lst,edist):
#     for i in lst:
#         if i==x:
#             continue
#         if distance(x,i)<edist:
#             print (x,i,distance(x,i))
#             return True
#     return False
# for x in myList:
#     if len(x)==0:
#         continue
#     if get_distance2(x,myList,edist):
#         continue
final.to_csv("Azusa.round2.tsv",sep="\t",index=False)

