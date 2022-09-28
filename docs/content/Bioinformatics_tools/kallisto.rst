Transcript-level abundance quantification
=========================================



::

	module load kallisto/0.43.1

	


Note
^^^^

Based on my own testing, a multi-mapped read will only be counted once in the abundance.tsv, but will occur multiple times in the pseudobam file.

If Kallisto multi-mapping reads, then one was selected at random.
http://genomespot.blogspot.com/2015/08/how-accurate-is-kallisto.html

https://github.com/pachterlab/kallistobustools/issues/15
