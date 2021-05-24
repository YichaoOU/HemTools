


Input
-----

I usually put soft links of bw files and bed files in the same working dir. Then run ``bw_over_bed.py`` will give me a feature table for each bed file in the current dir.

::

	HUDEP2_LRF_CHIP.rmdup.bw
	Hudep2_D3_merged_GATA1.all.bw
	loci.bed
	Hudep2_ATAC.rmdup.bw
	Hudep2_D3_merged_KLF1.all.bw
	Hudep2_BCL11A.rmdup.bw
	Hudep2_D3_merged_LDB1.all.bw
	Hudep2_D3_merged_CTCF.all.bw
	Hudep2_D3_merged_TAL1.all.bw


Usage
-----


.. code:: bash

	module load ucsc/041619

	bw_over_bed.py

	