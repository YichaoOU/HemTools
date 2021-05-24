#!/home/yli11/.conda/envs/mageck/bin/Rscript


args <- commandArgs(trailingOnly=TRUE)

knitr::opts_chunk$set(echo = TRUE)

rmarkdown::render(args[1], clean=T, output_format="html_document")

