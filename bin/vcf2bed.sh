vcf=$1
awk -F "\t" '{print $1"\t"$2-1"\t"$2"\t"$3"\t"$4"\t"$5}' $vcf.vcf > $vcf.bed 
awk -F "\t" '{print $1"\t"$2-100"\t"$2+100"\t"$3"\t"$4"\t"$5}' $vcf.vcf > $vcf.ext100.bed 
awk -F "\t" '{print $1"\t"$2-200"\t"$2+200"\t"$3"\t"$4"\t"$5}' $vcf.vcf > $vcf.ext200.bed 