RNA-seq: Identification of gene fusion events
==============================================

::

	usage: gene_fusion.py [-h] [-j JID] [-q MAPQ] (-f FASTQ_TSV | --guess_input)
	                      [-g GENOME] [--database DATABASE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        gene_fusion_yli11_2019-10-15)
	  -q MAPQ, --MAPQ MAPQ  Minimal mapping quality, whether to address multi-
	                        mapped reads, set q=0 to consider multi-mapped reads
	                        (default: 20)
	  -f FASTQ_TSV, --fastq_tsv FASTQ_TSV
	                        tab delimited 3 columns (tsv file): Read 1 fastq, Read
	                        2 fastq, sample ID (default: None)
	  --guess_input         Let the program generate the input files for you.
	                        (default: False)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  --database DATABASE   EricScript database (default: /home/yli11/Programs/Eri
	                        cScript/DataBase/ericscript_db_homosapiens_ensembl73)

Installation
^^^^^^^^^^^^

.. code:: bash

	module load R/3.5.1

	R

	install.packages('Ada')

Summary
^^^^^^^

EricScript is one of the best performed gene fusion detection algorithms in a recent review in 2016 Nature Scientific reports. "EricScript has the best balance between true and false fusion detection." "In conclusion, ..., among them, we found that EricScript had 100% PPV on the mixed dataset"

Ref: https://www.nature.com/articles/srep21597


Usage
^^^^^

.. code:: bash

    module load python/2.7.13

    gene_fusion.py --guess_input

    gene_fusion.py -f fastq.tsv

To use different genome version, add ``-g mm10`` option.

Output
^^^^^^

Look for ``fusion.results.filtered.tsv`` in the subfolders of the JobID folder.


Report bug
^^^^^^^^^^

.. code:: bash

    HemTools report_bug

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines



