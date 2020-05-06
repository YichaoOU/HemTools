bioinformatics
=========


chrom size can cause a lot of errors
^^^^^^^^^^^^^^^^^^^^^^^^^

In primary assembly we only have chr1 to chr22, chrX and chrY, chrM.

In another version, we can have many scaffolds, those weird names.

I've seen problems caused by:

1. sorted vs. unsorted chrom size

pyBigWig have to use sorted bed and sorted chrom size

::

	RuntimeError: The entries you tried to add are out of order, precede already added entries, or otherwise use illegal values.
	 Please correct this and try again.

2. Mapping index is only primary chromosomes, however, in the subsequenty analysis if you use a chrom size file for all chromsomes, it may cause errors like generating bw files.

2b. HiC-Pro to Juicebox .sh generate a restriction fragment file that considers only main chromsomes, now if you supplied all chrosomes size, it will have errors like:

::

	Problem with creating fragment-delimited maps, NullPointerException.
	This could be due to a null fragment map or to a mismatch in the chromosome name in the fragment map vis-a-vis the input file or chrom.sizes file.

0-index vs 1-index
^^^^^^^^

Like the index in R starts with 1 and in python starts with 0, bioinformatics has this problem too. I know bed file, start is 0-index and end is 1-index, so the length of the region can be directly computed as end-start, instead of end-start+1

vcf is 1-index

When people give you a file other than these format, we have to always make sure whether it is 0-index or 1-index.




