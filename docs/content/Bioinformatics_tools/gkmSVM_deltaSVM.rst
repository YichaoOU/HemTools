Find allele (e.g., SNPs) specific effects
==========================================








.. code:: bash

	hpcf_interactive

	module load conda3

	source activate /home/yli11/.conda/envs/gkmSVM

	Rscript run_gkmSVM.R ctcfpos.bed hg18 nr10mers.fa ref.fa alt.fa



run_gkmSVM.R H2_ATAC.bed hg19 ~/HemTools/share/misc/nr10mers.fa ../ref.fa ../alt.fa



::

	=cut delta 1

	inputFile=input

	ncore=1
	mem=16000

	module load conda3
	source activate gkmSVM

	dir=${COL1}
	cd $dir
	file=`ls *Peak`
	input=${file%.narrowPeak}.input.bed
	sort -k 8gr $file | head -n 20000 | awk -F "\t" '{print $1"\t"$2"\t"$3}' > $input
	run_gkmSVM.R $input hg19 ~/HemTools/share/misc/nr10mers.fa ../ref.fa ../alt.fa

	=cut email 2 all

	module load python/2.7.13

	send_email_v1.py -m "deltaSVM is finished!" -j "deltaSVM"






