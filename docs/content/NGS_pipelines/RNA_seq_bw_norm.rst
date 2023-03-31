Create normalized RNA-seq bigwiggle files
===================================


Input
^^^^^

The input file is a tsv format containing 2 columns: bam, sample name.

Output
^^^^^^

BW files are generated in the ``job ID`` folder 


Usage
^^^^^

Copy your ``bam`` files together with their index files ``.bam.bai`` into your working directory.



.. code:: bash

	# if you haven't logged into compute node, please do hpcf_interactive

	module load python/2.7.13

	# generate input.tsv
	run_lsf.py --guess_input --general --file_pattern bam --replace_name ".bam"

	# submit jobs
	run_lsf.py -f input.tsv -p rna_bw_rpm


Reference
^^^^^^^^^

https://github.com/ENCODE-DCC/long-rna-seq-pipeline/blob/dcd526d4b6d829fe2ffa0df5013eee7a499339f1/dnanexus/bam-to-bigwig/resources/usr/bin/lrna_bam_to_signals.sh



















