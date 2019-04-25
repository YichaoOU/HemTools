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

