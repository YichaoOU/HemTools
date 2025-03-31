PRO-seq analysis pipeline
===================

::

	usage: run_proseq.py [-h] [-i INPUT_FILE] [-j JOB_NAME] [-g {hg38,hg19,mm10,custom}] [--genome_index GENOME_INDEX] [-s GENOME_SIZE_FILE] [-a1 READ1_ADAPTER] [-a2 READ2_ADAPTER] [-l MIN_LENGTH] [--umi_pattern {regex,string}]
	                     [-u1 READ1_UMI] [-u2 READ2_UMI] [-n CPU]

	optional arguments:
	  -h, --help            show this help message and exit
	  -i INPUT_FILE, --input_file INPUT_FILE
	                        tab separated file with fastq file and name
	  -j JOB_NAME, --job_name JOB_NAME
	                        this will be used to create output directory
	  -g {hg38,hg19,mm10,custom}, --genome {hg38,hg19,mm10,custom}
	                        different genome versions available. Default = hg19. incase of custom genome provide index path in --genome_index
	  --genome_index GENOME_INDEX
	                        genome index for custom genome file
	  -s GENOME_SIZE_FILE, --genome_size_file GENOME_SIZE_FILE
	                        genome size file for custom genome
	  -a1 READ1_ADAPTER, --read1_adapter READ1_ADAPTER
	                        adapter sequence for read1
	  -a2 READ2_ADAPTER, --read2_adapter READ2_ADAPTER
	                        adapter sequence for read2
	  -l MIN_LENGTH, --min_length MIN_LENGTH
	                        minimum length after trimming adapters. Default value is set to 17
	  --umi_pattern {regex,string}
	                        default value is regex for umi extraction
	  -u1 READ1_UMI, --read1_umi READ1_UMI
	                        umi regex pattern for read1, this is for the umi at 3 prime end
	  -u2 READ2_UMI, --read2_umi READ2_UMI
	                        umi regex pattern for read2, this is for the umi at 3 prime end
	  -n CPU, --cpu CPU     number of processors, default = 10



Summary
^^^^^^



Input
^^^^^



Usage
^^^^^


.. code:: bash


	export PATH=$PATH:"/home/yli11/HemTools/bin"
	hpcf_interative.sh
	module load conda3/202402
	source activate /home/yli11/.conda/envs/jupyterlab_2024
	run_proseq.py
