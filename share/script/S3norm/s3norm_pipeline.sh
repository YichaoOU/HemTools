### get parameters
file_list=$1
reference_method=$2
reference_name=$3
script_folder=$4

#e.g.
#time bash ../src/S3norm_pipeline.sh file_list.txt median average_ref.bedgraph /Users/universe/Documents/2018_BG/S3norm/src/
#file_list='file_list.txt'
#reference_method='median'
#reference_name='average_ref.bedgraph'
#script_folder='/Users/universe/Documents/2018_BG/S3norm/src/'

###########################
### step1: get average signal track 
echo 'get average reference......'
time bash $script_folder/average_ref.awk.sh $file_list $reference_method $reference_name
echo 'get average reference......Done'

###########################
### step2: S3norm
echo 'S3norm......'
for file in $(cat $file_list | awk -F '\t' '{print $1}')
do
	echo $file
	time python $script_folder/s3norm.py -r $reference_name -t $file -o $file
done
echo 'S3norm......Done'

###########################
### step 3: negative log10 NB p-value
echo 'get NB p-value signal track......'
while read -r IP CTRL
do
	echo $IP ' vs ' $CTRL
	Rscript $script_folder/negative_binomial_neglog10p.R $IP'.s3norm.bedgraph' $CTRL $IP'.s3norm.NB.neglog10p.bedgraph'
done < $file_list
echo 'get NB p-value signal track......Done'

###########################
### step4: get average signal track NB p-value
echo 'get average reference......'
time bash $script_folder/average_ref.awk.sh $file_list $reference_method $reference_name'.NBP.bedgraph' '.s3norm.NB.neglog10p.bedgraph'
echo 'get average reference......Done'

###########################
### step5: S3norm NB p-value
echo 'S3norm......'
for file in $(cat $file_list | awk -F '\t' '{print $1}')
do
	echo $file
	time python $script_folder/s3norm.py -r $reference_name'.NBP.bedgraph' -t $file'.s3norm.NB.neglog10p.bedgraph' -o $file'.NBP' -p neglog10p
done
echo 'S3norm......Done'

######### organize folder
### save S3norm normalized NB model negative log10 p-value bedgraph
if [ -d NBP_S3norm_bedgraph ]; then rm -r NBP_S3norm_bedgraph; mkdir NBP_S3norm_bedgraph; else mkdir NBP_S3norm_bedgraph; fi
mv *.NBP.info.txt NBP_S3norm_bedgraph/
mv *.NBP.s3norm.bedgraph NBP_S3norm_bedgraph/
### save S3norm read counts bedgraph
if [ -d S3norm_rc_bedgraph ]; then rm -r S3norm_rc_bedgraph; mkdir S3norm_rc_bedgraph; else mkdir S3norm_rc_bedgraph; fi
mv *.info.txt S3norm_rc_bedgraph/
mv *.s3norm.bedgraph S3norm_rc_bedgraph/
### save NB model negative log10 p-value bedgraph
if [ -d NBP_bedgraph ]; then rm -r NBP_bedgraph; mkdir NBP_bedgraph; else mkdir NBP_bedgraph; fi
mv *.s3norm.NB.neglog10p.bedgraph NBP_bedgraph/



