Download fastq data from NCBI SRA
=================================

**Step 0**

.. highlight:: none

:: 

	hpcf_interactive -q standard -R "rusage[mem=4000]"

**Step 1. Put SRA accession IDs in a file, one per line.**

.. code:: bash

	nano sra_data.list

Copy and paste your SRA IDs.

.. code:: bash

	SRR7633094
	SRR7633093
	SRR7633095
	SRR7633096
	SRR036758
	SRR036759
	SRR036760
	SRR3721861
	SRR3721862
	SRR3721854
	SRR3721853
	SRR5367842

``Control + o`` save.

``Control + x`` exit.

**Step 2**

.. highlight:: none

:: 

	module load sra_toolkit/2.8.1.3

	dos2unix sra_data.list

	for i in `cat sra_data.list`; do echo $i; prefetch -v $i; fastq-dump --outdir . --split-files ~/ncbi/public/sra/$i.sra;done

The output fastq files will be, for example, ``SRR5367842.fastq``. Please remember to rename it using the metainfo.


.. note:: "The problem with SRA is that a fair number of uploaded datasets are simply crap, i.e., people uploaded poorly formatted or incorrect data. For all ERR* datasets, do not use SRA. Download the original fastq files from ENA. If those have different numbers of reads then that's what was uploaded.""



