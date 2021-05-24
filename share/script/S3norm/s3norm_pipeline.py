import os
import numpy as np
import subprocess
from subprocess import call
import pandas as pd
import uuid


def genereate_dummy_input(file_list):
	# also generate a temp input for this program
	cwd = os.getcwd()
	temp_input = cwd+"/"+str(uuid.uuid4()).split("-")[-1]
	df = pd.read_csv(file_list,sep="\t",header=None)
	df = df.dropna(how='all')
	shape1 = df.shape[0]
	df2 = df.dropna()
	shape2 = df2.shape[0]
	if df2.shape[1] <=1:
		shape2=0
	# print (shape1,shape2)
	# exit()
	if shape2 < shape1:
		print ("generating dummy input")
		control_file=cwd+"/"+"dummy_control.bdg"
		command = """awk -F "\t" '{print $1"\t"$2"\t"$3"\t1"}' %s > %s"""%(df.at[0,0],control_file)
		os.system(command)
		df = df.fillna("dummy_control.bdg")
		if shape2==0:
			df[1]="dummy_control.bdg"
		df.to_csv(temp_input,sep="\t",header=False,index=False)
		file_list = temp_input
	# exit()
	return file_list


def S3norm_pipeline(NTmethod, B_init, fdr_thresh, rank_lim, upperlim, lowerlim, p_method, common_pk_binary, common_bg_binary, script_folder, file_list, reference_method, cross_mark):
	reference_name = 'average_ref.bedgraph'
	
	### step 1
	print('Get average reference......')
	step1=call('bash '+script_folder+'/average_ref.awk.sh '+file_list+' '+reference_method+' '+reference_name+' '+script_folder, shell=True)
	print('Get average reference......Done')

	### step 2
	print('Get S3norm normalized read counts......')
	step2=call('for file in $(cat '+file_list+' | awk -F \'\\t\' \'{print $1}\'); do python '+script_folder+'/s3norm.py -r '+reference_name+' -t $file -o $file -m '+NTmethod+' -i '+B_init+' -f '+fdr_thresh+' -l '+rank_lim+' -a '+upperlim+' -b '+lowerlim+' -p '+p_method+' -k '+common_pk_binary+' -g '+common_bg_binary+'; done', shell=True)
	print('Get S3norm normalized read counts......Done')

	### step 3
	print('Get signal track of negative log10 p-value based on a NB background model......')
	step3=call('while read -r IP CTRL; do Rscript '+script_folder+'/negative_binomial_neglog10p.R $IP\'.s3norm.bedgraph\' $CTRL $IP\'.s3norm.NB.neglog10p.bedgraph\'; done < '+file_list, shell=True)
	print('Get signal track of negative log10 p-value based on a NB background model......Done')

	### step 4
	print('Get NBP average reference......')
	step4=call('bash '+script_folder+'/average_ref.awk.sh '+file_list+' '+reference_method+' '+reference_name+'.NBP.bedgraph'+' '+script_folder+' '+'.s3norm.NB.neglog10p.bedgraph', shell=True)
	print('Get NBP average reference......Done')

	### step 5
	print('Get S3norm normalized negative log10 p-value based on NB background model......')
	step5=call('for file in $(cat '+file_list+' | awk -F \'\t\' \'{print $1}\'); do python '+script_folder+'/s3norm.py -r '+reference_name+'.NBP.bedgraph -t $file\'.s3norm.NB.neglog10p.bedgraph\' -o $file\'.NBP\' -p neglog10p -m '+NTmethod+' -i '+B_init+' -f '+fdr_thresh+' -l '+rank_lim+' -a '+upperlim+' -b '+lowerlim+' -k '+common_pk_binary+' -g '+common_bg_binary+' -c '+cross_mark+'; done', shell=True)
	print('Get S3norm normalized negative log10 p-value based on NB background model......Done')

	### step 6
	print('Organize folder......')
	print('Save S3norm_NBP_bedgraph')
	call('if [ -d S3norm_NBP_bedgraph ]; then rm -r S3norm_NBP_bedgraph; mkdir S3norm_NBP_bedgraph; else mkdir S3norm_NBP_bedgraph; fi', shell=True)
	call('mv *.NBP.info.txt S3norm_NBP_bedgraph/', shell=True)
	call('mv *.NBP.s3norm.bedgraph S3norm_NBP_bedgraph/', shell=True)
	print('Save S3norm_rc_bedgraph')
	call('if [ -d S3norm_rc_bedgraph ]; then rm -r S3norm_rc_bedgraph; mkdir S3norm_rc_bedgraph; else mkdir S3norm_rc_bedgraph; fi', shell=True)
	call('mv *.info.txt S3norm_rc_bedgraph/', shell=True)
	call('mv *.s3norm.bedgraph S3norm_rc_bedgraph/', shell=True)
	print('Save NBP_bedgraph')
	call('if [ -d NBP_bedgraph ]; then rm -r NBP_bedgraph; mkdir NBP_bedgraph; else mkdir NBP_bedgraph; fi', shell=True)
	call('mv *.s3norm.NB.neglog10p.bedgraph NBP_bedgraph/', shell=True)
	print('Save average_ref_bedgraph')
	call('if [ -d average_ref_bedgraph ]; then rm -r average_ref_bedgraph; mkdir average_ref_bedgraph; else mkdir average_ref_bedgraph; fi', shell=True)
	call('mv average_ref.*bedgraph average_ref_bedgraph/', shell=True)
	print('Organize folder......Done')
	call('mv %s'%(file_list), shell=True)



