gtf=$1
(grep ^"#" $gtf; grep -v ^"#" $gtf | sort -k1,1 -k4,4n) | bgzip  > $gtf.st.gtf.gz
tabix -p gff $gtf.st.gtf.gz

