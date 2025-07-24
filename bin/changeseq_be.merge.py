#!/usr/bin/env python
import pandas as pd
import numpy as np
import pyfaidx
import regex
def nw(x, y, match = 1, mismatch = 1, gap = 6):
    nx = len(x)
    ny = len(y)
    # Optimal score at each possible pair of characters.
    F = np.zeros((nx + 1, ny + 1))
    F[:,0] = np.linspace(0, -nx * gap, nx + 1)
    F[0,:] = np.linspace(0, -ny * gap, ny + 1)
    # Pointers to trace through an optimal aligment.
    P = np.zeros((nx + 1, ny + 1))
    P[:,0] = 3
    P[0,:] = 4
    # Temporary scores.
    t = np.zeros(3)
    for i in range(nx):
        for j in range(ny):
            if x[i] == y[j]:
                t[0] = F[i,j] + match
            else:
                t[0] = F[i,j] - mismatch
            t[1] = F[i,j+1] - gap
            t[2] = F[i+1,j] - gap
            tmax = np.max(t)
            F[i+1,j+1] = tmax
            if t[0] == tmax:
                P[i+1,j+1] += 2
            if t[1] == tmax:
                P[i+1,j+1] += 3
            if t[2] == tmax:
                P[i+1,j+1] += 4
    # Trace through an optimal alignment.
    i = nx
    j = ny
    rx = []
    ry = []
    while i > 0 or j > 0:
        if P[i,j] in [2, 5, 6, 9]:
            rx.append(x[i-1])
            ry.append(y[j-1])
            i -= 1
            j -= 1
        elif P[i,j] in [3, 5, 7, 9]:
            rx.append(x[i-1])
            ry.append('-')
            i -= 1
        elif P[i,j] in [4, 6, 7, 9]:
            rx.append('-')
            ry.append(y[j-1])
            j -= 1
    # Reverse the strings.
    rx = ''.join(rx)[::-1]
    ry = ''.join(ry)[::-1]
    return rx,ry
nw("CCCTAGTGGAATGGAAGGGAATG","ATTATACCTGCCATGCCGTANGG")
reference = "/home/yli11/dirs/shengdar_group/genomes/hg38/hg38.fa"
fasta = pyfaidx.Fasta(reference)
def reverse_complement(seq):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N':'N', 'R':'Y', 'H':'D'}
    return ''.join(complement[base] for base in reversed(seq))

def regex_from_sequence(seq, insertions=0, deletions=0, mismatches=0):
    pattern = ''.join([{'A':'A', 'T':'T', 'C':'C', 'G':'G', 'N':'[ATCGN]', 'R':'[AG]', 'H':'[ACT]', 'Y':'[TC]', 'D':'[AGT]'}[c] for c in seq.upper()])
    pattern = f'(?b:{pattern})' + f'{{s<={mismatches},i<={insertions},d<={deletions}}}'
    return pattern

def align_sequences(target_seq, window_seq, max_insertions=1, max_deletions=1, max_mismatches=6):
    pattern = regex_from_sequence(target_seq, max_insertions, max_deletions, max_mismatches)
    match = regex.search(pattern, window_seq, regex.BESTMATCH)
    if match:
        start, end = match.span()
        strand = "+"
        num_mismatches, num_insertions, num_deletions = match.fuzzy_counts
        return window_seq[start:end], start, end, strand, end-start, num_mismatches, num_insertions, num_deletions
    
    # If no match, try reverse complement:
    target_seq_rc = reverse_complement(target_seq)
    pattern = regex_from_sequence(target_seq_rc, max_insertions, max_deletions, max_mismatches)
    match = regex.search(pattern, window_seq, regex.BESTMATCH)
    if match:
        start, end = match.span()
        strand = "-"
        num_mismatches, num_insertions, num_deletions = match.fuzzy_counts
        return reverse_complement(window_seq[start:end]), start, end, strand, end-start, num_mismatches, num_insertions, num_deletions
    
    return None, None, None, None, None, None, None, None #best_match, start, end, strand, length, num_mismatches, num_insertions, num_deletions

def get_genomic_sequence(chromosome, start, end):
    seq = fasta[chromosome][start:end].seq
    return seq
def get_off_target(r):
    chromosome = r[0]
    position = int((r[1]+r[2])/2)
    target_seq = r[28]
    flank = 40
    window_start = position - flank
    window_end = position + flank
    genomic_sequence = get_genomic_sequence(chromosome, window_start, window_end)
    best_match, start, end, strand, length, num_mismatches, num_insertions, num_deletions = align_sequences(target_seq, genomic_sequence, max_insertions = 1, max_deletions = 1, max_mismatches = 6)
    coord=""
    Site_Sequence_Gaps_Allowed=""
    Realigned_Target_Sequence=""
    aligned_start=r[1]
    aligned_end=r[2]
    if best_match:
        aligned_start = window_start + start
        aligned_end = window_start + end
        coord = f'{chromosome}:{aligned_start}-{aligned_end}'
        if len(best_match)!=len(target_seq):
            Site_Sequence_Gaps_Allowed,Realigned_Target_Sequence = nw(best_match,target_seq)
    r['#Chromosome'] = chromosome     
    r['Start'] = aligned_start     
    r['End'] = aligned_end     
    r['Genomic Coordinate'] = coord 
    r['Nuclease_Read_Count'] = r[4]      
    r['Strand'] = strand      
    r['Control_Read_Count'] = r[32]    
    r['Site_Sequence'] = best_match      
    r['Site_Substitution_Number'] = num_mismatches      
    r['Site_Sequence_Gaps_Allowed'] = Site_Sequence_Gaps_Allowed      
    r['File_Name'] = r[24]      
    r['Cell'] = r[25]       
    r['Target_site'] = r[26]       
    r['Full_Name'] = r[27]       
    r['Target_Sequence'] = target_seq      
    r['Realigned_Target_Sequence'] = Realigned_Target_Sequence      
    return r
import sys
label = sys.argv[1]
df = pd.read_csv(f"{label}_identified_matched.txt",sep="\t")

df = df.drop(['Nuclease_overlap_bp_list','Control_overlap_bp_list'],axis=1)

df2 = pd.read_csv(f"{label}_identified_unmatched.txt",sep="\t",header=None)
# df2 = df2.sample(n=100).apply(get_off_target,axis=1)
df2 = df2.apply(get_off_target,axis=1)
df2 = df2[df.columns.tolist()]
df = pd.concat([df,df2])
df.to_csv(f"{label}.merged.csv",index=False)






