.. HemTools documentation master file, created by
   sphinx-quickstart on Tue Apr  2 09:55:58 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=====================================================
HemTools: *a collection of NGS pipelines and bioinformatic analyses*
=====================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   cut_run
   diffpeaks
   crispr_seq
   chip_seq_pair
   chip_seq_single
   atac_seq
   methylmotifs
   
|                         | CUT&amp;RUN        | ATAC-seq           | ChIP-seq           |
|-------------------------|--------------------|--------------------|--------------------|
| QC1                     | FASTQC             | FASTQC             | FASTQC             |
| Trimming                | skewer             |                    |                    |
| Mapping                 | BWA                | BWA                | BWA                |
| Filtering               | samtools           | samtools           | samtools           |
| bamTobw                 | bamCoverage        | bamCoverage        | bamCoverage        |
| QC2                     | library complexity | library complexity | library complexity |
| QC3 (cross correlation) |                    |                    | run_spp.R          |
| peak calling            | MACS2              | MACS3              | MACS4              |
| bdgTobw                 | wigToBigwig        | wigToBigwig        | wigToBigwig        |

