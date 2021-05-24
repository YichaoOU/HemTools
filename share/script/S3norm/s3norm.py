#module load python/2.7
import os
from subprocess import call
import numpy as np
from scipy.stats import norm, nbinom

################################################################################################
### read 2d array
def read2d_array(filename,dtype_used):
	import numpy as np
	data=open(filename,'r')
	data0=[]
	for records in data:
		tmp = [x.strip() for x in records.split('\t')]
		data0.append(tmp)
	data0 = np.array(data0,dtype=dtype_used)
	data.close()
	return(data0)

################################################################################################
### write 2d matrix
def write2d_array(array,output):
	r1=open(output,'w')
	for records in array:
		for i in range(0,len(records)-1):
			r1.write(str(records[i])+'\t')
		r1.write(str(records[len(records)-1])+'\n')
	r1.close()

################################################################################################
### p-value adjust (fdr & bonferroni)
def p_adjust(pvalue, method):
	p = pvalue
	n = len(p)
	p0 = np.copy(p, order='K')
	nna = np.isnan(p)
	p = p[~nna]
	lp = len(p)
	if method == "bonferroni":
		p0[~nna] = np.fmin(1, lp * p)
	elif method == "fdr":
		i = np.arange(lp, 0, -1)
		o = (np.argsort(p))[::-1]
		ro = np.argsort(o)
		p0[~nna] = np.fmin(1, np.minimum.accumulate((p[o]/i*lp)))[ro]
	else:
		print("Method is not implemented")
		p0 = None
	return(p0)

################################################################################################
### NewtonRaphsonMethod
def NewtonRaphsonMethod(sig1_pk, sig1_bg, sig2_pk, sig2_bg, upperlim, A,B, method, converge_thresh, numIterations):
	np.random.seed(2018)
	### get methods
	if method == 'mean':
		sig1_pk = sig1_pk + 0.1
		sig2_pk = sig2_pk + 0.1
		sig1_bg = sig1_bg + 0.1
		sig2_bg = sig2_bg + 0.1
		sig1_pk_mean = np.mean(sig1_pk)
		sig1_bg_mean = np.mean(sig1_bg)
		print(sig1_pk_mean)
		print(sig1_bg_mean)
	elif method == 'median':
		sig1_pk = sig1_pk + 0.1
		sig2_pk = sig2_pk + 0.1
		sig1_bg = sig1_bg + 0.1
		sig2_bg = sig2_bg + 0.1
		sig1_pk_mean = np.median(sig1_pk)
		sig1_bg_mean = np.median(sig1_bg)
	elif method == 'non0mean':
		sig1_pk = sig1_pk[sig1_pk>0]
		sig2_pk = sig2_pk[sig2_pk>0]
		sig1_pk_mean = np.mean(sig1_pk)
		sig1_bg = sig1_bg[sig1_bg>0]
		sig2_bg = sig2_bg[sig2_bg>0]
		sig1_bg_mean = np.mean(sig1_bg)
	elif method == 'non0median':
		sig1_pk = sig1_pk[sig1_pk>0]
		sig2_pk = sig2_pk[sig2_pk>0]
		sig1_pk_mean = np.median(sig1_pk)
		sig1_bg = sig1_bg[sig1_bg>0]
		sig2_bg = sig2_bg[sig2_bg>0]
		sig1_bg_mean = np.median(sig1_bg)
	else:
		method = 'non0mean'
		sig1_pk = sig1_pk[sig1_pk>0]
		sig2_pk = sig2_pk[sig2_pk>0]
		sig1_pk_mean = np.mean(sig1_pk)
		sig1_bg = sig1_bg[sig1_bg>0]
		sig2_bg = sig2_bg[sig2_bg>0]
		sig1_bg_mean = np.mean(sig1_bg)

	##################### loop start
	converge_min = 1000000000.0
	###
	if (sig1_bg.shape[0]==0 and sig2_bg.shape[0]==0):
		print('The background of one sample is all 0s, then use peak mean ratio')
		sig2_pk_mean = np.mean(sig2_pk)
		used_AB = [sig1_pk_mean/sig2_pk_mean, 1.0]
		return(np.array(used_AB))
	elif (sig1_bg.shape[0]==0 and sig2_bg.shape[0]!=0):
		sig1_bg_mean = 0.1


	for i in range(0, numIterations):
		### transform target pk & bg
		sig2_pk_transformed = sig2_pk**(B)
		sig2_bg_transformed = sig2_bg**(B)
		### set limit
		sig2_pk_transformed[sig2_pk_transformed>upperlim] = upperlim
		sig2_bg_transformed[sig2_bg_transformed>upperlim] = upperlim
		### Newton method
		if method == 'non0mean' or method == 'mean':
			fb = sig1_bg_mean * np.mean(sig2_pk_transformed) - sig1_pk_mean * np.mean(sig2_bg_transformed)
			dfb = 2 * sig1_bg_mean * np.mean(np.log(sig2_pk) * sig2_pk_transformed) - 2 * sig1_pk_mean * np.mean(np.log(sig2_bg) * sig2_bg_transformed)
		elif method == 'non0median' or method == 'median':
			fb = sig1_bg_mean * np.median(sig2_pk_transformed) - sig1_pk_mean * np.median(sig2_bg_transformed)
			dfb = 2 * sig1_bg_mean * np.median(np.log(sig2_pk) * sig2_pk_transformed) - 2 * sig1_pk_mean * np.median(np.log(sig2_bg) * sig2_bg_transformed)
		### next step
		B = B - fb / dfb
		### if B become negative restart
		if B <=0:
			print('B become negative. Restart...')
			B = 1.0 + np.random.normal(0,1,1)[0]
		### update sig2_bg_transformed
		sig2_bg_transformed = sig2_bg**(B)
		sig2_bg_transformed[sig2_bg_transformed>upperlim] = upperlim
		### get A
		if method == 'non0mean' or method == 'mean':
			A = sig1_bg_mean / np.mean(sig2_bg_transformed)
		elif method == 'non0median' or method == 'median':
			A = sig1_bg_mean / np.median(sig2_bg_transformed)
		### this round done
		if i%10==0:
			print("Iteration %d | dFB: %f" % (i, fb/dfb))
			print([A,B])
		### check if update best A & B
		if abs(fb / dfb) < converge_min:
			i_min = i
			converge_min = abs(fb / dfb)
			converge_min_AB = [A, B]
		### check converge
		if abs(fb / dfb) < converge_thresh:
			print('converged!')
			used_AB = [A, B]
			break
	##################### loop done
	### when not converge
	if abs(fb / dfb) >= converge_thresh:
		print('converging...')
		print("Iteration %d | dFB: %f" % (i_min, converge_min))	
		if converge_min > 0.01:
			B0=B
			if method == 'non0mean' or method == 'mean':
				B = ( np.mean(np.log(sig1_pk)) - np.mean(np.log(sig1_bg)) ) / ( np.mean(np.log(sig2_pk)) - np.mean(np.log(sig2_bg)) )
			if method == 'non0median' or method == 'median':
				B = ( np.median(np.log(sig1_pk)) - np.median(np.log(sig1_bg)) ) / ( np.median(np.log(sig2_pk)) - np.median(np.log(sig2_bg)) )
			if B<0:
				B=B0
			sig2_bg_transformed = sig2_bg**(B)
			sig2_bg_transformed[sig2_bg_transformed>upperlim] = upperlim
			if method == 'non0mean' or method == 'mean':
				A = sig1_bg_mean / np.mean(sig2_bg_transformed)
			if method == 'non0median' or method == 'median':
				A = sig1_bg_mean / np.median(sig2_bg_transformed)
			mean_log_AB = [A, B]
			used_AB = mean_log_AB
		else:
			used_AB = converge_min_AB
	print('used: [A, B]')
	print(used_AB)
	return(np.array(used_AB))


