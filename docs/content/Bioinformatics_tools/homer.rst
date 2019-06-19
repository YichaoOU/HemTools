Homer ChIP-seq analysis
=======================

Reference: `Homer NGS annotation <http://homer.ucsd.edu/homer/ngs/annotation.html>`_

.. code:: bash

	hpcf_interactive -q standard -R "rusage[mem=20000]"

	module load homer/4.9.1



Peak annotation with genomic features: TSS, intron, exon, etc.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Using default genomes**

.. code:: bash

	annotatePeaks.pl [peak file] [genome version] -annStats annotate.log  > output.tsv

[peak file] : narrowPeak file from HemTools

[genome version] : hg18, hg19, mm9, mm10.

**output.tsv** is the peak annotation file, such as TSS-promoter, exon, etc.

Find motifs 
^^^^^^^^^^^

.. code:: bash

	findMotifsGenome.pl [peak_file] [genome_version] myOutput -size 200 -mask -preparsedDir parsing_genome_dir

Ref: http://homer.ucsd.edu/homer/ngs/peakMotifs.html

.. tip:: Need to add "-preparsedDir parsing_genome_dir"  homer will need to write a temp background files, you need some where that is writable.


Motif co-occurrence in peaks 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	annotatePeaks.pl [peak file] [genome version] -annStats annotate.log -m [knownResults/*.motif] -matrix co_occur_motifs > output.tsv

[peak file] : narrowPeak file from HemTools

[genome version] : hg18, hg19, mm9, mm10.

[knownResults/*.motif] : findMotifsGenome.pl output dir

**co_occur_motifs.stats.txt** contains the co-occuring statistics.

**output.tsv** is the peak annotation file, with additional motif occurrence information.

.. tip:: You can control the peak size from the peak mid-point and use it to look for co-occuring motifs. For example, ``-size -300,300`` will extend the peak to -300bp upstream from center and 300bp downstream.

.. code:: bash

	annotatePeaks.pl [peak file] [genome version] -annStats annotate.log -m [knownResults/*.motif] -matrix co_occur_motifs -size -300,300 > output.tsv

[peak file]: for this ``size`` option, you might want to use the ``summits.bed`` file from HemTools.



























