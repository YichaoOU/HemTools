#!/home/yli11/.conda/envs/py2/bin/python

import sys
import argparse
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import xgboost as xgb
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
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression,RidgeClassifier,SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB 
from sklearn.ensemble import RandomForestClassifier
from mlxtend.classifier import StackingCVClassifier
import umap
import warnings
from sklearn.metrics import roc_curve,roc_auc_score
from sklearn.datasets import load_iris
from mlxtend.classifier import StackingCVClassifier
from mlxtend.feature_selection import ColumnSelector
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings('ignore')
from sklearn.exceptions import ConvergenceWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=ConvergenceWarning)
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor,RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics.scorer import make_scorer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

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
from sklearn.svm import SVR,LinearSVC
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge,Lars,BayesianRidge
from copy import deepcopy as dp
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier,RadiusNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.gaussian_process import GaussianProcessClassifier
from xgboost import XGBClassifier
from sklearn.feature_selection import RFECV
import uuid

def gkm_SVM_fit_transform(pos_train,neg_train,pos_test,neg_test,d):
	addon_string = str(uuid.uuid4()).split("-")[-1]
	kernel_out = addon_string + ".kernel.out"
	train_out = addon_string + ".train"
	classify_out = addon_string + ".classify.out"
	kernel_command = "gkmsvm_kernel -d %s %s %s %s"%(d,pos_train,neg_train,kernel_out)
	train_command = "gkmsvm_train %s %s %s %s"%(kernel_out,pos_train,neg_train, train_out)
	
	classify_input = addon_string + ".classify_input.fa"
	combine_pos_neg_command = "cat %s %s > %s"%(pos_test,neg_test,classify_input)
	classify_command = "gkmsvm_classify -d %s %s %s_svseq.fa %s_svalpha.out %s"%(d,classify_input,train_out,train_out,classify_out)
	## run
	os.system(kernel_command)
	os.system(train_command)
	os.system(combine_pos_neg_command)
	os.system(classify_command)
	
	
	y_pred = pd.read_csv(classify_out,sep="\t",header=None,index_col=0)
	y_pred.columns = ['pred']
	y_true = to_true_label(pos_test,neg_test)
	df = pd.concat([y_true,y_pred],axis=1)

	print ("### y true and y pred ###")
	print (df.head())
	os.system("rm %s*"%(addon_string))	
	return df
	
	
def get_top_features(reg,X,y,top_n):
	"""Replace by RFECV"""
	current_feature_df = pd.DataFrame()
	current_feature_df['features'] = X.columns.tolist()

	reg.fit(X,y)
	try:
		current_feature_df['score'] = list(reg.feature_importances_) 
	except:
		try:
			current_feature_df['score'] = list(reg.coef_) 
		except:
			current_feature_df['score'] = list(reg.coef_[0]) 
				
	current_feature_df = current_feature_df.sort_values('score',ascending=False)
	return current_feature_df['features'].tolist()[:top_n]
def AUC_gridSearch(estimator,parameterDict,X,y):
    myModel = GridSearchCV(estimator,parameterDict,scoring="roc_auc",cv=3,verbose=0,n_jobs=-1,refit=True)
    myModel.fit(X,y)
    return myModel
