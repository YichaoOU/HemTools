Hybrid transcript quantification (ISOseq+RNAseq) with miniQuant
================================================

Summary
^^^^^^^

Ref: https://github.com/Augroup/miniQuant (miniQuant v1.4.1) and https://www.nature.com/articles/s41587-025-02633-9

miniQuant estimates transcript abundance by EM over a colored de Bruijn graph built from a reference transcript FASTA. No alignment, no BAM. This pipeline always runs **miniQuant-H** (hybrid): long reads and short reads go into one joint EM, weighted per gene by a learned model. It also computes **K-value**, which flags genes whose isoforms share enough sequence to make quantification error-prone.

``Hybrid mode requires matched short-read RNA-seq for every sample.``


Input format
^^^^^^^^^^^^^^^^^^^

**input.tsv**

This is a tab-seperated-value format file. The 4 columns are: long reads, short read 1, short read 2, sample ID.

::

	/path/3472835.fastq   /path/NT_1_R1.fq.gz   /path/NT_1_R2.fq.gz   H2_NT_1
	/path/3472837.fastq   /path/M2_1_R1.fq.gz   /path/M2_1_R2.fq.gz   H2_g2_1

Long reads may be plain or gzipped FASTA/FASTQ.

Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	run_lsf.py -p miniQuant -f input.tsv -g hg38

Output
^^^^^^

1. abundance.tsv, one per sample
---------------------------------

``<jid>_results/<sample>/abundance.tsv`` -- the only file miniQuant itself writes.

===================================  ==========================================
column                                unit
===================================  ==========================================
``Transcript_id``                     transcript id from the reference FASTA
``TPM``                               transcripts per million (sums to 1e6)
``Expected_num_long_reads``           reads, fractional (EM posterior)
``Expected_num_short_read_pairs``     read **pairs**, fractional
``Effective_length``                  bp
===================================  ==========================================

It contains the transcript id only, **no gene name** -- miniQuant never reads a GTF during ``quant``.

2. merged matrices
-------------------


* ``miniQuant_TPM_hybrid.tsv``
* ``miniQuant_counts_longreads_hybrid.tsv``
* ``miniQuant_counts_shortreadpairs_hybrid.tsv``

Each is laid out as ``transcript_id | gene_name | gene_id | kvalue | <one column per sample>``.




Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines
