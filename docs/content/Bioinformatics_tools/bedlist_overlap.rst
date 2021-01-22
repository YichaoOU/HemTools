Query bed overlap with a list of bed files
==============


Summary
^^^^^^^

The goal is to look at the percentage of overlap of your region of interest in a list of bed files. For example, we have a N chip-seq peaks, we would like to know if these N peaks remain in open chromatin across the whole blood lineage. Then, the N peaks is your query list, and the list of bed files is your reference list.


Input
^^^^^

There are two input files. The first in your query list, the second is your reference list.

Query list
----------


::
	query.list
	----------
	NFIX_peaks.bed

Reference list
---------------

::
	mouse_blood.list
	----------------
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/B.ImmGen.mm10.ATAC.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/CMP.ENCODE.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/DC.ImmGen.mm10.ATAC.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/Ery.ENCODE.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/GMP.ENCODE.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/HSC.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/MEP.ENCODE.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/MK.ENCODE.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/MKP.ENCODE.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/Mono.ENCODE.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/MPP.ImmGen.mm10.ATAC.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/Neutro.ENCODE.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/NK.ImmGen.mm10.ATAC.mm9.bed
	/home/yli11/Data/Mouse/mouse_blood/mm9_blood_ATAC/T.ImmGen.mm10.ATAC.mm9.bed

Usage
^^^^^

::
	module load python/2.7.13

	bedlist_overlap.py query.list mouse_blood.list 

Output
^^^^^^

The percentage of overlap (percentage in terms of query size) is printed out in the terminal

The output file is a binary matrix with each row being your query peak and each column being the reference bed file

