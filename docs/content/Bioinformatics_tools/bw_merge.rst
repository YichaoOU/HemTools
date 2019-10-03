Merging bigwiggle files into one bw
===================================

::

	usage: bw_merge.py [-h] [-j JID] [-o OUTPUT]
	                   (--glob GLOB | -l LIST | -f INPUT) [-g GENOME]
	                   [-s CHROM_SIZE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        bw_merge_yli11_2019-10-02)
	  -o OUTPUT, --output OUTPUT
	                        Output Name (default: merged)
	  --glob GLOB           Matching substring in the current dir (default: None)
	  -l LIST, --list LIST  Input a file containing a list of bw files (default:
	                        None)
	  -f INPUT, --input INPUT
	                        Input file names seperated by , (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -s CHROM_SIZE, --chrom_size CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Human/hg19/anno
	                        tations/hg19.chrom.sizes)


Summary
^^^^^^^

``bigWigMerge``: Merge together multiple bigWigs into a single bw file. The signal values are just added together to merge them. 

.. note:: By default, genome is hg19.

Usage
^^^^^

There are 3 ways to use this program.

Example 1: Merge all bw files that match to a common string
---------

The following code will merge all bw files that match to ``*CTCF*all.bw``

.. code:: bash

	bw_merge.py --glob "*CTCF*all.bw"

.. note:: quotation mark here is required.

Example 2: Specify the files in a list
---------

::

	input.list
	----------

	1047946_Hudep1_CTCFIP.all.bw
	1047946_Hudep1_CTCFIP.rmdup.bw
	1047946_Hudep1_CTCFIP.rmdup.uq.bw

.. code:: bash

	bw_merge.py -l input.list

Example 3: Specify the filenames
---------

File names are separated by ,

.. code:: bash

	bw_merge.py -f 1047946_Hudep1_CTCFIP.all.bw,1047946_Hudep1_CTCFIP.rmdup.bw


Output
^^^^^^

The merged bw file ``merged.bw`` is located at jobID folder. You can also specify the output filename using ``-o`` option.

FAQ
^^^

Known issue: ChIP-seq IgG or input tracks can't be merged. I don't know why.

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines

