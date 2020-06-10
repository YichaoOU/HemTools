Super-enhancer identification
===============


There are several super-enhancer prediction tools available. However, when looking at the papers, some of them are not well documented or required many CHIP-seq datasets  (e.g., https://github.com/asntech/improse, https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3180-z). The best one still seems to be a tool published in 2010: ROSE.


ROSE: RANK ORDERING OF SUPER-ENHANCERS
^^^^^

REF: http://younglab.wi.mit.edu/super_enhancer_code.html

There are two usage example I've found:

1. super-enhancer prediction using just H3K27ac.

https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM3439934

2. from their own paper. 

step1: predict enhancer using master TF chip-seq.

Author doesn't provide any code for this step. Reading the method, this step is more subjective and requires some manual inspection on chip-seq peak distribution.

::
	To identify super-enhancers, we first ranked all enhancers in a cell type by increasing total background-subtracted ChIP-seq
	occupancy of Med1, and plotted the total background-subtracted ChIP-seq occupancy of Med1 in units of total rpm/bp (reads
	per million per base pair) (Figures 1C and 4B). In cases where Med1 ChIP-seq data were not available, we used the total background
	subtracted ChIP-seq occupancy of the master regulator instead (Figure S5). These plots revealed a clear point in the distribution of
	enhancers where the occupancy signal began increasing rapidly. To geometrically define this point, we first scaled the data such that
	the x and y axis were from 0-1. We then found the x axis point for which a line with a slope of 1 was tangent to the curve. We define
	enhancers above this point to be super-enhancers, and enhancers below that point to be typical enhancers. The classification of
	enhancers in each cell type as a super-enhancer or typical enhancer can be found in Table S1 for ESCs, Table S5 for pro-B cells,
	and Table S6 for myotubes, Th cells, and macrophages.


step2: construct SE using one master TF chip-seq.

This is ROSE.py

:: 
	We calculated background subtracted total reads per million of OSN, DNaseI, H3K27ac, Med1, and H3K4me1 at the 8,794 ESC
	enhancers. We then normalized the signal such that the maximum was 1.0 for each factor. We then sorted the enhancers and visualized the distribution, zooming in on the bottom right corner of the plot for greater clarity (Figures 1E and S2). Med1 has the
	sharpest transition between the two populations and was therefore considered ‘‘optimal.’’
	We also investigated whether the enhancer feature H3K27ac alone can be used to identify super-enhancers. We found enriched
	regions of H3K27ac ChIP-seq data, and clustered the binding peaks as described in the Definition of Enhancers section. We then
	ranked these domains by H3K27ac ChIP-seq signal, and used the tangent of the curve to define two enhancer populations, as
	described above. This analysis identifies 725 candidate super-enhancers. Of these, 155 were previously identified using OSN and
	Mediator (Figure 1C). Hence, the enhancer feature H3K27ac alone cannot directly substitute for the master transcription factors
	and Mediator in our analysis pipeline

Usage
^^^^^

The simplest one will be just using H3K27ac.


A more complicated one will be using some tool to predict enhancers and then use ROSE to predict super enhancers.

In terms of enhancer prediction, there are also many tools available. The best I found is:

1. CSI-ANN. this tool can use any number of chip-seq data.

2. https://github.com/broadinstitute/ABC-Enhancer-Gene-Prediction

This tool requires ATAC-seq and H3K27ac.




ref
^^^
https://rpubs.com/skyrosepark/393694

