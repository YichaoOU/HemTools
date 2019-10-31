Filter bam files and generate bw files
======================


::

	usage: bam_to_bw.py [-h] [-j JID] [--bamCoverage_addon BAMCOVERAGE_ADDON]
	                    [-g GENOME] [-e EFFECTIVEGENOMESIZE]
	                    file [file ...]

	positional arguments:
	  file

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        bam_to_bw_yli11_2019-10-31)
	  --bamCoverage_addon BAMCOVERAGE_ADDON
	                        for PE data, you add --center to get sharper peaks
	                        (default: "")

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -e EFFECTIVEGENOMESIZE, --effectiveGenomeSize EFFECTIVEGENOMESIZE
	                        effectiveGenomeSize for bamCoverage (default:
	                        2451960000)



Summary
^^^^^^^

Read all bam files in the current dir, keep only properly paired mapped reads (``-f 3``) and remove ummapped and duplicated reads (``-F 4 -F 8 -F 1024``). Lastly, generate bw files using the filtered bam files.

Input
^^^^^

No need to prepare an input list of files. This program will parse all files in a specified pattern.

For example:

``*.bam`` will match all bam files in the current dir.

``../../../*.rmdup.bam`` will match all rmdup.bam files in up 3 dir level. 

Output
^^^^^^

See ``bam_files`` folder and ``bw_files`` folder.


Usage
^^^^^

Suppose all your bam files are in the current working dir.

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	bam_to_bw.py *.bam

For PE data, use:

.. code:: bash

	bam_to_bw.py *.bam --bamCoverage_addon " --center"


Source code
^^^^


.. code:: bash


	inbam=$(basename ${COL1})
	outbam=${inbam%.bam}.filtered.bam
	outbw=${inbam%.bam}.bw

	ln -s ${COL1} {{jid}}/$inbam

	cd {{jid}}

	# filter
	samtools view -b -h -f 3 -F 4 -F 8 -F 1024 -o $outbam $inbam

	# index filter bam

	samtools sort $outbam -o ${outbam}.sorted
	rm $outbam
	mv ${outbam}.sorted $outbam
	samtools index $outbam

	# bam Coverage

	module purge
	module load python/2.7.15-rhel7

	bamCoverage -b $outbam -o $outbw --smoothLength=200 --ignoreForNormalization chrX chrM  --effectiveGenomeSize {{effectiveGenomeSize}} --numberOfProcessors 4 {{bamCoverage_addon}}

	rm $inbam











