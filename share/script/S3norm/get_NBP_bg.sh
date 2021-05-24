### get parameters
input_bedgraph=$1
output_bedgraph=$2
method=$3


if [ "$method" == "1" ]
	then
		echo 'get all 1 bg bedgraph'
		cut -f1,2,3 $input_bedgraph | gawk -F '\t' -v OFS='\t' '{print $1,$2,$3,"1"}' > $output_bedgraph
fi
if [ "$method" == "atac" ]
	then
		echo 'get all atac bg (no 1kb) bedgraph'
		### get bigwig
		time ~/group/software/ucsc/bedGraphToBigWig $input_bedgraph ~/group/projects/vision/input_norm/mm10.chrom.sizes $input_bedgraph'.bw'
		### get 5kb 10kb signal track
		time ~/group/software/ucsc/bigWigAverageOverBed $input_bedgraph'.bw' ~/group/projects/vision/merged_input/200_noblack.11_22_2017.5kb.bed $input_bedgraph'.5kb.tab'
		time ~/group/software/ucsc/bigWigAverageOverBed $input_bedgraph'.bw' ~/group/projects/vision/merged_input/200_noblack.11_22_2017.10kb.bed $input_bedgraph'.10kb.tab'
		time ~/group/software/ucsc/bigWigAverageOverBed $input_bedgraph'.bw' ~/group/genome/mm10/mm10.1to19_X.genome.bed $input_bedgraph'.wg.bw'
		cut -f1,6 $input_bedgraph'.5kb.tab' | awk -F '\t' -v OFS='\t' '{print $1,$2,$3}' | sort -k1,1 -k2,2n > $input_bedgraph'.5kb.bedgraph'
		cut -f1,6 $input_bedgraph'.10kb.tab' | awk -F '\t' -v OFS='\t' '{print $1,$2,$3}' | sort -k1,1 -k2,2n > $input_bedgraph'.10kb.bedgraph'
		### get BG signal track
		paste $input_bedgraph'.5kb.bedgraph' $input_bedgraph'.10kb.bedgraph' | awk -F '\t' -v OFS='\t' '{print $1,$2,$3,$4,$8}' > $input_bedgraph'.1X_5_10kb.txt'
		time Rscript get_local_bg_rc.R $input_bedgraph $input_bedgraph'.1X_5_10kb.txt' $output_bedgraph
fi
if [ "$method" == "chipseq" ]
	then
		echo 'get all atac bg bedgraph'
		### get bigwig
		time ~/group/software/ucsc/bedGraphToBigWig $input_bedgraph ~/group/projects/vision/input_norm/mm10.chrom.sizes $input_bedgraph'.bw'
		### get 5kb 10kb signal track
		time ~/group/software/ucsc/bigWigAverageOverBed $input_bedgraph'.bw' ~/group/projects/vision/merged_input/200_noblack.11_22_2017.1kb.bed $input_bedgraph'.1kb.tab'
		time ~/group/software/ucsc/bigWigAverageOverBed $input_bedgraph'.bw' ~/group/projects/vision/merged_input/200_noblack.11_22_2017.5kb.bed $input_bedgraph'.5kb.tab'
		time ~/group/software/ucsc/bigWigAverageOverBed $input_bedgraph'.bw' ~/group/projects/vision/merged_input/200_noblack.11_22_2017.10kb.bed $input_bedgraph'.10kb.tab'
		time ~/group/software/ucsc/bigWigAverageOverBed $input_bedgraph'.bw' ~/group/genome/mm10/mm10.1to19_X.genome.bed $input_bedgraph'.wg.bw'
		cut -f1,6 $input_bedgraph'.1kb.tab' | awk -F '\t' -v OFS='\t' '{print $1,$2,$3}' | sort -k1,1 -k2,2n > $input_bedgraph'.1kb.bedgraph'
		cut -f1,6 $input_bedgraph'.5kb.tab' | awk -F '\t' -v OFS='\t' '{print $1,$2,$3}' | sort -k1,1 -k2,2n > $input_bedgraph'.5kb.bedgraph'
		cut -f1,6 $input_bedgraph'.10kb.tab' | awk -F '\t' -v OFS='\t' '{print $1,$2,$3}' | sort -k1,1 -k2,2n > $input_bedgraph'.10kb.bedgraph'
		### get BG signal track
		paste $input_bedgraph'.5kb.bedgraph' $input_bedgraph'.10kb.bedgraph' $input_bedgraph'.1kb.bedgraph' | awk -F '\t' -v OFS='\t' '{print $1,$2,$3,$4,$8,$12}' > $input_bedgraph'.1X_5_10kb.txt'
		time Rscript get_local_bg_rc.R $input_bedgraph $input_bedgraph'.1X_5_10kb.txt' $output_bedgraph
fi






