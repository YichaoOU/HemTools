gtf=$1
sort -k1,1 -k2,2n $gtf | bgzip  > $gtf.st.bed.gz
tabix -p bed $gtf.st.bed.gz

