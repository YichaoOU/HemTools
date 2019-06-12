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

	annotatePeaks.pl [peak file] [genome version] -annStats annotate.log  > [output.tsv]

[peak file] : narrowPeak file from HemTools

[genome version] : hg18, hg19, mm9, mm10.


Motif co-occurrence in peaks 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	annotatePeaks.pl [peak file] [genome version] -annStats annotate.log -m [knownResults/*.motif] -matrix co_occur_motifs > [output.tsv]

[peak file] : narrowPeak file from HemTools

[genome version] : hg18, hg19, mm9, mm10.

[knownResults/*.motif] : findMotifsGenome.pl output dir

.. tip:: You can control the peak size from the peak mid-point and use it to look for co-occuring motifs. For example, ``-size -300,300`` will extend the peak to -300bp upstream from center and 300bp downstream.

.. code:: bash

	annotatePeaks.pl [peak file] [genome version] -annStats annotate.log -m [knownResults/*.motif] -matrix co_occur_motifs ``-size -300,300`` > [output.tsv]





























