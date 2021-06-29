Smoothing a bedgraph file 
=============


::

	usage: smooth_bedgraph.py [-h] [-j JID] -f INPUT_LIST [-w WINDOW_SIZE]
	                          [-s STEP_SIZE] [-g GENOME] [-cs CHROM_SIZE]

	Smooth bedgraph

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        smooth_bedgraph_yli11_2021-06-29)
	  -f INPUT_LIST, --input_list INPUT_LIST
	                        a list of bedgraph files (default: None)
	  -w WINDOW_SIZE, --window_size WINDOW_SIZE
	                        window size (default: 200)
	  -s STEP_SIZE, --step_size STEP_SIZE
	                        step size (default: 20)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -cs CHROM_SIZE, --chrom_size CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Human/hg19/anno
	                        tations/hg19.chrom.sizes)




Summary
^^^^^

This tool will smooth a bedgraph file given a window size and step size using ``bedops``. Main command behind this tool is:

::

	bedops -w $window_size --stagger $step_size --range $window_size $$.temp.ref | bedmap --skip-unmapped --faster --echo --mean --delim "\t" --bases-uniq-f - $$.temp.ref | awk -F "\t" '{print ($1"\t"$2"\t"$2+1"\t"$4*$5)}' > $(basename ${COL1}).smooth.bdg

Using ``-w`` and ``-s`` to control smoothness. Basically, the higher ``w/s`` ratio, the more smoothed output it will be.

Usage
^^^^^

Copy and paste all bedgraph files (e.g., *.bdg or *bedgraph or *wig) into your working directory, and:

::

	hpcf_interactive

	module load python/2.7.13

	ls * > input.list

	smooth_bedgraph.py -f input.list -g hg19

Output
^^^^^

Smoothed bw file will be stored in the {{jid}} folder.


Comments
^^^^^^^^

.. disqus::
	:disqus_identifier: NGS_pipelines



