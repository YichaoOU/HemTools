Genomic features annotatoin given bed file
===================================

::

	usage: annot_gene_features.py [-h] -f INPUT_BED [-g GENOME] [--tss TSS]
	                              [--exon EXON] [--promoter PROMOTER]
	                              [--UTR5 UTR5] [--UTR3 UTR3] [--intron INTRON]
	                              [-d1 D1] [-d2 D2] [-o OUTPUT] [--label LABEL]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT_BED, --input_bed INPUT_BED
	                        3 column bed file, additional columns are OK, but will
	                        be ignored (default: None)
	  -d1 D1                extend query bed for intersection (default: 0)
	  -d2 D2                extending genomic features for intersection (default:
	                        0)
	  -o OUTPUT, --output OUTPUT
	                        output intermediate file (default: output)
	  --label LABEL         prefix for the file (default: genomic_features)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        the annotation file (default: hg19)
	  --tss TSS             tss feature file, 4 columns, chr, start, end , gene
	                        name (default: None)
	  --exon EXON           exon feature file, 4 columns, chr, start, end , gene
	                        name (default: None)
	  --promoter PROMOTER   promoter feature file, 4 columns, chr, start, end ,
	                        gene name (default: None)
	  --UTR5 UTR5           5UTR feature file, 4 columns, chr, start, end , gene
	                        name (default: None)
	  --UTR3 UTR3           3UTR feature file, 4 columns, chr, start, end , gene
	                        name (default: None)
	  --intron INTRON       intron feature file, 4 columns, chr, start, end , gene
	                        name (default: None)



Summary
^^^^^^^

Genomic features are based on Gencode annotation, which is then parsed to exon, promoter, 5UTR, 3UTR, intron, intergenic regions using : https://github.com/saketkc/gencode_regions

Feature assignment program is based on :doc:`EPI assignment program <assign_targets>`


Input
^^^^^

Bed file with at least 3 columns: chr, start, end


Output
^^^^^^

8 columns will be added to the input bed file:

The first 2 columns are nearest_TSS_gene, nearest_TSS_distance.

The next 5 columns are overlaps with exon_gene, promoter_gene, 5UTR_gene, 3UTR_gene, intron_gene.

The last columns is Genomic_features, the priority is Exon, Promoter, 5UTR, 3UTR, Intron, Intergenic. 



Usage
^^^^^

.. code:: bash

	export PATH=$PATH:"/home/yli11/HemTools/bin"
	hpcf_interative.sh
	module load conda3
	source activate /home/yli11/.conda/envs/py2
	annot_gene_features.py -f input.bed -o output.bed






