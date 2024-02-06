RNA velocity analysis
======================




Input
^^^^^

A list of absolute path to 10x job folder


::

	/research/dept/hem/common/sequencing/chenggrp/pdoerfler_single-cell/rep2_data_analysis/PD1
	/research/dept/hem/common/sequencing/chenggrp/pdoerfler_single-cell/rep2_data_analysis/PD2
	/research/dept/hem/common/sequencing/chenggrp/pdoerfler_single-cell/rep2_data_analysis/PD3
	/research/dept/hem/common/sequencing/chenggrp/pdoerfler_single-cell/rep2_data_analysis/PD5

Usage
^^^^

::

	run_lsf.py -f data.list -p scvelo_10x
