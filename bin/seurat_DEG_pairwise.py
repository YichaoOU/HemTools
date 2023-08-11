#!/usr/bin/env python

import sys
import os
import argparse

R_code="""
library(Seurat)
library(dplyr)
library(glue)
library(ggplot2)
library(patchwork)
library(cowplot)
library(stringr)
library(tidyr)
library(DAseq)
library(reshape2)
library(ggrepel)
library(corrplot)
library(scales)
library(cluster)
library(misc3d)
library(MASS)
library(plotly)
library(grid)
library(tibble)
library(clustifyr)
library(clustifyrdata)
library(RColorBrewer)
library(DOSE)
library(scclusteval)
library(Scillus)
library(enrichplot)
library(devtools)
library(sccore)
library(Signac)
library(scCATCH)
library(tidyverse)
library(reshape)
library(dittoSeq)
library(clustree)
library(IKAP)
library(ggforce)
library(yaml)
library(org.Mm.eg.db)
library(org.Hs.eg.db)
library(clusterProfiler)
library(scRepertoire)

merged_obj = readRDS("{{R_obj}}")
t <- FindMarkers(merged_obj, ident.1 = "{{ident1}}", ident.2 = "{{ident2}}",logfc.threshold = 0.1)
write.table(t,file=paste0("{{ident1}}",".vs.","{{ident2}}",".DEG.csv"),sep=",",row.names=T)


"""

def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		if myDict[k] == None:
			value = ""
		else:
			value = myDict[k]
		myString = str(myString).replace("{{"+str(k)+"}}",str(value))
	return myString

def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()
	
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	# mainParser.add_argument('-f','--sample_info',  help="a tsv table | if -t and -c not used, you need to provide this sample info file",default="None")
	mainParser.add_argument('-r','--R_obj',required=True)
	mainParser.add_argument('-1','--ident1',  help="ident 1",required=True)
	mainParser.add_argument('-2','--ident2',  help="ident 2",required=True)
	mainParser.add_argument('-o','--output_name',  help="output R script name",required=True)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main(R_code):

	args = my_args()
	args.output_name = args.output_name.replace(" ","")
	R_command = multireplace(R_code,vars(args))
	write_file(args.output_name+".R",R_command)
	os.system("Rscript "+args.output_name+".R")



if __name__ == "__main__":
	main(R_code)



