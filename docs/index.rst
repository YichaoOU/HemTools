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
   content/Installation/Installation

General principles
^^^^^^^^^^^^^^^^^^

A typical HemTools command looks like this:

.. code:: bash

    module load python/2.7.13

    HemTools cut_run -f fastq.tsv -d peakcall.tsv

You can always see all available sub-commands by:

.. code:: bash

    HemTools -h

