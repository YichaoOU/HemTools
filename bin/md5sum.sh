md5sum */*fastq.gz | awk '{print $2 "\t" $1}'

