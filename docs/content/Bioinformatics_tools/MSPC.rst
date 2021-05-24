Consensus peaks given multiple (>=2) replicates
==================

::

	usage: MSPC.py [-h] [-j JID] [-w WEAK] [-s STRONG] [-g GAMMA]
	               [--score_cutoff SCORE_CUTOFF]
	               file [file ...]

	positional arguments:
	  file

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        MSPC_yli11_2020-04-20)
	  -w WEAK, --weak WEAK  weak peak cutoff (default: 0.0001)
	  -s STRONG, --strong STRONG
	                        strong peak cutoff (default: 1e-08)
	  -g GAMMA, --gamma GAMMA
	                        combined pvalue peak cutoff (default: 1e-12)
	  --score_cutoff SCORE_CUTOFF
	                        combined log pvalue peak cutoff for consensus peak
	                        (default: 30)


Summary
^^^^^


MSPC comparatively evaluates ChIP-seq peaks and combines the statistical significance of repeated evidences.

The output

https://github.com/Genometric/MSPC

Input
^^^^^

Narrow peak files. The format of narrow peak files is:

NAME_peaks.narrowPeak is BED6+4 format file which contains the peak locations together with peak summit, p-value, and q-value. You can load it to the UCSC genome browser. Definition of some specific columns are:

::

	5th: integer score. It's calculated as int(-10*log10pvalue) or int(-10*log10qvalue) 
	7th: fold-change at peak summit
	8th: -log10pvalue at peak summit
	9th: -log10qvalue at peak summit
	10th: relative summit position to peak start

The 8th column will be used as input pvalue to the MSPC program.


Output
^^^^^

``ConsensusPeaks.sig.bed`` inside the {{jobID}} folder.

A consensus peak is a peak occurring in at least 2 replicates of the given replicates and it must pass the significance cutoff.

Usage
^^^^^

Copy all the narrowPeak files into your current working dir and run the following


::

	hpcf_interactive

	module load python/2.7.13

	MSPC.py *.narrowPeak




Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines









