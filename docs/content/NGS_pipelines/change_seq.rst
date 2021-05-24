CHANGE-seq analysis pipeline
===================

::

	usage: changeseq.py [-h]
	                    {all,parallel,align,merge,identify,visualize,variants,reference-free}
	                    ...

	optional arguments:
	  -h, --help            show this help message and exit

	subcommands:
	  Individual Step Commands

	  {all,parallel,align,merge,identify,visualize,variants,reference-free}
	                        Use this to run individual steps of the pipeline
	    all                 Run all steps of the pipeline
	    parallel            Run all steps of the pipeline in parallel
	    align               Run alignment only
	    merge               Merge paired end reads
	    identify            Run identification only
	    visualize           Run visualization only
	    variants            Run variants analysis only
	    reference-free      Run reference-free discovery only


Summary
^^^^^^

(1) Three new YAML parameters to specify:

	1. PAM sequence (default: ``PAM: NGG``)
	2. Read count threshold for off-target calling (default:  ``read_count_cutoff: 6``)
	3. Read length parameter for outputs from different sequencing platform (default:  ``read_length: 151``)

(2) Fix the code to get the ‘realigned target sequence’ to use the new feature in regex library that provides fuzzy_changes

(3) Fix bug in visualization.py where it stops when no off-targets are found

(4) Add control read counts to output

Input
^^^^^

A YAML file, (same as before, the three new parameters are not required)

::

	reference_genome: data/input/CIRCLEseq_test_genome.fa
	analysis_folder: data/MergedOutput

	bwa: bwa
	samtools: samtools

	window_size: 3
	mapq_threshold: 50
	start_threshold: 1
	gap_threshold: 3
	mismatch_threshold: 6
	merged_analysis: True
	PAM: NGG
	read_count_cutoff: 6
	read_length: 151

	samples:
	    TestSample:
	        target: GAGTCCGAGCAGAAGAAGAANGG
	        read1: data/input/TEST.r1.fastq.gz
	        read2: data/input/TEST.r2.fastq.gz
	        controlread1: data/input/TEST_control.r1.fastq.gz
	        controlread2: data/input/TEST_control.r2.fastq.gz
	        description: TestCell

Usage
^^^^^


.. code:: bash


	export PATH=$PATH:"/home/yli11/HemTools/bin"
	hpcf_interative.sh
	module load conda3
	source activate /home/yli11/.conda/envs/change_seq
	module load bwa
	# copy test data
	cp -r /home/yli11/Tools/changeseq/test .
	cd test
	changeseq.py all -m CIRCLEseq_MergedTest.yaml

Output files are located in ``data/MergedOutput/``



