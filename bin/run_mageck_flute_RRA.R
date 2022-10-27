#!/usr/bin/env Rscript
library(MAGeCKFlute)
library(clusterProfiler)
library("pathview")
library(ReactomePA)
library(org.Hs.eg.db)
library(ggplot2)
library(gridExtra)
library(grid)


# fix no output error for ncRNA
FluteRRA <- function(gene_summary,
                     sgrna_summary = NULL,
                     keytype = "Symbol",
                     organism = "hsa",
                     incorporateDepmap = TRUE,
                     cell_lines = NA, lineages = "All",
                     omitEssential = FALSE,
                     top = 5, toplabels = NULL,
                     scale_cutoff = 2,
                     limit = c(2, 200),
                     pvalueCutoff = 0.25,
                     proj = NA,
                     width = 12, height = 12,
                     outdir = ".",
                     verbose = TRUE){

  ## Prepare the output environment ##
  requireNamespace("ggplot2")
  message(Sys.time(), " # Create output dir and pdf file ...")
  outdir = file.path(outdir, paste0("MAGeCKFlute_", proj))
  dir.create(file.path(outdir), showWarnings = FALSE)
  dir.create(file.path(outdir,"RRA"), showWarnings=FALSE)
  output_pdf = paste0("FluteRRA_", proj, ".pdf")

  pdf(file.path(outdir, output_pdf), width = width, height = height)

  ## Visualize the top essential genes ##
  message(Sys.time(), " # Read RRA result ...")
  dd = ReadRRA(gene_summary)
  dd$LogFDR = -log10(dd$FDR)
  if(tolower(keytype)!="entrez"){
    dd$EntrezID = TransGeneID(dd$id, keytype, "Entrez", organism = organism)
  }else{
    dd$EntrezID = dd$id
  }
  if(tolower(keytype)!="symbol"){
    dd$Symbol = TransGeneID(dd$id, keytype, "Symbol", organism = organism)
  }else{
    dd$Symbol = dd$id
  }
  if(organism != "hsa"){
    dd$HumanGene = TransGeneID(dd$id, keytype, "Symbol",
                               fromOrg = organism, toOrg = "hsa")
  }else{
    dd$HumanGene = dd$Symbol
  }
  idx1 = is.na(dd$EntrezID)
  idx2 = !is.na(dd$EntrezID) & duplicated(dd$EntrezID)
  idx = idx1|idx2
  if(sum(idx1)>0) message(sum(idx1), " genes genes fail to convert into Entrez IDs: ",
                          paste0(dd$id[idx1], collapse = ", "))
  if(sum(idx2)>0) message(sum(idx2), " genes have duplicate Entrez IDs: ",
                          paste0(dd$id[idx2], collapse = ", "))
  # print (dd)
		if (dim(dd[!idx, ])[1]>2){
			dd = dd[!idx, ]
		}
		
		# print (dd)
  if(!is.null(sgrna_summary)){
    dd.sgrna = ReadsgRRA(sgrna_summary)
    dd.sgrna = dd.sgrna[dd.sgrna$Gene%in%dd$id, ]
    if(tolower(keytype)!="entrez"){
      dd.sgrna$EntrezID = TransGeneID(dd.sgrna$id, keytype, "Entrez", organism = organism)
    }else{
      dd.sgrna$EntrezID = dd.sgrna$id
    }
    if(tolower(keytype)!="symbol"){
      dd.sgrna$Symbol = TransGeneID(dd.sgrna$id, keytype, "Symbol", organism = organism)
    }else{
      dd.sgrna$Symbol = dd.sgrna$id
    }
    if(organism != "hsa"){
      dd.sgrna$HumanGene = TransGeneID(dd.sgrna$Gene, keytype, "Symbol",
                                       fromOrg = organism, toOrg = "hsa")
    }else{
      dd.sgrna$HumanGene = dd.sgrna$Symbol
    }
  }else{
    dd.sgrna = data.frame(sgrna = NA, Gene = NA, LFC = NA,
                          EntrezID = NA, Symbol = NA, HumanGene = NA)
  }
  cutoff = c(-CutoffCalling(dd$Score, scale_cutoff),
             CutoffCalling(dd$Score, scale_cutoff))
  write.table(dd, file.path(outdir, paste0("RRA/", proj, "_processed_data.txt")),
              sep = "\t", row.names = FALSE, quote = FALSE)
		tryCatch(
		{
  if(incorporateDepmap){
    dd = IncorporateDepmap(dd, symbol = "HumanGene", cell_lines = cell_lines,
                           lineages = lineages)
    ## Nine-squares ##
    p.square = ScatterView(dd, x = "Depmap", y = "Score", label = "Symbol",
                           groups = c("midleft", "topcenter", "midright", "bottomcenter"),
                           groupnames = c("Group1", "Group2", "Group3", "Group4"),
                           auto_cut_x = TRUE, y_cut = cutoff,
                           auto_cut_diag = TRUE, top = top,
                           display_cut = TRUE) + ylab("Customized")
    ggsave(file.path(outdir, "RRA/SquareView_Customized_Depmap.png"),
           p.square, width = 5, height = 4)
    write.table(dd, file.path(outdir, paste0("RRA/", proj, "_incorporate_depmap.txt")),
                sep = "\t", row.names = FALSE, quote = FALSE)

    E1 = EnrichSquare(p.square$data, id = "EntrezID", keytype = "entrez",
                      x = "Depmap", y = "Score", pvalue = pvalueCutoff,
                      organism=organism, filename="RRA", limit = limit,
                      out.dir=file.path(outdir, "RRA/"))
  }
  if(omitEssential){
    dd = OmitCommonEssential(dd, symbol = "HumanGene")
    dd.sgrna = OmitCommonEssential(dd.sgrna, symbol = "HumanGene")
    write.table(dd, file.path(outdir, paste0("RRA/", proj, "_omit_essential.txt")),
                sep = "\t", row.names = FALSE, quote = FALSE)
  }



		},
		error=function(cond){}
		
		,
		warning=function(cond){}
		
		,
		finally={
  dd$RandomIndex = sample(1:nrow(dd), nrow(dd))

  p1 = ScatterView(dd, x = "Score", y = "LogFDR", label = "Symbol",
                   x_cut = cutoff, model = "volcano", top = top,
                   toplabels = toplabels, display_cut = TRUE)
  ggsave(file.path(outdir,"RRA/VolcanoView_RRA.png"), p1,
         units = "in", width = 5, height = 4)
		# message("failed gene level volcano")
		}
		)


  # geneList = dd$Score
  # names(geneList) = dd$Symbol
  # dd$Rank = rank(dd$Score)
  # p2 = ScatterView(dd, x = "Rank", y = "Score", label = "Symbol",
  #                  y_cut = cutoff, groups = c("top", "bottom"),
  #                  top = top, toplabels = toplabels,
  #                  display_cut = TRUE)
  # ggsave(file.path(outdir,"RRA/RankView_Gene.png"), p2,
  #        units = "in", width = 3, height = 5)
		# print (dd.sgrna)
  p2 = sgRankView(dd.sgrna, top = top, bottom = top)
  ggsave(file.path(outdir,"RRA/RankView_sgRNA.png"), p2, units = "in", width = 6.5, height = 5)
		# message("#####################################ddd")
		# tryCatch({
		# message("#####################################p3")
		# print (head(dd))
		# print (head(dd[dd$Score>0, ]))
		# print (head(dd[dd$Score<0, ]))
  p3 = ScatterView(dd[dd$Score>0, ], x = "RandomIndex", y = "Score", label = "Symbol",
                   y_cut = cutoff, groups = "top", top = top)
  ggsave(file.path(outdir, "RRA/ScatterView_Positive.png"), p2, width = 5, height = 4)
  p4 = ScatterView(dd[dd$Score<0, ], x = "RandomIndex", y = "Score", label = "Symbol",
                   auto_cut_y = TRUE, groups = "bottom", top = top)
  ggsave(file.path(outdir, "RRA/ScatterView_Negative.png"), p2, width = 5, height = 4)
dd$Rank = rank(dd$Score,ties.method="first")
# print (head(dd))
p5 = ScatterView(dd, x = "Rank", y = "Score", label = "id", 
                 top = top, auto_cut_y = TRUE, ylab = "Log2FC", 
                 groups = c("top", "bottom"))
ggsave(file.path(outdir, "RRA/ScatterView_rankFC.png"), p5, width = 5, height = 5)
dd$Rank = rank(-dd$LogFDR,ties.method="first")
# print (head(dd))
save(dd,file="test.RData")
p6 = ScatterView(dd, x = "Rank", y = "LogFDR", label = "id", model ="rank",
                 top = top,x_cut=top,ylab = "LogFDR",label.top=T,max.overlaps=100)
ggsave(file.path(outdir, "RRA/ScatterView_rank_logFDR.png"), p6, width = 5, height = 5)
		# }
		# ,
		# error=function(cond){}
		
		# ,
		# warning=function(cond){}
		
		# ,
		# finally={
  # p3 = ScatterView(dd[dd$Score>0, ], x = "RandomIndex", y = "Score", label = "Gene",
                   # y_cut = cutoff, groups = "top", top = top)
  # ggsave(file.path(outdir, "RRA/ScatterView_Positive.png"), p2, width = 5, height = 4)
  # p4 = ScatterView(dd[dd$Score<0, ], x = "RandomIndex", y = "Score", label = "Gene",
                   # auto_cut_y = TRUE, groups = "bottom", top = top)
  # ggsave(file.path(outdir, "RRA/ScatterView_Negative.png"), p2, width = 5, height = 4)

		# }
		# )
		
		



  grid.arrange(p1, p2, p3, p4, p5,p6, ncol = 2)
		
  ## Enrichment analysis ##
  # dd = dd[!(is.na(dd$HumanGene)|duplicated(dd$HumanGene)), ]
  universe = dd$EntrezID
  geneList = dd$Score; names(geneList) = dd$EntrezID
  idx1 = dd$Score<cutoff[1]; idx2 = dd$Score>cutoff[2]
  kegg.pos = EnrichAnalyzer(geneList=geneList[idx2], universe=universe,
                            organism=organism, pvalueCutoff=pvalueCutoff,
                            limit = limit, keytype = "entrez",
                            type = "KEGG+REACTOME+GOBP+Complex")
  if(!is.null(kegg.pos) && nrow(kegg.pos@result)>0){
    keggA = kegg.pos@result[grepl("KEGG", kegg.pos@result$ID), ]
    gobpA = kegg.pos@result[grepl("^GO", kegg.pos@result$ID), ]
    reactomeA = kegg.pos@result[grepl("REACTOME", kegg.pos@result$ID), ]
    complexA = kegg.pos@result[grepl("CPX|CORUM", kegg.pos@result$ID), ]
    keggA = list(enrichRes = keggA, gridPlot = EnrichedView(keggA, top = top, bottom = 0)
                 + labs(title = "KEGG: positive"))
    gobpA = list(enrichRes = gobpA, gridPlot = EnrichedView(gobpA, top = top, bottom = 0)
                 + labs(title = "GOBP: positive"))
    reactomeA = list(enrichRes = reactomeA, gridPlot = EnrichedView(reactomeA, top = top, bottom = 0)
                     + labs(title = "REACTOME: positive"))
    complexA = list(enrichRes = complexA, gridPlot = EnrichedView(complexA, top = top, bottom = 0)
                    + labs(title = "Complex: positive"))
  }else{
    keggA = gobpA = reactomeA = complexA = list(enrichRes = NULL, gridPlot = noEnrichPlot())
  }
  kegg.neg = EnrichAnalyzer(geneList=geneList[idx1], universe=universe,
                            organism=organism, pvalueCutoff=pvalueCutoff,
                            limit = limit, keytype = "entrez",
                            type = "KEGG+REACTOME+GOBP+Complex")
  if(!is.null(kegg.neg) && nrow(kegg.neg@result)>0){
    keggB = kegg.neg@result[grepl("KEGG", kegg.neg@result$ID), ]
    gobpB = kegg.neg@result[grepl("^GO", kegg.neg@result$ID), ]
    reactomeB = kegg.neg@result[grepl("REACTOME", kegg.neg@result$ID), ]
    complexB = kegg.neg@result[grepl("CPX|CORUM", kegg.neg@result$ID), ]
    keggB = list(enrichRes = keggB,
                 gridPlot = EnrichedView(keggB, top = 0, bottom = top)
                 + labs(title = "KEGG: negative"))
    gobpB = list(enrichRes = gobpB,
                 gridPlot = EnrichedView(gobpB, top = 0, bottom = top)
                 + labs(title = "GOBP: negative"))
    reactomeB = list(enrichRes = reactomeB,
                     gridPlot = EnrichedView(reactomeB, top = 0, bottom = top)
                     + labs(title = "REACTOME: negative"))
    complexB = list(enrichRes = complexB,
                    gridPlot = EnrichedView(complexB, top = 0, bottom = top)
                    + labs(title = "Complex: negative"))
  }else{
    keggB = gobpB = reactomeB = complexB = list(enrichRes = NULL, gridPlot = noEnrichPlot())
  }
  grid.arrange(keggA$gridPlot, gobpA$gridPlot, reactomeA$gridPlot, complexA$gridPlot, ncol = 2)
  grid.arrange(keggB$gridPlot, gobpB$gridPlot, reactomeB$gridPlot, complexB$gridPlot, ncol = 2)

  ## Save enrichment results ##
  if(!is.null(kegg.pos) && nrow(kegg.pos@result)>0){
    write.table(keggA$enrichRes, file.path(outdir, "RRA/Positive_kegg.txt"),
                sep="\t", row.names = FALSE, col.names = TRUE, quote=FALSE)
    ggsave(keggA$gridPlot, filename=file.path(outdir, "RRA/Positive_kegg.png"),
           units = "in", width=6.5, height=4)
    write.table(reactomeA$enrichRes, file.path(outdir, "RRA/Positive_reactome.txt"),
                sep="\t", row.names = FALSE, col.names = TRUE,quote=FALSE)
    ggsave(reactomeA$gridPlot, filename=file.path(outdir, "RRA/Positive_reactome.png"),
           units = "in", width=6.5, height=4)
    write.table(gobpA$enrichRes, file.path(outdir, "RRA/Positive_gobp.txt"),
                sep="\t", row.names = FALSE, col.names = TRUE,quote=FALSE)
    ggsave(gobpA$gridPlot, filename=file.path(outdir, "RRA/Positive_gobp.png"),
           units = "in", width=6.5, height=4)
    write.table(complexA$enrichRes, file.path(outdir, "RRA/Positive_complex.txt"),
                sep="\t", row.names = FALSE, col.names = TRUE,quote=FALSE)
    ggsave(complexA$gridPlot, filename=file.path(outdir, "RRA/Positive_complex.png"),
           units = "in", width=6.5, height=4)
  }
  if(!is.null(kegg.neg) && nrow(kegg.neg@result)>0){
    write.table(keggB$enrichRes, file.path(outdir, "RRA/Negative_kegg.txt"),
                sep="\t", row.names = FALSE, col.names = TRUE, quote=FALSE)
    ggsave(keggB$gridPlot, filename=file.path(outdir, "RRA/Negative_kegg.png"),
           units = "in", width=6.5, height=4)
    write.table(reactomeB$enrichRes, file.path(outdir, "RRA/Negative_reactome.txt"),
                sep="\t", row.names = FALSE, col.names = TRUE,quote=FALSE)
    ggsave(reactomeB$gridPlot, filename=file.path(outdir, "RRA/Negative_reactome.png"),
           units = "in", width=6.5, height=4)
    write.table(gobpB$enrichRes, file.path(outdir, "RRA/Negative_gobp.txt"),
                sep="\t", row.names = FALSE, col.names = TRUE,quote=FALSE)
    ggsave(gobpB$gridPlot, filename=file.path(outdir, "RRA/Negative_gobp.png"),
           units = "in", width=6.5, height=4)
    write.table(complexB$enrichRes, file.path(outdir, "RRA/Negative_complex.txt"),
                sep="\t", row.names = FALSE, col.names = TRUE,quote=FALSE)
    ggsave(complexB$gridPlot, filename=file.path(outdir, "RRA/Negative_complex.png"),
           units = "in", width=6.5, height=4)
  }
  if(incorporateDepmap){
    grid.arrange(p.square, ncol = 1)
    grid.arrange(E1$kegg1$gridPlot, E1$reactome1$gridPlot,
                 E1$gobp1$gridPlot, E1$complex1$gridPlot, ncol = 2)
    grid.arrange(E1$kegg2$gridPlot, E1$reactome2$gridPlot,
                 E1$gobp2$gridPlot, E1$complex2$gridPlot, ncol = 2)
    grid.arrange(E1$kegg3$gridPlot, E1$reactome3$gridPlot,
                 E1$gobp3$gridPlot, E1$complex3$gridPlot, ncol = 2)
    grid.arrange(E1$kegg4$gridPlot, E1$reactome4$gridPlot,
                 E1$gobp4$gridPlot, E1$complex4$gridPlot, ncol = 2)
    grid.arrange(E1$kegg12$gridPlot, E1$reactome12$gridPlot,
                 E1$gobp12$gridPlot, E1$complex12$gridPlot, ncol = 2)
    grid.arrange(E1$kegg13$gridPlot, E1$reactome13$gridPlot,
                 E1$gobp13$gridPlot, E1$complex13$gridPlot, ncol = 2)
    grid.arrange(E1$kegg24$gridPlot, E1$reactome24$gridPlot,
                 E1$gobp24$gridPlot, E1$complex24$gridPlot, ncol = 2)
    grid.arrange(E1$kegg34$gridPlot, E1$reactome34$gridPlot,
                 E1$gobp34$gridPlot, E1$complex34$gridPlot, ncol = 2)
  }
  dev.off()
}


