def nested_cv_evaluation(model,params,X,y):

	outer = StratifiedKFold(n_splits=5,random_state=0)
	# outer = KFold(n_splits=X.shape[0]) ## this is for leave one out CV
	# min_samples_split 
	my_pred=[]
	my_true=[]
	roc_x = []
	roc_y = []	
	AUC_list = []
	for train_index, test_index in outer.split(X,y):
		X_train, X_test = X.iloc[train_index], X.iloc[test_index]
		y_train, y_test = y.iloc[train_index], y.iloc[test_index]



		# selector = RFECV(dp(model), step=2, cv=StratifiedKFold(3),scoring="roc_auc",n_jobs=-1)
		# selector.fit(X_train,y_train)
		# print ("Number of selected features: %s"%(selector.n_features_))
		# top_features = X.columns[selector.support_].tolist()
		# print ("selected features: %s"%(", ".join(top_features)))
		# current_model = AUC_gridSearch(dp(model),params,X_train[top_features].values,y_train)	
		# best_model = current_model.best_estimator_ 
		# print ("best_params_: ",current_model.best_params_ )
		# print ("best_score: ",current_model.best_score_ )

		## gkmSVM features
		
		current_model = AUC_gridSearch(dp(model),params,X_train.values,y_train)
		best_model = current_model.best_estimator_
		selector = RFECV(dp(best_model), min_features_to_select=5,step=1, cv=3,scoring="roc_auc",n_jobs=-1,verbose =1)
		selector.fit(X_train,y_train)
		print ("Number of selected features: %s"%(selector.n_features_))
		top_features = X.columns[selector.support_].tolist()
		print ("selected features: %s"%(", ".join(top_features)))
		best_model.fit(X_train[top_features],y_train)	
		 
		print ("best_params_: ",current_model.best_params_ )
		print ("best_score: ",current_model.best_score_ )

		pred_y = best_model.predict_proba(X_test[top_features].values)
		my_pred += [x[1] for x in pred_y]
		my_true += y_test.tolist()
		AUC_score = roc_auc_score(y_test.tolist(),[x[1] for x in pred_y])
		print ("test AUC: %s"%(AUC_score))
		
		AUC_list.append(AUC_score)
		fpr, tpr, thresholds = roc_curve(y_test.tolist(),[x[1] for x in pred_y])
		roc_x += list(fpr)
		roc_y += list(tpr)	
		
	df = pd.DataFrame()
	df['true']=my_true
	df['pred']=my_pred
	df2 = pd.DataFrame()
	df2['x']=roc_x
	df2['y']=roc_y
	print ("mean AUC: %s, std: %s"%(np.mean(AUC_list),np.std(AUC_list)))
	return df,df2,AUC_list
	
def xgb_clf(par=False):
	est = XGBClassifier(n_estimators=1000,seed=0)
	if par:
		est = XGBClassifier(**par)
	myDict = {}
	myDict['max_depth']= [5] ## maximum tree depth
	myDict['booster']= ["gblinear"] ## maximum tree depth
	myDict['subsample']=[0.5] ## proportion of training instances used in trees
	myDict['colsample_bytree']= [0.5] ## subsample ratio of columns
	myDict['eta']= [0.01]  ## learning rate
	myDict['gamma']= [0]  ## minimum loss function reduction required for a split
	myDict['min_samples_leaf']= [1]  ## minimum loss function reduction required for a split
	myDict['min_child_samples']= [2]  ## minimum loss function reduction required for a split
	myDict['min_split_gain'] = [0]
	myDict['num_leaves']= [15]
	return est, myDict	
def sklearn_GBT(par=False):
	est = GradientBoostingClassifier(n_estimators=100,random_state=0)
	if par:
		est = GradientBoostingClassifier(**par)
	myDict = {}
	myDict['loss']=['deviance']
	myDict['learning_rate']=[0.05,0.01,0.1]
	myDict['max_depth']=[30,10,5]
	myDict['subsample']=[0.8,0.5,1]
	myDict['min_samples_leaf']=[1,5,9]
	myDict['min_impurity_decrease']=[0,0.05,0.1,0.2]
	return est, myDict

def sklearn_RidgeClassifier(par=False):
	est = RidgeClassifier()
	if par:
		est = RidgeClassifier(**par)
	myDict = {}
	myDict['alpha']=[0.01,0.1,0.5,1,3,5,10]
	return est, myDict
def sklearn_LogisticRegression(par=False):
	est = LogisticRegression()
	if par:
		est = LogisticRegression(**par)
	myDict = {}
	myDict['penalty']=["l1","l2"]
	# myDict['dual']=[True, False]
	myDict['C']=[0.1,1,10]
	
	return est, myDict


