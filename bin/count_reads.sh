file=$1
echo $(zcat $file|wc -l) $file
