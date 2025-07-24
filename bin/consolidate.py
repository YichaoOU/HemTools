#!/research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/python/bin/python

__author__ = 'Martin Aryee'

# source /apps/lab/aryee/pyenv/versions/venv-2.7.6/bin/activate
# python consolidate.py /data/ngscid-research/testing/CTCTCTACACTGATGG.sorted.fastq tmp.fastq 15 0.9

import HTSeq
import sys
import os
import logging

#fastq_file = '/data/ngscid-research/testing/CTCTCTACACTGATGG.sorted.fastq'
#consolidated_fastq_file = '/PHShome/ma695/tmp/tmp.fastq'
#min_qual = 15
#min_freq = 0.9

# Configure logger
logger = logging.getLogger('root')

def read_bins(fastq_file):
	infile = HTSeq.FastqReader(fastq_file)
	read_num = 0
	#bin_name = [] # Will consist of the molecular_id followed by the incoming 2nd header field (which includes sample_id)
	#bin_reads = []
	cur_molecular_id = ''
	#import itertools
	#for read in itertools.islice( infile, 10000 ): # Read the first few reads for testing
	for read in infile:
		read_num += 1
		read_name, sample_id, molecular_id = read.name.split(' ')
		if molecular_id == cur_molecular_id:
			bin_reads.append(read)
		else:
			if cur_molecular_id != '':
				yield cur_molecular_id, cur_sample_id, bin_reads
			cur_molecular_id = molecular_id
			cur_sample_id = sample_id
			#bin_name = '@%s %s' % (molecular_id, sample_id)
			bin_reads = [read]
	yield cur_molecular_id, cur_sample_id, bin_reads # The last bin


def consolidate_position(bases, quals, min_qual, min_freq):
	num = {}
	qual = {}
	num['A'] = num['C'] = num['G'] = num['T'] = num['N'] = 0
	qual['A'] = qual['C'] = qual['G'] = qual['T'] = qual['N'] = 0
	for bb, qq in zip(bases, quals):
		if qq > min_qual:
			num[bb] += 1
		if qq > qual[bb]:
			qual[bb] = qq
	most_common_base = max(num.iterkeys(), key=(lambda key: num[key]))
	freq = float(num[most_common_base]) / len(bases)
	if freq > min_freq:
		return True, most_common_base, qual[most_common_base]
	else:
		return False,'N', 0


def consolidate(fastq_file, consolidated_fastq_file, min_qual, min_freq):
	print("Consolidating reads in", fastq_file)
	outfolder = os.path.dirname(consolidated_fastq_file)
	# if not os.path.exists(outfolder):
		# os.makedirs(outfolder)

	outfile = open(consolidated_fastq_file, 'w')
	bins = read_bins(fastq_file)
	#next(bins)

	num_input_reads = 0
	num_consolidated_reads = 0
	num_successes = 0 # Bases with successful consolidation
	num_bases = 0
	count = 0
	for cur_molecular_id, cur_sample_id, reads in bins:
		count += 1
		num_input_reads += len(reads)
		num_consolidated_reads += 1
		# Get all the bases and quals in the read
		read_bases = zip(*[list(read.seq) for read in reads])
		read_quals = zip(*[list(read.qual) for read in reads])
		# Iterate position by position
		consolidation_sucess, cons_seq, cons_qual = zip(*[consolidate_position(bases, quals, min_qual, min_freq) for bases, quals in zip(read_bases, read_quals)])
		# Count consolidation successes and failures
		num_successes += sum(consolidation_sucess)
		num_bases += len(consolidation_sucess)
		# Write consolidated FASTQ read
		outfile.write('@%s_%d %s\n' % (cur_molecular_id, len(reads), cur_sample_id)) # Header: Molecular id, number of reads, 2nd incoming header field (includes sample id)
		outfile.write(''.join(cons_seq) +'\n')
		outfile.write('+\n')
		outfile.write(''.join([chr(q+33) for q in cons_qual]) + '\n')

	print(fastq_file,"Read %d input reads", num_input_reads)
	print(fastq_file,"total unique UMI: %d", count)
	print(fastq_file,"Wrote %d consolidated reads to %s", num_consolidated_reads, consolidated_fastq_file)
	print(fastq_file,"Successfully consolidated %d bases out of %d (%.2f%%)", num_successes, num_bases, 100*float(num_successes)/num_bases)
	outfile.close()


def main():
	if len(sys.argv) < 5:
		print 'Usage: python consolidate.py fastq_file consolidated_fastq_file min_qual min_freq'
		sys.exit()

	fastq_file = sys.argv[1]
	consolidated_fastq_file = sys.argv[2]
	min_qual = int(sys.argv[3])
	min_freq = float(sys.argv[4])
	consolidate(fastq_file, consolidated_fastq_file, min_qual, min_freq)


if __name__ == '__main__':
	main()