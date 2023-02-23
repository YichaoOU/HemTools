Seurat to Loupe browser
-----------------------

There is no simple way for this conversion.

Step 1. Merge individual samples
^^^^^^^^^^^^^^^^^^^

Create ``aggr.csv``:

::

	sample_id,molecule_h5
	Thymus_12d,Thymus-12d/outs/molecule_info.h5
	Thymus_2d,Thymus-2d/outs/molecule_info.h5
	Thymus_Oil,Thymus-Oil/outs/molecule_info.h5
	Thymus_12h,Thymus-12h/outs/molecule_info.h5
	Thymus_5d,Thymus-5d/outs/molecule_info.h5


and then run ``cellranger aggr --id out_merge --csv aggr.csv``

The cloupe file is in ``out_merge/outs/count/cloupe.cloupe``

Step 2. Create umap and metadata table for your Seurat obj.
^^^^^^^^^^^^^^^^^^^


::

	library("funcutils")

	seurat2cloupe(merged_obj,reduction="umap",dims=c("UMAP_1","UMAP_2"),metadata=colnames(merged_obj[[]]),keyword="MJ_annot",opdir="./")

Step 3. Use python to rename cell barcode.
^^^^^^^^^^^^^^^^^^

::

	import pandas as pd
	import re
	df = pd.read_csv("data4cloupe_MJ_annot.csv")
	order_list = ["Thymus-12d","Thymus-2d","Thymus-Oil","Thymus-12h","Thymus-5d"]
	myDict = {}
	for i in range(5):
	    myDict[order_list[i]]=i+1
	def rename_barcode(x):
	    for i in myDict:
	        if i in x:
	            tmp = re.split("-|_",x)
	            barcode = tmp[-2]
	            if len(barcode)!=16:
	                print ("Error")
	                print (x)
	            return f"{barcode}-{myDict[i]}"
	df['Barcode'] = df.Barcode.apply(rename_barcode)
	df.to_csv("UMAP_1_10_23.csv",index=False)
	df = pd.read_csv("cluster4cloupe_MJ_annot.csv")
	df['Barcode'] = df.Barcode.apply(rename_barcode)
	df.to_csv("metadata_1_10_23.csv",index=False)

Step 4. Open loupe file and import these csv files and then save.
^^^^^^^^^^^^^^

