Blood data inquiry
==================

::


	usage: blood_data_inquiry.py [-h] [-j JID] -f BED_FILE [-o OUTPUT]
	                             [--bam_file_list BAM_FILE_LIST]
	                             [--bw_list BW_LIST] (--on_bw | --on_bam)

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        blood_data_inquiry_yli11_2019-10-03)
	  -f BED_FILE, --bed_file BED_FILE
	                        input bed file for featureCount (default: None)
	  -o OUTPUT, --output OUTPUT
	                        output file name (default: featureCount)
	  --bam_file_list BAM_FILE_LIST
	                        HemTools blood collection (default:
	                        /home/yli11/HemTools/config/blood_ATAC.data)
	  --bw_list BW_LIST     HemTools blood collection (default:
	                        /home/yli11/HemTools/config/blood_ATAC.bw.list)
	  --on_bw               extract values based on bw files (default: False)
	  --on_bam              extract values based on bam files (default: False)

Summary
^^^^^^^

This is a suite of tools for users to query specific regions or genes among public blood datasets.

Output read counts over given bed.

Input
^^^^^

Input format varies by different usage. 

Bed format 
-------------------

Additional columns are OK. The first 3 columns have to be chr, start, end.

::

	chr11	4167364	4167385	chr11:4167374-4167375
	chr11	4167366	4167387	chr11:4167376-4167377
	chr11	4167367	4167388	chr11:4167377-4167378
	chr11	4167370	4167391	chr11:4167380-4167381

Usage
^^^^^

Signal values (bw) over input bed
----------------------------

.. code:: bash

	blood_data_inquiry.py -f input.bed --on_bw

You can also input your own list of bw files by ``--bw_list`` option.

Read counts (bam) over input bed
----------------------------

.. code:: bash

	blood_data_inquiry.py -f input.bed --on_bam

You can also input your own list of bam files by ``--bam_file_list`` option.





BigWiggle Data
^^^^

