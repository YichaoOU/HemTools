Motif Annotation
================

::

	usage: motif_annotation.py [-h] [-j JID] -f BED_FILE [-d1 D1] [-d2 D2]
	                           [-d3 D3] [-g GENOME] [-m MOTIF_LIST]
	                           [-a GENE_ANNOTATION]

	motif annotation

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        motif_annotation_yli11_2020-07-22)
	  -f BED_FILE, --bed_file BED_FILE
	                        a bed file with chr, start, end as the first 3
	                        columns, addtional columns will be ignored (default:
	                        None)
	  -d1 D1                extend query bed for intersection (default: 0)
	  -d2 D2                extend tss for intersection (default: 2000)
	  -d3 D3                extend epi for intersection (default: 0)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -m MOTIF_LIST, --motif_list MOTIF_LIST
	                        a list of motif location bed files (default:
	                        /home/yli11/Data/Human/hg19/motif_mapping/motif.list)
	  -a GENE_ANNOTATION, --gene_annotation GENE_ANNOTATION
	                        gene annotation file (default: /home/yli11/Data/Human/
	                        hg19/Ensembl_v99_2020_Jan/hg19.ensembl.TSS.gene_name.b
	                        ed)



Summary
^^^^^^^

Given a bed file, this program add columns for nearest TSS and known motifs.


Only working for hg19 and mm9.


Input
^^^^^

bed file, the first 3 columns should be chr, start, end, additional columns will be ignored.


Usage
^^^^

.. code:: bash

	hpcf_interactive

	module load python/2.7.13

	motif_annotation.py -f loci.bed -g hg19

	motif_annotation.py -f loci.bed -g mm9

You will be notified by email when it is finished.

You can use "-d1, -d2, -d3" to extend the input regions.

Output
^^^^^^

The first 3 columns are from user's bed file, then we have columns showing the region name and the extended coordinates (by default, extending length = 0).

Then we have nearest_TSS_gene, nearest_TSS_distance, hard_assignment. Hard_assignment means if the region is overlaped with promoter,  (by default, defined as +-2kb TSS). If YES, the value will be the gene name; otherwise will be ".".

The last column is the overlapped motifs.

+-----------+-------------+-----------+-----------------------+--------------------+------------------+------------------+----------------------+-----------------+----------------------------------------------------------------------------------------------------------------------------+
| query_chr | query_start | query_end | query_name            | query_extend_start | query_extend_end | nearest_TSS_gene | nearest_TSS_distance | hard_assignment | merged_info                                                                                                                |
+===========+=============+===========+=======================+====================+==================+==================+======================+=================+============================================================================================================================+
| chr11     | 4167360     | 4167570   | chr11:4167360-4167570 | 4167360            | 4167570          | OR55B1P          | 955                  | OR55B1P         |                                                                                                                            |
+-----------+-------------+-----------+-----------------------+--------------------+------------------+------------------+----------------------+-----------------+----------------------------------------------------------------------------------------------------------------------------+
| chr11     | 4203440     | 4203590   | chr11:4203440-4203590 | 4203440            | 4203590          | RP11-23F23.2     | 4781                 | .               | HOCOM_ANDR_HUMAN.H11MO.1.A_chr11_4203580,HOCOM_AP2B_HUMAN.H11MO.0.B_chr11_4203571                                          |
+-----------+-------------+-----------+-----------------------+--------------------+------------------+------------------+----------------------+-----------------+----------------------------------------------------------------------------------------------------------------------------+
| chr11     | 4208260     | 4208430   | chr11:4208260-4208430 | 4208260            | 4208430          | RP11-23F23.2     | 0                    | RP11-23F23.2    | HOCOM_AP2A_HUMAN.H11MO.0.A_chr11_4208404,HOCOM_AP2B_HUMAN.H11MO.0.B_chr11_4208332,HOCOM_AP2B_HUMAN.H11MO.0.B_chr11_4208406 |
+-----------+-------------+-----------+-----------------------+--------------------+------------------+------------------+----------------------+-----------------+----------------------------------------------------------------------------------------------------------------------------+
| chr11     | 4208860     | 4209050   | chr11:4208860-4209050 | 4208860            | 4209050          | RP11-23F23.2     | 490                  | RP11-23F23.2    | HOCOM_AP2B_HUMAN.H11MO.0.B_chr11_4208943                                                                                   |
+-----------+-------------+-----------+-----------------------+--------------------+------------------+------------------+----------------------+-----------------+----------------------------------------------------------------------------------------------------------------------------+
| chr11     | 4216260     | 4216410   | chr11:4216260-4216410 | 4216260            | 4216410          | RP11-23F23.2     | 7890                 | .               | HOCOM_AIRE_HUMAN.H11MO.0.C_chr11_4216392                                                                                   |
+-----------+-------------+-----------+-----------------------+--------------------+------------------+------------------+----------------------+-----------------+----------------------------------------------------------------------------------------------------------------------------+
| chr11     | 4218180     | 4218330   | chr11:4218180-4218330 | 4218180            | 4218330          | RP11-23F23.2     | 9810                 | .               | HOCOM_ANDR_HUMAN.H11MO.0.A_chr11_4218218,HOCOM_ANDR_HUMAN.H11MO.0.A_chr11_4218220,HOCOM_ANDR_HUMAN.H11MO.2.A_chr11_4218229 |
+-----------+-------------+-----------+-----------------------+--------------------+------------------+------------------+----------------------+-----------------+----------------------------------------------------------------------------------------------------------------------------+
| chr11     | 4353240     | 4353390   | chr11:4353240-4353390 | 4353240            | 4353390          | SSU72P3          | 2145                 | .               |                                                                                                                            |
+-----------+-------------+-----------+-----------------------+--------------------+------------------+------------------+----------------------+-----------------+----------------------------------------------------------------------------------------------------------------------------+
| chr11     | 4403240     | 4403410   | chr11:4403240-4403410 | 4403240            | 4403410          | OR52B3P          | 3728                 | .               |                                                                                                                            |
+-----------+-------------+-----------+-----------------------+--------------------+------------------+------------------+----------------------+-----------------+----------------------------------------------------------------------------------------------------------------------------+



