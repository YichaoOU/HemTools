ENCODE database query
=============

Input
^^^^^

You should have your query bed file.


Usage
^^^^^

::

	# login to a compute node
	hpcf_interactive.sh

	db=/research_jude/rgs01_jude/groups/chenggrp/projects/blood_regulome/common/atac_footprint/siqi/k562_igd_db/k562_igd_db.igd

	igd search $db -q my.bed -f > out.tsv

Output
^^^^^^

Each line in the query bed file will be shown as ``Query chr,start,end`` in the output table, followed by the overlaped file name

::

	Query chr11, 5268397, 5268664: 			
	0	5268508	5268848	 ENCFF388LUX_MLLT1-human.bed
	Query chr11, 5268798, 5269050: 			
	0	5268508	5268848	 ENCFF388LUX_MLLT1-human.bed
	Total overlaps: 2			