::

	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA382394_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5442277_HCT116_HCT116_cell_line_expressing_dCas9minusBFPminusKRAB_construct.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA382394_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5442274_MDAminusMBminus231_MDAminusMBminus231_clonal_cell_line_expressing_dCas9minusBFPminusKRAB_construct.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA382394_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5442275_MCF7_MCF7_clonal_cell_lines_expressing_dCas0minusBFPminusKRAB_construct.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA382394_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5442276_MCF7_MCF7_clonal_cell_lines_expressing_dCas9minusBFPminusKRAB_construct.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA382394_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5442272_MDAminusMBminus231_MDAminusMBminus231_clonal_cell_line_expressing_dCas9minusBFPminusKRAB_construct.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA382394_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5442270_MDAminusMBminus231_MDAminusMBminus231_clonal_cell_line_expressing_dCas9minusBFPminusKRAB_construct.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA382394_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5442278_HCT116_HCT116_cell_line_expressing_dCas9minusBFPminusKRAB_construct.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA382394_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5442269_MDAminusMBminus231_MDAminusMBminus231_clonal_cell_line_expressing_dCas9minusBFPminusKRAB_construct.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA382394_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5442273_MDAminusMBminus231_MDAminusMBminus231_clonal_cell_line_expressing_dCas9minusBFPminusKRAB_construct.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA382394_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5442271_MDAminusMBminus231_MDAminusMBminus231_clonal_cell_line_expressing_dCas9minusBFPminusKRAB_construct.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920502_CD71plusGPAplus_erythroblast_cell_Ery.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920484_granulocyte_macrophage_progenitor_cell_GMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920531_hematopoietic_stem_cell_HSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920525_CD71plusGPAplus_erythroblast_cell_Ery.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920582_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920518_CD4plus_T_cell_CD4Tcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920510_multipotent_progenitor_cell_MPP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920519_CD4plus_T_cell_CD4Tcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920495_CD56plus_natural_killer_cell_NKcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920504_CD71plusGPAplus_erythroblast_cell_Ery.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920472_granulocyte_macrophage_progenitor_cell_GMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920476_CD14plus_monocyte_cell_Mono.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920488_CD14plus_monocyte_cell_Mono.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920492_CD19plusCD20plus_B_cell_Bcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920574_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920554_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920477_hematopoietic_stem_cell_HSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920500_common_myeloid_progenitor_cell_CMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920497_CD8plus_T_cell_CD8Tcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920490_CD34plus_bone_marrow_CD34_Bone_Marrow.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920483_granulocyte_macrophage_progenitor_cell_GMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920471_granulocyte_macrophage_progenitor_cell_GMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920470_common_myeloid_progenitor_cell_CMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920494_CD8plus_T_cell_CD8Tcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920545_common_lymphoid_progenitor_cell_CLP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920548_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920499_common_lymphoid_progenitor_cell_CLP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920516_CD56plus_natural_killer_cell_NKcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920542_CD14plus_monocyte_cell_Mono.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920528_common_lymphoid_progenitor_cell_CLP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920475_CD14plus_monocyte_cell_Mono.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920570_acute_myeloid_leukemia__leukmeia_stem_cell_LSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920506_hematopoietic_stem_cell_HSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920538_granulocyte_macrophage_progenitor_cell_GMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920550_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920580_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920564_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920526_CD56plus_natural_killer_cell_NKcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920508_megakaryocyte_erythroid_progenitor_cell_MEP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920473_megakaryocyte_erythroid_progenitor_cell_MEP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920530_CD71plusGPAplus_erythroblast_cell_Ery.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920514_CD4plus_T_cell_CD4Tcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920586_acute_myeloid_leukemia__leukmeia_stem_cell_LSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920533_multipotent_progenitor_cell_MPP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920547_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920498_common_lymphoid_progenitor_cell_CLP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920544_CD19plusCD20plus_B_cell_Bcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920576_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920467_multipotent_progenitor_cell_MPP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920478_hematopoietic_stem_cell_HSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920563_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920482_common_myeloid_progenitor_cell_CMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920584_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920595_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920552_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920511_CD56plus_natural_killer_cell_NKcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920539_granulocyte_macrophage_progenitor_cell_GMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920509_multipotent_progenitor_cell_MPP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920572_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920513_CD19plusCD20plus_B_cell_Bcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920517_CD19plusCD20plus_B_cell_Bcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920520_CD8plus_T_cell_CD8Tcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920560_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920577_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920501_common_myeloid_progenitor_cell_CMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920481_common_myeloid_progenitor_cell_CMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920505_granulocyte_macrophage_progenitor_cell_GMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920565_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920594_acute_myeloid_leukemia__leukmeia_stem_cell_LSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920566_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920489_CD34plus_bone_marrow_CD34_Bone_Marrow.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920593_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920468_lymphoidminusprimed_multipotent_progenitor_cell_LMPP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920575_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920551_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920546_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920587_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920524_CD71plusGPAplus_erythroblast_cell_Ery.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920534_multipotent_progenitor_cell_MPP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920585_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920493_CD4plus_T_cell_CD4Tcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920591_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920540_megakaryocyte_erythroid_progenitor_cell_MEP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920527_CD56plus_natural_killer_cell_NKcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920515_CD8plus_T_cell_CD8Tcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920496_CD4plus_T_cell_CD4Tcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920466_hematopoietic_stem_cell_HSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920568_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920507_hematopoietic_stem_cell_HSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920553_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920480_lymphoidminusprimed_multipotent_progenitor_cell_LMPP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920588_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920485_megakaryocyte_erythroid_progenitor_cell_MEP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920573_acute_myeloid_leukemia__leukmeia_stem_cell_LSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920474_megakaryocyte_erythroid_progenitor_cell_MEP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920521_CD8plus_T_cell_CD8Tcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920549_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920555_acute_myeloid_leukemia__leukmeia_stem_cell_LSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920532_hematopoietic_stem_cell_HSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920522_common_lymphoid_progenitor_cell_CLP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920536_common_myeloid_progenitor_cell_CMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920556_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920578_acute_myeloid_leukemia__leukmeia_stem_cell_LSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920590_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920589_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920579_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920503_CD71plusGPAplus_erythroblast_cell_Ery.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920537_common_myeloid_progenitor_cell_CMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920487_CD14plus_monocyte_cell_Mono.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920491_CD34plus_cord_blood_CD34_Cord_Blood.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920512_CD56plus_natural_killer_cell_NKcell.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920557_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920592_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920535_lymphoidminusprimed_multipotent_progenitor_cell_LMPP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920583_acute_myeloid_leukemia__leukmeia_stem_cell_LSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920559_acute_myeloid_leukemia__leukmeia_stem_cell_LSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920562_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920543_CD14plus_monocyte_cell_Mono.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920581_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920541_megakaryocyte_erythroid_progenitor_cell_MEP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920558_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920486_megakaryocyte_erythroid_progenitor_cell_MEP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920571_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920561_acute_myeloid_leukemia__preminusleukemic_hematopoietic_stem_cell_pHSC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920529_CD71plusGPAplus_erythroblast_cell_Ery.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920469_common_myeloid_progenitor_cell_CMP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920567_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920569_acute_myeloid_leukemia__blast_cell_Blast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920479_multipotent_progenitor_cell_MPP.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA301969_bulkATAC_Chang_HY_2016/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR2920523_CD71plusGPAplus_erythroblast_cell_Ery.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR6288280_Cultured_cancer_cell_line_K562_Lymphoblast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5831760_Cultured_cancer_cell_line_Leukemic_lymphoblasts.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR6288278_Cultured_cancer_cell_line_K562_Lymphoblast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5831757_Cultured_cancer_cell_line_Leukemic_lymphoblasts.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5831767_Cultured_cancer_cell_line_Leukemic_lymphoblasts.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR6288277_Cultured_cancer_cell_line_K562_Lymphoblast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5831759_Cultured_cancer_cell_line_Leukemic_lymphoblasts.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5831755_Cultured_cancer_cell_line_Leukemic_lymphoblasts.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR6288281_Cultured_cancer_cell_line_K562_Lymphoblast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5831768_Cultured_cancer_cell_line_Leukemic_lymphoblasts.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5831758_Cultured_cancer_cell_line_Leukemic_lymphoblasts.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5831756_Cultured_cancer_cell_line_Leukemic_lymphoblasts.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR6288279_Cultured_cancer_cell_line_K562_Lymphoblast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA394713_bulkATAC_Pommier_Y_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR6288282_Cultured_cancer_cell_line_K562_Lymphoblast.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356163_GMPminusB_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356156_pDC_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356159_Mega_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356157_UNK_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356164_GMPminusB_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356166_pDC_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356161_UNK_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356168_UNK_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356167_UNK_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356158_Mega_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356165_GMPminusC_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356162_GMPminusA_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA379614_bulkATAC_Chang_HY_2018/sra_download_yli11_2019-09-26/atac_seq_yli11_2019-09-27/bw_files/SRR5356160_pDC_Bone_Marrow_CD34plus.rmdup.bw
	/research/rgs01/home/clusterHome/yli11/HemPortal/SRA/PRJNA207663/sra_download_yli11_2019-09-18/fastq_files/atac_seq_yli11_2019-09-18/bw_files/CD4plus_Tcell.rmdup.bw
	/research/rgs01/home/clusterHome/yli11/HemPortal/SRA/PRJNA207663/sra_download_yli11_2019-09-18/fastq_files/atac_seq_yli11_2019-09-18/bw_files/GM12878_ATAC.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295261_CD34plus_hematopoietic_cells_CD71minus_CD235minus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295276_CD34plus_hematopoietic_cells_CD71plus_CD235plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295262_CD34plus_hematopoietic_cells_CD71plus_CD235minus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295277_CD34plus_hematopoietic_cells_CD71minus_CD235minus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295263_CD34plus_hematopoietic_cells_CD71plus_CD235lo.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295278_CD34plus_hematopoietic_cells_CD71plus_CD235minus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295264_CD34plus_hematopoietic_cells_CD71plus_CD235plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295279_CD34plus_hematopoietic_cells_CD71plus_CD235lo.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295265_CD34plus_hematopoietic_cells_CD49dplus_Band3minus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295280_CD34plus_hematopoietic_cells_CD71plus_CD235plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295267_CD34plus_hematopoietic_cells_CD49dlo_Band3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295281_CD34plus_hematopoietic_cells_CD49dplus_Band3minus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295268_CD34plus_hematopoietic_cells_CD49dminusBand3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295282_CD34plus_hematopoietic_cells_CD49dplus_Band3minus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295269_CD34plus_hematopoietic_cells_CD49dplus_Band3minus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295283_CD34plus_hematopoietic_cells_CD49dint_Band3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295270_CD34plus_hematopoietic_cells_CD49dint_Band3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295284_CD34plus_hematopoietic_cells_CD49dint_Band3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295271_CD34plus_hematopoietic_cells_CD49dlo_Band3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295285_CD34plus_hematopoietic_cells_CD49dlo_Band3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295272_CD34plus_hematopoietic_cells_CD49dminusBand3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295286_CD34plus_hematopoietic_cells_CD49dlo_Band3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295273_CD34plus_hematopoietic_cells_CD71minus_CD235minus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295287_CD34plus_hematopoietic_cells_CD49dminusBand3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295274_CD34plus_hematopoietic_cells_CD71plus_CD235minus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295288_CD34plus_hematopoietic_cells_CD49dminusBand3plus.rmdup.bw
	/research/rgs01/project_space/chenggrp/blood_regulome/common/blood_ATAC/PRJNA475744_bulkATAC_VG_2019/sra_download_yli11_2019-10-02/atac_seq_yli11_2019-10-02/bw_files/SRR7295275_CD34plus_hematopoietic_cells_CD71plus_CD235lo.rmdup.bw

