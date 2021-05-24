#!/home/yli11/.conda/envs/janggu3/bin/python


from keras.models import Model

import argparse
import matplotlib
matplotlib.use('agg')
import tensorflow as tf
import seaborn as sns
import matplotlib.pyplot as plt
from pkg_resources import resource_filename
from janggu.data import Bioseq
from janggu.data import ReduceDim

import numpy as np
from keras.layers import Conv2D,LSTM,Conv1D
from keras.layers import AveragePooling2D
from janggu import inputlayer
from janggu import outputconv
from janggu import DnaConv2D
from janggu.data import ReduceDim
from janggu.data import Cover
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D,Input,GlobalAveragePooling2D,MaxPooling1D
from keras import backend as K
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import scipy
import seaborn as sns
import glob
from sklearn.model_selection import KFold,StratifiedKFold
import warnings
from sklearn.metrics import roc_curve,roc_auc_score,precision_recall_curve,average_precision_score
import warnings
warnings.filterwarnings('ignore')
# warnings.simplefilter(action='ignore', category=FutureWarning)
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor,RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics.scorer import make_scorer
from sklearn.model_selection import train_test_split
from sklearn.base import TransformerMixin
from sklearn.datasets import make_regression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor,GradientBoostingClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
import scipy
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
from sklearn import linear_model
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge,Lars,BayesianRidge
from keras.utils import plot_model
from copy import deepcopy as dp
from keras.layers import Layer, Input, Lambda,TimeDistributed
from keras.layers import Reshape, Lambda,Bidirectional


"""
This program uses janggu to get one-hot encoding of DNA sequences 

Input
-----

pos.bed

neg.ned

Parameters
----------

flanking length
nb_Conv2d_filter
nb_MaxPool_filter

Method
------

Network types

1. CP -> BLSTM -> Dense

2. Janggu DNAconv2D

"""


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="deep learning DNA")
	
	mainParser.add_argument("-p","--positive_bed",  help="3 columns or 6 columns with strand info",required=True,type=str)
	mainParser.add_argument("-n","--negative_bed",  help="3 columns or 6 columns with strand info",required=True,type=str)
	mainParser.add_argument("--refgenome",  help="genome fasta",default="/home/yli11/Data/Human/hg19/fasta/hg19.fa",type=str)
	mainParser.add_argument("--flank",  help="extend flank length",type=int,default=100)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def plot_ROC(df):
	plt.figure()
	plot_df = pd.DataFrame()
	x_predict,y_predict,_ = roc_curve(df['true'],df['pred'])
	auc = roc_auc_score(df['true'],df['pred'])
	print ("auROC score is:",auc)
	plot_df['x'] = x_predict
	plot_df['y'] = y_predict
	sns.lineplot(data=plot_df,x="x",y="y",ci=1,label="auROC=%.2f"%(auc))
	plt.plot([0, 1], [0, 1], 'k--')
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.xlabel('False positive rate')
	plt.ylabel('True positive rate')	
	plt.title('ROC curve')
	plt.legend(loc='best',title="")
	plt.savefig("ROC.png")


def plot_PRC(df):
	plt.figure()
	plot_df = pd.DataFrame()
	x_predict,y_predict,_ = precision_recall_curve(df['true'],df['pred'])
	auc = average_precision_score(df['true'],df['pred'])
	print ("auPRC score is:",auc)
	plot_df['x'] = x_predict
	plot_df['y'] = y_predict
	sns.lineplot(data=plot_df,x="x",y="y",ci=1,label="auPRC=%.2f"%(auc))
	plt.plot([0, 1], [0, 1], 'k--')
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.xlabel('False positive rate')
	plt.ylabel('True positive rate')	
	plt.title('Precision-Recall Curve')
	plt.legend(loc='best',title="")
	plt.savefig("PRC.png")




def CP_BLSTM_model(dna_length):

	dna_input = Input(shape=(dna_length,4,1),name="DNA_input")
	conv_length=15
	pool_length = 20
	DNA_shared_Conv2D_1 = Conv2D(20, kernel_size=(conv_length, 4),activation='relu',name="DNA_Conv2d")
	DNA_shared_MaxPool_1 = MaxPooling2D(pool_size=(pool_length, 1),strides=(1,1),name="DNA_MaxPool")
	DNA_model = DNA_shared_MaxPool_1((DNA_shared_Conv2D_1(dna_input)))
	conv_to_LSTM_dims=(dna_length - conv_length - pool_length + 2,pool_length)
	DNA_model = Reshape(target_shape=conv_to_LSTM_dims, name='DNA_CNN_reshape')(DNA_model)
	DNA_LSTM = Bidirectional(LSTM(32))(DNA_model)
	combined_dense = Dense(200, activation='relu')(DNA_LSTM)
	output = Dense(2, activation = (tf.nn.softmax))(combined_dense)
	return dna_input,output


## CV
def DNA_model(dna_train,dna_test,y_train, y_test):
	y_train = keras.utils.to_categorical(y_train, 2)
	y_test = keras.utils.to_categorical(y_test, 2)
	dna_input,output = CP_BLSTM_model(dna_train.shape[1])
	model = Model(inputs=dna_input, outputs=output)

	model.compile(loss=keras.losses.binary_crossentropy,
				  optimizer=keras.optimizers.Adadelta(),
				  metrics=['accuracy'])

	model.fit(dna_train, y_train,
			  batch_size=20,
			  epochs=100,
			  verbose=1,
			  validation_data=(dna_test, y_test))
	plot_model(model, to_file='DNA_model.png',show_shapes=True)
	y_pred = model.predict(dna_test)
	

	return [x[1] for x in y_pred]

def cv_evaluation(dna,y):
	outer = StratifiedKFold(n_splits=3)
	my_pred=[]
	my_true=[]
	for train_index, test_index in outer.split(np.zeros(len(y)),y):
		dna_train, dna_test = dna[train_index,:,:,:], dna[test_index,:,:,:]
		y_train, y_test = y[train_index], y[test_index]
		pred_y = DNA_model(dna_train,dna_test,y_train, y_test)
		my_pred += pred_y
		my_true += y_test.tolist()
	df = pd.DataFrame()
	df['true']=my_true
	df['pred']=my_pred
	return df   

def combine_bed(pos_bed_file,neg_bed_file):
	pos = pd.read_csv(pos_bed_file,sep="\t",header=None)
	neg = pd.read_csv(neg_bed_file,sep="\t",header=None)
	df = pd.concat([pos,neg])
	df['mid'] = (df[1]+df[2])/2
	df['mid'] = df['mid'].astype(int)
	df[1] = df['mid']-1
	df[2] = df['mid']
	df = df.drop(['mid'],axis=1)
	df.to_csv("input.bed",sep="\t",header=False,index=False)
	return np.array([1]*pos.shape[0]+[0]*neg.shape[0])

def get_data(refgenome,flank):
	dna = Bioseq.create_from_refgenome(name='dna',refgenome=refgenome,roi="input.bed",flank=flank)
	print (dna.shape[0])
	return np.reshape(dna,(dna.shape[0],flank*2+1,4,1))		  


def main():

	args = my_args()
	
	y = combine_bed(args.positive_bed,args.negative_bed)
	X = get_data(args.refgenome,args.flank)
	df = cv_evaluation(X,y)
	plot_ROC(df)
	plot_PRC(df)
	

		
		
if __name__ == "__main__":
	main()















