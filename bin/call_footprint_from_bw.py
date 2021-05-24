#!/home/yli11/.conda/envs/py2/bin/python
import pyBigWig
import argparse
import pandas as pd
import numpy as np
import scipy
from scipy.signal import find_peaks
"""

find peak, find regions in between, check depth




"""

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('--bw',  help="biwiggle file",required=True)
	mainParser.add_argument('--bed',  help="motif bed file",required=True)
	mainParser.add_argument('-o','--output',  help="outputfile",required=True)
	mainParser.add_argument('-l','--window_length',  help="scan window size",default=50,type=int)
	mainParser.add_argument('-s','--step_size',  help="moving window by this size",default=10,type=int)

	


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def find_peak(x,bw,extend_length=60):
	# print ("x",x)
	start = max(0,x[1]-extend_length)
	myList = bw.values(x[0], start , x[2]+extend_length)
	# print (myList)
	peaks, prop = find_peaks(myList,height=5,prominence=0,wlen=3)
	# print (peaks)
	selected = []
	for i in range(len(peaks)):
		current_value = myList[peaks[i]]
		# print (start+peaks[i],current_value,prop['prominences'][i])
		if prop['prominences'][i]>=current_value/2.0:
			# selected.append([x[0],start+peaks[i]])
			selected.append(start+peaks[i])
	footprints = []
	# print ("selected",selected)
	for i in range(len(selected)-1):
		# print (i)
		current_FT = [x[0],selected[i]+1,selected[i+1]]
		size = selected[i+1]-selected[i]-2
		if size <=5 or size >=50:
			continue
		if depth_filter(current_FT,bw):
			footprints.append(current_FT)
	return footprints

# def find_candidate_region(x):
	

			
def depth_filter(x,bw):
	# print ("peak",x)
	# print ("FT:",bw.values(x[0], x[1] , x[2]))
	# print ("ALL:",bw.values(x[0], x[1]-3 , x[2]+3))
	FT_mean = np.mean(bw.values(x[0], x[1] , x[2]))
	left_mean = np.mean(bw.values(x[0], x[1]-3 , x[1]))
	# print ("left:",bw.values(x[0], x[1]-3 , x[1]))
	right_mean = np.mean(bw.values(x[0], x[2] , x[2]+3))
	# print ("right:",bw.values(x[0], x[2] , x[2]+3))
	
	# print (left_mean,FT_mean,right_mean)
	# exit()
	if left_mean/FT_mean>=2 and right_mean/FT_mean>=2:
		return True
	return False



def main():

	args = my_args()
	bw = pyBigWig.open(args.bw)
	bed = pd.read_csv(args.bed,sep="\t",header=None)
	# print (bed.head())
	selected_footprints = []
	peaks=[]
	for i in bed.index:
		# print ("START",i)
		peaks.append(find_peak(bed.loc[i].tolist(),bw))
	# print (peaks)
	for i in peaks:
		if i == []:
			continue
		selected_footprints+=i
	# print (selected_footprints)
	out = pd.DataFrame(selected_footprints)
	# print (out.head())
	out['name'] = out[0]+out[1].astype(str)+out[2].astype(str)
	out = out.drop_duplicates('name')
	out[[0,1,2]].to_csv(args.output,sep="\t",header=False,index=False)

	
if __name__ == "__main__":
	main()


























