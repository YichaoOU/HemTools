HemTools Mouse Motif data
=====================

Motif databases
^^^^^^

We have totaly 4809 redudant motifs.


Known motifs come from the following 8 sources:

1. ENCODE motif from Kellis lab (http://compbio.mit.edu/encode-motifs/)

Five motif discovery tools used, train-test cross validated, based on enrichment score

2. Homer (http://homer.ucsd.edu/homer/motif/motifDatabase.html, ``motif2meme.R custom.motifs``)

Included many in silico motifs based on independent analysis of mostly ChIP-Seq data sets using homer. Also included motif databases like JASPAR.

3. JASPAR (downloaded from meme motif database, JASPAR2018_CORE_vertebrates_redundant.meme, motif_databases.12.19.tgz)

4. CIS-BP (downloaded from meme motif database)

Included many inferred motifs from other species.

5. HOCOMOCO (downloaded from meme motif database, HOCOMOCOv11_full_HUMAN_mono_meme_format.meme)

The lab who developed this database is one of the top performing teams in the ENCODE-DREAM challenge.

6. Factorbook (Another version of ENCODE motif, only ~70 motifs, pwm is provided in the supplementary file)

7. Custom motifs from our ChIP-seq data using homer

Currently only included BCL11A (hudep2 cut-run), LRF (hudep2), KLF1 (hudep2) and NFIX (hpc5).

8. Consensus sequence

Current only included GATA_Ebox: ``CAGGTG{N=8,9}GATA``. Consensus sequence pattern is searched using :doc:`cas_motif.py <cas_motif>`.


Annotate bed file with known motifs
^^^^^^^^^^^^^^^^^^^^^^^^^^

Here, we provide one example of using `assign_targets_multi.py <../Bioinformatics_tools/assign_targets>` to annotate your bed file with known motifs. This tool is a generic tool for annotating bed file given another list of bed files.

Motif mapping bed file is generated using FIMO. For motif length <= 7, p-value cutoff is 1e-3. For motif length >=8, default cutoff 1e-4 is used.













