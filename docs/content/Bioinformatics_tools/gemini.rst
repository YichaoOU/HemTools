Annotate vcf file (custom annotation not work)
====================



Summary
^^^^^^^

I found this tool when I try to add GERP score to my vcf files. I tried SnpSift. Built 4.0a database, not working. I then downloaded version 2.9 database, for my >100k variants, it only annotated 450 SNPs, and the GERP scores are all similar for different position. So I gave up on this tool, although it does have a more visually-appealing documentation and capacity to add custom files to annotation database.

Gemini is developed by the same author from bedtools. So I know it must have good quality.

Installation is easy but there is a trick. You can use conda to install it. But conda won't create annotation database for you. So you have to create ``~/.gemini/`` folder and create a yaml file ``gemini-config.yaml`` like below:

::

	annotation_dir: /home/yli11/.gemini/data
	versions:
	  ALL.wgs.phase3_shapeit2_mvncall_integrated_v5a.20130502.sites.tidy.vcf.gz: 4
	  ESP6500SI.all.snps_indels.tidy.v2.vcf.gz: 2
	  ExAC.r0.3.sites.vep.tidy.vcf.gz: 4
	  GRCh37-gms-mappability.vcf.gz: 2
	  cosmic-v68-GRCh37.tidy.vcf.gz: 3
	  detailed_gene_table_v75: 2
	  geno2mp.variants.tidy.vcf.gz: 1
	  hg19.rmsk.bed.gz: 2
	  summary_gene_table_v75: 2

Then do a ``gemini update --dataonly --extra gerp_bp``.

You are good to go now.

The latest gemini version only works for hg19.

Input
^^^^^^^

Input must be a vcf file like below:

::

	##fileformat=VCFv4.1
	#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
	11	4167375	11_4167374_4167375	A	G	.	.	.
	11	4167377	11_4167376_4167377	A	G	.	.	.
	11	4167378	11_4167377_4167378	A	G	.	.	.
	11	4167381	11_4167380_4167381	A	G	.	.	.
	11	4167382	11_4167381_4167382	A	G	.	.	.
	11	4167384	11_4167383_4167384	A	G	.	.	.
	11	4167389	11_4167388_4167389	A	G	.	.	.
	11	4167392	11_4167391_4167392	A	G	.	.	.

Usage
^^^^^^^

.. code:: bash

	module load conda3

	source activate /home/yli11/.conda/envs/variant

	gemini --annotation-dir /home/yli11/.gemini/data load --save-info-string -v input.vcf output.db

	## this output.db is a binary file

	gemini query --header -q "select * from variants" output.db > my_results.tsv

Output
^^^^^^^

See ``my_results.tsv`` from the commands above.
