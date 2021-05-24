#!/usr/bin/env python
import pandas as pd
import sys

"""bdg+bed to ibed




output format
--------

ID_Bait	chr_Bait	start_Bait	end_Bait	Bait_name	ID_OE	chr_OE	start_OE	end_OE	OE_name	N
30	chr1	3090913	3092556	U6.149	590	chr1	4592259	4592779	.	0
30	chr1	3090913	3092556	U6.149	593	chr1	4595997	4596467	.	1
30	chr1	3090913	3092556	U6.149	596	chr1	4605050	4610398	.	2

for runnning https://github.com/yousra291987/ChiCMaxima





"""


bdg_file = sys.argv[1]
bed_file = sys.argv[2]

bdg = pd.read_csv(bdg_file,sep="\t",header=None,comment="#")
bed = pd.read_csv(bed_file,sep="\t",header=None,comment="#")
bed[4] = bed[0]+"_"+bed[1].astype(str)+"_"+bed[2].astype(str)
bed[5] = bed.index.tolist()
bdg[4] = bdg[0]+"_"+bdg[1].astype(str)+"_"+bdg[2].astype(str)
bdg[5] = bdg.index.tolist()
## ID has to be int
df_list= []
for chr,start,end,name,id in bed.values:
	# print (chr,start,end,name)
	tmp =bdg[bdg[0]==chr]
	# start+=3000
	# end+=3000
	tmp2 = tmp[(tmp[1]<end)&(tmp[1]>start)]
	tmp3 = tmp[(tmp[2]>start)&(tmp[1]<start)]

	tmp = tmp[~tmp.index.isin(tmp2.index)]
	tmp = tmp[~tmp.index.isin(tmp3.index)]
	tmp['ID_Bait'] = id
	tmp['chr_Bait'] = chr
	tmp['start_Bait'] = start
	tmp['end_Bait'] = end
	tmp['Bait_name'] = name
	tmp['ID_OE'] = tmp[5]
	tmp['chr_OE'] = tmp[0]
	tmp['start_OE'] = tmp[1]
	tmp['end_OE'] = tmp[2]
	tmp['OE_name'] = tmp[4]
	tmp['N'] = tmp[3]
	tmp = tmp.drop([0,1,2,3,4,5],axis=1)

	df_list.append(tmp)
df = pd.concat(df_list)
df.to_csv("input.ibed",sep="\t",index=False)












