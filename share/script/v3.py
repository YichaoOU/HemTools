from __future__ import print_function
import re
import gzip
import argparse
import pyfaidx
import pysam
from collections import Counter, defaultdict
from skbio.alignment import StripedSmithWaterman
import pandas as pd

def get_sequence(reference_genome, chromosome, start, end, strand="+"):
	if strand == "+":
		seq = reference_genome[chromosome][start:end]
	elif strand == "-":
		seq = reference_genome[chromosome][start:end].reverse.complement
	return str(seq)

def alignSequences(reference, read):
	query = StripedSmithWaterman(reference, gap_open_penalty=10)
	alignment = query(read)
	return alignment

def readBed(bedfile, reference_genome,cut_pos=6,flank_length=200):
	# Input is 0-based, half-open BED file (includes start but not end)
	# Sequence is always returned where 200 is the breakpoint and in the forward orientation
	cut_pos = -cut_pos
	flank_length = flank_length
	BED_dict = {}
	with open(bedfile, 'r') as f:
		for line in f:
			if len(line) <=1:
				continue
			if line[0] != '#':
				# line = line.rstrip('\n').split('\t')
				line = line.strip().split()
				# chr, start, end, name, CHANGEseq_reads, strand = line.rstrip('\n').split('\t')
				chr, start, end, name, CHANGEseq_reads, strand = line[:6]
				start = int(start)
				end = int(end)
				if strand == "-" :
					sequence = get_sequence(reference_genome, chr, start + cut_pos - flank_length, start + cut_pos + flank_length)
				else:
					sequence = get_sequence(reference_genome, chr, end - cut_pos - flank_length , end - cut_pos + flank_length)
				BED_dict[name] =  { 'chr' : chr,
									'start' : start,
									'end' : end,
									'strand' : strand,
									'seq' : sequence
									}
	return BED_dict

def readBAM(bam, BED_dict, site, log, filterlog,flank_length=200,window_size=8,out=None):
		integrations = 0
		indels = 0
		total = 0
		breakpoint_pos = flank_length
		window = window_size

		# alignment_score_dict = Counter()
		# cigar_dict = Counter()
		fwd_query= StripedSmithWaterman('GTTTAATTGAGTTGTCATATGTTAATAACGGTAT', gap_open_penalty=10)
		rev_query = StripedSmithWaterman('ATACCGTTATTAACATATGACAACTCAATTAAAC', gap_open_penalty=10)
		read_query = StripedSmithWaterman(BED_dict[site]['seq'], gap_open_penalty=10, gap_extend_penalty=1) # zero_index=True, doesn't matter zero or one index when we use CIGAR

		# with open(logfile, 'a') as o2:
		read_align_status = []
		for read in bam.fetch(BED_dict[site]['chr'], BED_dict[site]['start'], BED_dict[site]['end']):

			# Align read
			read_aln = read_query(read.query_sequence)
			m = re.findall(r'(\d+)([A-Z]{1})', read_aln.cigar) # this is align to the 400bp sequence, 

			current_pos = read_aln.query_begin # this is the 400bp sequence alignment start
			match_min_pos = 1000 # set to number above possible current positions
			match_max_pos = -1 # set to number below current max)
			match_window = 30
			indel_detected = False
			read_current_pos = 0
			for length, type in m:
				length = int(length)
				read_current_pos += length
				if type == "M":
					match_min_pos = min(current_pos, match_min_pos) # Get minimum
					current_pos += int(length) # Move position counter
					match_max_pos = max(current_pos, match_max_pos) # Get maximum
				elif type == "I":
					if breakpoint_pos + window >= current_pos and breakpoint_pos - window <= current_pos + int(length):
						indel_detected = True
						read_align_status.append([read.query_name,-length,read_aln.aligned_query_sequence[read_current_pos-length:read_current_pos]])
					current_pos += int(length)
				elif type == "D":
					if breakpoint_pos + window >= current_pos and breakpoint_pos - window <= current_pos:
						indel_detected = True
						read_align_status.append([read.query_name,length,read_aln.aligned_target_sequence[read_current_pos-length:read_current_pos]])

			# Align to forward and reverse oligo
			fwd_aln = fwd_query(read.query_sequence)
			rev_aln = rev_query(read.query_sequence)

			# Tabulate integrations
			if (fwd_aln.optimal_alignment_score > 30 or rev_aln.optimal_alignment_score > 30):
				if breakpoint_pos - match_window >= match_min_pos and breakpoint_pos + match_window <= match_max_pos:
					integrations += 1
					print(site, 'fwd', 'query', fwd_aln.aligned_query_sequence, sep="\t", file=log)
					print(site, 'fwd', 'target', fwd_aln.aligned_target_sequence, sep="\t", file=log)
					print(site, 'rev', 'query', rev_aln.aligned_query_sequence, sep="\t", file=log)
					print(site, 'rev', 'target', rev_aln.aligned_target_sequence, sep="\t", file=log)
					print(site, 'read', 'query', read_aln.aligned_query_sequence, sep="\t", file=log)
					print(site, 'read', 'target', read_aln.aligned_target_sequence, sep="\t", file=log)
					print(site, 'read', 'cigar', read_aln.cigar, sep="\t", file=log)
					print(site, 'read', 'bam_sequence', read.query_sequence, sep="\t", file=log)
					print(site, 'read', 'indel_detected', indel_detected, sep="\t", file=log)
				else:
					print(site, 'fwd', 'query', fwd_aln.aligned_query_sequence, file=filterlog)
					print(site, 'fwd', 'target', fwd_aln.aligned_target_sequence, file=filterlog)
					print(site, 'rev', 'query', rev_aln.aligned_query_sequence, file=filterlog)
					print(site, 'rev', 'target', rev_aln.aligned_target_sequence, file=filterlog)
					print(site, 'read', 'query', read_aln.aligned_query_sequence, file=filterlog)
					print(site, 'read', 'target', read_aln.aligned_target_sequence, file=filterlog)
					print(site, 'read', 'cigar', read_aln.cigar, file=filterlog)
					print(site, 'read', 'query_name', read.query_name, file=filterlog)
					print(site, 'read', 'bam_sequence', read.query_sequence, file=filterlog)
					print(site, 'read', 'indel_detected', indel_detected, file=filterlog)
			if indel_detected:
				indels += 1
			total += 1
		try:
			df = pd.DataFrame(read_align_status)
			df.to_csv("%s.%s.indel_spectrum.raw.csv"%(out,site),index=False,header=False)
			a=pd.DataFrame(df[1].value_counts().sort_values(ascending=False))
			a.index.name="indel_type"
			a.columns = ['read_counts']
			a.to_csv("%s.%s.indel_spectrum.sum.csv"%(out,site))
		except:
			print ("No indel found")
		return (indels, integrations, total)


