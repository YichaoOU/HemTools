eCLIP-seq data analysis pipeline
===================================

Summary
^^^^^^^

Pipeline adopted from https://www.encodeproject.org/documents/739ca190-8d43-4a68-90ce-1a0ddfffc6fd/@@download/attachment/eCLIP_analysisSOP_v2.2.pdf

Only work for hg19 right now, by 6/6/2022.

Pipeline has been tested using the ENCODE data from K562: blood_regulome/chenggrp/Projects/Siqi_data/CLIP/RBM9_Public/RBM9_K562

Input
^^^^^

fastq.tsv
-------

Depending on single-end or paired-end, you might use ``run_lsf.py --guess_input`` or ``run_lsf.py --guess_input --single`` to automatically generate this file.

::

	Banana_R1.fastq.gz	Banana_R2.fastq.gz	Banana_lovers
	Orange_R1.fastq.gz	Orange_R2.fastq.gz	Orange_lovers


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	# for paired-end data
	run_lsf.py -f fastq.tsv -p eclip_pe

	# for single-end data
	run_lsf.py -f fastq.tsv -p eclip_se


Output
^^^^^^

1. eCLIP QC report
-----------------

Please check the QC in the html file.

2. strand specific signals
----------------------

See the bw files

3. called peaks
---------------

See the bed files.

QC
^^^^^

eCLIP experiments should have 1 million unique fragments or have saturated peak detection in each biological replicate.

The following stats are obtained by re-analysis ENCODE data, not part of the data standards.

FASTqc: duplicates, 30%-40%, input control maybe up to 60%.

STAR align of rRNA removed reads, ~40% mapping rate. Input control maybe lower.

Reference
^^^^^^^

1. https://www.genome.gov/sites/default/files/Multimedia/Slides/ENCODE2016-ResearchAppsUsers/vanNostrand_eCLIP.pdf


2. https://eclipsebio.com/wp-content/uploads/2022/03/RBP-eCLIP-Protocol-1.pdf

3. https://www.nature.com/articles/nmeth.3810

4. https://www.encodeproject.org/eclip/

