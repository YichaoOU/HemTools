#!/usr/bin/env Rscript
library(chromoMap)
library(plotly)
args <- commandArgs(trailingOnly=TRUE)

chrom_size = args[1] 
annot = args[2] 
a=chromoMap(chrom_size,annot,
          labels=T,
          chr_color = c("#d6d6d6"),
          data_type = "categorical",
          data_based_color_map = T,
          legend=T,
          v_align=F,
          canvas_width=500,
          canvas_height=520,
          lg_x=50,
          lg_y=50
          )
htmlwidgets::saveWidget(a,"chromoMAP_output.html")
export(a,"chromoMAP_output.pdf")

# data_colors = list(c("#f02424","#0e32e6"))
