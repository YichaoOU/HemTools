RNA-seq alternative splicing pipeline
===================================


Summary
^^^^^^^

This pipeline performs the following steps:

1. RNA-Seq De novo Assembly Using ``Trinity`` (https://github.com/trinityrnaseq/trinityrnaseq/wiki)

2. Map de novo transcripts to genome using ``gmap``

3. Quantify de novo transcripts abundance using ``kallisto``

Cons
^^^^

De novo transcripts are not annotated, people can use the bam file from step2 to perform annotation.

Usually I just use this pipeline to check some specific genes, so I will just subset the bam file and visualize in IGV. I can manually check the abundance in the abundance.tsv using the read names from IGV.

::

	samtools view -b trinity_gmap.st.bam chr8:87173540-87374477 > trinity_gmap.NFIX.bam

	samtools index trinity_gmap.NFIX.bam

Input
^^^^^

fastq.tsv

Use ``run_lsf.py --guess_input`` to automatically generate this.

::

	Banana_R1.fastq.gz	Banana_R2.fastq.gz	Banana_lovers
	Orange_R1.fastq.gz	Orange_R2.fastq.gz	Orange_lovers

Usage
^^^^^

::

	hpcf_interactive

	module load python/2.7.13

	run_lsf.py -f fastq.tsv -p trinity.lsf

Output
^^^^^^

Outputs are generated for each fastq file, named as ``{label}_trinity_out``

1. step1 output file is ``Trinity.fasta``. There are also many intermediate files from Trinity.

2. step2 output file is ``trinity_gmap.st.bam``

3. step3 output file is ``{label}_abundance/abundance.tsv``

