#!/home/yli11/.conda/envs/captureC/bin/python
# from __future__ import print_function
import os
import re
import gzip
import itertools
import argparse
import subprocess


def fq2(file):
	if re.search('.gz$', file):
		fastq = gzip.open(file, 'rb')
	else:
		fastq = open(file, 'r')
	with fastq as f:
		while True:
			l1 = f.readline()
			if not l1:
				break
			l2 = f.readline()
			l3 = f.readline()
			l4 = f.readline()
			yield [l1.decode('utf-8'), l2.decode('utf-8'), l3.decode('utf-8'), l4.decode('utf-8')]
def fq(file): # py3
    if file.endswith('.gz'):
        fastq = gzip.open(file, 'rt', encoding='utf-8')  # Open in text mode, decode as UTF-8
    else:
        fastq = open(file, 'r', encoding='utf-8')
    
    with fastq as f:
        while True:
            l1 = f.readline()
            if not l1:
                break
            l2 = f.readline()
            l3 = f.readline()
            l4 = f.readline()
            yield [l1, l2, l3, l4]  # No need for decode, already a string in text mode


# Create molecular ID by concatenating molecular barcode and beginning of r1 and r2 read sequences
def get_umi(r1,r2,l1=5,l2=2,l3=5):
	umi1 = r1[1][0:l1]
	skip1 = r1[1][l1:l1+l2]
	mbio1 = r1[1][l1+l2:l1+l2+l3]
	umi2 = r2[1][0:l1]
	skip2 = r2[1][l1:l1+l2]
	mbio2 = r2[1][l1+l2:l1+l2+l3]
	molecular_barcode=umi1+umi2
	return f'{molecular_barcode}_{mbio1}_{mbio2}'

def umitag(read1, read2, read1_out, read2_out, out_dir,l1=5,l2=2,l3=5):

	# if not os.path.exists(out_dir):
		# os.makedirs(out_dir)

	r1_umitagged_unsorted_file = read1_out + '.tmp'
	r2_umitagged_unsorted_file = read2_out + '.tmp'

	# Create UMI-tagged R1 and R2 FASTQs
	# r1_umitagged = open(r1_umitagged_unsorted_file, 'w')
	# r2_umitagged = open(r2_umitagged_unsorted_file, 'w')
	with open(r1_umitagged_unsorted_file, 'w', buffering=1) as r1_umitagged, open(r2_umitagged_unsorted_file, 'w', buffering=1) as r2_umitagged:
		for r1,r2 in zip(fq(read1), fq(read2)):
			# Create molecular ID by concatenating molecular barcode and beginning of r1 read sequence
			molecular_id = get_umi(r1,r2,l1,l2,l3)
			# Add molecular id to read headers
			r1[0] = f'{r1[0].rstrip()} {molecular_id}\n'
			r2[0] = f'{r2[0].rstrip()} {molecular_id}\n'
			r1[1] = r1[1][l1+l2:]
			r2[1] = r2[1][l1+l2:]
			r1[3] = r1[3][l1+l2:]
			r2[3] = r2[3][l1+l2:]
			for line in r1:
				r1_umitagged.write(line)
			for line in r2:
				r2_umitagged.write(line)
	# r1_umitagged.close()
	# r2_umitagged.close()

	# Sort fastqs based on molecular barcode
	cmd = 'cat ' + r1_umitagged_unsorted_file + ' | paste - - - - | sort -k3,3 -k1,1 | tr "\t" "\n" >' + read1_out
	subprocess.check_call(cmd, shell=True, env=os.environ.copy())
	cmd = 'cat ' + r2_umitagged_unsorted_file + ' | paste - - - - | sort -k3,3 -k1,1 | tr "\t" "\n" >' + read2_out
	subprocess.check_call(cmd, shell=True, env=os.environ.copy())


	os.remove(r1_umitagged_unsorted_file)
	os.remove(r2_umitagged_unsorted_file)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-r1','--read1_in', required=True)
	parser.add_argument('-r2','--read2_in', required=True)
	parser.add_argument('-o1','--read1_out', required=True)
	parser.add_argument('-o2','--read2_out', required=True)
	parser.add_argument('-o','--out_dir', default='.')
	parser.add_argument('-l1','--umi_length', help="Xbp starting from R1 and R2 is the UMI",default=5,type=int)
	parser.add_argument('-l2','--skip_length', help="Xbp starting from R1 and R2 is the UMI",default=2,type=int)
	parser.add_argument('-l3','--mbio_length', help="Xbp starting from R1 and R2 is the UMI",default=5,type=int)
	args = parser.parse_args()


	umitag(args.read1_in, args.read2_in, args.read1_out, args.read2_out, args.out_dir, args.umi_length, args.skip_length, args.mbio_length)

if __name__ == '__main__':
	main()