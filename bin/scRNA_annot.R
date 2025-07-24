#!/home/yli11/.conda/envs/jupyterlab_2024/bin/Rscript
# run in seurat v5, but read in seruat v4 obj, for bonemarrowMap
library(Seurat)
library(tidyverse)
library(symphony)
library(ggpubr)
library(patchwork)
library(BoneMarrowMap)
library(Seurat)
library(SeuratData)
library(SeuratWrappers)
library(Azimuth)
library(ggplot2)
library(patchwork)
options(future.globals.maxSize = 1e9)
library(dplyr)
library(glue)
library(ggplot2)
library(patchwork)
library(cowplot)
library(stringr)
library(tidyr)
library(reshape2)
library(ggrepel)
library(scales)
library(cluster)
library(MASS)
library(plotly)
library(grid)
library(tibble)
library(RColorBrewer)
library(enrichplot)
library(devtools)
library(Signac)
library(tidyverse)
library(reshape)
library(dittoSeq)
library(ggforce)
library(yaml)
library(org.Mm.eg.db)
library(org.Hs.eg.db)
library(clusterProfiler)
library(scCustomize)

args <- commandArgs(trailingOnly=TRUE)

main_obj = readRDS(args[1])
label = args[2]

# cell type annotation
# load BoneMarrowMap obj
# Load Symphony reference
path="/home/yli11/HemTools/share/misc/scRNA/"
ref <- readRDS(paste0(path, 'BoneMarrow_RefMap_SymphonyRef.rds'))
# Set uwot path for UMAP projection
ref$save_uwot_path <- paste0(path, 'BoneMarrow_RefMap_uwot_model.uwot')

# batch variable to correct in the query data, set as NULL if no batches in query
batchvar <- 'orig.ident'
# Map query dataset using Symphony (Kang et al 2021)
query <- map_Query(
    exp_query = main_obj@assays$RNA@counts, 
    metadata_query = main_obj@meta.data,
    ref_obj = ref,
    vars = batchvar
)
# very slow
query <- predict_CellTypes(
  query_obj = query, 
  ref_obj = ref, 
  mapQC_col=NULL,
  initial_label = 'initial_CellType', # celltype assignments before filtering on mapping QC
  final_label = 'predicted_CellType'  # celltype assignments with map QC failing cells assigned as NA
) 

DimPlot(query, reduction = 'umap', group.by = c('predicted_CellType'), raster=T)
# DimPlot(query, reduction = 'umap', group.by = c('predicted_CellType'), raster=T, label=TRUE, label.size = 4,repel=T)
ggsave(paste0(label,".BM.UMAP.pdf"), height = 6, width = 10)
# Predict Pseudotime values by KNN
query <- predict_Pseudotime(
  query_obj = query, 
  ref_obj = ref, 
  mapQC_class =NULL,
  initial_label = 'initial_Pseudotime',  # pseudotime assignments before filtering on mapping QC
  final_label = 'predicted_Pseudotime'   # pseudotime assignments with map QC failing cells assigned as NA
)
# Visualize Hematopoietic Pseudotime in query data
FeaturePlot(query, features = c('predicted_Pseudotime'))
ggsave(paste0(label,".BM.Pseudotime.pdf"), height = 6, width = 10)

main_obj = AddMetaData(main_obj,query[[]])

DimPlot(
  query,
  reduction = "umap",
  split.by = c("orig.ident"),
  combine = T, label.size = 5,label=T,ncol=4,repel=T
)
ggsave(paste0(label,".BM.UMAP.split.pdf"), height = 16, width = 20)
# query
# saveRDS(query,paste0(label,".query.rds"))
umap_coords <- Embeddings(query, reduction = "umap")
DefaultAssay(object = main_obj) <- "RNA"
# generate our own UMAP
# main_obj <- Convert_Assay(seurat_object = main_obj, convert_to = "V5")
main_obj[["RNA"]] <- split(main_obj[["RNA"]], f = main_obj$orig.ident)
main_obj <- NormalizeData(main_obj)
main_obj <- FindVariableFeatures(main_obj)
main_obj <- ScaleData(main_obj)
VariableFeaturePlot_scCustom(main_obj,20)
ggsave(paste0(label,".VariableFeaturePlot.pdf"), height = 4, width = 4)

main_obj <- RunPCA(main_obj,features=head(VariableFeatures(main_obj),1000),reduction.name="pca.1000",npcs=50,reduction.key="PC.1000_")
main_obj <- RunPCA(main_obj,features=head(VariableFeatures(main_obj),2000),reduction.name="pca.2000",npcs=50,reduction.key="PC.2000_")
main_obj[['umap']] <- CreateDimReducObject(embeddings = umap_coords, key = "UMAP_")

saveRDS(main_obj,paste0(label,".main_obj.rds"))
quit(save = "no")

# RPCA Integration
try({
  main_obj <- IntegrateLayers(
    object = main_obj, method = RPCAIntegration,
    orig.reduction = "pca.1000", new.reduction = "pca.1000.rpca.20",
    dims = 1:20, k.weight = 50,
    verbose = FALSE
  )
})

try({
  main_obj <- IntegrateLayers(
    object = main_obj, method = RPCAIntegration,
    orig.reduction = "pca.1000", new.reduction = "pca.1000.rpca.50",
    dims = 1:50, k.weight = 50,
    verbose = FALSE
  )
})

# Harmony Integration
try({
  main_obj <- IntegrateLayers(
    object = main_obj, method = HarmonyIntegration,
    orig.reduction = "pca.1000", new.reduction = "pca.1000.harmony.20",
    dims = 1:20,
    verbose = FALSE
  )
})

try({
  main_obj <- IntegrateLayers(
    object = main_obj, method = HarmonyIntegration,
    orig.reduction = "pca.1000", new.reduction = "pca.1000.harmony.50",
    dims = 1:50,
    verbose = FALSE
  )
})

# FastMNN Integration
try({
  main_obj <- IntegrateLayers(
    object = main_obj, method = FastMNNIntegration,
    orig.reduction = "pca.1000",
    new.reduction = "pca.1000.FMNN",
    verbose = FALSE
  )
})


# RPCA Integration with pca.2000
try({
  main_obj <- IntegrateLayers(
    object = main_obj, method = RPCAIntegration,
    orig.reduction = "pca.2000", new.reduction = "pca.2000.rpca.20",
    dims = 1:20, k.weight = 50,
    verbose = FALSE
  )
})

try({
  main_obj <- IntegrateLayers(
    object = main_obj, method = RPCAIntegration,
    orig.reduction = "pca.2000", new.reduction = "pca.2000.rpca.50",
    dims = 1:50, k.weight = 50,
    verbose = FALSE
  )
})

# Harmony Integration with pca.2000
try({
  main_obj <- IntegrateLayers(
    object = main_obj, method = HarmonyIntegration,
    orig.reduction = "pca.2000", new.reduction = "pca.2000.harmony.20",
    dims = 1:20,
    verbose = FALSE
  )
})

try({
  main_obj <- IntegrateLayers(
    object = main_obj, method = HarmonyIntegration,
    orig.reduction = "pca.2000", new.reduction = "pca.2000.harmony.50",
    dims = 1:50,
    verbose = FALSE
  )
})

# FastMNN Integration with pca.2000
try({
  main_obj <- IntegrateLayers(
    object = main_obj, method = FastMNNIntegration,
    orig.reduction = "pca.2000",
    new.reduction = "pca.2000.FMNN",
    verbose = FALSE
  )
})

saveRDS(main_obj,paste0(label,".main_obj.rds"))

library(patchwork)
# Define the function
run_UMAP_plot <- function(main_obj, reduction_name, dims, resolution = 0.5) {
  result <- try({
    # Find Neighbors
    main_obj <- FindNeighbors(main_obj, reduction = reduction_name, dims = dims)
    
    # Find Clusters
    cluster_name <- paste0(reduction_name, ".clusters")
    main_obj <- FindClusters(main_obj, resolution = resolution, cluster.name = cluster_name)
    
    # Run UMAP
    umap_name <- paste0("umap.", reduction_name)
    reduction_key <- paste0("umap_", gsub("\\.", "_", reduction_name), "_")
    main_obj <- RunUMAP(main_obj, reduction = reduction_name, dims = dims, 
                        reduction.name = umap_name, reduction.key = reduction_key)
    
    # Create Plots
    p1_list <- DimPlot(
      main_obj,
      reduction = umap_name,
      group.by = "orig.ident",
      combine = FALSE, label.size = 2,repel=T
    )
    p1 <- p1_list[[1]]
    
    p2_list <- DimPlot(
      main_obj,
      reduction = umap_name,
      group.by = "predicted_CellType",
      combine = FALSE, label.size = 2,repel=T
    )
    p2 <- p2_list[[1]]

    p3_list <- FeaturePlot(
      main_obj,
      reduction = umap_name,
      features = "predicted_Pseudotime",
      combine = FALSE
    )
    p3 <- p3_list[[1]]

    # Combine plots
    combined_plot <- wrap_plots(p1, p2,p3, ncol = 3)
    
    return(list(main_obj = main_obj, plot = combined_plot))
    
  }, silent = TRUE)
  
  # Return empty plots and the original main_obj if an error occurred
  if (inherits(result, "try-error")) {
    empty_plot <- ggplot() + theme_void() + ggtitle(paste0("Error: ", reduction_name))
    return(list(main_obj = main_obj, plot = wrap_plots(empty_plot, empty_plot,empty_plot, ncol = 3)))
  } else {
    return(result)
  }
}

# Example usage for all new reductions
new_reductions <- c("pca.1000.rpca.20", "pca.1000.rpca.50", "pca.1000.harmony.20", 
                    "pca.1000.harmony.50", "pca.1000.FMNN",
                    "pca.2000.rpca.20", "pca.2000.rpca.50", "pca.2000.harmony.20", 
                    "pca.2000.harmony.50", "pca.2000.FMNN")

# List to store plots
all_plots <- list()

# Run the function for each new reduction and store the plots
for (reduction in new_reductions) {
  dims <- if (grepl("20$", reduction)) 1:20 else 1:50
  result <- run_UMAP_plot(main_obj, reduction, dims)
  main_obj <- result$main_obj
  all_plots[[reduction]] <- result$plot
}

# Combine all plots into a single plot
final_plot <- wrap_plots(all_plots, ncol = 2)

# Display the combined plot
print(final_plot)

ggsave(paste0(label,".UMAP.merged.pdf"), height = 30, width = 30,limitsize =F)

