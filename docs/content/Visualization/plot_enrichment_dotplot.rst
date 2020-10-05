Plot Enrichment dotplot
=======================




::

	usage: plot_enrichment_dotplot.py [-h] -f INPUT -o OUTPUT -x X -y Y -c
	                                  COLOR_BY -s SIZE_BY -W W -H H

	plot enrichment dotplot given dataframe.

	optional arguments:
	  -h, --help            show this help message and exit
	  -f INPUT, --input INPUT
	                        data table input (default: None)
	  -o OUTPUT, --output OUTPUT
	                        output (default: None)
	  -x X                  X-axis (default: None)
	  -y Y                  y-axis (default: None)
	  -c COLOR_BY, --color_by COLOR_BY
	                        color_by (default: None)
	  -s SIZE_BY, --size_by SIZE_BY
	                        size_by (default: None)
	  -W W                  width (default: None)
	  -H H                  heigh (default: None)




Summary
^^^^^^

This python script is just a wrapper for R ggplot2. For cosmetic setting, please modify the generated .R file directly.




Input
^^^^^

Input should be a tsv file. 

::

	Y	logFDR	enrichment	peaks
	regulation of leukocyte degranulation	2.762334384964788	3.355918	NFIX-close
	activation of MAPKKK activity	1.392819473287668	3.099571	NFIX-close
	cell activation	1.1745266252543596	1.2919100000000001	NFIX-close
	regulation of defense response	1.0343254907026753	1.300915	NFIX-close
	response to biotic stimulus	1.0182154493732174	1.2527760000000001	NFIX-close
	response to other organism	0.9941719618960897	1.253802	NFIX-close
	cytoskeleton organization	0.9129401669292968	1.192971	NFIX-close
	positive regulation of immune system process	0.86708967663595	1.218733	NFIX-close
	B cell activation involved in immune response	0.6619875902942272	1.814427	NFIX-close



Usage
^^^^^

All parameters are required parameters. You have to specify X-axis column, Y-axis column, which column used to color, which color used to define dot size, and the output figure name and size.

::

	plot_enrichment_dotplot.py -f plot3.tsv -o test.pdf -x peaks -y Y -c logFDR -s enrichment -W 7 -H 8



R script
^^^^^^^


.. code-block:: R

	# module load R/3.6.1
	library(ggplot2)
	library(DOSE)
	df = read.table("plot3.tsv",header=TRUE,sep="	")
	head(df)
	

	## specifying Y-axis order
	orderBy="logFDR"
	idx <- order(df[[orderBy]], decreasing = T)
	df$Y <- factor(df$Y,levels=rev(unique(df$Y[idx])))

	## specifying X-axis order
	df$peaks <- factor(df$peaks, levels=c("NFIX-open", "NFIX-close", "ATAC-flanking-close"))

	## main plot fuction
	ggplot(df, aes_string(x="peaks", y="Y", size="enrichment", color="logFDR")) +
		geom_point() + scale_size_continuous(range = c(1, 10))+
		scale_color_continuous(low="blue", high="red", name = "logFDR",
			guide=guide_colorbar(reverse=F)) +ylab(NULL)+theme_dose(10)

	## save file, width and height is important,useDingbats=FALSE, compatible with illustrator
	ggsave("test.pdf",width=7,heigh=4,useDingbats=FALSE)





