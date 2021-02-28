Python Pandas
=========



Working with excel
^^^^^^^^

::


	import pandas as pd
	f="bar plot-summary.xlsx"
	xls = pd.ExcelFile(f)
	xls.sheet_names
	import scipy.stats
	writer = pd.ExcelWriter('barplot_data_with_pvalue.xlsx', engine='xlsxwriter')
	for s in xls.sheet_names:
	    ## calculate p-value
	    df = pd.read_excel(f,sheet_name=s,header=None)
	    out = [""]
	    for i in range(1,df.shape[1]):
	        x=scipy.stats.ttest_ind(df[0].tolist(),df[i].tolist()).pvalue
	        out.append(x)
	    df.loc["P-value"] = out
	    df.to_excel(writer, sheet_name=s)
	writer.save()


