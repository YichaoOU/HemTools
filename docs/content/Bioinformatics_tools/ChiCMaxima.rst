Calling significant interactions from Capture-C or Capture-HiC
=========================



Notes
^^^^^

ChiCMaxima_Caller has to roll back to v0.9, because the latest one does not have the enrichment score.

::

	w=$1
	s=$2
	c=$3

	# -w/--window_size [LOCAL MAXIMUM CALLING WINDOW] -s/--loess_span [LOESS SPAN] -c/--cis_window [GENOMIC SEPARATION THRESHOLD]
	# c('output','o', 1, 'character',"output.ibed"),
	# c('window_size', 'w', 1, 'integer', 20),
	# c('loess_span','s',1,'numeric',0.05),
	# c('input','i',1,'character',"chr1_mESCs.ibed"),
	# c('cis_window','c',1,'integer',1500000),

	bdg_to_ibed.py merged.non_target.bdg target.merge.bed
	ChiCMaxima_Caller.r -i input.ibed -o 20copy -w $w -s $s -c $c
	sed -i '1d' 20copy_interactions.ibed
	awk -F"\t" '$12 >= 1 { print $2"\t"$3"\t"$4"\t"$7"\t"$8"\t"$9"\t"$12 }' 20copy_interactions.ibed > 20copy_interactions.mango
	cut -f 4,5,6,7 20copy_interactions.mango > 20copy_interactions.oe.bed 
	bedtools intersect -a 20copy_interactions.oe.bed -b CTCF.3kb.bed -u | cut -f 4 > A.list
	bedtools intersect -a 20copy_interactions.oe.bed -b CTCF.3kb.bed -v | cut -f 4 > B.list
	boxplot_two_list.py -l1 A.list -l2 B.list

	# create_tracks.py --current_dir





