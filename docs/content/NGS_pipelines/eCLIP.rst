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

``clipper`` results looks more accurate than ``pureCLIP``, because ``pureCLIP`` predicted binding sites are basically merged bed file from the predicted cross-link sites, and if we look at the signals, these binding sites do not align well with the binding sites. P.S., I don't know why crosslink site is different than binding sites yet.

``clipper`` takes a week to finish for 100-200M bam file (UMI-deduplicated).

Example of clipper output:

::

	# column names
	chr, start, end
	gene_ID|unique ID|read count (default read count cutoff is 3)
	minimal pvalue (clipper has a p-value for each position)
	strand, peak center start, peak center end

::


	chr1    133723  133804  ENSG00000233750.3_0_4   0.006532397293615632    +       133761  133765
	chr1    235687  235773  ENSG00000228463.4_0_3   0.021506732213281816    -       235722  235726
	chr1    329595  329633  ENSG00000233653.3_0_3   0.023548354478527544    -       329611  329615
	chr1    564499  564571  ENSG00000230021.2_0_29  3.452872201838815e-29   -       564545  56454


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

