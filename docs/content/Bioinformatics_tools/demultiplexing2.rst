CRISPR Screening Demultiplexing (hard trim first N random bp)
=============================================================

.. note:: This protocol assumes your barcode is located after 4 random bp beginning at 5'-end.

Summary
^^^^^^^

We will remove the first 4 base pairs and then do the same thing as described in :doc:`this post <demultiplexing>`.

Usage
^^^^^

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

Edit and save the file in ``sublime text``, and then use ``FileZilla`` to upload it to HPC.


**Step 2: Submit job**

.. tip::
	You can change the requested memory in ``rusage[mem=10000]``. This example requests 10G memory. If the original fastq.gz file is less than 20G, then it doesn't need much memory. 

.. code:: bash

	#BSUB -P split
	#BSUB -oo split.out -eo split.err
	#BSUB -n 1
	#BSUB -q standard
	#BSUB -R "rusage[mem=10000]"
	#BSUB -J "Demultiplex"

	module load python/3.7.0

	cutadapt --cut 4 -o output.fastq.gz gRNA_S1_R1_001.fastq.gz

	/home/yli11/HemTools/bin/dos2unix barcode.fa

	cutadapt \
	--no-indels \
	-g file:barcode.fa \ 
	--no-trim \ 
	--untrimmed-output untrimmed.fastq.gz \
	-o {name}.fastq.gz \
	output.fastq.gz


``barcode.fa`` is the barcode file

``gRNA_S1_R1_001.fastq.gz`` is the fastq file to be demultiplexed.

You can copy and edit the above code in ``sublime text``, and save it as ``split.lsf`` and then use ``FileZilla`` to upload it to HPC. For example, you need to change the input file name (i.e., ``gRNA_S1_R1_001.fastq.gz``) to yours.

Once you have the ``split.lsf`` on HPC, you can do the following to submit the job.

.. code:: bash

	/home/yli11/HemTools/bin/dos2unix split.lsf
	bsub < split.lsf
