Functional Variant scores
=========================


DeepSEA
^^^^^^^


URL: https://deepsea.princeton.edu/

Input vcf file as 5 column tsv


Once finished, you can download jobs.zip. Then you can use the ``.funsig`` score, this is similar to a p-value, the smaller the more significant. So you can take a log10 transformation.


CADD
^^^^^^

::

	module load python/2.7.13
	
	cd /home/yli11/dirs/blood_regulome/chenggrp/Data_resource/CADD_score/hg19_v1.4

	# the input vcf should not contain chr string
	# sed 's/chr//g' your_file.vcf > CADD.input.vcf
	python extractCADDscores.py -p whole_genome_SNVs.tsv.gz < ~/Projects/Li_gRNA/get_bp_editbale/run2/gRNA_all_A_nochr.vcf > gRNA_all_A.CADD.vcf

	






