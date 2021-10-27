STARR-seq analysis pipeline
===================================

::

	usage: starr_seq.py [-h] [-j JID] -f FASTQ_TSV -d DESIGN_MATRIX [-bs BIN_SIZE]
	                    [-ss STEP_SIZE] [-c FDR_CUTOFF] [-min MIN_FRAG]
	                    [-max MAX_FRAG] [-q MAPQ] [-a ADDON_PARAMETERS]
	                    [-g GENOME] [-i INDEX_FILE] [-s CHROM_SIZE] [-b BLACKLIST]
	                    [--gc_cov GC_COV] [--map_cov MAP_COV]
	                    [--conv_cov CONV_COV]

	starr-seq pipeline

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        starr_seq_yli11_2021-10-27)
	  -f FASTQ_TSV, --fastq_tsv FASTQ_TSV
	                        paired-end fastq tsv (default: None)
	  -d DESIGN_MATRIX, --design_matrix DESIGN_MATRIX
	                        3 column tsv for design matrix (default: None)
	  -bs BIN_SIZE, --bin_size BIN_SIZE
	                        bin_size (default: 500)
	  -ss STEP_SIZE, --step_size STEP_SIZE
	                        step_size (default: 100)
	  -c FDR_CUTOFF, --FDR_cutoff FDR_CUTOFF
	                        FDR_cutoff (default: 0.05)
	  -min MIN_FRAG, --min_frag MIN_FRAG
	                        min_frag size (default: 200)
	  -max MAX_FRAG, --max_frag MAX_FRAG
	                        max_frag size (default: 1000)
	  -q MAPQ, --MAPQ MAPQ  MAPQ cutoff (default: 40)
	  -a ADDON_PARAMETERS, --addon_parameters ADDON_PARAMETERS
	                        other parameters to add to starrPeaker (default: )

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -i INDEX_FILE, --index_file INDEX_FILE
	                        BWA index file (default: /home/yli11/Data/Human/hg19/i
	                        ndex/bwa_16a_index/hg19.fa)
	  -s CHROM_SIZE, --chrom_size CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Human/STARR_seq
	                        /hg19.chrom.sizes.simple.sorted)
	  -b BLACKLIST, --blacklist BLACKLIST
	                        blacklist size (default: /home/yli11/Data/Human/hg19/a
	                        nnotations/hg19.blacklist.bed)
	  --gc_cov GC_COV       gc_cov (default: /home/yli11/Data/Human/STARR_seq
	                        /STARRPeaker_cov_hg19_ucsc-gc-5bp.bw)
	  --map_cov MAP_COV     map_cov (default: /home/yli11/Data/Human/STARR_seq
	                        /STARRPeaker_cov_hg19_gem-mappability-100mer.bw)
	  --conv_cov CONV_COV   conv_cov (default: /home/yli11/Data/Human/STARR_seq
	                        /STARRPeaker_cov_hg19_linearfold-folding-energy-
	                        100bp.bw)


Summary
^^^^^^^

STARR-seq is an assay to profile self-transcribed active regions (e.g., enhancer). This pipeline produces called peaks for these active regions.

Input
^^^^^

1. fastq.tsv
---------

Use ``run_lsf.py --guess_input`` to automatically generate this.

::

	myDNA1_R1.fastq.gz	myDNA1_R2.fastq.gz	myDNA1
	myDNA2_R1.fastq.gz	myDNA2_R2.fastq.gz	myDNA2
	myRNA1_R1.fastq.gz	myRNA1_R2.fastq.gz	myRNA1
	myRNA2_R1.fastq.gz	myRNA2_R2.fastq.gz	myRNA2
	myRNA3_R1.fastq.gz	myRNA3_R2.fastq.gz	myRNA3

2. peakcall.tsv
------------

A tsv file containing three columns specifying comparisons. For example, RNA sample name, DNA sample name, comparison name. The names have to match the third column specified in fastq.tsv.

Always RNA vs DNA

.. code:: bash

	myRNA1	myDNA1	myRNA1.vs.myDNA1
	myRNA2	myDNA1	anyName
	myRNA3	myDNA2	Who

Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	run_lsf.py --guess_input # to generate fastq.tsv

	starr_seq.py -f fastq.tsv -d peakcall.tsv -g hg19










