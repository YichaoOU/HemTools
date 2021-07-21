Given any count table, run DESEQ2
=====================================


::

	usage: run_DESEQ2.py [-h] -f INPUT_TSV -s SAMPLE_NAMES -t TREATMENT -c CONTROL [-o OUTPUT] [--count_cutoff COUNT_CUTOFF]
	                     [--N_sample_cutoff N_SAMPLE_CUTOFF]

	optional arguments:
	  -h, --help            show this help message and exit
	  -o OUTPUT, --output OUTPUT
	                        output prefix (default: auto)
	  --count_cutoff COUNT_CUTOFF
	                        usually it's better for prefilter out some low-count genes/peaks (default: 0)
	  --N_sample_cutoff N_SAMPLE_CUTOFF
	                        usually it's better for prefilter out some low-count genes/peaks (default: 0)

	required named arguments:
	  -f INPUT_TSV, --input_tsv INPUT_TSV
	                        count table, each row is a feature, each column is a sample (default: None)
	  -s SAMPLE_NAMES, --sample_names SAMPLE_NAMES
	                        2 column tsv, first column, sample name matched to input_tsv column names, second column is the group
	                        name (default: None)
	  -t TREATMENT, --treatment TREATMENT
	                        treatment group name, must match group names specified in sample_names (default: None)
	  -c CONTROL, --control CONTROL
	                        control group name, must match group names specified in sample_names (default: None)


Summary
^^^^^^^

This program performs differential analysis given a user provided count table.


Usage
^^^^^

.. code:: bash

	hpcf_interactive

	module load conda3

	source activate /home/yli11/.conda/envs/captureC

	run_DESEQ2.py -f DESEQ2.input.tsv -s samples.tsv -t HBBP1_VHL -c HBBP1_NT

Input
^^^^^

Count table: DESEQ2.input.tsv
-------------


each row is a feature, each column is a sample.

sample names mapping: samples.tsv
-------------

::

	CaptureC_NT_BGLT3_r1_S27	BGLT3_NT
	CaptureC_VHL_BGLT3_r1_S29	BGLT3_VHL
	CaptureC_NT_BGLT3_r2_S28	BGLT3_NT
	CaptureC_VHL_BGLT3_r2_S30	BGLT3_VHL
	CaptureC_NT_HBBP1_r1_S31	HBBP1_NT


First column is sample name, must match column names in count table

Second column is group name

Output
^^^^^^

Output name by default is treatment.vs.control, folder is created, and DESEQ2 raw count, norm count, stats are put as, ``treatment.vs.control.deseq2_result.tsv``. Examples shown below

::

	HBBP1_VHL.vs.HBBP1_NT.plotDispEsts.pdf  HBBP1_VHL.vs.HBBP1_NT.R
	HBBP1_VHL.vs.HBBP1_NT.cooks_distance.pdf  HBBP1_VHL.vs.HBBP1_NT.plotMA.pdf
	HBBP1_VHL.vs.HBBP1_NT.deseq2_result.tsv   HBBP1_VHL.vs.HBBP1_NT.pvalue_hist.pdf


Convert deseq2 result to bw files for visualization
^^^^^^^^^^

::

	bdg_to_bw.py -f HBBP1.deseq2_result.tsv --data_frame -j HBBP1_bw_files
	bdg_to_bw.py -f BGLT3.deseq2_result.tsv --data_frame -j BGLT3_bw_files
