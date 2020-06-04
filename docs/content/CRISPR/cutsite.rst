convert gRNA bed file to cutsite bed file
==========================


::

	usage: to_cutsite_bed.py [-h] [-o OUTPUT] -f INPUT
	                         (--offset OFFSET | --ABE | --CBE)

	optional arguments:
	  -h, --help            show this help message and exit
	  -o OUTPUT, --output OUTPUT
	                        output file name, 4 columns (default: cutsite.bed)
	  -f INPUT, --input INPUT
	                        input bed file, 6 columns, chr, start, end, seq,
	                        value, strand (default: None)
	  --offset OFFSET       use cas9 cut site (e.g., -3) as gRNA score (default:
	                        None)
	  --ABE                 ABE mode not implemented (default: False)
	  --CBE                 CBE mode not implemented (default: False)

Summary
^^^^^^^

This program will generate the bed file for cas9 cut positions. User is required to input the offset for Cas9 protein from PAM. spCas9 is -3.





Usage
^^^^^

**Step 0: Load python version 2.7.13.**

.. code:: bash

    module load python/2.7.13

**Step 1: Run the command**

.. code:: bash

	to_cutsite_bed.py -f gRNA.loci307.bed --offset -3 -o gRNA.cutsite.bed


Input and Output
^^^^^^

::

	==> gRNA.cutsite.bed <==
	chr19	13215439	13215440	CTATGCGCAAGCCCGTGGCC
	chr6	135501716	135501717	GACATGTGACAATACGACGG
	chr6	135495900	135495901	GCCTGTAATCACAACACTTT
	chr6	135376057	135376058	CGCATGCGCACTGCTGTGCA
	chr19	12983944	12983945	AGTGGCCAAAGGGGGTGGGT
	chr2	58274508	58274509	CGGCTTCTGGGTACCTTCCC
	chr6	135376617	135376618	TCTCACTCACTTTGTCGCCC
	chr19	13207655	13207656	GGCCCGGGCCGGAGCGTGCC
	chr11	4167489	4167490	TTTACTACCTTCGAAAGTTG
	chr11	5265111	5265112	AACTGCACACTGGATGGTGG

	==> gRNA.loci307.bed <==
	chr19	13215423	13215443	CTATGCGCAAGCCCGTGGCC	0	+
	chr6	135501700	135501720	GACATGTGACAATACGACGG	0	+
	chr6	135495884	135495904	GCCTGTAATCACAACACTTT	0	+
	chr6	135376041	135376061	CGCATGCGCACTGCTGTGCA	0	+
	chr19	12983928	12983948	AGTGGCCAAAGGGGGTGGGT	0	+
	chr2	58274505	58274525	CGGCTTCTGGGTACCTTCCC	0	-
	chr6	135376614	135376634	TCTCACTCACTTTGTCGCCC	0	-
	chr19	13207639	13207659	GGCCCGGGCCGGAGCGTGCC	0	+
	chr11	4167486	4167506	TTTACTACCTTCGAAAGTTG	0	-
	chr11	5265108	5265128	AACTGCACACTGGATGGTGG	0	-


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



