def main():
	parser = argparse.ArgumentParser(description='Count sequence positions')
	parser.add_argument('--bed', help='BED filename', required=True)
	parser.add_argument('--ref', help='Reference filename', required=True)
	parser.add_argument('--bam', help='BAM filename', required=True)
	parser.add_argument('--out', help='Output filename', required=True)
	parser.add_argument('--site', help='Site (optional)', nargs='?', const='')
	parser.add_argument('--setting', help='cas9 or cas12a',default="cas9")
	# parser.add_argument('-p', '--projects_to_build', nargs='?', const='')

	args = parser.parse_args()
	print (args)
	# exit()
	flank_length=200
	if str(args.setting).lower() == "cas9":
		cut_pos=-6
		window_size=8
	elif str(args.setting).lower() == "cas12a":
		cut_pos=-3
		window_size=9
	else:
		cut_pos=-6
		window_size=8
		print ("using cas9 setting as default")

	# Load reference sequence
	print("Loading reference sequence...")
	reference_genome = pyfaidx.Fasta(args.ref)

	# Load BED file
	print("Loading BED file and get sequences...")
	BED_dict = readBed(args.bed, reference_genome,cut_pos=cut_pos,flank_length=flank_length)

	# Allow analysis of subset if specified
	if(args.site in BED_dict.keys()):
		BED_dict = {args.site: BED_dict[args.site]}
	else:
		print("Site not found. Processing entire BED file")

	# Load BAM file
	print("Loading BAM file...")
	bam = pysam.AlignmentFile(args.bam, "rb")
	bam_file_name = args.bam.split("/")[-1]
	with open(args.out, 'w') as o1, open(args.out + ".log", 'w') as o2, open(args.out + ".filtered.log", 'w') as o3:
		for site in BED_dict:
			indels, integrations, total = readBAM(bam, BED_dict, site, o2, o3,flank_length=flank_length,window_size=window_size,out=args.out)
			print(site, BED_dict[site]['chr'], BED_dict[site]['start'], BED_dict[site]['end'], BED_dict[site]['seq'],
				  indels, integrations, total, sep="\t")
			print(bam_file_name,site, BED_dict[site]['chr'], BED_dict[site]['start'], BED_dict[site]['end'], BED_dict[site]['seq'],
				  indels, integrations, total, sep="\t", file=o1)



if __name__ == "__main__":
	main()