CRISPR Screening Demultiplexing
===============================

.. note:: This protocol assumes your barcodes locating at 5'-end


**Step 1: Prepare barcode.fa**

.. note::
	Your barcode file must start with ``^``. The ``^`` is supposed to indicate the the adapter is "anchored" at the beginning of the read. 

.. highlight:: none

:: 

	>BE_D5_R1
	^GCATGCAC
	>BE_D5_R2
	^TACGATGC
	>ABE_DIFF_D5_R1
	^CTATAGAG



**Step 2: Submit job**

.. tip::
	You can change the requested memory in ``rusage[mem=10000]``. This example requests 10G memory. If the original fastq.gz file is less than 20G, then it doesn't need much memory. 

.. code:: bash

	#BSUB -P split
	#BSUB -oo split.out -eo split.err
	#BSUB -n 1
	#BSUB -q standard
	#BSUB -R "rusage[mem=10000]"

	module load python/3.7.0

	cutadapt \
	--no-indels \
	-g file:barcode.fa \ 
	--no-trim \ 
	--untrimmed-output untrimmed.fastq.gz \
	-o {name}.fastq.gz \
	gRNA_S1_R1_001.fastq.gz


``barcode.fa`` is the barcode file

``gRNA_S1_R1_001.fastq.gz`` is the fastq file to be demultiplexed.



