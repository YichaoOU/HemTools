HemTools public data
====================


bulk RNA-seq data
-------

::

	/home/yli11/dirs/blood_regulome/chenggrp/HemPortal/HemTools_uniform_processed_files/blood_rna_seq


TSS data
----


*hg19 non-redundant TSS from ensembl*

/home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed

*hg19 redundant TSS (ensembl + gencode)*

In this dataset, each gene can have multiple TSSs, but gene-TSS combination is unique

/home/yli11/Data/Human/hg19/gencode33/hg19.redundant.tss.bed

hg19 data
---------


Hi-CHIP
--------

::

	Hudep2 GATA1 HiCHIP 20kb: /research_jude/rgs01_jude/groups/chenggrp/projects/blood_regulome/chenggrp/Projects/jchen6/GATA1_TFBS_ABE8e_screening/pre-test_vali/HiChIP/merged/GATA1_ATAC_P_to_all_results/GATA1_H2_HiCHIP/fihichip_results/FitHiChIP_Peak2ALL_b20000_L10000_U2000000/P2PBckgr_0/Coverage_Bias/FitHiC_BiasCorr/Merge_Nearby_Interactions/GATA1_H2_HiCHIP.interactions_FitHiC_Q0.05_MergeNearContacts.bed

	H3K27AC Hudep2 2.5kb: /research_jude/rgs01_jude/groups/chenggrp/projects/blood_regulome/chenggrp/HemPortal/HemTools_uniform_processed_files/HICHIP

   7880 1374932_1400249_Hudep2_H3K27AC_HiChIP.count.bedpe
  13109 1374933_1400250_Hudep2_H3K27AC_HiChIP_FS.count.bedpe
   6781 1482819_1512832_Hudep2_D3_H3K27AC_HiChIP.count.bedpe
  18979 1482820_1512831_CD34_D13_rep1_H3K27AC.count.bedpe

  Jurkat CTCF hichip: /research_jude/rgs01_jude/groups/chenggrp/projects/blood_regulome/common/insulator_screen/insulator_oligo_screen/hichip_dove_raw_data/hichip_dshresth_2022-09-09/ctcf_hichip/merged_CTCF_peak.fithichip_005.results/FitHiChIP_Peak2ALL_b5000_L10000_U2000000/P2PBckgr_0/Coverage_Bias/FitHiC_BiasCorr/ctcf_hichip.interactions_FitHiC_Q0.05.bed



TF histone peaks
--------------

::


	H1 GATA1 Day0 IDR peak: /research_jude/rgs01_jude/groups/chenggrp/projects/blood_regulome/chenggrp/Projects/fetal_vs_adult/data/GATA1_new/pair_end/PE-chip-seq_qqi_2019-03-21/IDR_peak/idr_peaks_qqi_2020-05-16_13c13bb9aad9/idr_peaks.rmblck.merged_peaks.bed

	H2 GATA1 Day0 IDR peak: /home/yli11/dirs/blood_regulome/chenggrp/Projects/fetal_vs_adult/data/GATA1_new/pair_end/PE-chip-seq_qqi_2019-03-21/IDR_peak/idr_peaks_qqi_2020-06-04/idr_peaks.rmblck.merged_peaks.bed
	
	blood_regulome/chenggrp/HemPortal/HemTools_uniform_processed_files/Hudep2/unknown/ATAC_seq/atac_seq_yli11_2020-06-12/peak_files/H2_ATAC_peak.union.bed

	blood_regulome/chenggrp/HemPortal/HemTools_uniform_processed_files/

	CD34/ChIP_seq/chip_seq_single_yli11_2021-01-28/peak_files/H3K27ac_CD34.merged.bed

	Hudep1/ChIP_seq/chip_seq_single_yli11_2021-01-28/peak_files/H3K27ac_H1.merged.bed

	./Hudep2/unknown/Histone_chip_seq_single/chip_seq_single_yli11_2021-01-28/peak_files/H3K27ac_H2_D0.merged.bed

	Sequencing_runs/Li_data/raw_data_ABE_CRM/ChIP_seq/histone/chip_seq_single_yli11_2020-08-21/peak_files/H3K27ac_H2_D3.merged.bed

	Jurkat CTCF merged peak: blood_regulome/chenggrp/HemPortal/HemTools_uniform_processed_files/Jurkat/ChIP_seq/CTCF/Jurkat_CTCF.merged.bed


chromHMM data
-------

There is chromatin states (N=10) annotation ``chromHMM_heatmap.pdf`` in the same folder. 

::
	
	Hudep2 Day0: blood_regulome/chenggrp/HemPortal/HemTools_uniform_processed_files/Hudep2/Day0/chromHMM/chromHMM_yli11_2022-09-01/learned_model_10/myCellLine_10_segments.bed

	CD34: blood_regulome/chenggrp/HemPortal/HemTools_uniform_processed_files/CD34/chromHMM/chromHMM_yli11_2022-09-01/learned_model_10/myCellLine_10_segments.bed



Data Table
--------