def sklearn_RF(par=False):
	print (sys._getframe().f_code.co_name)
	# print (__name__)
	est = RandomForestClassifier(n_estimators=500,random_state=0)
	if par:
		est = RandomForestClassifier(**par)
	myDict = {}
	myDict['max_depth']=[10,30]
	# myDict['criterion']=['gini','entropy'] 
	# myDict['max_features']=['sqrt',None] 
	myDict['min_samples_leaf']=[1, 5] 
	# myDict['min_samples_split']=[2,8,14,20] 
	# myDict['min_weight_fraction_leaf']=[0,0.001,0.01,0.1] 
	# myDict['min_impurity_decrease']=[0,0.05,0.1,0.2]    
	# myDict['warm_start']=[True,False]    
	return est, myDict

def KNN_clf(par=False):
	est = KNeighborsClassifier(n_neighbors=3)
	if par:
		est = RandomForestClassifier(**par)
	myDict = {}
	myDict['max_depth']=[30]
	myDict['min_samples_leaf']=[1,3] 
	myDict['max_features']=["sqrt"]
	myDict['min_impurity_decrease']=[0,0.1]    
	return est, myDict	

def linear_stacking_clf():
	RANDOM_SEED=0
	clf1 = KNeighborsClassifier()
	clf2 = RandomForestClassifier(random_state=RANDOM_SEED,max_depth=30,n_estimators=100)
	clf3 = GaussianNB()
	clf4 = RidgeClassifier()
	clf5 = SGDClassifier()
	clf6 = GaussianProcessClassifier()
	# clf7 = RadiusNeighborsClassifier(outlier_label =-1)
	clf8 = GradientBoostingClassifier()
	lr = LogisticRegression()
	linearSVM = LinearSVC()
	# params = {'kneighborsclassifier__n_neighbors': [10, 5],
			# 'radiusneighborsclassifier__radius': [10,20],
			# 'gradientboostingclassifier__learning_rate': [0.1,0.8],
			# 'meta_classifier__C': [0.01,0.1,1,10],
			# 'logisticregression__C': [1,10.0]}
	params = {'kneighborsclassifier__n_neighbors': [10, 5],
			'gradientboostingclassifier__learning_rate': [0.1,0.8],
			'linearsvc__C': [0.01,0.1,1,10],
			'meta_classifier__max_depth': [20,30,50],
			'meta_classifier__min_samples_leaf': [1,5],
			'meta_classifier__min_impurity_decrease': [0,0.1],
			'logisticregression__C': [1,10.0]}
	# sclf = StackingCVClassifier(classifiers=[clf1, clf2, clf3,clf4,clf5,clf6,clf7,clf8,lr], 
	sclf = StackingCVClassifier(classifiers=[clf1,linearSVM, clf3,clf4,clf5,clf6,clf8,lr], 
							meta_classifier=clf2,use_features_in_secondary=False,
							random_state=RANDOM_SEED)
	# grid = GridSearchCV(sclf,params,n_jobs=-1,cv=3,verbose=1,refit=True,scoring="roc_auc")

	# grid.fit(X.values,y.values)
	
	# print("Best: %f using %s" % (grid.best_score_, grid.best_params_))
	# best_model = grid.best_estimator_ 
	
	return sclf,params

def plot_top_features(reg,X,y,output):
	
	current_feature_df = pd.DataFrame()
	current_feature_df['features'] = X.columns.tolist()

	reg.fit(X,y)
	try:
		current_feature_df['score'] = list(reg.feature_importances_) 
	except:
		try:
			current_feature_df['score'] = list(reg.coef_) 
		except:
			current_feature_df['score'] = list(reg.coef_[0]) 
				
	current_feature_df = current_feature_df.sort_values('score',ascending=False)
	

	plt.figure()
	sns.barplot(x=current_feature_df['features'],y=current_feature_df['score'] )
	plt.xticks(rotation=90)
	plt.xlabel("")
	plt.ylabel("Feature importance")
	plt.savefig("%s_feature_importance.pdf"%(output), bbox_inches='tight')	
	
	
