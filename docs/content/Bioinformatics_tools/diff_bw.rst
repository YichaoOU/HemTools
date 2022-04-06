Diff or merge of two bw files
===============================


::


	usage: diff_bw.py [-h] -b1 B1 -b2 B2 -o O [-op OP] [-pc PC] [-bs BS]

	bw operations

	optional arguments:
	  -h, --help  show this help message and exit
	  -b1 B1      bigwiggle file 1 (default: None)
	  -b2 B2      bigwiggle file 2 (default: None)
	  -o O        output name (default: None)
	  -op OP      operation:
	              log2,ratio,subtract,add,mean,reciprocal_ratio,first,second,
	              diff_mean_log2 (default: diff_mean_log2)
	  -pc PC      pseudocount (default: 1)
	  -bs BS      bin size (default: 10)


Usage
^^^^

Default operation is the difference over mean signal in log2 transformation. Need psedocount, default is 1, but you may want to change it according to the scale of your bw file. Also need to adjust bin size. usually TAD or A/B compartment scores are in 100kb or 10kb scale.

::

	diff_bw.py -b1 Jurkat_20copy_100kb_PC1.iced.bw -b2 Jurkat_HiC_100kb_PC1.iced.bw -pc 0.01 -bs 50000 -o PC1.diff_mean_log2.bw 
	diff_bw.py -b1 Jurkat_20copy_100kb_PC2.iced.bw -b2 Jurkat_HiC_100kb_PC2.iced.bw -pc 0.01 -bs 50000 -o PC2.diff_mean_log2.bw 
	diff_bw.py -b1 Jurkat_20copy.hicexplorer_10kb.tad_score.bedgraph.bw -b2 Jurkat_HiC.hicexplorer_10kb.tad_score.bedgraph.bw -pc 0.1 -bs 5000 -o TAD.diff_mean_log2.bw 


Custom usage
^^^^^^^^^^^^

Please directly using ``bigwigCompare`` to subtract/add bigwiggle files.

https://deeptools.readthedocs.io/en/develop/content/tools/bigwigCompare.html

Usage
----


::

	module load python/2.7.15-rhel7
	bigwigCompare -b1 KO.r1.bw -b2 KO.r2.bw --operation mean -o KO.mean.bw
	bigwigCompare -b1 WT.r1.bw -b2 WT.r2.bw --operation mean -o WT.mean.bw
	bigwigCompare -b1 KO.mean.bw -b2 WT.mean.bw --operation subtract -o KO-WT.bw

commands are running interactively, might take hours.

