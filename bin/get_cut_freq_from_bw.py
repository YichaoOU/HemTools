#!/home/yli11/.conda/envs/py2/bin/python
import pyBigWig
import argparse
import pandas as pd
import numpy as np
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('--bw',  help="biwiggle file",required=True)
	mainParser.add_argument('--bed',  help="motif bed file",required=True)
	mainParser.add_argument('-o','--output',  help="outputfile",required=True)
	mainParser.add_argument('-l','--length',  help="extending length",default=100,type=int)
	mainParser.add_argument('--depth_cutoff',default=1,type=float)
	


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def row_apply(x,bw,extend_length):
	# print (x[0])
	# print (x[1])
	# print (x[2],extend_length)
	try:
		myList = bw.values(x[0], max(0,x[1]-extend_length), x[2]+extend_length)
		if len(x) <= 3:
			return myList
		if x[5] == "+":
			return myList
		if x[5] == "-":
			# print ("using -")
			return myList[::-1]
	except:
		# print ("some error")
		print (x)
		myList = bw.values(x[0], max(0,x[1]-extend_length), x[2])+[0]*extend_length
		if x[5] == "+":
			return myList
		if x[5] == "-":
			# print ("using -")
			return myList[::-1]
			
def cal_FOS(x,args,motif_length):
	left_start = args.length-3
	# print ("left_start",left_start)
	# print (x[0:left_start])
	left_mean = x[left_start:args.length].mean(axis=0)
	# print ("left_mean",left_mean)
	motif_mean = x[args.length:args.length+motif_length].mean(axis=0)
	right_mean = x[args.length+motif_length:args.length+motif_length+3].mean(axis=0)
	# left_flag = (motif_mean)/float(left_mean+1)
	# right_flag = (motif_mean)/float(right_mean+1)
	# FOS = left_flag+right_flag
	# num_count = left_mean + right_mean
	flank_mean = np.mean([left_mean,right_mean])
	depth = flank_mean - motif_mean
	return depth
	# num_count = x.sum(axis=0)
	# if num_count < 10:
		# return False
	# else:
		# return True
	# if FOS < 2:
		# return True
	# else:
		# return False


def main():

	args = my_args()
	bw = pyBigWig.open(args.bw)
	bed = pd.read_csv(args.bed,sep="\t",header=None)
	motif_length = bed.at[0,2]-bed.at[0,1]
	# print (bed.head())
	# bed[1] = bed[1].astype(int)
	# bed[2] = bed[2].astype(int)
	cut_freq = bed.apply(lambda x:pd.Series(row_apply(x,bw,args.length)),axis=1)
	# print (list(cut_freq))
	cut_freq.index = bed.index.tolist()
	cut_freq = pd.DataFrame(cut_freq)
	cut_freq = cut_freq.fillna(0)
	cut_freq['depth'] = cut_freq.apply(lambda x:cal_FOS(x,args,motif_length),axis=1)
	bed[4] = cut_freq['depth']
	bed.to_csv(args.output+".raw_fimo.bed",sep="\t",index=False,header=False)
	# cut_freq = cut_freq[cut_freq['depth']>0]
	cut_freq = cut_freq[cut_freq['depth']>=args.depth_cutoff]
	cut_freq = cut_freq.drop(['depth'],axis=1)
	bed = bed.loc[cut_freq.index.tolist()]
	# cut_freq = cut_freq.astype(int)
	# cut_freq = pd.concat([cut_freq,cut_freq[cut_freq.columns.tolist()[::-1]]],axis=1)
	cut_freq.to_csv(args.output,sep="\t",index=False,header=False)
	bed.to_csv(args.output+".filtered_fimo.bed",sep="\t",index=False,header=False)
	print (cut_freq.shape)

	
if __name__ == "__main__":
	main()


























