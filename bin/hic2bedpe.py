

df_list = []
import pandas as pd
import os
for i in range(22):
	i = i+1
	command = "java -jar /home/yli11/HemTools/share/script/jar/juicer_tools_1.22.01.jar dump observed KR GSE63525_GM12878_insitu_primary_replicate_combined.hic chr{0} chr{0} BP 10000 chr{0}.bed".format(i)
	print (i)
	os.system(command)
	df = pd.read_csv("chr{0}.bed".format(i),sep="\t",header=None)
	print (df.head())
	df['chr'] = "chr%s"%(i)
	df['start'] = df[0]
	df['end'] = df[0]+10000
	df['R2_start'] = df[1]
	df['R2_end'] = df[1]+10000
	df['score'] = df[2]
	df_list.append(df[['chr','start','end','chr','R2_start','R2_end','score']])
df = pd.concat(df_list)
df.shape
df.head()
df = df.fillna(0)
df.shape
df.head()
df = df.dropna()
df.shape
df.head()
df.columns = [0,1,2,3,4,5,6]
df.head()
df = df.sort_values([0,1])
df.to_csv("dewan.bedpe",index=False,header=False,sep="\t")
