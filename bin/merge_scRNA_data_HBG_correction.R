#!/home/yli11/.conda/envs/captureC/bin/Rscript

# has to be seurat v4
library(Seurat)
library(ggplot2)
library(Signac)
library(EnsDb.Hsapiens.v86)
set.seed(1234)
annotation <- GetGRangesFromEnsDb(ensdb = EnsDb.Hsapiens.v86)
annotation <- renameSeqlevels(annotation, mapSeqlevels(seqlevels(annotation), "UCSC"))

args <- commandArgs(trailingOnly=TRUE)


read_10x = function(sample_tsv,cite_seq_flag){
    dataTable = read.table(sample_tsv,sep="\t",header=FALSE)
    myList=list()
    for(i in 1:dim(dataTable)[1]){
        s=dataTable[i,1]
        dir=dataTable[i,2]
        message(paste("reading sample",s))
        myData <- Seurat::Read10X(data.dir = dir,strip.suffix=T)
        if (cite_seq_flag){
            myList[[i]]  <- Seurat::CreateSeuratObject(counts = myData[["Gene Expression"]], min.cells = 0, min.features = 0,project = s, assay = "RNA")
            myList[[i]][["ADT"]] <- Seurat::CreateAssayObject(myData[["Antibody Capture"]][, colnames(x = myList[[i]] )])                    
            
        }else{
            tmp  <- Seurat::CreateSeuratObject(counts = myData, min.cells = 0, min.features = 0,project = s, assay = "RNA")
            new_cell_names <- paste(rownames(tmp[[]]), s, sep="_")
            RenameCells(object = tmp, new.names = new_cell_names)
            myList[[i]]  <- tmp
        }

    }
    return (myList)
}

# Rename the cells in the Seurat object



read_10x_multi_single = function(sample_name){
    metadata <- read.csv(
      file = paste0(sample_name,"/outs/per_barcode_metrics.csv"),
      header = TRUE,
      row.names = 1
    )
    counts = Read10X_h5(paste0(sample_name,"/outs/filtered_feature_bc_matrix.h5"))
    ATAC_fragments = paste0(sample_name,"/outs/atac_fragments.tsv.gz")

    
    obj <- CreateSeuratObject(
      counts = counts$`Gene Expression`,
      project = sample_name,
      assay = "RNA",
        meta.data=metadata
    )
    obj[["ATAC"]] <- CreateChromatinAssay(
      counts = counts$Peaks,
      sep = c(":", "-"),
      fragments = ATAC_fragments,
      annotation = annotation
    )
    new_cell_names <- paste(rownames(obj[[]]), sample_name, sep="_")
    RenameCells(object = obj, new.names = new_cell_names)
    return (obj)
}
read_10x_multi_list = function(myList){
    outList = list()
    for(i in 1:length(myList) ){
        print (myList[i])
        outList[[i]] = read_10x_multi_single(myList[i])
    }
    return (outList)
}


sample_tsv=args[1]
# label, dir
# if cite-seq or regular RNA_seq, the dir should end with filtered_feature_bc_matrix
# if multi-omics, the dir should end with the parent folder containing outs
cite_seq <- as.numeric(args[2])
scATAC_seq <- as.numeric(args[3])

if (scATAC_seq){
	sample_list = read.table(sample_tsv,sep="\t",header=FALSE)
	my_seurat_list = read_10x_multi_list(sample_list$V2)
}else{
	my_seurat_list = read_10x(sample_tsv,cite_seq)
}




merged_obj = merge(my_seurat_list[[1]], y = my_seurat_list[-1])
merged_obj[["percent.mt"]] <- PercentageFeatureSet(merged_obj, pattern = "^MT-",assay = 'RNA')
# options(repr.plot.width = 10, repr.plot.height = 6)
VlnPlot(merged_obj, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)
ggsave(paste0(sample_tsv,".raw_stats.png"), height = 6, width = 10)
# merged_obj <- subset(merged_obj, subset = nFeature_RNA >= 200 & nFeature_RNA <= 6000 & percent.mt <= 20 & nCount_RNA <=50000)
# ggsave(paste0(sample_tsv,".filtered_stats.png"), height = 6, width = 10)

# VlnPlot(merged_obj, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)


# merged_obj <- FindVariableFeatures(merged_obj)
# merged_obj <- ScaleData(merged_obj)
# merged_obj <- RunPCA(merged_obj)
# merged_obj <- FindNeighbors(merged_obj, dims = 1:30, reduction = "pca")
# merged_obj <- FindClusters(merged_obj, resolution = 2, cluster.name = "unintegrated_clusters")
# merged_obj <- RunUMAP(merged_obj, dims = 1:30, reduction = "pca", reduction.name = "umap.unintegrated")
# DimPlot(merged_obj, reduction = "umap.unintegrated", group.by = c("orig.ident"))
# ggsave(paste0(sample_tsv,".unintegrated.UMAP.png"), height = 5, width = 6)


# concat HBG1 HBG2 HBA1 HBA2 reads
my_seurat_list <- lapply(X = my_seurat_list, FUN = function(x) {
    counts <- GetAssayData(x, assay = "RNA")
    HBG = counts[(which(rownames(counts) %in% c('HBG2','HBG1'))),]
    HBA = counts[(which(rownames(counts) %in% c('HBA2','HBA1'))),]
    counts["HBG2",] = colSums(HBG)
    counts["HBA2",] = colSums(HBA)
    counts <- counts[-(which(rownames(counts) %in% c('HBG1',"HBA1"))),]
    x=subset(x, features = rownames(counts))
    x@assays$RNA@counts = counts
    return (x)
})  
merged_obj2 = merge(my_seurat_list[[1]], y = my_seurat_list[-1])
merged_obj2 <- NormalizeData(merged_obj2)
merged_obj <- AddMetaData(
  object = merged_obj,
  metadata = merged_obj2@assays$RNA@data["HBG2",],
  col.name = 'HBG_data'
)
merged_obj <- AddMetaData(
  object = merged_obj,
  metadata = merged_obj2@assays$RNA@data["HBA2",],
  col.name = 'HBA_data'
)
merged_obj <- AddMetaData(
  object = merged_obj,
  metadata = merged_obj2@assays$RNA@data["HBB",],
  col.name = 'HBB_data'
)

merged_obj <- AddMetaData(
  object = merged_obj,
  metadata = merged_obj2@assays$RNA@counts["HBG2",],
  col.name = 'HBG_counts'
)
merged_obj <- AddMetaData(
  object = merged_obj,
  metadata = merged_obj2@assays$RNA@counts["HBA2",],
  col.name = 'HBA_counts'
)
merged_obj <- AddMetaData(
  object = merged_obj,
  metadata = merged_obj2@assays$RNA@counts["HBB",],
  col.name = 'HBB_counts'
)
write.csv(merged_obj2@meta.data, file=paste0(sample_tsv,".merged_HBG_HBA.metadata.csv"), quote=F, row.names=T)

saveRDS(merged_obj,paste0(sample_tsv,".rds"))
