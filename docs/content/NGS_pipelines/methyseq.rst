DNA methylation (Bisulfite-Sequencing) analysis pipeline using nf-core 
===================


::

	usage: methylseq.py [-h] [-j JID] -f INPUT [-q QUEUE] -fa FASTA

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        Methyl_seq_yli11_2022-08-11)
	  -f INPUT, --input INPUT
	                        fastq_tsv (default: None)
	  -q QUEUE, --queue QUEUE
	                        submit queue (default: standard)
	  -fa FASTA, --fasta FASTA
	                        only map to a small region (default: None)




Summary
^^^^^^^

bwa-meth mapping + MethylDackel calling

See https://nf-co.re/methylseq/1.6.1/parameters




Input
^^^^^

Copy paired-end fastq files to a working dir.

.. note:: Make sure your fastq files follow this patter: *_R{1,2}.fastq.gz. So ``ABC.R1.fastq.gz`` will fail, should be ``ABC_R1.fastq.gz``


Usage
^^^^^

This example only uses chr11 sequence for faster computation. We found some regions tend to have reads that are forced mapped by bwa. So it is not recommened to map to just one chr. For testing purposes, it is OK.

::

	hpcf_interactive

	# cd to your workng dir

	module load python/2.7.13

	run_lsf.py --guess_input

	methylseq.py -f fastq.tsv -fa /home/yli11/test/chr11.fa

	# methylseq.py -f fastq.tsv -fa /home/yli11/Data/Human/hg19/mask_genome/hg19.hbg_mask.fa
	# default is to use hgb1 promoter masked hg19 genome
	methylseq.py -f fastq.tsv

You will see the following message indicating the job is submitted.
::

	2022-08-11 15:42:03,451 - INFO - main - The job id is: Methyl_seq_yli11_2022-08-11
	Job <166956652> is submitted to queue <standard>.
	Job <166956653> is submitted to queue <standard>.
	Job <166956654> is submitted to queue <standard>.
	Job <166956656> is submitted to queue <standard>.
	Job <166956657> is submitted to queue <standard>.



Output
^^^^^^

In the jobID folder ``Methyl_seq_yli11_2022-08-11``, you will find results for each sample. The coverage track (``.bedGraph`` file) is inside ``MethylDackel`` folder.

Some post analysis
^^^^^^^^

By default methyldackel give C and G values for each CpG sies, but users just want one value. Run the following pipeline to merge.


::

	[yli11@noderome134 whole_genome_mapping_results_8_17]$ ls > input.list
	[yli11@noderome134 whole_genome_mapping_results_8_17]$ less input.list 
	[yli11@noderome134 whole_genome_mapping_results_8_17]$ vim input.list 
	[yli11@noderome134 whole_genome_mapping_results_8_17]$ run_lsf.py -f input.list -p methyldackel_merge


FAQ
^^^^

One sample was failed due to memory in Picard Markdup, we need to add a config file to increase memory:

https://github.com/nf-core/rnaseq/issues/293

::

	head bigmem.config 
	-----------

	process {
	  withName:markDuplicates {
	    memory = '240 GB'
	    time = '120h'
	  }
	}


::

	bsub -q priority -n 16 -P Methy -R 'span[hosts=1] rusage[mem=15000]' -J Methy nextflow run nf-core/methylseq --input '*_R{1,2}.fastq.gz' -profile singularity --fasta /home/yli11/Data/Human/hg19/mask_genome/hg19.hbg_mask.fa --fasta_index /home/yli11/Data/Human/hg19/mask_genome/hg19.hbg_mask.fa.fai --bwa_meth_index /home/yli11/Data/Human/hg19/mask_genome/hg19.hbg_mask.fa --save_reference --accel --aligner bwameth -resume -c bigmem.config
