
input=$1
NPEAKS=$2
sort -k 8gr,8gr $input | awk 'BEGIN{OFS="\t"}{$4="Peak_"NR ; print $0}' | head -n ${NPEAKS}