args <- commandArgs(trailingOnly=TRUE)

rra_gene = read.table(args[1],header=T,sep="\t")
rra_sgRNA = read.table(args[2],header=T,sep="\t")
# rra_gene = read.table(rra_gene,header=T,sep="\t")
# rra_sgRNA = read.table(rra_sgRNA,header=T,sep="\t")
gdata = ReadRRA(args[1])
outFile=args[3]
organism=args[4]

# from MAGeCKFlute
# FluteRRA(rra_gene, rra_sgRNA, prefix=outFile, organism=organism)
FluteRRA(rra_gene, rra_sgRNA, outdir="./",proj=outFile, organism=organism)
# FluteRRA(rra_gene, rra_sgRNA, outdir=paste("MAGeCKFlute_",outFile,"",sep=""),proj=outFile, organism=organism)

# geneList = gdata$Score
# names(geneList) = gdata$id
LFC_cut = subset(gdata,Score>=1 | Score<=-1)
geneList_LFC= LFC_cut$Score
names(geneList_LFC) = LFC_cut[,1]
enrich = EnrichAnalyzer(geneList = geneList_LFC, keytype = "Symbol", method = "HGT", limit = c(3, 200),pvalueCutoff = 0.5, organism=organism)
write.table(enrich, file=paste("MAGeCKFlute_",outFile,"/EnrichAnalyzer.tsv",sep=""), sep="\t", quote=FALSE, row.names=TRUE)

