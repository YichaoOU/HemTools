Notes on ATAC-seq, open chromatin, and footprints/motif
========================




low chip-seq peak overlap with ATAC-seq peak
^^^^^^^^^^^^^^^^^^^^^^^^^

In one of the projects I'm doing, one TF only has 55% overlap with ATAC-seq peak, while another TF in the same cell line overlaped 93%. 

I was suprised by this and checked TF-chip-seq data in Hudep2, for BCL11A, GATA1, KLF1 and TAL1. They all above 90%. CTCF is a little lower, 83%. LRF (from GEO), 33%, our LRF (51%). LRF tends to have >100k peaks, same thing in public data and our data.



raw TN5 cut freq from pyDNase
^^^^^^^^^^^^^^^^^^

.. code:: bash

	module load conda3

	source activate /home/yli11/.conda/envs/pydnase

	cd /home/yli11/Pipelines/example_NGS_data/atac_seq/atac_seq_yli11_2021-02-13/bam_files

	dnase_wig_tracks.py -A test.bed 1631312_RFA007.rmdup.uq.bam fw.bdg rev.bdg

fw.bdg and rev.bdg contains the Tn5 cut count.

ref: https://pythonhosted.org/pyDNase/scripts.html?highlight=atac#dnase-wig-tracks-py

reference
^^^^^^^^

https://www.cell.com/cell-systems/pdfExtended/S2405-4712(20)30079-X

