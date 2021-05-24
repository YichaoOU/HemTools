
# bash run.sh scATAC_3T3.markdup.bam scATAC_3T3
file=$1
label=$2
samtools view -u  -f 4 -F 264 $file  > tmps1.bam
samtools view -u -f 8 -F 260 $file  > tmps2.bam
samtools view -u -f 12 -F 256 $file > tmps3.bam
samtools merge -u - tmps[123].bam | samtools sort -o unmapped.bam -n - 
bamToFastq -i unmapped.bam -fq $label.unmapped.R1.fastq -fq2 $label.unmapped.R2.fastq
bamToFastq -i unmapped.bam -fq $label.unmapped.single.fastq

