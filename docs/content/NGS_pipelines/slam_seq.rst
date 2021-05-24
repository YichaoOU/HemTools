SLAM-seq for time-resolved RNA sequencing
=========================================================







Summary
^^^^^^^

Original SLAM-seq pipeline is designed for single-end RNA-seq data, the difference is read alignment. SLAM-seq pipeline works well with ``NextGenMap`` aligner, instead of ``BWA`` or ``bowtie``, because it has a conversion-aware alignment method, although I'm sure you can also use BWA, but it can be troublesome.

.. note:: Even though SLAM-seq had a simple command as ``slamdunk all``, if it uses more than 1 thread, it can cause problems at the ``snp`` step. So it is better to run the 4 steps seperately, given ``map`` and ``filter`` more thread to speed up the analysis.



Suggestions for analyzing PE data is here: 

- https://github.com/t-neumann/slamdunk/issues/57
- https://github.com/Cibiv/NextGenMap/wiki/Documentation








References
^^^^^^^^


https://www.nature.com/articles/nmeth.4435.pdf

https://github.com/t-neumann/slamdunk

http://t-neumann.github.io/slamdunk/docs.html


https://en.wikipedia.org/wiki/Time-resolved_RNA_sequencing

https://www.youtube.com/watch?v=M-hJLlapNPM

