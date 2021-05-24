#!/usr/bin/env python
import pandas as pd
import os
import sys
import glob
"""
Input is two column tsv

sample id, sample name
scRNA_qc.py input2.list
"""

R_code = """



library(scRNABatchQC)

scRNABatchQC(inputs=c({inputs}),names=c({names}),mincounts=100,mingenes=100,maxmito=0.8)
"""

R_code2 = """
library(Seurat)

library(dplyr)
library(glue)
library(ggplot2)
library(patchwork)
library(cowplot)
library(stringr)
library(tidyr)
library("dplyr")
library(scRNABatchQC)
sample_id = c(%s)
myList = list()
for(i in 1:length(sample_id)){
	s=sample_id[i]
	dir = glue("{s}_results/{s}/outs/filtered_feature_bc_matrix")
	myData <- Read10X(data.dir = dir)
	myList[[i]] = CreateSeuratObject(counts = myData, project = s, assay = "RNA")

}

merged_obj = merge(myList[[1]], y = myList)
# features <- c("HBG1", "HBB", "HBG2",'GYPA',"HBA","GATA1")

human_plot <- function(x){
    tryCatch(
        # This is what I want to do...
        {
        features <- c("HBG1", "HBB", "HBG2",'GYPA',"HBA","GATA1")
		RidgePlot(merged_obj, features = features, ncol = 2,log=TRUE)
		ggsave("RidgePlot_human_genes.png",dpi=400)
        },
        # ... but if an error occurs, tell me what happened: 
        error=function(error_message) {
            message("Human gene failed, using mouse")
        }
    )
}

mouse_plot <- function(x){
    tryCatch(
        # This is what I want to do...
        {
        features <- c("Gata1", "Hbb-bs",'Rhbg','Shbg',"Klf1","Klf4")
		RidgePlot(merged_obj, features = features, ncol = 2,log=TRUE)
		ggsave("RidgePlot_mouse_genes.png",dpi=400)
        },
        # ... but if an error occurs, tell me what happened: 
        error=function(error_message) {
            message("Mouse gene failed")
        }
    )
}

human_plot()
mouse_plot()

scRNABatchQC(inputs=myList,names=c(%s))
"""

# for cite-seq out
R_code3 = """
library(Seurat)

library(dplyr)
library(glue)
library(ggplot2)
library(patchwork)
library(cowplot)
library(stringr)
library(tidyr)
library("dplyr")
library(scRNABatchQC)
sample_id = c(%s)
myList = list()
for(i in 1:length(sample_id)){
	s=sample_id[i]
	dir = glue("{s}/outs/filtered_feature_bc_matrix")
	myData <- Read10X(data.dir = dir)
	myList[[i]] = CreateSeuratObject(counts = myData$`Gene Expression`, project = s, assay = "RNA")

}

merged_obj = merge(myList[[1]], y = myList)
# features <- c("HBG1", "HBB", "HBG2",'GYPA',"HBA","GATA1")

human_plot <- function(x){
    tryCatch(
        # This is what I want to do...
        {
        features <- c("HBG1", "HBB", "HBG2",'GYPA',"HBA","GATA1")
		RidgePlot(merged_obj, features = features, ncol = 2,log=TRUE)
		ggsave("RidgePlot_human_genes.png",dpi=400)
        },
        # ... but if an error occurs, tell me what happened: 
        error=function(error_message) {
            message("Human gene failed, using mouse")
        }
    )
}

mouse_plot <- function(x){
    tryCatch(
        # This is what I want to do...
        {
        features <- c("Gata1", "Hbb-bs",'Rhbg','Shbg',"Klf1","Klf4")
		RidgePlot(merged_obj, features = features, ncol = 2,log=TRUE)
		ggsave("RidgePlot_mouse_genes.png",dpi=400)
        },
        # ... but if an error occurs, tell me what happened: 
        error=function(error_message) {
            message("Mouse gene failed")
        }
    )
}

human_plot()
mouse_plot()

scRNABatchQC(inputs=myList,names=c(%s))
"""


def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

def to_inputs(myList):
	tmp = '"{0}"'
	out = [tmp.format(x) for x in myList]
	return ",".join(out)
def to_inputs2(myList):
	tmp = '"{0}_results/{0}/outs/filtered_feature_bc_matrix"'
	out = [tmp.format(x) for x in myList]
	return ",".join(out)
	
def to_names(myList):
	tmp = '"{0}"'
	out = [tmp.format(x) for x in myList]
	return ",".join(out)
	
# df = pd.read_csv(sys.argv[1],sep="\t",header=None)

# out  = R_code.format(inputs=to_inputs2(df[0]),names = to_names(df[1]))

myList = [x.replace("_results","") for x in glob.glob("*_results")]

if len(myList)>0:
	out  = R_code2%(to_inputs(myList),to_names(myList))
	write_file("tmp.R",out)
	os.system("Rscript tmp.R")
else:
	myList = [x.replace("/","") for x in glob.glob("*/")]
	myList.remove("log_files")
	out  = R_code3%(to_inputs(myList),to_names(myList))
	write_file("tmp.R",out)
	os.system("Rscript tmp.R")