pdf(paste("MAGeCKFlute_",outFile,"/EnrichedGeneView.pdf",sep=""))
EnrichedGeneView(slot(enrich, "result"), geneList_LFC, keytype = "Symbol",width=10)
dev.off()

pdf(paste("MAGeCKFlute_",outFile,"/EnrichedView.pdf",sep=""))
EnrichedView(slot(enrich, "result"))
dev.off()

# pdf(paste("MAGeCKFlute_",outFile,"/GSEA_plot_1.pdf",sep=""))
# gseaplot(enrich, geneSetID = 1, title = enrich$Description[1])
# dev.off()






# from https://yulab-smu.top/biomedical-knowledge-mining-book/clusterprofiler-kegg.html
LFC_cut = subset(gdata,Score>=1 | Score<=-1)
geneList_LFC= LFC_cut$Score
names(geneList_LFC) = LFC_cut[,1]
gene_names = bitr(LFC_cut[,1], "SYMBOL", "ENTREZID", OrgDb = org.Hs.eg.db,drop=F)
names(geneList_LFC) = gene_names$ENTREZID
# gene_names = bitr(LFC_cut[,1], "SYMBOL", "ENTREZID", OrgDb = org.Hs.eg.db,drop=T)
geneList_LFC = geneList_LFC[!is.na(names(geneList_LFC))]
kk <- enrichKEGG(gene = names(geneList_LFC),organism = organism, pvalueCutoff = 0.5)
write.table(kk, file=paste("MAGeCKFlute_",outFile,"/enrichKEGG.tsv",sep=""),  sep="\t", quote=FALSE, row.names=TRUE)
for (id in head(kk,n=20)$ID){
pathview(gene.data  = geneList_LFC,
                     pathway.id = id,
                     species    = organism,
                     limit      = list(gene=max(abs(geneList_LFC)), cpd=1),
                     kegg.dir = paste("MAGeCKFlute_",outFile,"/",sep=""))


}


kk <- enrichPathway(gene = gene_names$ENTREZID,pvalueCutoff = 0.5,readable=T)
write.table(kk, file=paste("MAGeCKFlute_",outFile,"/enrichReactome.tsv",sep=""),  sep="\t", quote=FALSE, row.names=TRUE)

for(n in 1:min(nrow(kk),20)) {
# pdf(paste("MAGeCKFlute_",outFile,"/",kk[n,1],".pdf",sep=""))
# png(paste("MAGeCKFlute_",outFile,"/",kk[n,1],".png",sep=""))
viewPathway(kk[n,2], 
            readable = TRUE, 
            foldChange = geneList_LFC)
ggsave(paste("MAGeCKFlute_",outFile,"/",kk[n,1],".png",sep=""))
}


