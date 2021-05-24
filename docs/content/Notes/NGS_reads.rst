Duplicated reads, multi-mapped reads
=================================


RNA-seq
^^^^^

We usually keep duplicated reads in RNA-seq but remove multi-mapped reads. This is kind of standard.



ChIP-seq & ATAC-seq
^^^^^^^^^^^^^

Usually we only use distinct reads (i.e., ``rmdup.uq``) for paired-end data.

For single-end chip-seq, PCR duplicates are not really differentiable vs true reads, so they are kept, just like RNA-seq.

For study focusing on duplicated regions, e.g., HBG1/HBG2, you can use all reads or de-duplicated reads, but multi-mapped reads should be kept.



Peak calling
^^^^^^^^^^^^

Same thing in peak calling, usually use ``rmdup.uq``. MACS2 peak calling uses all the supplied reads and HemTools provides peaks for 1. all reads 2. rmdup reads 3. rmdup.uq reads. The difference is not that much.


"My conclusion is that there's not much of a difference between only using the uniquely mapped reads or using uniquely mapped reads plus multi-mapped reads as input for peak calling.  But if you want greater specificity of your peak profile and avoid bias from repetitive/ambiguous genomic regions, it's better to use uniquely mapped reads only."

https://groups.google.com/g/macs-announcement/c/9spIkeLwZgE

Some pipelines use multi-mapped reads: https://informatics.fas.harvard.edu/atac-seq-guidelines.html


Mate pairs vs pair-end sequencing
^^^^^^^^^^^

Mate pair sequencing is a specific class of paired-end sequencing where several kb fragments were circularized and chopped to get much longer insertion size.

https://www.illumina.com/documents/products/datasheets/datasheet_genomic_sequence.pdf

