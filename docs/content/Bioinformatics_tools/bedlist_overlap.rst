Query bed overlap with a list of bed files
==============


Summary
^^^^^^^

The goal is to look at the percentage of overlap of your region of interest in a list of bed files. For example, we have a N chip-seq peaks, we would like to know if these N peaks remain in open chromatin across the whole blood lineage. Then, the N peaks is your query list, and the list of bed files is your reference list.


Input
^^^^^

There are two input files. The first in your query list, the second is your reference list.

Query Bed
----------

Input is a bed file (chr, start, end, additional columns are not used), e.g., ``query.bed``

Reference list
---------------

Input is a file contaning a list of bed files, e.g., ``peak.list``

::

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

	# for mm9
	bedlist_overlap.py query.bed /home/yli11/Data/Mouse/mouse_blood/peak.list

	# for hg19
	bedlist_overlap.py query.bed /home/yli11/Data/Human/hg19/annotations/blood.peaks.list

	## for mm9 data visualization
	plot_blood_lineage.py --svg_template /home/yli11/HemTools/share/misc/mouse_blood.svg -f peak_overlap_percent.tsv

	## for hg19 data visualization
	plot_blood_lineage.py --svg_template /home/yli11/HemTools/share/misc/blood_lineage_Hchang_13cells.svg -f peak_overlap_percent.tsv

Output
^^^^^^

The percentage of overlap (percentage in terms of query size) is provided in file ``peak_overlap_percent.tsv``, this file can be directly used to :doc:`plot_blood_lineage.py <../Gallery/plot_blood_lineage.rst>`.

The ``my_overlap_matrix.tsv`` file is a binary matrix with each row being your query peak and each column being the reference bed file (class)

