#!/usr/bin/env python


import pysam
from Levenshtein import distance
import sys
inBam = sys.argv[1]
in_bam = pysam.AlignmentFile(inBam, "rb")
out_bam_path=inBam.replace(".bam","")+".clean.bam"
out_bam = pysam.AlignmentFile(out_bam_path, "wb", header=in_bam.header)

A_window_size=20
edit_distance_check_length=8
def read_A_frac(A,A_cutoff=0.5):
    return A.upper().count('A') / len(A)>A_cutoff
def mispriming_check(A,cutoff=3):
    return distance(A,"GGGTTGGG")<=cutoff
for read in in_bam.fetch(until_eof=True):
    # skip unmapped reads
    if read.is_unmapped:
        continue
    # walk through the CIGAR to locate all matched segments (op code 0 = M)
    # and record their start positions within the read’s query sequence
    m_segments = []  # list of (q_start, length)
    s_segments = []  # list of (q_start, length)
    qpos = 0
    for op, length in read.cigartuples:
        if op == 0:  # M (match)
            m_segments.append((qpos, length))
            qpos += length
        elif op == 4:  # softclip
            s_segments.append((qpos, length))
            qpos += length
        elif op in (1, 5):  # I, S, H—consumes query
            qpos += length
        # D, N, P do not consume query, so qpos unchanged

    if not m_segments:
        # no matches? skip read
        continue
    has_N = any(cig_op == 3 for cig_op, _ in read.cigartuples or [])
    if not has_N:
        continue
    # extract the first and last M segments
    first_start, first_len = m_segments[0]
    last_start, last_len   = m_segments[-1]
    seq = read.query_sequence or ""
    first_seq = seq[first_start : first_start + first_len]
    last_seq  = seq[last_start  : last_start  + last_len]
    # internal A priming
    internal_A_priming_flag = False
    mispriming_flag = False
    if read_A_frac(first_seq[:A_window_size]) or read_A_frac(last_seq[-A_window_size:]) :
        internal_A_priming_flag=True
    if mispriming_check(first_seq[-edit_distance_check_length:]) or mispriming_check(last_seq[:edit_distance_check_length]) :
        mispriming_flag=True
    # print (read.query_name,internal_A_priming_flag,mispriming_flag)
    if internal_A_priming_flag or mispriming_flag:
        continue
    out_bam.write(read)

# clean up
in_bam.close()
out_bam.close()

# create index for the filtered BAM
pysam.index(out_bam_path)

