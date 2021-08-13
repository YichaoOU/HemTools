.. HemTools documentation master file, created by
   sphinx-quickstart on Tue Apr  2 09:55:58 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================================================================
HemTools: *a collection of NGS pipelines and bioinformatic analyses*
====================================================================


.. toctree::
   :maxdepth: 2
   
   content/NGS_pipelines/NGS_pipelines
   content/Visualization/data_visualization
   content/Motif_analysis/motif_analysis
   content/Integrative_analysis/Integrative_analysis
   content/Linux_Art/linux_art
   content/Installation/Installation
   jupyter_notebooks/notebooks
   content/Bioinformatics_tools/tools
   content/Data/data
   MetaData/metadata
   content/Gallery/standalones
   content/Differential_analysis/index
   content/Notes/notes
   content/Machine_learning/index
   content/CRISPR/index
   content/Bioinformatics_Core_Competencies/index

Ask question here
^^^^^^^^^^^^^^^^^

https://gitter.im/hemtools/community

General principles
^^^^^^^^^^^^^^^^^^

A typical HemTools command looks like this:

.. code:: bash

    module load python/2.7.13

    HemTools cut_run -f fastq.tsv -d peakcall.tsv

You can always see all available sub-commands by:

.. code:: bash

    HemTools -h

.. highlight:: none

:: 

  usage: HemTools [-h] [-v]
                  {cut_run,chip_seq_pair,chip_seq_single,atac_seq,report_bug,volcano_plot,crispr_seq}
                  ...

  HemTools: performs NGS pipelines and other common analyses. Contact:
  Yichao.Li@stjude.org or Yong.Cheng@stjude.org

  positional arguments:
    {cut_run,chip_seq_pair,chip_seq_single,atac_seq,report_bug,volcano_plot,crispr_seq}
                          Available APIs in HemTools
      cut_run             CUT & RUN pipeline
      chip_seq_pair       Paired-end ChIP-seq pipeline
      chip_seq_single     Single-end ChIP-seq pipeline
      atac_seq            ATAC-seq pipeline
      report_bug          Email the log files to the developer.
      volcano_plot        Data visualization: Volcano plot
      crispr_seq          Genome-wide CRISPR Screening pipeline

  optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit


Duplicated reads and unique reads
^^^^

Duplicated reads refer to reads that have the same 5'end position.

Unique reads refer to uniquely mapped reads as compared to multi-mapped reads.

In all NGS pipelines, we provide results from:

1. raw reads: .markdup.bam, .all.bw, _peak.NarrowPeak

2. remove duplicates reads: rmdup.bam, rmdup.bw, rmdup_peak.NarrowPeak

3. remove duplicates and unique reads: rmdup.uq.bam, rmdup.uq.bw, rmdup.uq_peak.NarrowPeak

For general usage, rmdup.uq is commonly accepted.

For people focusing on HBG1 and HBG2, raw reads or rmdup reads can be used.

Mapping rate is usually > 95% for high quality data.

Duplicated reads could be PCR duplicates or real signals, can be ranging from 5% to 20% for high quality data. I think I've seen cases where the duplicate rate is nearly 40% in some GEO datasets. 

Multi-mapped reads are not a lot, maybe 1% to 2%. Never seen any data with >10% multi-mapped reads yet.

FAQ
^^^

How do I list all of my past analyses?
---------------------------------

All the locations of the past analyses are logged here:  ``~/.hemtools_meta/my_dir.csv``

Error loading python
---------------------------------

.. code:: bash 

  /hpcf/apps/python/install/2.7.13/bin/python: error while loading shared libraries: libpython2.7.so.1.0: cannot open shared object file: No such file or directory

A: Missing python module. Just do ``module load python``
 
ERROR: temporary directory is not writable: 'normalize_bw_given_peak_yli11_2021-06-20'
-----------------------

Interesting, this should be an HPC error, not due to HemTools bug.


Here is a video

.. video:: _static/video.mp4

.. raw:: html

  <video controls width="690" src="_static/video.mp4#t=0.1"></video>