############################################################################
### time python ../src/s3norm.py -r reference.bedgraph -t target.bedgraph -o target -m non0mean -i 2.0 -f 0.05 -l 0.001 -a 100 -b 0 -p z -k 0 -g 0
### time python ../src/s3norm.py -r reference.bedgraph -t target.bedgraph -o target

### time python ../src/s3norm.py -r reference.bedgraph -t target.bedgraph -o target -m non0mean -i 2.0 -f 0.05 -l 0.001 -a 100 -b 0 -p z -k 0 -g 0
### time python ../src/S3norm_pipeline.py -s /Users/universe/Documents/2018_BG/S3norm/src/ -t file_list.txt

import getopt
import sys
def main(argv):
	### read user provided parameters
	opts, args = getopt.getopt(argv,"hr:s:t:m:i:f:l:a:b:p:k:g:c:")
	for opt,arg in opts:
		if opt=="-h":
			print('time python ../src/S3norm_pipeline.py -s script_folder -t input_file_list -r reference_method -m (Method for matching peaks and background: non0mean, non0median, mean, median) -i initial_B -f FDR_thresh -l rank_lim_p -a upperlimit -b lowerlimit -p (p-value_method: neglog10p, z) -k common_pk_binary (0 for nocommon_pk; common_pk_binary.txt) -g common_bg_binary (0 for nocommon_pk; common_bg_binary.txt) -c cross_mark (F for NOT use cross mark mode; T for use cross mark mode)')
			return()	
		elif opt=="-m":
			NTmethod=str(arg.strip())
		elif opt=="-i":
			B_init=str(arg.strip())
		elif opt=="-f":
			fdr_thresh=str(arg.strip())
		elif opt=="-l":
			rank_lim=str(arg.strip())
		elif opt=="-a":
			upperlim=str(arg.strip())
		elif opt=="-b":
			lowerlim=str(arg.strip())
		elif opt=="-p":
			p_method=str(arg.strip())
		elif opt=="-k":
			common_pk_binary=str(arg.strip())
		elif opt=="-g":
			common_bg_binary=str(arg.strip())
		elif opt=="-s":
			script_folder=str(arg.strip())				
		elif opt=="-t":
			file_list=str(arg.strip())
		elif opt=="-r":
			reference_method=str(arg.strip())
		elif opt=="-c":
			cross_mark=str(arg.strip())

	############ Default parameters
	###### required parameters
	try:
		print('User provide script_folder: -s '+str(script_folder))
		print('User provide input_file_list: -t '+str(file_list))
	except NameError:
		print('Missing required parameter(s): time python ../src/S3norm_pipeline.py -s /Users/universe/Documents/2018_BG/S3norm/src/ -t file_list.txt')	
		return()	
	###
	###### optional parameters
	try:
		print('User provide reference_method: -r '+str(reference_method))
		if reference_method!='mean' and reference_method!='median' and reference_method!='max1' and reference_method!='median1':
			print('-r (mean, median, max1, median1)')
			return()
	except NameError:
		print('Default reference_method: -m max1')
		reference_method = 'max1'
	###
	try:
		print('User provide NTmethod: -m '+str(NTmethod))
		if NTmethod!='non0mean' and NTmethod!='non0median' and NTmethod!='mean' and NTmethod!='median':
			if float(NTmethod)+0!=float(NTmethod):
				print('-m (non0mean, non0median, mean, median, filelist_row_number)')
				return()
	except NameError:
		print('Default NTmethod: -m non0mean')
		NTmethod = 'non0mean'
	###
	try:
		print('User provide B_init: -i '+str(B_init))
	except NameError:
		print('Default B_init: -i 2.0')
		B_init = '2.0'
	###
	try:
		print('User provide fdr_thresh: -f '+str(fdr_thresh))
		if float(fdr_thresh)<0 or float(fdr_thresh)>1:
			print('-f (0.000001~1.0)')
			return()
	except NameError:
		print('Default fdr_thresh: -f 0.05')
		fdr_thresh = '0.05'
	###
	try:
		print('User provide rank_lim: -l '+str(rank_lim))
		if float(rank_lim)<0 or float(rank_lim)>1:
			print('-l (0.000001~1.0)')
			return()
	except NameError:
		print('Default rank_lim: -l 0.001')
		rank_lim = '0.001'
	###
	try:
		print('User provide upperlim: -a '+str(upperlim))
	except NameError:
		print('Default upperlim: -a 100000')
		upperlim = '100000'
	###
	try:
		print('User provide lowerlim: -b '+str(lowerlim))
	except NameError:
		print('Default lowerlim: -b 0')
		lowerlim = '0'
	###
	try:
		print('User provide p_method: -p '+str(p_method))
		if p_method!='z' and p_method!='neglog10p':
			print('-p (neglog10p, z)')
			return()
	except NameError:
		print('Default p_method: -p z')
		p_method = 'z'
	###
	try:
		print('User provide common_pk_binary: -k '+str(common_pk_binary))
	except NameError:
		print('Default common_pk_binary: -k 0')
		common_pk_binary = '0'
	###
	try:
		print('User provide common_bg_binary: -g '+str(common_bg_binary))
	except NameError:
		print('Default common_bg_binary: -g 0')
		common_bg_binary = '0'
	###
	try:
		print('User provide cross_mark: -c '+str(cross_mark))
	except NameError:
		print('Default cross_mark: -c F')
		cross_mark = 'F'
	###

	######### run s3norm
	print('start S3norm.......')
	S3norm_pipeline(NTmethod, B_init, fdr_thresh, rank_lim, upperlim, lowerlim, p_method, common_pk_binary, common_bg_binary, script_folder, genereate_dummy_input(file_list), reference_method, cross_mark)


if __name__=="__main__":
	main(sys.argv[1:])
