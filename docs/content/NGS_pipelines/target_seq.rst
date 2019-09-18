Target-Seq analysis
===================


Summary
^^^^^^^


Input
^^^^^


Usage
^^^^^

Go to your data directory and type the following.

**Step 0: Load python version 2.7.13.**

.. code:: bash

    module load python/2.7.13

**Step 1: Run the program**

.. code:: bash

	idr_peaks.py -r1 R1_input -r2 R2_input -g hg19 --macs_genome hs


Note that if you are working on mouse genome, you have to change both ``-g`` and ``--macs_genome`` options, for example:

.. code:: bash

	idr_peaks.py -r1 R1_input -r2 R2_input -g mm9 --macs_genome mm

Output
^^^^^^

IDR peaks is shown in ``idr_peaks.bed``

You can also find outputs from homer analysis: ``homer_motifs_result`` and ``idr_peaks.annotated.tsv``




Ref: https://hbctraining.github.io/Intro-to-ChIPseq/lessons/07_handling-replicates-idr.html



