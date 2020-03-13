Uditas
===================================

::

	uditas -h
	usage: uditas [-h] [-folder_genome_2bit FOLDER_GENOME_2BIT]
	              [-skip_demultiplexing SKIP_DEMULTIPLEXING]
	              [-skip_trimming SKIP_TRIMMING]
	              [-skip_genome_local_alignment SKIP_GENOME_LOCAL_ALIGNMENT]
	              [-skip_genome_global_alignment SKIP_GENOME_GLOBAL_ALIGNMENT]
	              [-process_amplicon PROCESS_AMPLICON]
	              [-skip_amplicon_global_alignment SKIP_AMPLICON_GLOBAL_ALIGNMENT]
	              [-check_plasmid_insertions CHECK_PLASMID_INSERTIONS]
	              [-skip_plasmid_alignment SKIP_PLASMID_ALIGNMENT] [-ncpu NCPU]
	              [-window_size WINDOW_SIZE]
	              [-default_amplicon_window_around_cut DEFAULT_AMPLICON_WINDOW_AROUND_CUT]
	              [-min_MAPQ MIN_MAPQ] [-min_AS MIN_AS]
	              [-process_AMP_seq_run PROCESS_AMP_SEQ_RUN]
	              dir_sample

	Process UDiTaS data

	positional arguments:
	  dir_sample            Directory with the sample to be processed

	optional arguments:
	  -h, --help            show this help message and exit
	  -folder_genome_2bit FOLDER_GENOME_2BIT
	                        Folder containing the 2bit file(s) with the reference
	                        genome being used (default:
	                        /home/yli11/Data/Human/hg38/)
	  -skip_demultiplexing SKIP_DEMULTIPLEXING
	                        Skip demultiplexing? Options: 0, 1 (skip) (default: 0)
	  -skip_trimming SKIP_TRIMMING
	                        Skip adapter trimming? Options: 0, 1 (skip) (default:
	                        0)
	  -skip_genome_local_alignment SKIP_GENOME_LOCAL_ALIGNMENT
	                        Skip genome-wide local alignment? Options: 0 , 1
	                        (skip) (default: 1)
	  -skip_genome_global_alignment SKIP_GENOME_GLOBAL_ALIGNMENT
	                        Skip genome-wide global alignment? Options: 0 , 1
	                        (skip) (default: 0)
	  -process_amplicon PROCESS_AMPLICON
	                        Select row number (0-based) of amplicon to process,
	                        set to all to process all amplicons (default: all)
	  -skip_amplicon_global_alignment SKIP_AMPLICON_GLOBAL_ALIGNMENT
	                        Skip amplicon global alignment? Options: 0, 1 (skip)
	                        (default: 0)
	  -check_plasmid_insertions CHECK_PLASMID_INSERTIONS
	                        Check for plasmid insertions. Options: 0 (skip), 1
	                        plamid_name and plasmid_sequence required in
	                        sample_info.csv (default: 1)
	  -skip_plasmid_alignment SKIP_PLASMID_ALIGNMENT
	                        Skip plasmid alignment? Note, just alignment. Counts
	                        still evaluated. Options: 0, 1 (skip) (default: 0)
	  -ncpu NCPU            Number of CPUs to use (default: 4)
	  -window_size WINDOW_SIZE
	                        Window size around cut sites used to grab UDiTaS reads
	                        (default: 15)
	  -default_amplicon_window_around_cut DEFAULT_AMPLICON_WINDOW_AROUND_CUT
	                        Window size around cut sites used to create amplicons
	                        (default: 1000)
	  -min_MAPQ MIN_MAPQ    Minimum mapping quality to include a read (default: 5)
	  -min_AS MIN_AS        Minimum alignment score to include a read (default:
	                        -180)
	  -process_AMP_seq_run PROCESS_AMP_SEQ_RUN
	                        Set to 1 to process an AMP-seq run using GUIDE-seq
	                        adapters (default: 0)


Summary
^^^^^^^

UDiTaS (UniDirectional Targeted Sequencing) is a method to capture small indels and structural rearrangements. 

Input
^^^^^

A folder that contains:

- R1.fastq.gz
- R2.fastq.gz
- I1.fastq.gz
- I2.fastq.gz
- sample_info.csv

``sample_info.csv`` this file name is fixed, has to be exactly the same. Format can be found here: https://github.com/editasmedicine/uditas/blob/master/data/fig2c/sample_info.csv

fastq file names have to be exactly the same except for R1, R2, I1, I2.


Usage
^^^^^

.. code:: bash

	hpcf_interactive -q standard -R "rusage[mem=20000]"

	module load conda3

	source activate /home/yli11/.conda/envs/uditas_env

	export BOWTIE2_INDEXES=/home/yli11/Data/Human/hg38/bowtie2/

	export GENOMES_2BIT=/home/yli11/Data/Human/hg38/

	module load bowtie2/2.2.9

	uditas /path/to/your/input_folder

Output
^^^^^^

Output files are located inside the input_folder

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines

