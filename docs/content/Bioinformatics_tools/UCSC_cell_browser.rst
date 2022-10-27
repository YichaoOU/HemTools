Local UCSC cell browser usage for Seurat
========================



Notes
^^^^^

An important step is to give the markers to misc attribute. ``merged_obj@misc$markers <- markers`` so that the program can automatically know the cluster markers.

::

	Idents(object = merged_obj) <- merged_obj@meta.data$'manual_label'
	markers <- FindAllMarkers(merged_obj, min.pct = 0.2, logfc.threshold = 0.2)
	merged_obj@misc$markers <- markers
	saveRDS(merged_obj, "merged_obj.rds")


Usage
^^^^^

::

	module load conda3/202011

	source activate /home/yli11/.conda/envs/captureC

	cbImportSeurat -i merged_obj.rds -o merged_obj_CB # it will take a while

	# I usually modify the configuration file to use the log normalized counts, instead of raw counts
	# nano cellbrowser.conf
	# exprMatrix="data_exprMatrix.tsv.gz"

	cd merged_obj_CB

	bsub -q standard -P Genomics -R 'rusage[mem=20000]' -J CB cbBuild -o ./CB_cells/ -p 8051









