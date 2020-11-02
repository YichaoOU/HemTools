Quantify base editing efficiency for crispressoPooled experiments
====================================

::


	usage: crispressoPooled_BE.py [-h] [-j JID] -a AMPLICON_BED -gRNA GRNA_BED -f
	                              FASTQ_TSV [--ref REF] [--alt ALT] [-g GENOME]
	                              [--genome_fasta GENOME_FASTA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        crispressoPooled_BE_yli11_2020-10-26)
	  -a AMPLICON_BED, --amplicon_bed AMPLICON_BED
	                        amplicon_bed required (default: None)
	  -gRNA GRNA_BED, --gRNA_bed GRNA_BED
	                        gRNA_bed required (default: None)
	  -f FASTQ_TSV, --fastq_tsv FASTQ_TSV
	                        fastq tsv 3 columns required (default: None)
	  --ref REF             reference base (default: A)
	  --alt ALT             alternative base (default: G)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  --genome_fasta GENOME_FASTA
	                        genome fasta file (default:
	                        /home/yli11/Data/Human/hg19/fasta/hg19.fa)


Summary
^^^^^^

Code is designed to analyze rhAmp-seq based on ``crispressoPooled``, but should be generic.



Input
^^^^^

The 4th column (name column) in the following two files should match (case sensitive!)

1. Amplicon sequence bed file
-----------------------------

The amplicon sequence can be downloaded from IDT. ``Assay.bed``

::

	chr2	57769587	57769832	HBGg22_Target09	0	+
	chrX	120721125	120721318	HBGg22_Target122	0	+
	chr7	14859651	14859845	HBGg22_Target105	0	+



2. gRNA bed file
----------------

Header starting with "#" is acceptable.

::

	#chr	start	end	name	CHANGEseq_reads	strand
	chr1	171455834	171455854	HBGg22_Target01	1	-
	chr1	235564562	235564582	HBGg22_Target02	1	-
	chr10	21466883	21466903	HBGg22_Target03	1	+



Output
^^^^^^

For each sample, it outputs a tsv file containing the gRNA name, gRNA sequence, base editing efficiency for each position (only consider the 20bp gRNA length), and 'indel_frequency','total_indel','Reads_total'. So totally 25 columns.

file name: ``$sample_id.edit_eff.tsv``

If editing efficiency is -1, meaning no reads mapped to the amplicon sequence.


Usage
^^^^^

Copy fastq files, amplicon bed file, and gRNA bed file  in the working dir and run the following:

::

	hpcf_interactive

	PATH=/home/yli11/HemTools/bin:/hpcf/lsf/lsf_prod/10.1/linux3.10-glibc2.17-x86_64/etc:/hpcf/lsf/lsf_prod/10.1/linux3.10-glibc2.17-x86_64/bin:/usr/lpp/mmfs/bin:/usr/lpp/mmfs/lib:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/ibutils/bin:/sbin:/cm/local/apps/environment-modules/3.2.10/bin:/opt/puppetlabs/bin
	export PATH=$PATH:"/home/yli11/HemTools/bin"


	module load python/2.7.13

	run_lsf.py --guess_input

	crispressoPooled_BE.py -a amp.bed -gRNA gRNA.bed -f fastq.tsv -g hg38 --ref A --alt G

For CBE use:

::

	crispressoPooled_BE.py -a amp.bed -gRNA gRNA.bed -f fastq.tsv -g hg38 --ref C --alt T