################################################################################################
### s3norm
def s3norm(sig1_wg_raw, sig2_wg_raw, sig2_output_name, NTmethod, B_init, fdr_thresh, rank_lim, upperlim, lowerlim, p_method, common_pk_binary, common_bg_binary, cross_mark):
	### read whole genome signals
	sig1_raw = read2d_array(sig1_wg_raw, str)
	sig2_raw = read2d_array(sig2_wg_raw, str)

	### check if the bedgraph files have the same coordinates
	bin_num = sig1_raw.shape[0]
	if np.sum(sig1_raw[:,1]==sig2_raw[:,1]) != bin_num:
		print('The bedgraph files are not sorted. Please use "sort -k1,1 -k2,2n target.bedgraph > target.sorted.bedgraph" to sort bedgraph files')
		return()

	### get signal
	sig1 = np.array(sig1_raw[:,3], dtype=float)
	sig2 = np.array(sig2_raw[:,3], dtype=float)

	### limit signal
	#sig1[sig1>upperlim] = upperlim
	#sig1[sig1<lowerlim] = lowerlim
	#sig2[sig2>upperlim] = upperlim
	#sig2[sig2<lowerlim] = lowerlim

	### get whole genome binary label for reference & target
	if p_method == 'z':
		### reference
		sig1_z_p_fdr = p_adjust(1 - norm.cdf((sig1 - np.mean(sig1))/ np.std(sig1)), 'fdr')
		sig1_binary = sig1_z_p_fdr < fdr_thresh
		### target
		sig2_z_p_fdr = p_adjust(1 - norm.cdf((sig2 - np.mean(sig2))/ np.std(sig2)), 'fdr')
		sig2_binary = sig2_z_p_fdr < fdr_thresh
	elif p_method == 'neglog10p':
		### reference
		sig1_p = 10.0**(-sig1)
		sig1_z_p_fdr = p_adjust(sig1_p, 'fdr')
		sig1_binary = (sig1_z_p_fdr < fdr_thresh)
		### target
		sig2_p = 10.0**(-sig2)
		sig2_z_p_fdr = p_adjust(sig2_p, 'fdr')
		sig2_binary = (sig2_z_p_fdr < fdr_thresh)


	print('check peak number in reference')
	sig1_pk_num = np.sum(sig1_binary)
	print('reference_pk_num')
	print(sig1_pk_num)

	print('check peak number in target')
	sig2_pk_num = np.sum(sig2_binary)
	print('target_pk_num')
	print(sig2_pk_num)

	### if pk number < 10000 then use rank for reference
	if sig1_pk_num <= int(bin_num * rank_lim):
		sig1_thresh = np.sort(sig1, axis=None)[-int(bin_num * rank_lim)]
		print('fdr peak number < bin_num * rank_lim')
		print('use rank for reference')
		sig1_binary = sig1 >= sig1_thresh
		print(sig1_thresh)

	### if pk number < 10000 then use rank for target
	if sig2_pk_num <= int(bin_num * rank_lim):
		sig2_thresh = np.sort(sig2, axis=None)[-int(bin_num * rank_lim)]
		print('fdr peak number < bin_num * rank_lim')
		print('use rank for target')
		sig2_binary = sig2 >= sig2_thresh
		print(sig2_thresh)

	print('reference_pk_num')
	print(sig1_pk_num)
	print('target_pk_num')
	print(sig2_pk_num)

	### get user provided common pk 
	if (common_pk_binary!='0'):
		print('check user provided common peaks')
		common_pk_binary_sig = read2d_array(common_pk_binary, float)
		if np.sum(common_pk_binary_sig == 1.0)>int(bin_num * rank_lim):
			print('use user provided common peaks')
			print(np.sum(common_pk_binary_sig == 1.0))
			peak_binary = (common_pk_binary_sig == 1.0)[:,0]
		else:
			print('user provided common peaks number < bin_num * rank_lim. Not use')
			peak_binary = (sig1_binary[:,0] & sig2_binary[:,0])
	else:
		print('use FDR common peaks')
		peak_binary = (sig1_binary & sig2_binary)

	### get user provided common bg
	if (common_bg_binary!='0'):
		print('check user provided common background')
		common_bg_binary_sig = read2d_array(common_bg_binary, float)
		bg_binary = (common_bg_binary_sig == 1.0)[:,0]
	else:
		print('use FDR common background')
		bg_binary = ~(sig1_binary | sig2_binary)

	print('common peaks number:')
	print(np.sum(peak_binary))
	print('common background number:')
	print(np.sum(bg_binary))

	### get common bg pk
	if cross_mark == 'T':
		sig1_cbg = sig1[~sig1_binary]
		sig2_cbg = sig2[~sig2_binary]
		sig1_cpk = sig1[sig1_binary]
		sig2_cpk = sig2[sig2_binary]
	else:
		sig1_cbg = sig1[bg_binary]
		sig2_cbg = sig2[bg_binary]
		sig1_cpk = sig1[peak_binary]
		sig2_cpk = sig2[peak_binary]

	### get transformation factor
	print('check!!!')
	print(np.sum(sig1==sig2))
	if sig1_wg_raw != sig2_wg_raw:
		AB = NewtonRaphsonMethod(sig1_cpk, sig1_cbg, sig2_cpk, sig2_cbg, upperlim, 0.5, 2.0, NTmethod, 1e-5, 200)
		A=AB[0]
		B=AB[1]
	else:
		A=1.0
		B=1.0		
	print('transformation: '+'B: '+str(B)+'; A: '+str(A))
	Ao=A
	Bo=B
	### transformation get round 0 normalized signal
	sig2_norm = []
	for s in sig2:
		s_norm = (A * (s)**B)
		if s_norm > upperlim:
			s_norm = upperlim
		elif s_norm < lowerlim:
			s_norm = lowerlim
		sig2_norm.append(s_norm)

	sig2_norm = np.array(sig2_norm)

	### total reads sf (for compare)
	sig1_totalmean = np.mean(sig1)
	sig2_totalmean = np.mean(sig2)
	total_mean_sf = sig1_totalmean / sig2_totalmean

	### convert to float np.array
	sig2_norm = np.array(sig2_norm, float)
	#sig2_norm[sig2[:,0]==0] = 0.0
	sig2_norm_totalmean = np.mean(sig2_norm)
	### reshape for writing oputput
	sig2_norm = np.reshape(sig2_norm, (sig2_norm.shape[0],1))

	###FRiP score
	sig2_norm_FRiP = np.sum(sig2_norm[(sig2_binary!=0)]) / np.sum(sig2_norm)
	sig2_FRiP = np.sum(sig2[(sig2_binary!=0)]) / np.sum(sig2)
	sig1_FRiP = np.sum(sig1[(sig1_binary!=0)]) / np.sum(sig1)

	### write output: normalized signal
	sig2_norm_bedgraph = np.concatenate((sig1_raw[:,0:3], sig2_norm), axis=1)
	write2d_array(sig2_norm_bedgraph, sig2_output_name + '.s3norm.bedgraph')
	### write output: sf & FRiP
	info = np.array([['Mean_ratio', 'S3norm_B', 'S3norm_A'], [total_mean_sf, Bo, Ao]])
	write2d_array(info, sig2_output_name + '.info.txt')