+-----------------------------+-----------------------------------------------------------------------------------------+
| Name                        | Path                                                                                    |
+=============================+=========================================================================================+
| hg19\_BWA\_index            | /home/yli11/Data/Human/hg19/index/bwa\_16a\_index/hg19.fa                               |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_kallisto\_index       | /home/yli11/Data/Human/hg19/index/kallisto/hg19.idx                                     |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_black\_list           | /home/yli11/Data/Human/hg19/annotations/hg19.blacklist.bed                              |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_chrom\_size           | /home/yli11/Data/Human/hg19/annotations/hg19.chrom.sizes                                |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_fasta                 | /home/yli11/Data/Human/hg19/fasta/hg19.fa                                               |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_motif                 | /home/yli11/Data/Motif\_database/Human/human.meme                                       |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_rRNA                  | /home/yli11/Data/RSEQC\_bed/hg19\_rRNA.bed3                                             |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_HBG                   | /home/yli11/Data/Human/hg19/features/HBG.bed                                            |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_hemoglobin            | /home/yli11/Data/Human/hg19/features/hg19.ENCODE\_GENE.hem.bed3                         |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_t2g                   | /home/yli11/Data/Human/hg19/index/kallisto/hg19.ensembl\_v75.t2g                        |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_FANTOM5\_enhancer     | /home/yli11/Data/Human/hg19/FANTOM/human\_permissive\_enhancers\_phase\_1\_and\_2.bed   |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_FANTOM5\_TSS          | /home/yli11/Data/Human/hg19/FANTOM/TSS\_human.bed                                       |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_3UTR                  | /home/yli11/Data/Human/hg19/UCSC\_table\_browser/gene\_3UTR.bed                         |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_gene\_body            | /home/yli11/Data/Human/hg19/UCSC\_table\_browser/gene\_body.bed                         |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_gene\_end\_2000       | /home/yli11/Data/Human/hg19/UCSC\_table\_browser/gene\_down2000.bed                     |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_intron                | /home/yli11/Data/Human/hg19/UCSC\_table\_browser/gene\_intron.bed                       |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_promoter\_up2000      | /home/yli11/Data/Human/hg19/UCSC\_table\_browser/gene\_promoter\_up2000.bed             |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_intergenic\_regions   | /home/yli11/Data/Human/hg19/UCSC\_table\_browser/intergenic.bed                         |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_5UTR                  | /home/yli11/Data/Human/hg19/UCSC\_table\_browser/gene\_5UTR.bed                         |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_gene\_end\_1000       | /home/yli11/Data/Human/hg19/UCSC\_table\_browser/gene\_down1000.bed                     |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_exon                  | /home/yli11/Data/Human/hg19/UCSC\_table\_browser/gene\_exon.bed                         |
+-----------------------------+-----------------------------------------------------------------------------------------+
| hg19\_promoter\_up1000      | /home/yli11/Data/Human/hg19/UCSC\_table\_browser/gene\_promoter\_up1000.bed             |
+-----------------------------+-----------------------------------------------------------------------------------------+

hg38 data
---------

+-------------------------+--------------------------------------------------------------------+
| Name                    | Path                                                               |
+=========================+====================================================================+
| hg38\_motif             | /home/yli11/Data/Motif\_database/Human/human.meme                  |
+-------------------------+--------------------------------------------------------------------+
| hg38\_t2g               | /home/yli11/Data/Human/hg38/index/kallisto/hg38.ensembl\_v67.t2g   |
+-------------------------+--------------------------------------------------------------------+
| hg38\_kallisto\_index   | /home/yli11/Data/Human/hg38/index/kallisto/hg38.idx                |
+-------------------------+--------------------------------------------------------------------+

mm10 data
---------

+-------------------------+--------------------------------------------------------------------+
| Name                    | Path                                                               |
+=========================+====================================================================+
| mm10\_t2g               | /home/yli11/Data/Mouse/mm10/index/kallisto/mm10.ensembl\_v67.t2g   |
+-------------------------+--------------------------------------------------------------------+
| mm10\_kallisto\_index   | /home/yli11/Data/Mouse/mm10/index/kallisto/mm10.idx                |
+-------------------------+--------------------------------------------------------------------+

mm9 data
--------

+------------------------+------------------------------------------------------------------+
| Name                   | Path                                                             |
+========================+==================================================================+
| mm9\_t2g               | /home/yli11/Data/Mouse/mm9/index/kallisto/mm9.ensembl\_v67.t2g   |
+------------------------+------------------------------------------------------------------+
| mm9\_kallisto\_index   | /home/yli11/Data/Mouse/mm9/index/kallisto/mm9.idx                |
+------------------------+------------------------------------------------------------------+

chromHMM
--------

+--------------------------+---------------------------------------------------------------------+
| Name                     | Path                                                                |
+==========================+=====================================================================+
| known\_association       | /home/yli11/HemTools/share/misc/chromHMM\_known\_associations.tsv   |
+--------------------------+---------------------------------------------------------------------+
| chromatin\_state\_info   | /home/yli11/HemTools/share/misc/chromatin\_state\_info.tsv          |
+--------------------------+---------------------------------------------------------------------+

RNA-seq data
------------

Blood lineage data:

Paired-end: /home/yli11/HemPortal/RNA_seq/blood/PRJNA299579

Single-end: /home/yli11/HemPortal/RNA_seq/blood/GSE61566_GSE53983

BE-editor: /research/rgs01/project_space/chenggrp/blood_regulome/chenggrp/Projects/BE_editor/GSE121668

