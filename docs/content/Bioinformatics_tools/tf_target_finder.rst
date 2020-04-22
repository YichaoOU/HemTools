Identify direct targets and co-binding factors
=============





Summary
^^^^^

A common down-stream analysis of ChIP-seq peaks (or more generally, a set of cis-regulatory elements) is to find their target genes. However, assigning distal regulatory elements to their correct target genes is not an easy problem. Systematic comparison of several target gene assignment algorithms based on real promoter capture-C or HiC has found that the best-performing method is only modestly better than a baseline distance method for most benchmark datasets, suggesting that the most confident assignment should be still based on real experiments.

Therefore, our ``TF_target_finder`` pipeline uses promoter-enhancer interactions from promoter capture-C or HiC datasets and outputs a list of high-confidence assignments using differentially expressed genes from WT.vs.KO datasets.


Ref: https://github.com/YichaoOU/TF_target_finder


Input
^^^^^

1. query bed file

2. tss annotation

3. EPI data

4. RNA-seq data

5. A list of chip-seq peaks used for co-binding test

::

	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088371_Cebpb_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088372_cFos_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088373_cMyc_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088378_E2f4_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088379_Egr1_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088380_Elf1_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088381_Eto2_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088382_Gata2_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088383_H2A_AcK5_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088384_H3K27me3_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088385_H3K36me3_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088386_H3K4me3_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088409_Jun_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088410_Ldb1_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088411_Max_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088412_Myb_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088413_Nfe2_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088414_p53_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088415_Rad21_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088416_Stat1P_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/ERR1088417_Stat3_HPC7.vs.ERR1088408_IgG_HPC7_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/SRR054909_HPCminus7_Cell_Line_GSM552232_HPC7_H3AcK9_HPCminus7_Cell_Line.vs.SRR054913_HPCminus7_Cell_Line_GSM552236_HPC7_IgG_HPCminus7_Cell_Line_Input_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/SRR054910_HPCminus7_Cell_Line_GSM552233_HPC7_Fli1_HPCminus7_Cell_Line.vs.SRR054913_HPCminus7_Cell_Line_GSM552236_HPC7_IgG_HPCminus7_Cell_Line_Input_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/SRR054911_HPCminus7_Cell_Line_GSM552234_HPC7_Gata2_HPCminus7_Cell_Line.vs.SRR054913_HPCminus7_Cell_Line_GSM552236_HPC7_IgG_HPCminus7_Cell_Line_Input_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/SRR054912_HPCminus7_Cell_Line_GSM552235_HPC7_Gfi1b_HPCminus7_Cell_Line.vs.SRR054913_HPCminus7_Cell_Line_GSM552236_HPC7_IgG_HPCminus7_Cell_Line_Input_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/SRR054914_HPCminus7_Cell_Line_GSM552237_HPC7_Lmo2_HPCminus7_Cell_Line.vs.SRR054913_HPCminus7_Cell_Line_GSM552236_HPC7_IgG_HPCminus7_Cell_Line_Input_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/SRR054915_HPCminus7_Cell_Line_GSM552238_HPC7_Lyl1_HPCminus7_Cell_Line.vs.SRR054913_HPCminus7_Cell_Line_GSM552236_HPC7_IgG_HPCminus7_Cell_Line_Input_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/SRR054916_HPCminus7_Cell_Line_GSM552239_HPC7_Meis1_HPCminus7_Cell_Line.vs.SRR054913_HPCminus7_Cell_Line_GSM552236_HPC7_IgG_HPCminus7_Cell_Line_Input_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/SRR054917_HPCminus7_Cell_Line_GSM552240_HPC7_Pu1_HPCminus7_Cell_Line.vs.SRR054913_HPCminus7_Cell_Line_GSM552236_HPC7_IgG_HPCminus7_Cell_Line_Input_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/SRR054918_HPCminus7_Cell_Line_GSM552241_HPC7_Runx1_HPCminus7_Cell_Line.vs.SRR054913_HPCminus7_Cell_Line_GSM552236_HPC7_IgG_HPCminus7_Cell_Line_Input_peaks.rmblck.narrowPeak
	/home/yli11/Tools/TF_target_finder/data/HPC7_chip_seq/SRR054919_HPCminus7_Cell_Line_GSM552242_HPC7_Scl_HPCminus7_Cell_Line.vs.SRR054913_HPCminus7_Cell_Line_GSM552236_HPC7_IgG_HPCminus7_Cell_Line_Input_peaks.rmblck.narrowPeak


6.a. main TF motif pwm files

::

	/home/yli11/Tools/TF_target_finder/data/NFIX_mouse_known_motifs.meme

6.b. A list of motif ids used for co-binding test

This input is a tsv file containing TF name and motif names (separated by comma). Full mapping file can be found at: :doc:`motif mapping table <../Data/mouse_motif>`

::

	GATA5	GATA5_MOUSE.H11MO.0.D,M0784_1.02,UP00080_1,UP00080_2
	GATA6	GATA6_MOUSE.H11MO.0.A,M0782_1.02,UP00100_1,UP00100_2
	GCM1	GCM1_MOUSE.H11MO.0.D,M0812_1.02,UP00070_1,UP00070_2
	GCR	GCR_MOUSE.H11MO.0.A,GCR_MOUSE.H11MO.1.A
	GFI1	GFI1_MOUSE.H11MO.0.C,GFI1B_MOUSE.H11MO.0.A,M2285_1.02
	GLI1	GLI1_MOUSE.H11MO.0.C,M6264_1.02




