### get parameters
file_list=$1
method=$2
outputname=$3
script_folder=$4
end=$5

echo 'read first file name'
file1=$(head -1 $file_list | awk -F '\t' '{print $1}')

echo 'get bed file'
cut -f1,2,3 $file1$end > $outputname

echo 'get first file signals'
echo $file1
cut -f4 $file1 > sigmat.txt
echo 'get all file signals'
for file in $(tail -n+2 $file_list | awk -F '\t' '{print $1}')
do
	echo $file
	cut -f4 $file$end > sigmat.txt.tmp
	paste sigmat.txt sigmat.txt.tmp > sigmat.txt.tmp.tmp && mv sigmat.txt.tmp.tmp sigmat.txt
	rm sigmat.txt.tmp
done

echo 'get average_ref'
if [ "$method" == "median" ]
	then
		echo 'get reference median'
		cat sigmat.txt | gawk -F '\t' -v OFS='\t' '{sum=0; n=split($0,a); for(i=1;i<=n;i++) sum+=a[i]; asort(a); median=n%2?(a[(n+1)/2])/1:(a[n/2]+a[n/2+1])/2; print median}' > sigmat.average_ref.txt 
fi
if [ "$method" == "mean" ]
	then
	echo 'get reference mean'
	cat sigmat.txt | awk -F '\t' -v OFS='\t' '{sum=0; for(i=1; i<=NF; i++){sum+=$i}; sum/=NF; print sum}' > sigmat.average_ref.txt 
fi
if [ "$method" == "max1" ]
	then
	echo 'get reference ' $method
	Rscript $script_folder'get_max_median1.R' $method $file_list sigmat.average_ref.txt $end
fi
if [ "$method" == "median1" ]
	then
	echo 'get reference ' $method
	Rscript $script_folder'get_max_median1.R' $method $file_list sigmat.average_ref.txt $end
fi

if [ "$method" != "median" ] && [ "$method" == "mean" ] && [ "$method" == "max1" ] && [ "$method" == "median1" ]
	then
	echo 'get reference ' $method
	cut -f$method sigmat.txt > sigmat.average_ref.txt
fi

echo 'get output bedgraph file'
paste $outputname sigmat.average_ref.txt > $outputname'.tmp' && mv $outputname'.tmp' $outputname
rm sigmat.average_ref.txt
rm sigmat.txt

