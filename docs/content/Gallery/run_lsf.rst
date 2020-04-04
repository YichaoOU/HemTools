A simple solution to submit LSF jobs
====================================

Motivation
^^^^^^^

Suppose I'm going to run the following command(s) for 4 files:

.. code:: bash

	DP_GP_cluster.py -i file1 -o output_prefix --plot --plot_types png -a 0.2 -s 10

Instead of running it 4 times manually, I can submit a job array to the LSF system.

It can be a little time consuming everytime when you submit a job array. Moreover, it is likely that your pipeline is a tree structure, meaning that job2 depends on job1 and maybe job3 can be paralleled and job4 has to wait for all job3 finished. In all these cases, this script is to help you.

Summary
^^^^^^^

This solution, based on some new syntax, can help you:

1. run the same script for a list of files

2. job dependency

3. help you implement parallel jobs

Usage
^^^^^

**1. Prepare input list**

You should have a tab-seperated file containing all the inputs, parameters, and outputs. I often put input files as the first column and output names as the second column, and parameters in other columns.

Then, the ``keyword`` for using these columns are: ``${COL1}``, ``${COL2}``, ``${COL3}``, upto ``${COL8}``. You will see how to use them later.

An example shown below:

.. highlight:: none

:: 

	ETS1_Jurkat.fastq	ETS1_Jurkat	3
	Jurkat_input.fastq	Jurkat_input	5

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


In the above example, keywords ``${COL1}`` and ``${COL2}`` are used to specify input and output names, which are strings in the first and second column. ``=cut`` is a keyword declaring a new job, followed by job name, index number and optional dependent job. 

``inputFile=input`` is a keyword, you have to have this line in every ``=cut`` declared jobs if you have a input tsv file, otherwise you don't need it.

``ncore`` and ``mem`` specify how many CPUs and memory (in Mb) you need. If you don't specify these lines, default is 1 CPU and 4G memory.

In summary, ``=cut job_name job_index_number`` is required. All other lines are optional. But you need to put some commands, otherwise, you are running an empty job.


Hello World example
^^^^^^^^

::



	=cut H1 1

	module load python

	inputFile=input

	ncore=1
	mem=4000

	echo "Hello 1"

	=cut H2 1

	inputFile=input

	ncore=1
	mem=4000

	echo "Hello 2"


	=cut H1.2 2 H1

	inputFile=input

	ncore=1
	mem=4000

	echo "Hello 1 * 2"

	=cut H1.2.1 3 H1.2

	inputFile=input

	ncore=1
	mem=4000

	echo "Hello 1 * 2 * 1"

	=cut email 4 all

	module load python/2.7.13

	cd {{jid}}

	send_email_v1.py -m "{{jid}} is finished" -j {{jid}}



In the above example, H1 and H2 will run in parallel because they have no parent jobs. ``H1.2`` run after ``H1``, ``H1.2.1`` run after ``H1.2``. Then after ``all`` jobs finished, send user an email. Here ``all`` is a keyword, based on the ``job index``, the current job should wait until all previous jobs have finished.