############################################################################
### time python ../src/s3norm.py -r reference.bedgraph -t target.bedgraph -o target -m non0mean -i 2.0 -f 0.05 -l 0.001 -a 100 -b 0 -p z -k 0 -g 0
### time python ../src/s3norm.py -r reference.bedgraph -t target.bedgraph -o target

import getopt
import sys
def main(argv):
	### read user provided parameters
	opts, args = getopt.getopt(argv,"hr:t:o:m:i:f:l:a:b:p:k:g:c:")
	for opt,arg in opts:
		if opt=="-h":
			print('time python ../src/s3norm.py -r reference.bedgraph -t target.bedgraph -o target -m (Method for matching peaks and background: non0mean, non0median, mean, median) -i initial_B -f FDR_thresh -l rank_lim_p -a upperlimit -b lowerlimit -p (p-value_method: neglog10p, z) -k common_pk_binary (0 for nocommon_pk; common_pk_binary.txt) -g common_bg_binary (0 for nocommon_pk; common_bg_binary.txt) -c cross_mark (T for using dataset pk; F using cpk & cbg)')
			return()	
		elif opt=="-r":
			sig1_wg_raw=str(arg.strip())				
		elif opt=="-t":
			sig2_wg_raw=str(arg.strip())
		elif opt=="-o":
			sig2_output_name=str(arg.strip())
		elif opt=="-m":
			NTmethod=str(arg.strip())
		elif opt=="-i":
			B_init=float(arg.strip())
		elif opt=="-f":
			fdr_thresh=float(arg.strip())
		elif opt=="-l":
			rank_lim=float(arg.strip())
		elif opt=="-a":
			upperlim=float(arg.strip())
		elif opt=="-b":
			lowerlim=float(arg.strip())
		elif opt=="-p":
			p_method=str(arg.strip())
		elif opt=="-k":
			common_pk_binary=str(arg.strip())
		elif opt=="-g":
			common_bg_binary=str(arg.strip())
		elif opt=="-c":
			cross_mark=str(arg.strip())

	############ Default parameters
	###### required parameters
	try:
		print('User provide reference.bedgraph: -r '+str(sig1_wg_raw))
		print('User provide target.bedgraph: -t '+str(sig2_wg_raw))
		print('User provide outputname: -o '+str(sig2_output_name))
	except NameError:
		print('Missing required parameter(s): time python ../src/s3norm.py -r reference.bedgraph -t target.bedgraph -o target')	
		return()	
	###
	###### optional parameters
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
		B_init = 2.0
	###
	try:
		print('User provide fdr_thresh: -f '+str(fdr_thresh))
		if fdr_thresh<0 or fdr_thresh>1:
			print('-f (0.000001~1.0)')
			return()
	except NameError:
		print('Default fdr_thresh: -f 0.05')
		fdr_thresh = 0.05
	###
	try:
		print('User provide rank_lim: -l '+str(rank_lim))
		if rank_lim<0 or rank_lim>1:
			print('-l (0.000001~1.0)')
			return()
	except NameError:
		print('Default rank_lim: -l 0.001')
		rank_lim = 0.001
	###
	try:
		print('User provide upperlim: -a '+str(upperlim))
	except NameError:
		print('Default upperlim: -a 100000')
		upperlim = 100000
	###
	try:
		print('User provide lowerlim: -b '+str(lowerlim))
	except NameError:
		print('Default lowerlim: -b 0')
		lowerlim = 0
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
	s3norm(sig1_wg_raw, sig2_wg_raw, sig2_output_name, NTmethod, B_init, fdr_thresh, rank_lim, upperlim, lowerlim, p_method, common_pk_binary, common_bg_binary, cross_mark)

if __name__=="__main__":
	main(sys.argv[1:])


