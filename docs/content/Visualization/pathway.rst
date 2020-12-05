Pathway visualization
===================







Summary
^^^^^^^

1. a good online server to search and visualize pathways containing a gene set

https://pathme.scai.fraunhofer.de/

Q: is there a way to highlight up and down-regulated genes in this visualization

A: PathView from R is able to do it (only for KEGG pathways). First, go to https://www.kegg.jp/ to find a list of KEGG pathway ids that contain your query gene, and then run pathview.R

source activate single_cell

::


	library(pathview)

	input_table = "20copy_vs_Jurkat.gene.final.combined.tpm.csv"
	seperator = ","
	LFC_column = "logFC"

	if (seperator == "\\t"){
		res <- read.csv(input_table, header=TRUE,sep="\t")
	}else{
		res <- read.csv(input_table, header=TRUE,sep=seperator)
	}


	rownames(res) = make.unique(as.character(res[,1]))
	print (head(res))
	pathway_ids = c("04060","04061","04144","04151","04630","04640","04658","04659","05162","05166","05200")


	for (i in pathway_ids){

	pv.out <- pathview(gene.data = res[LFC_column],
	gene.idtype = "ENSEMBL", 
	pathway.id = i, species = "hsa", same.layer = T,
	out.suffix = i, keys.align = "y", kegg.native = T,res=600,key.pos = "bottomright")

	}