#!/hpcf/apps/python/install/2.7.13/bin/python
import pandas as pd
import sys
df = pd.read_csv(sys.argv[1])
df.index = df['Gene ID']
gene_df = df.groupby("Gene ID").sum()
df = df.drop_duplicates("Gene ID")
gene_df['Gene Name'] = df.loc[gene_df.index.tolist()]['Gene Name'].tolist()
gene_df.columns = [x.replace(".tpm","") for x in gene_df.columns]
gene_df.to_csv(sys.argv[1]+".gene.csv")







