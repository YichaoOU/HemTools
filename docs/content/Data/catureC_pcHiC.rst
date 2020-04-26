Promoter interaction data
==================



hg19
----


Significant interactions were downloaded from two resources

1. https://www.nature.com/articles/s41588-019-0494-8

Supp file 3 (PO interaction) and 4 (PP interaction)

There are 53 genes not found in our TSS file.

::

	{'RP11-332O19.5', 'PHF17', '1-Dec', 'MKI67IP', '1-Mar', 'KIAA1984', 'RP11-57H12.6', 'CTC-360G5.1', 'AC006132.1', 'RP11-122A3.2', '7-Sep', 'CTD-3148I10.1', 'AP003068.6', '1-Sep', '8-Mar', 'C5orf50', '10-Mar', 'AC007405.2', 'AC007431.1', 'AC016722.2', 'C7orf10', '9-Sep', 'C7orf41', '3-Sep', 'AC016722.1', 'RP11-865B13.1', 'NEURL', 'C11orf34', 'SELRC1', 'KIAA1737', 'PHF15', 'NIM1', '6-Mar', '11-Sep', 'AC084121.16', 'CTD-2049J23.3', '2-Mar', 'AP000322.54', 'AC007390.5', 'RP11-1118M6.1', 'C12orf52'}

This paper didn't provide bait coordinates. We will use the coordinates from our TSS annotation file: /home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed

2. https://www.ncbi.nlm.nih.gov/pubmed/27863249

"Detected interactions.zip" from the paper link, using "PCHiC_peak_matrix_cutoff5.txt"

There are 484 baits with NA gene name. NA is filled with nearest gene name based on: /home/yli11/Data/Human/hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.bed

*Process*


Data were processed to output to the following format:

chr, start, end, gene name, score


PP interactions will be double-counted in this format.

bait names such as: AL645728.1;SSU72 will be split into two gene names.

bing ren's data doesn't have score column

::


	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Hippocampus.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Human_ES_cells.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Left_Ventricle.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Psoas.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Aorta.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Fibroblast.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Neural_Progenitor_Cell.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Lung.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Dorsolateral_Prefrontal_Cortex.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Gastric.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Ovary.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Sigmoid_Colon.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Pancreas.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Mesenchymal_Stem_Cell.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Liver.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Small_Bowel.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Trophoblast.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Adrenal_Gland.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Lymphoblastoid_cell_lines.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Bladder.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Mesendoderm.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Spleen.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Thymus.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Right_Ventricle.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Fat.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Right_Atrium.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/hg19.Esophagus.pcHiC.bing_ren.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.tCD4.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.EP.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.Mac0.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.nB.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.naCD4.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.tB.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.tCD8.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.nCD4.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.Mon.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.Mac1.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.nCD8.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.aCD4.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.Ery.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.MK.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.Mac2.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.FoeT.pcHiC.cutoff5.bed
	/home/yli11/Data/Human/hg19/promoter_interaction/PCHi-C/hg19.Neu.pcHiC.cutoff5.bed

