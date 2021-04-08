CITE-seq (scRNA-seq with antibodies) analysis
============================

:: 

	usage: single_cell2.py [-h] [-j JID] -f LIBRARY_CSV [-a ANTIBODY_BARCODE]
	                       [-g GENOME] [--genes GENES]
	                       [--cellranger_refdata CELLRANGER_REFDATA]

	perform 10X single-cell RNA-seq analysis or CITE-seq

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        single_cell2_yli11_2021-04-05)
	  -f LIBRARY_CSV, --library_csv LIBRARY_CSV
	                        A list of group name (fastq file prefix). (default:
	                        None)
	  -a ANTIBODY_BARCODE, --antibody_barcode ANTIBODY_BARCODE
	                        antibody barcodes see: https://support.10xgenomics.com
	                        /single-cell-gene-
	                        expression/software/pipelines/latest/using/feature-bc-
	                        analysis (default: None)
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm10. (default: hg38)
	  --cellranger_refdata CELLRANGER_REFDATA
	                        Not for end-user (default: /research/rgs01/application
	                        s/hpcf/authorized_apps/rhel7_apps/cellranger/refdata
	                        /refdata-cellranger-GRCh38-3.0.0/)


Summary
^^^^^^^

Perform CITE-seq analysis. Only for CITE-seq data.



Input
^^^^^

You need two input files: ``library.csv`` and ``antibody.csv``, corresponding to the Library CSV and Feature Reference CSV here: https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/feature-bc-analysis

For CITE-seq data, we should have one normal scRNA-seq data and one seq data only for antibody. In the original ``library.csv`` format, the ``sample`` column should be unique. But here, ``note that for the library.csv used here``, we keep ``sample name`` the same for the same sample, but with 2 different library_type, namely Gene Expression and Antibody Capture. The python script will transform this batch run library.csv to correct library.csv used for cell ranger.

The following antibody.csv is for TotalSeq-B type. There are also A or C types.

::


	==> antibody.csv <==
	id,name,read,pattern,sequence,feature_type
	CD235ab,CD235ab_TotalSeqB,R2,5PNNNNNNNNNN(BC)NNNNNNNNN,GCTCCTTTACACGTA,Antibody Capture
	CD71,CD71_TotalSeqB,R2,5PNNNNNNNNNN(BC)NNNNNNNNN,CCGTGTTCCTCATTA,Antibody Capture


	==> library.csv <==
	fastqs,sample,library_type
	/ABS_PATH/2-1437806/,WT_CD34_Diff_D7,Gene Expression
	/ABS_PATH/2-1437807/,HS_D0_CD34_Diff_D7,Gene Expression
	/ABS_PATH/2-1437808/,HS_D6_CD34_Diff_D7,Gene Expression
	/ABS_PATH/2-1437809/,WT_CD34_Diff_D7,Antibody Capture
	/ABS_PATH/2-1437810/,HS_D0_CD34_Diff_D7,Antibody Capture
	/ABS_PATH/2-1437811/,HS_D6_CD34_Diff_D7,Antibody Capture




Usage
^^^^^

.. code:: bash

    module load python/2.7.13

    single_cell2.py -f library.csv -a antibody.csv -g hg38


Output
^^^^^^


Gene expression table
"""""""""""""""""""""

A file named ``cellrange_final_gene_expression_removed_all_zeros.csv`` is located at ``{{job_id}}/{{group_name}}_results/{{group_name}}/outs``

Report bug
^^^^^^^^^^

.. code:: bash

    $ HemTools report_bug




Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines




















