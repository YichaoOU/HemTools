Calculate motif occurrence given bed
=====================

Motif databases
^^^^^^

We have totaly 4809 redudant motifs. Currently, we have motif mapping bed files for HOMOCOMO and JASPAR, correponds to 800+ TFs.


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

Input
-----

**A list of motif bed files**

For example:

::
	ls /home/yli11/Data/Human/hg38/motif_mapping/new_format/*.bed > input.list

::

	head input.list
	===============

	/home/yli11/Data/Human/hg38/motif_mapping/new_format/AHR.processed.bed
	/home/yli11/Data/Human/hg38/motif_mapping/new_format/AIRE.processed.bed
	/home/yli11/Data/Human/hg38/motif_mapping/new_format/ALX1.processed.bed
	/home/yli11/Data/Human/hg38/motif_mapping/new_format/ALX3.processed.bed

File name is ``[TF].processed.bed``.

**Query bed file**

at least 3 columns: chr, start, end. Additional columns will be kept in the output.



Usage
----


.. code:: bash

	export PATH=$PATH:"/home/yli11/HemTools/bin"

	hpcf_interative.sh

	module load conda3

	source activate /home/yli11/.conda/envs/py2

	assign_targets_multi.py -q input.bed --epi_file_list input.list -o input.bed.assigned_targets.bed










