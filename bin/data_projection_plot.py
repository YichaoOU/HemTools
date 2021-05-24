import pandas as pd
import seaborn as sns
%matplotlib inline
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
import matplotlib
import pandas as pd
# matplotlib.use('agg')
import seaborn as sns
import numpy as np
import scipy
import glob
import sys
import matplotlib.pyplot as plt
import os
%matplotlib inline
import numpy as np
import plotly.graph_objs as go
import plotly.io as plio
import plotly.express as px
import plotly
from sklearn.metrics import pairwise_distances

def get_projected_data(query,X,predict_class,top_k):
	my_df_list = []
	for i in list(range(len(predict_class))):
		current_class  = predict_class[i]
		query_dist = pd.DataFrame(pairwise_distances(np.array([query.iloc[i].tolist()]),X)).T
		query_dist.columns = ['distance']
		query_dist['class'] = Y
		query_dist = query_dist[query_dist['class']==predict_class[i]]
		query_dist = query_dist.sort_values("distance")
		my_top_k_index = query_dist.index.tolist()[:top_k]
		projected_features = pd.DataFrame(X.iloc[my_top_k_index].mean()).T
		my_df_list.append(projected_features)
	new_df = pd.concat(my_df_list)
	new_df.index = query.index.tolist()
	return new_df



# Train a RF model for reference data frame
ref = pd.read_csv("public_data.csv",index_col=0)
X = ref.drop(['type','disease'],axis=1)
le = preprocessing.LabelEncoder()
Y = ref.type.tolist()
le.fit(Y)
clf = RFC(n_estimators=200,random_state=0,oob_score=True)
clf.fit(X, le.transform(Y))  
print ("generalized accuracy (oob_score) is:%s"%(clf.oob_score_ ))
# given a query, get its class and its k most similar 
query = pd.read_csv("Li_data.csv",index_col=0)
query_X = query.drop(['type','disease'],axis=1)
predict_class =list(le.inverse_transform(clf.predict(query_X)))
top_k=3
projected_df = get_projected_data(query_X,X,predict_class,top_k)

# tSNE plot
plot_df = pd.concat([X,projected_df])
nPC=100
pca = PCA(nPC)
tsne = TSNE(2)
tmp_df = pd.DataFrame(pca.fit_transform(plot_df))
tmp_df2 = pd.DataFrame(tsne.fit_transform(tmp_df))
tmp_df2.columns = ['x','y']
tmp_df2['color'] = Y+predict_class
tmp_df2['text'] = plot_df.index.tolist()
tmp_df2['shape'] = ref['disease'].tolist()+query['disease'].tolist()
tmp_df2['size']=[1]*ref['disease'].shape[0]+[3]*query['disease'].shape[0]
px.scatter(tmp_df2,x="x",y='y',color='color',hover_data=['text'],opacity=0.8,symbol='shape',size='size',size_max=12)

