Call interactions from HiC
=============

::


	usage: hic_interactions.py [-h] [-j JID] -f HIC --chr CHR [--juicer_commands JUICER_COMMANDS] [-b BED] [--juicer_tools_path JUICER_TOOLS_PATH] [--HICCUPS_parameters HICCUPS_PARAMETERS]
	                           [-g GENOME]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory. Every output will be moved into this folder. (default: hic_interactions_yli11_2021-07-23)
	  -f HIC, --hic HIC     .hic file (default: None)
	  --chr CHR             which chr to call (default: None)
	  --juicer_commands JUICER_COMMANDS
	                        juicer_tools commands to call interactions (default: None)
	  -b BED, --bed BED     user input bed file to subset interactions (default: None)
	  --juicer_tools_path JUICER_TOOLS_PATH
	                        juicer_tools_path (default: /home/yli11/HemTools/share/script/jar/juicer_tools_1.13.01.jar)
	  --HICCUPS_parameters HICCUPS_PARAMETERS
	                        HICCUPS_parameters relaxed (best for now) (default: -r 25000 -k VC_SQRT -f 0.2 -p 2 -i 5 -t 0.02,1.5,1.75,2 -d 20000 --cpu)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. Used for homer annotation (default: hg19)


Summary
^^^^^

From ``.hic`` file, call interactions using juicer_tools (specifically, HICCUPS), then given a user input bed file, extract all the regions interacted with this bed file.

The current parameter ``-r 25000 -k VC_SQRT -f 0.2 -p 2 -i 5 -t 0.02,1.5,1.75,2 -d 20000 --cpu``, is almost the same as the default parameter used for Medium resolution HiC data: https://github.com/aidenlab/juicer/wiki/HiCCUPS 

But I found ``-k VC_SQRT -f 0.2`` tends to give more called interactions.

Current program use the union of 10k, 25k, 50k, and merged called interactions.

Usage
^^^^^

::

	cd /home/yli11/dirs/genome_browser/yli11/Antonio/relaxed_analysis

::


	=cut hic 1

	inputFile=input

	ncore=1
	mem=20000
	q=priority

	module load conda3

	source activate captureC

	hic_interactions.py -f ${COL1} -j ${COL2} -g ${COL3} -b ${COL4} --chr X

Input
^^^^^


hic file, a bed file, a specific chr to call interactions (speed consideration)


Output
^^^^^

The final output is homer annotated. ``{{jobID}}.{{bed file name column, i.e., 4th column}}.annot.tsv``


Comments
^^^^^^^^

.. disqus::
	:disqus_identifier: NGS_pipelines



