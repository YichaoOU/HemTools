Consensus peaks given multiple (>=2) replicates
===============================================

::

	usage: MSPC.py [-h] [-j JID] [-w WEAK] [-s STRONG] [-g GAMMA]
	               [--score_cutoff SCORE_CUTOFF] [-r {bio,tec}] [-c MIN_OVERLAP]
	               [-a ALPHA] [-m {lowest,highest}] [-d DEGREE_OF_PARALLELISM]
	               [--input_format {narrowPeak,broadPeak,bed}]
	               [--value_col VALUE_COL] [--pvalue_format {0,1,2,3}]
	               file [file ...]

	positional arguments:
	  file                  peak files, one per replicate (>=2). narrowPeak by
	                        default, see --input_format

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        MSPC_yli11_<today>)
	  -w WEAK, --weak WEAK  weak peak cutoff (mspc tauW) (default: 0.0001)
	  -s STRONG, --strong STRONG
	                        strong peak cutoff (mspc tauS) (default: 1e-08)
	  -g GAMMA, --gamma GAMMA
	                        combined pvalue peak cutoff (mspc gamma) (default: 1e-12)
	  --score_cutoff SCORE_CUTOFF
	                        combined -log10 pvalue cutoff used to select the final
	                        consensus peaks (ConsensusPeaks.sig.bed) (default: 30)

	MSPC options:
	  -r {bio,tec}, --replicate {bio,tec}
	                        replicate type: biological (bio) or technical (tec)
	                        (default: bio)
	  -c MIN_OVERLAP, --min_overlap MIN_OVERLAP
	                        minimum number of overlapping peaks before combining
	                        p-values; an absolute number (e.g. 2) or a percentage of
	                        samples (e.g. 100%) (default: 2)
	  -a ALPHA, --alpha ALPHA
	                        false discovery rate of the Benjamini-Hochberg step-up
	                        procedure (default: 0.05)
	  -m {lowest,highest}, --multiple_intersections {lowest,highest}
	                        when multiple peaks from one sample overlap a given peak,
	                        use the one with the lowest or highest p-value
	                        (default: lowest)
	  -d DEGREE_OF_PARALLELISM, --degree_of_parallelism DEGREE_OF_PARALLELISM
	                        degree of parallelism; default uses as many threads as
	                        the scheduler allows (default: None)

	Input parser (0-based column index):
	  --input_format {narrowPeak,broadPeak,bed}
	                        input peak file format; sets the p-value column and
	                        format (default: narrowPeak)
	  --value_col VALUE_COL
	                        0-based column index holding the p-value; overrides
	                        --input_format (default: None)
	  --pvalue_format {0,1,2,3}
	                        p-value representation: 0=as is, 1=-log10, 2=-10log10,
	                        3=-100log10; overrides --input_format (default: None)


Summary
^^^^^^^

MSPC comparatively evaluates ChIP-seq peaks and combines the statistical significance of repeated evidences. Weak peaks that are supported by repeated evidence across replicates are rescued, while noisy peaks that only appear in a single replicate are discarded.

Unlike the other HemTools wrappers, ``MSPC.py`` does **not** submit an LSF job. It runs ``mspc`` directly (interactively) on the current node and post-processes the consensus peaks for you.

* MSPC method / documentation: https://genometric.github.io/MSPC/docs
* Source code: https://github.com/Genometric/MSPC

Input
^^^^^

Two or more narrow peak files, one per replicate. ``NAME_peaks.narrowPeak`` is a BED6+4 format file which contains the peak locations together with peak summit, p-value, and q-value. You can load it into the UCSC genome browser. Definition of some specific columns:

::

	5th : integer score. It's calculated as int(-10*log10pvalue) or int(-10*log10qvalue)
	7th : fold-change at peak summit
	8th : -log10pvalue at peak summit
	9th : -log10qvalue at peak summit
	10th: relative summit position to peak start

The **8th column** (``-log10pvalue``) is used as the input p-value to the MSPC program.

.. note::

	MSPC's own default parser reads the p-value from the 5th column, so a raw
	narrowPeak file is **not** a valid default MSPC input. ``MSPC.py`` solves this
	automatically: it writes an MSPC parser configuration (``<jobID>/parser.json``)
	that points MSPC at the 8th column and tells it the value is ``-log10(p)``.
	You therefore feed narrowPeak files directly, no reformatting needed.

	If your peaks use q-value instead of p-value, use ``--value_col 8`` (that column
	is also ``-log10``). For non-narrowPeak inputs, set ``--input_format`` or override
	the column / format with ``--value_col`` and ``--pvalue_format``.

Output
^^^^^^

Everything is written under the ``<jobID>`` folder:

::

	<jobID>/
	├── parser.json                        # MSPC parser config written by MSPC.py
	├── ConsensusPeaks.sig.bed             # <-- final result (significant consensus peaks)
	└── mspc_output/
	    ├── ConsensusPeaks.bed             # all consensus peaks (col 5 = combined -log10 p-value)
	    ├── ConsensusPeaks_mspc_peaks.txt
	    ├── <sample>/Confirmed.bed
	    ├── <sample>/Stringent.bed / Weak.bed / Background.bed
	    ├── <sample>/TruePositive.bed / FalsePositive.bed / Discarded.bed
	    └── ...

``ConsensusPeaks.sig.bed`` is the main deliverable. A consensus peak is a peak occurring in at least 2 replicates (controlled by ``-c``) whose combined significance passes ``--score_cutoff`` (default 30, i.e. combined p-value <= 1e-30). It is produced by filtering ``mspc_output/ConsensusPeaks.bed`` on its 5th column (the combined ``-log10`` p-value) and stripping the header line.

Usage
^^^^^

Copy (or symlink) all the narrowPeak files into your current working dir and run the following:

::

	hpcf_interactive

	module load python/2.7.13

	MSPC.py *.narrowPeak

Give the run a name and a stricter significance cutoff:

::

	MSPC.py -j K562_H3K27ac *.narrowPeak --score_cutoff 50

Require a peak to be present in a fraction of replicates before combining (useful when you have many replicates):

::

	MSPC.py -j K562_H3K27ac -c '60%' *.narrowPeak

Technical replicates instead of biological, with an explicit p-value column:

::

	MSPC.py -j run1 -r tec --value_col 8 *.narrowPeak

.. note::

	All files passed on the command line are treated as replicates of **one**
	experiment and combined into a single consensus set. Only glob a folder if
	every file in it belongs to the same condition; otherwise list the replicates
	of each condition explicitly and run ``MSPC.py`` once per condition.

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines
