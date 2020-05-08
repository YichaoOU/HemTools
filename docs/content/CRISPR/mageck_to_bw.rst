Convert MaGeCK RRA sgRNA results to bw tracks
==========================


::

	usage: Mageck2bw.py [-h] [-o OUTPUT] -f MAGECK_RRA -b GRNA_BED
	                    (--cas9 | --ABE | --CBE) [-g GENOME] [-s CHROM_SIZE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -o OUTPUT, --output OUTPUT
	                        output file name, output_FDR.bw, output_LFC.bw,
	                        output_FDR.bdg, output_LFC.bdg (default: output)
	  -f MAGECK_RRA, --mageck_RRA MAGECK_RRA
	                        mageck_RRA sgRNA summary file (default: None)
	  -b GRNA_BED, --gRNA_bed GRNA_BED
	                        gRNA bed file, need strand info (default: None)
	  --cas9                use cas9 cut site (-3) as gRNA score (default: False)
	  --ABE                 ABE mode (default: False)
	  --CBE                 CBE mode (default: False)

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

Generate LFC and FDR tracks given Mageck RRA results.

Input
^^^^^

1. Mageck RRA sgRNA results

File: ``/home/yli11/test/ABE_high_vs_low_mageck_RRA_results.sgrna_summary.txt``

::

sgrna	Gene	control_count	treatment_count	control_mean	treat_mean	LFC	control_var	adj_var	score	p.low	p.high	p.twosided	FDR	high_in_treatment
chr19:13190675-TGCTGCCTGTGTAGAGGGCC	chr19:13190380-13190550	2.3734/6.9212	272.09/293.85	4.6473	282.97	5.652	10.342	11.686	81.417	1	0	0	0	True
chr11:5306112-TACTCATGGTCTATCTCTCC	chr11:5305920-5306090	252.76/250.89	2342.7/2282.8	251.83	2312.8	3.194	1.7444	1243.7	58.439	1	0	0	0	True
chr2:57948343-ACGAGGCCAGGAAGACACAG	chr2:57948080-57948230	386.86/415.27	2447.9/2378.2	401.07	2413	2.586	403.76	2167	43.221	1	0	0	0	True
chr11:5173389-TATCTGAATGACAAGCTGGT	chr11:5173040-5173250	59.334/50.179	623.5/674.32	54.756	648.91	3.543	41.907	204.44	41.554	1	0	0	0	True
chr11:5248516-AGGGCTGGGCATAAAAGTCA	chr11:5248300-5248490	192.24/174.76	1285.7/1348.1	183.5	1316.9	2.8366	152.79	853.54	38.795	1	0	0	0	True
chr11:5264509-GCACTGTAACAAGCTGCACG	chr11:5264320-5264470	315.66/176.49	1586.4/1585.5	246.07	1585.9	2.6832	9683.4	1210	38.519	1	0	0	0	True
chr11:5646581-TATCAGTGTGCACTCAAAGC	chr11:5646340-5646490	354.82/304.53	1641.8/1828.3	329.68	1735.1	2.3923	1264.2	1714.7	33.939	1	8.893e-253	1.7786e-252	1.5791e-249	True
chr11:5256103-TGCGGTGGGGAGATATGTAG	chr11:5255800-5255990	325.15/389.32	1837.3/1794.9	357.23	1816.1	2.3427	2058.9	1887.2	33.582	1	1.5248e-247	3.0495e-247	2.3691e-244	True
chr19:12952224-GCGGGGCCTATAAGAAGGCG	chr19:12952024-12952190	176.82/257.82	1332.8/1270.8	217.32	1301.8	2.5771	3280.6	1043.6	33.57	1	2.3175e-247	4.635e-247	3.2007e-244	True

The ``sgrna`` column should contain sgRNA sequence, which could be just sgRNA sequence or any name ending with sgRNA sequence.

2. gRNA bed file

File: ``/home/yli11/Data/gRNA_libary/ruopeng_library/gRNA.loci307.bed.sorted``

::

	chr11	4167374	4167394	ACAAGCAACAGTTGACCAAC	0	+
	chr11	4167375	4167395	CAAGCAACAGTTGACCAACA	0	+
	chr11	4167392	4167412	CTCAACAGCAGGTTCCCTGT	0	-
	chr11	4167403	4167423	CAGATTACGGGCTCAACAGC	0	-
	chr11	4167406	4167426	GTTGAGCCCGTAATCTGCTG	0	+
	chr11	4167415	4167435	AAATTTCCTCAGCAGATTAC	0	-
	chr11	4167416	4167436	CAAATTTCCTCAGCAGATTA	0	-
	chr11	4167441	4167461	AGCAGGCAGTACTCAGGGAC	0	-
	chr11	4167446	4167466	AGATAAGCAGGCAGTACTCA	0	-
	chr11	4167447	4167467	GAGATAAGCAGGCAGTACTC	0	-

The columns should be chr, start, end, gRNA_sequence, value (not used), strand (required). 

Usage
^^^^^


.. code:: bash

	hpcf_interative.sh

	module load python/2.7.13

	module load ucsc/041619

	Mageck2bw.py -f /home/yli11/test/ABE_high_vs_low_mageck_RRA_results.sgrna_summary.txt -b /home/yli11/Data/gRNA_libary/ruopeng_library/gRNA.loci307.bed.sorted --cas9 -o HbF


Output
^^^^^^


::

	-rwxrwx--- 1 yli11 chenggrp  254K Mar 10 16:48 HbF.FDR.bdg
	-rwxrwx--- 1 yli11 chenggrp  205K Mar 10 16:48 HbF.LFC.bdg
	-rwxrwx--- 1 yli11 chenggrp  152K Mar 10 16:48 HbF.FDR.bw
	-rwxrwx--- 1 yli11 chenggrp  158K Mar 10 16:48 HbF.LFC.bw



Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



























