Replicate correlation and QC for HiC data
===================



::



Input
^^^^^

Use ``hicpro_to_bedpe.py`` to generate input1 and input2.

1. contact matrix for your two samples (.gz)
---------

I found the last column has to be int

::

	21	10050000	21	10050000	6
	21	10050000	21	10150000	1
	21	10050000	21	11000000	1
	21	10100000	21	41700000	1
	21	10200000	21	40350000	1
	21	10350000	21	10900000	1
	21	10350000	21	25600000	1
	21	10400000	21	10400000	12
	21	10400000	21	10450000	4
	21	10400000	21	10500000	1

2. bed.gz
------

::

	chr22	0	50000	0
	chr22	50000	100000	50000
	chr22	100000	150000	100000
	chr22	150000	200000	150000
	chr22	200000	250000	200000
	chr22	250000	300000	250000


looks like we need to remove chr? Answer is no, tested.

you have to remove chrM from the matrix and bed file.


3. metadata
------

::

	==> metadata.pairs <==
	HIC001	HIC002

	==> metadata.samples <==
	HIC001	/home/yli11/Programs/3DChromatin_ReplicateQC/examples/HIC001.res50000.gz
	HIC002	/home/yli11/Programs/3DChromatin_ReplicateQC/examples/HIC002.res50000.gz

Notes
^^^^

https://github.com/kundajelab/3DChromatin_ReplicateQC

Installation
----------

You have to create a new conda env for python2.7 because HiFive requires py2.

R>3.4

I have no problem following the installation.sh but for R, I have to do some manual installation. 

Overall it is smooth, the original document did not specify python2.7.

Starter example
--------------

Finished correctly.


3d_genome_py2

bsub -q priority -P Genomics -R 'rusage[mem=60000]' 3DChromatin_ReplicateQC run_all --metadata_samples metadata.samples --metadata_pairs metadata.pairs --bins /home/yli11/dirs/hg19_20copy_result/keep_dup_Jurkat_20copy/hicpro_results/hic_results/matrix/Jurkat_20copy/HiCPro_100000_bed.repQC.gz --outdir replicate_QC

 


