RNA-seq QC
==========







1. read distribution
---------------


::

	module load conda3
	source activate /home/yli11/.conda/envs/rseqc

	read_distribution.py -i test.markdup.uq.bam -r /home/yli11/Data/RSEQC_bed/hg19_RefSeq.bed

Output:

::

	Total Reads                   550
	Total Tags                    607
	Total Assigned Tags           468
	=====================================================================
	Group               Total_bases         Tag_count           Tags/Kb             
	CDS_Exons           34584069            184                 0.01              
	5'UTR_Exons         7945567             107                 0.01              
	3'UTR_Exons         27291196            52                  0.00              
	Introns             955378898           91                  0.00              
	TSS_up_1kb          19477091            0                   0.00              
	TSS_up_5kb          88605716            4                   0.00              
	TSS_up_10kb         161012560           20                  0.00              
	TES_down_1kb        19913631            0                   0.00              
	TES_down_5kb        85343516            4                   0.00              
	TES_down_10kb       151518466           14                  0.00              
	=====================================================================

