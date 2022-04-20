Python visualization code examples
======================================


Pairplot
^^^^^^^^

Use ``size=3, aspect=1, layout_pad=2`` to control figure size and subplots margin.

Use ``map_upper, map_lower, map_diag`` to control figure type

Use ``g.axes.flat`` and ``int(count/3),count%3`` to manage which sub plot. Here 3 is the number of columns I have. 

::


	sns.set_style("whitegrid")
	g = sns.PairGrid(df, diag_sharey=False,size=3, aspect=1,layout_pad=2)
	cols = df.columns.tolist()
	from scipy import stats
	g.map_upper(sns.histplot,color="grey")
	g.map_lower(sns.regplot,scatter=False,line_kws={"color": "red"},ci=99)
	g.map_lower(sns.kdeplot,fill=True)
	g.map_diag(sns.histplot)
	count = 0
	for ax in g.axes.flat:
	    ax.set_title(count)
	    i,j = int(count/3),count%3
	    count += 1
	    if j >= i:
	        continue
	    print (count-1,i,j)
	    pr = stats.pearsonr(df[cols[i]], df[cols[j]])[0]
	    sr = stats.spearmanr(df[cols[i]], df[cols[j]])[0]
	    leg=ax.legend(['R=%.2f\nr=%.2f'%(sr,pr)],frameon=False) #add text
	    for item in leg.legendHandles:
	        item.set_visible(False) 
	plt.savefig("SPROUT_DeepSpCas9.pairplot.pdf",bbox_inches='tight')




displot, histplot, kdeplot
^^^^^^^^^^^^^^^

::

	sns.histplot(data=model_selection,x="N_outlier",hue="treatment",multiple="dodge")

