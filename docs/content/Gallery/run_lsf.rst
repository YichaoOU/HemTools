A simple solution to submit LSF jobs
====================================

Summary
^^^^^^^

Suppose I'm going to run the following command(s) for 4 files:

.. code:: bash

	DP_GP_cluster.py -i file1 -o output_prefix --plot --plot_types png -a 0.2 -s 10

Instead of running it 4 times manually, I can submit a job array to the LSF system.

It can be a little time consuming everytime when you submit a job array. Therefore, this script is to help you.

Usage
^^^^^

**1. Prepare input list**

You should have a tab-seperated file containing all the inputs and outputs, define the columns in whatever way you like. I often put input files as the first column and output names as the second column. If you have two inputs, then you can put output names as the third column.

Then, the ``keyword`` for using these columns are: ``${COL1}``, ``${COL2}``, ``${COL3}``. You will see how to use them later.

An example shown below:

.. highlight:: none

:: 

	ETS1_Jurkat.fastq	ETS1_Jurkat
	Jurkat_input.fastq	Jurkat_input

**2. Prepare job file**

A normal LSF job file will look like the following:

.. highlight:: none

:: 

	#BSUB -P chip_seq_single
	#BSUB -o chip_seq_single_yli11_2019-06-20.macs2.message_%J_%I.out -e chip_seq_single_yli11_2019-06-20.macs2.message_%J_%I.err
	#BSUB -n 1
	#BSUB -q standard
	#BSUB -R "span[hosts=1] rusage[mem=30000]"
	#BSUB -J "macs2[1-1]"
	module purge
	#BSUB -w "ended(81082927)"
	module load macs2/2.1.1
	module load bedtools/2.25.0

	id=$LSB_JOBINDEX
	COL1=`head -n $id peakcall.tsv|tail -n1|awk '{print $1}'`
	COL2=`head -n $id peakcall.tsv|tail -n1|awk '{print $2}'`
	COL3=`head -n $id peakcall.tsv|tail -n1|awk '{print $3}'`
	LINE=`head -n $id peakcall.tsv|tail -n1`

	macs2 callpeak -t ${COL1}.bam -c ${COL2}.bam -g hs --keep-dup all -n ${COL3} -B
	YOUR_COMMANDS

In this simple solution, you don't need to worry about remembering/writing all the information. You just need to write down your dependencies (e.g., ``module load macs2/2.1.1``), your input files (e.g., ``peakcall.tsv``), and your commands. For example:


.. highlight:: none

:: 

	=cut run1 1

	module load conda3
	source activate py2

	inputFile=input

	ncore=1
	mem=8000

	DP_GP_cluster.py -i ${COL1} -o ${COL2} --plot --plot_types png -a 0.01 -s 1


In the above example, keywords ``${COL1}`` and ``${COL2}`` are used to specify input and output names, which are strings in the first and second column. 

















