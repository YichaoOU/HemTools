#!/hpcf/apps/python/install/2.7.13/bin/python

import pandas as pd
import sys
import numpy as np
def read_bed(file,label):
	df = pd.read_csv(file,header=None,sep="\t")
	df['name'] = df[0]+":"+df[1].astype(str)+"-"+df[2].astype(str)+"|"+df[3]
	df = df.drop_duplicates('name')
	df['duplicated'] = df.groupby(3)[3].transform('size')
	df = df.drop_duplicates(3)
	df = df.drop(['name',4],axis=1)
	df['mid'] = (df[1]+df[2])/2
	# print (df.head())
	df.columns=['%s.chr'%(label),'%s.start'%(label),'%s.end'%(label),3,'%s.strand'%(label),'%s.Num_dup'%(label),'%s.mid'%(label)]
	
	return df



r1 = read_bed(sys.argv[1],'R1')
r2 = read_bed(sys.argv[2],"R2")
output_name = sys.argv[3]

unique_read_names = list(set(r1[3].tolist()+r2[3].tolist()))
r1 = r1.set_index(3)
r2 = r2.set_index(3)
all = pd.concat([r1.loc[unique_read_names],r2.loc[unique_read_names]],axis=1)
# all.isnull().any().any()
all['R1.Num_dup'] = all['R1.Num_dup'].fillna(0)
all['R2.Num_dup'] = all['R2.Num_dup'].fillna(0)
all['R1.strand'] = all['R1.strand'].fillna("NA")
all['R2.strand'] = all['R2.strand'].fillna("NA")
all['distance'] = all['R1.mid']-all['R2.mid']
all['chr_dis'] = all["R1.chr"] == all["R2.chr"]
all.to_csv("%s.mapping.info.csv"%(output_name))

all['N_match'] = all['R1.Num_dup']+all['R2.Num_dup']
all = all[all['N_match']<=2]
com = pd.DataFrame({'count' : all.groupby( [ "R1.strand", "R2.strand"] ).size()}).reset_index()
com["count"] = com["count"]/com["count"].sum()
com['name'] = com['R1.strand'] + " " + com['R2.strand']
com = com[['name','count']]
com = com.set_index('name')
com = com.T
com.index = [output_name]
# print (com)
columns = ["+ +","+ -","+ NA","- +","- -","- NA","NA +","NA -"]
for c in columns:
	try:
		com[c]
	except:
		com[c] = 0
com[columns].to_csv("%s.direction.summary.csv"%(output_name),header=False)

def get_dis_info(df):
	total = float(df.shape[0])
	if total == 0:
		total = 1.0
	interCHR = df[df['chr_dis']==False].shape[0]
	median_pos = df[(df['chr_dis']==True) & (df['distance']>0)]['distance'].median()
	median_neg = df[(df['chr_dis']==True) & (df['distance']<0)]['distance'].median()
	overlap = df[(df['chr_dis']==True) & (df['distance']>=-10) & (df['distance']<=10)].shape[0]
	return interCHR/total,overlap/total,median_pos,median_neg
out = {}
for s,d in all.groupby( [ "R1.strand", "R2.strand"] ):
	name = " ".join(s)
	interCHR,overlap,median_pos,median_neg = get_dis_info(d)
	out["%s.interCHR"%(name)] = interCHR
	out["%s.overlap"%(name)] = overlap
	out["%s.pos-d"%(name)] = median_pos
	out["%s.neg-d"%(name)] = median_neg

df = pd.DataFrame.from_dict(out,orient='index').T
df.index = [output_name]
columns = ["NA +.overlap","+ +.overlap","- NA.overlap","+ NA.interCHR","- NA.neg-d","- +.pos-d","+ NA.overlap","+ +.pos-d","- NA.interCHR","NA +.neg-d","+ +.neg-d","- -.pos-d","- -.overlap","- -.neg-d","- +.interCHR","NA +.interCHR","+ +.interCHR","+ NA.pos-d","- NA.pos-d","+ -.pos-d","NA -.pos-d","- -.interCHR","+ -.neg-d","NA -.neg-d","- +.overlap","- +.neg-d","NA -.overlap","+ -.overlap","+ NA.neg-d","NA -.interCHR","+ -.interCHR","NA +.pos-d"]
for c in columns:
	try:
		df[c]
	except:
		df[c] = np.nan
df[columns].to_csv("%s.distance.summary.csv"%(output_name),header=False)
"""

For all uniquely mapped reads, what is the percentage of 

FR, RF, FF, RR?

F-, R-, -F, -R?

in each of the four (FR, RF, FF, RR), how is the insertion size difference?




dup=1
chr_dis =True
summary of FR,RF, FF, RR

"""









