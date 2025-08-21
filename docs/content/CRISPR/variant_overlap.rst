Off-targets and Variants overlap
==========================

::

	usage: off_target_overlap_variant.py [-h] -o OUTPUT --cols COLS -f INPUT file [file ...]

	positional arguments:
	  file                  any number of vcf file, vcf file name is used as additional columns added to your input

	optional arguments:
	  -h, --help            show this help message and exit
	  -o OUTPUT, --output OUTPUT
	                        output file (default: None)
	  --cols COLS           input chr, start, column names, sep by comma (default: None)
	  -f INPUT, --input INPUT
	                        input a csv table with chr start end of your off-targets (default: None)

Summary
^^^^^^^

Variant can affect CRISPR-cas9 activity, especially at PAM positions. This script will report any variant overlap with given off-targets.


Input
^^^^^


1. Off-target table (CSV)
--------------

This CSV table can have any number of columns, but it must have columns for chromosome, start and end location. Users need to provide these 3 column names.

e.g. ``-f CHANGE-seq-BE_CRISPRme_Circle-Seq.all.2_7_2025.csv``, if  your input file is in your working dir. 

2. Variant file (VCF)
----------------------

Usually these files end with ``.haplotype.g.vcf.gz``.

e.g., ``3278245_VK_2506/249598260/3278245_VK_2506.haplotype.g.vcf.gz  3278246_VK_2507/249598265/3278246_VK_2507.haplotype.g.vcf.gz  3278247_VK_2508/249598269/3278247_VK_2508.haplotype.g.vcf.gz`` You can input any number of vcf files, they can be provided as relative path or absolute path. 


Usage
^^^^^

::

	hpcf_interactive

	module load conda3/202402

	source activate /home/yli11/.conda/envs/jupyterlab_2024

	bsub -R "rusage[mem=40000] span[hosts=1]" -n 4 -P Genome -J VCF -q standard -oo job.out -eo job.err "off_target_overlap_variant.py -f CHANGE-seq-BE_CRISPRme_Circle-Seq.all.2_7_2025.csv -o overlap.result --cols '#Chromosome,Start,End' 3278245_VK_2506/249598260/3278245_VK_2506.haplotype.g.vcf.gz  3278246_VK_2507/249598265/3278246_VK_2507.haplotype.g.vcf.gz  3278247_VK_2508/249598269/3278247_VK_2508.haplotype.g.vcf.gz"


Output
^^^^^^^^


Overlap results keep the original input table the same, but adding vcf file name columns to indicate variants overlap. The last columns are vcf file names, if it shows variant(s), then it means that off-target overlaps with a variant. Variant ID is ``chr:pos:ref:variant`` format, the ref or variant base is always on positive strand. 








