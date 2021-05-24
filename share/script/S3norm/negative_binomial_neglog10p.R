### get parameters
args = commandArgs(trailingOnly=TRUE)

signal_track_file = args[1]
input_track_file = args[2]
output_name = args[3]

mean_vec = c()
var_vec = c()
size_vec = c()
prob_vec = c()

###### get NB model prob and size
get_true_NB_prob_size = function(x){
	m=mean(x[x>0]);
	m2=mean(x[x>0]^2);
	p0 = length(which(x==0)) / length(x);
	p = m/(m2-m^2 * (1-p0));
	s = m * (1 - p0) * p /(1-p);
	rt=c(p,s,p0);

	for(i in 1:100){
		op = p;
		os = s;
		p0=p^s;
		#print(p0)
		p=m/(m2-m^2*(1-p0));
		if (p<0.001){
			p = 0.001
		}
		if (p>=0.999){
			p = 0.999
		}
		s=m * (1 - p0) * p / (1-p);
		#rt=rbind(rt,c(p,s,p0));
		rt = c(p,s,p0)
		if(abs(op-p)<0.00001 & abs(os-s)<0.00001) break;
	}
	#print('change best_p0: ')
	#print(p0)
	return(rt);
}

###### get NB model p-value
get_pval = function(N, l, sig_0_size, sig_0_prob, num_0){
	if (N != 0){
		pval_new = pnbinom(N-1, sig_0_size, sig_0_prob, lower.tail=FALSE) / pnbinom(0, sig_0_size, sig_0_prob, lower.tail=FALSE) * (l-num_0)/l
	} else {
		pval_new = 1.0
	}
	return(pval_new)
}

### read data
sig_raw = read.table(signal_track_file, header = F)
input_raw = read.table(input_track_file, header = F)

#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
### get sig bg regions no bgs
sig = sig_raw[,4]
thresh = 0
min_non0 = min(sig[sig>=1])

### remove used value smaller than 1
sig[sig<1]=0

### remove extrame signals
sig_notop = sig[sig<=quantile(sig, 0.99)]
if (sum(sig_notop>1)<30){
print('Bins with signal greater than 1 is Less than 30. There may have some problem in the data')
sig_notop = sig
}

### make sure the min(positive number is 1)
if (min_non0>10){
	print('The minimum non0 value is greater than 10. The reads may be extended. Please use counts without extension by divide minimum signal that is greater than 1')
}

### get 0 number
obs_0_num = sum(sig_notop==thresh)
### get none 0 signals
sig_notop = sig_notop[sig_notop>thresh]
### get mean moment2 var
sig_mean = mean(sig_notop)
sig_moment2 = mean(sig_notop^2)
sig_var = var(sig_notop)

###### get NB model prob and size and p0
sig_probT_sizeT = get_true_NB_prob_size(sig_notop)
p0 = sig_probT_sizeT[3]
sig_size = sig_probT_sizeT[2]
sig_prob = sig_probT_sizeT[1]
### set limit for prob
if (sig_prob<0.001){
	sig_prob = 0.001
}
if (sig_prob>=0.999){
	sig_prob = 0.999
}

### get input bg regions
input = input_raw[,4]
### get input mean and var
input_mean = mean(input)
input_var = var(input)

### get bin number
bin_num = dim(sig_raw)[1]

### cbind IP and CTRL
sig_input = cbind(sig, input)

### get negative binomial p-value 
nb_pval = apply(sig_input, MARGIN=1, function(x) get_pval(x[1], bin_num, sig_size * (x[2]+0.1)/(input_mean+0.1), sig_prob, obs_0_num) )

### remove extrame p-value
nb_pval[nb_pval<=1e-323] = 1e-323

### get -log10(p-value)
nb_pval[nb_pval<=1e-323] = 1e-323
nb_pval[nb_pval>1] = 1.0
neglog10_nb_pval = -log10(nb_pval)
neglog10_nb_pval_bedgraph = cbind(sig_raw[,1:3], neglog10_nb_pval)
print('summary negative log10 NB p-value:')
print(summary(neglog10_nb_pval_bedgraph[,4]))

### write output
write.table(neglog10_nb_pval_bedgraph, output_name, quote=FALSE, col.names=FALSE, row.names=FALSE, sep='\t')

