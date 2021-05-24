input=$1
output=$2


awk -F "\t" '{print $1"\t"$4"\t.\t"$2"\t"$3"\t.\t.\t.\t"$4}' $input > $output
