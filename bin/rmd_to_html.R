#!/home/yli11/.conda/envs/mageck/bin/Rscript


args <- commandArgs(trailingOnly=TRUE)

knitr::opts_chunk$set(dev = 'svg')
knitr::opts_chunk$set(echo = TRUE)


knitr::opts_chunk$set(out.width="200%")
knitr::opts_chunk$set(out.height="200%")

size = as.integer(args[2])
knitr::opts_chunk$set(fig.dim=c(size,size))

rmarkdown::render(args[1], clean=T, output_format="html_document")

