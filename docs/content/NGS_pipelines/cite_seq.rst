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


.. note:: This program assumes the fastq files for each sample is stored in an individual folder. For example, if you have A,B,C sample fastq files in the same directory, then please create a folder for each sample and mv the corresponding fastq files there.

.. note:: If you have A_S1_L001 and A_S2_L001, please note that each sample name should match to a unique S number. So in this example, you can rename A_S2_L001 to A_S1_L002.


You need two input files: ``library.csv`` and ``antibody.csv``, corresponding to the Library CSV and Feature Reference CSV here: https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/feature-bc-analysis

For CITE-seq data, we should have one normal scRNA-seq data and one seq data only for antibody. In the original ``library.csv`` format, the ``sample`` column should be unique, and fastq files should start with the string specified in this column. But here, ``note that for the library.csv used here``, we keep ``sample name`` the same for the same sample, but with 2 different library_type, namely ``Gene Expression`` and ``Antibody Capture``. The python script will transform this batch run library.csv to correct library.csv used for cellranger.

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


Note
^^^^^



cite-seq DASH visualization
"""""""""""""""

This has been included in the pipeline, you don't need to run it manually any more.

::

	usage: cite_seq_vis.py [-h] (--current_dir | --input_csv INPUT_CSV)
	                       [--MT_percent MT_PERCENT] [--max_genes MAX_GENES]
	                       [-o OUTPUT] [-g GENOME]

	cite-seq visualization pipeline

	optional arguments:
	  -h, --help            show this help message and exit
	  --current_dir         run in current dir, suppose cellRanger is finished
	                        correctly (default: False)
	  --input_csv INPUT_CSV
	                        manually input csv (default: None)
	  --MT_percent MT_PERCENT
	                        MT_percent, default is 20, sometimes I use 10 or 5
	                        (default: 20)
	  --max_genes MAX_GENES
	                        max_genes (default: 6000)
	  -o OUTPUT, --output OUTPUT
	                        output prefix (default:
	                        sc_integration_yli11_2021-04-26)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)


Run this after ``sc_data_integration.py``

::

	usage: sc_data_integration.py [-h] -f INPUT_CSV [--MT_prefix MT_PREFIX] [--MT_percent MT_PERCENT] [--max_genes MAX_GENES] [-o OUTPUT] [--citeseq]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT_CSV, --input_csv INPUT_CSV
	                        Need at least 2 columns with column names, Sample,Location, see: https://pegasus.readthedocs.io/en/stable/usage.html (default: None)
	  --MT_prefix MT_PREFIX
	                        MT_prefix, seems that mm is mt- and human is MT- (default: MT-)
	  --MT_percent MT_PERCENT
	                        MT_percent, default is 20, sometimes I use 10 or 5 (default: 20)
	  --max_genes MAX_GENES
	                        max_genes (default: 6000)
	  -o OUTPUT, --output OUTPUT
	                        output prefix pdf (default: sc_integration_yli11_2021-04-26)
	  --citeseq             is data is cite-seq (default: False)

::

	module load conda3
	source activate /home/yli11/.conda/envs/dash
	cite_seq_dash.py sc_integration_yli11_2021-04-25



Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines




















