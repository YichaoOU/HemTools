diffpeak given bedgraph
=================


Summary
^^^^^^

Using the normalized read count bedgraph from S3Norm.

The result is float, you have to convert it to int, suggested by the people who developed S3Norm.

Input
^^^^^

You need diffpeak input.list and design matrix.

You need to run ``plot_bw_corr.py --bed merge_gata.bed -j gata_site`` first.

Then use ``scores_per_bed.tsv`` for edgeR.

::

	import pandas as pd

	file = pd.read_csv("input.tsv",sep="\t",header=None)
	file
	design = pd.read_csv("GATAmotif_mutation_diffPeak_matrix.tsv",sep="\t",header=None)
	design
	for t,c,n in design.values:
		print (t,c,n)
		
	import glob
	glob.glob("*.tsv")

	df = pd.read_csv("scores_per_bed.tsv",sep="\t")
	df.columns = [x.replace("'","") for x in df.columns]
	df.head()
	df.index = df['#chr']+"_"+df.start.astype(str)+"_"+df.end.astype(str)
	# df = df[df['#chr']=="chr11"]
	# df=df[df.start >5219844]
	# df=df[df.end <5330588]
	import os
	# chr11:5219844-5330588
	# chr11_5276180_5276219
	for t,c,n in design.values:
		print (t,c,n)
		# if not "113" in t:
			# continue
		t_group = file[file[3]==c][2].tolist()
		c_group = file[file[3]==t][2].tolist()
		input = "%s.input.tsv"%(n)
		tmp = df[t_group+c_group]
		for c in tmp.columns:
			tmp[c] = tmp[c].astype(int)
		tmp.to_csv(input,sep="\t")
		command = "module load R/3.5.1;run_EdgeR.R %s %s %s %s"%(input,",".join(t_group),",".join(c_group),n)
		os.system(command)
		print (command)