def general_df_reader(args):
	if args.header:
		if args.index:
			df = pd.read_csv(args.input,sep=args.sep,index_col=0)
		else:
			df = pd.read_csv(args.input,sep=args.sep)
	else:
		if args.index:
			df = pd.read_csv(args.input,sep=args.sep,index_col=0,header=None)
		else:
			df = pd.read_csv(args.input,sep=args.sep,header=None)
	return df

def plot_ROC(output):
	plt.figure()
	plot_df = pd.read_csv("%s_prediction.csv"%(output))
	score = roc_auc_score(plot_df['true'],plot_df['pred'])
	print ("AUC:%s"%(score))	
	x_predict2,y_predict2,_ = roc_curve(plot_df['true'],plot_df['pred'])
	plt.plot([0, 1], [0, 1], 'k--')
	plt.plot(x_predict2, y_predict2, label='My Model: %s'%(score))
	plt.xlabel('False positive rate')
	plt.ylabel('True positive rate')
	plt.title('ROC curve')
	plt.legend(loc='best')
	plt.savefig("%s_correlation_plot.pdf"%(output), bbox_inches='tight')
	
def plot_correlation(output):

	plot_df = pd.read_csv("%s_prediction.csv"%(output))
	plt.figure()
	sns.regplot(x=plot_df['true'],y=plot_df['pred'],x_bins =20)
	r,p = scipy.stats.pearsonr(plot_df["pred"],plot_df["true"])
	plt.xlabel("True value")
	plt.ylabel("Predicted value")
	plt.text(plot_df['true'].quantile(.05), plot_df['pred'].quantile(.85), 'r=%f'%(r))
	plt.text(plot_df['true'].quantile(.05), plot_df['pred'].quantile(.8), 'p=%.2E'%(Decimal(p)))

	plt.savefig("%s_correlation_plot.pdf"%(output), bbox_inches='tight')
	plt.close()
	
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--input",  help="input data frame", required=True)
	mainParser.add_argument('-s',"--sep",  help="separator",default="\t")
	mainParser.add_argument('--index',  help=" index is true", action='store_true')
	mainParser.add_argument('--header',  help=" header is true", action='store_true')
	mainParser.add_argument('--ignore_cols', default="None")
	mainParser.add_argument('--only_cols', default="None")
	
	mainParser.add_argument('--target',  help="target column name, if no header, use column order, start from 0",required=True)
	mainParser.add_argument('-o','--output',  help="output file name prefix",default="classification_test_output")


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	df = general_df_reader(args)
	X = df.drop([args.target],axis=1)
	if args.ignore_cols != "None":
		ignore = []
		for i in X.columns:
			if args.ignore_cols in i:
				ignore.append(i)
		X = X.drop(ignore,axis=1)
	if args.only_cols != "None":
		only = []
		for i in X.columns:
			if args.only_cols in i:
				only.append(i)
		X = X[only]		
	y = df[args.target]
	print ("Input feature size: %s"%(X.shape[1]))
	# print ("sklearn_GBT")
	# model,params=sklearn_GBT()
	# model,params=xgb_clf()
	model,params=sklearn_RF()
	# model,params=sklearn_LogisticRegression()
	# model,params=linear_stacking_clf()
	# exit()
	# with warnings.catch_warnings():
		# warnings.simplefilter("ignore")
	ddf,df2,AUC_list = nested_cv_evaluation(model,params,X,y)
	ddf.to_csv("%s_prediction.csv"%(args.output),index=False)
	
	plot_top_features(dp(model),X,y,args.output)
	plot_ROC(args.output)
	

if __name__ == "__main__":
	main()



		
		
		