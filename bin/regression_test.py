#!/home/yli11/.conda/envs/py2/bin/python




"""

This code is specifically design to do an evaluation, although the general utils can be used any where else.




"""
import argparse
import matplotlib
matplotlib.use('agg')
import seaborn as sns
import matplotlib.pyplot as plt

from copy import deepcopy as dp
from sklearn.model_selection import KFold
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics.scorer import make_scorer
from sklearn.model_selection import train_test_split
from sklearn.base import TransformerMixin
from sklearn.datasets import make_regression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
import pandas as pd
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
from mlxtend.regressor import StackingCVRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge,Lars,BayesianRidge
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


def MAE_grid(estimator,parameterDict,X,y):
    myModel = GridSearchCV(estimator,parameterDict,scoring="neg_mean_absolute_error",cv=3,verbose=0,n_jobs=10,refit=True)
    myModel.fit(X,y)
    return myModel


def sklearn_GBT_reg(par=False):
	est = GradientBoostingRegressor(n_estimators=100)
	if par:
		est = GradientBoostingRegressor(**par)
	myDict = {}
	myDict['loss']=['ls','lad']
	myDict['learning_rate']=[0.05,0.1]
	myDict['max_depth']=[5,8]
	return est, myDict

def sklearn_RF_reg(par=False):
	est = RandomForestRegressor(n_estimators=300)
	if par:
		est = RandomForestRegressor(**par)
	myDict = {}
	myDict['min_samples_split']=[2,3,5]
	myDict['min_samples_leaf']=[1,2,3]
	myDict['max_depth']=[3,5,7,10]
	myDict['criterion']=['mse','mae']
	return est, myDict
	
	
def xgb_reg(par=False):
	est = XGBRegressor(n_estimators=300,objective="reg:squarederror")
	if par:
		est = XGBRegressor(**par)
	myDict = {}
	myDict['learning_rate']=[0.01,0.05,0.1]
	myDict['max_depth']=[3,5,7]
	myDict['gamma']=[0,0.1,0.5]
	return est, myDict

def ridge_reg(par=False):
	est = Ridge()
	if par:
		est = Ridge(**par)	
	myDict = {}
	myDict['alpha']=[0.1,0.5,1,2]
	return est, myDict
def lasso_reg(par=False):
	est = Lasso()
	if par:
		est = Lasso(**par)	
	myDict = {}
	myDict['alpha']=[0.1,0.5,1,2]
	return est, myDict
def Lars_reg(par=False):
	est = Lars()
	if par:
		est = Lars(**par)	
	myDict = {}
	myDict['n_nonzero_coefs']=[1,5,10,50,100,200,300]
	return est, myDict
def BayesianRidge_reg(par=False):
	est = BayesianRidge()
	if par:
		est = BayesianRidge(**par)	
	myDict = {}
	myDict['alpha_1']=[1e-10,1e-5,1e-3,0.1]
	myDict['alpha_2']=[1e-10,1e-5,1e-3,0.1]
	myDict['lambda_1']=[1e-10,1e-5,1e-3,0.1]
	myDict['lambda_2']=[1e-10,1e-5,1e-3,0.1]
	return est, myDict
def KernelRidge_reg(par=False):
	## dual_coef_ is not working
	est = KernelRidge()
	if par:
		est = KernelRidge(**par)	
	myDict = {}
	myDict['alpha']=[1e-5,1e-3,0.1,0.5,1,2]
	myDict['gamma']=[1e-5,1e-3,0.1,0.5,1,2]
	myDict['kernel']=['linear','rbf']

	return est, myDict
def SVM_reg(par=False):
	est = SVR(kernel="linear")
	if par:
		est = SVR(**par)	
	myDict = {}
	myDict['C']=[1e-5,1e-3,0.1,0.5,1,2,10,100]
	myDict['gamma']=[1e-5,1e-3,0.1,0.5,1,2]
	myDict['kernel']=['linear']

	return est, myDict

def linear_stacking_reg(X,y):
	RANDOM_SEED=0
	reg1,dict1 = SVM_reg()
	reg2,dict2 = sklearn_GBT_reg()
	reg3,dict3 = xgb_reg()
	reg4,dict4 = ridge_reg()
	reg5,dict5 = lasso_reg()
	reg6,dict6 = Lars_reg()
	reg7,dict7 = KNeighborsRegressor_reg()
	reg8,dict8 = sklearn_RF_reg()
	reg9,dict9 = KernelRidge_reg()
	reg10,dict10 = BayesianRidge_reg()
	params ={}
	my_dict_list = [dict1,dict2,dict3,dict4,dict5,dict6,dict7,dict8,dict9,dict10]
	name_list = ["svr","gradientboostingregressor","xgbregressor",
				"ridge","lasso","lars","kneighborsregressor","randomforestregressor",
				"kernelridge","meta_regressor"]
	for i in range(len(my_dict_list)):
		current_dict = my_dict_list[i]
		for xx in current_dict:
			if i == 9:
				continue
			params['%s__%s'%(name_list[i],xx)]=current_dict[xx]
	linear_stacker = StackingCVRegressor(regressors=(reg1,reg2,reg3,reg4,reg5,reg6,reg7,reg8,reg9),
					meta_regressor=reg10,use_features_in_secondary=True)

	grid = RandomizedSearchCV(linear_stacker,params,n_iter=10,n_jobs=10,scoring="neg_mean_absolute_error",cv=3,verbose=1)

	grid.fit(X.values,y)
	
	print("Best: %f using %s" % (grid.best_score_, grid.best_params_))
	best_model = grid.best_estimator_ 
	
	return best_model
	
	

def KNeighborsRegressor_reg(par=False):
	est = KNeighborsRegressor()
	if par:
		est = KNeighborsRegressor(**par)	
	myDict = {}
	myDict['n_neighbors']=[1,2,3,5,10,20]
	myDict['leaf_size']=[1,5,10,20]
	myDict['p']=[1,2]
	myDict['weights']=['uniform','distance']

	return est, myDict
											
def recursive_feature_elimination_reg(reg,X,y):
	features = X.columns
	score_list = []
	my_feature_score_df = pd.DataFrame()
	feature_list = []
	for i in range(len(features-1)):
		X = X[features]
		feature_list.append(features)
		current_feature_df = pd.DataFrame()
		current_feature_df['features'] = features
		# print (current_feature_df.shape)
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
		reg.fit(X_train,y_train)
		y_pred = reg.predict(X_test)
		MAE_score = mean_absolute_error(y_test, y_pred)
		score_list.append(MAE_score)
		# print (i,MAE_score)
		# print (len(reg.feature_importances_ ))
		try:
			current_feature_df['score'] = list(reg.feature_importances_) 
		except:
			try:
				current_feature_df['score'] = list(reg.coef_) 
			except:
				# print (reg.coef_[0])
				# current_feature_df['score'] = list(reg.dual_coef_) 
				current_feature_df['score'] = list(reg.coef_[0]) 
				
		current_feature_df = current_feature_df.sort_values('score')
		current_feature_df = current_feature_df.reset_index(drop=True)
		current_feature_df = current_feature_df.drop(0)
		features = current_feature_df['features'].tolist()
	my_feature_score_df['score'] = 	score_list
	my_feature_score_df['features'] = 	feature_list
	my_feature_score_df = my_feature_score_df.sort_values('score')
	best_MAE = my_feature_score_df['score'].tolist()[0]
	best_featureSet = my_feature_score_df['features'].tolist()[0]
	print ("Best MAE is %s, using %s features"%(best_MAE,len(best_featureSet)))
	return best_featureSet



def loo_reg(reg,X,y):
	my_pred = []
	my_true = []   
	index_list = []
	for i in X.index:
		print (i)
		train_X = X.drop([i])
		train_y = y.drop([i])
		test_X = pd.DataFrame(X.loc[i]).T
		test_y = y.loc[i]
		reg.fit(train_X.values,train_y)
		pred_y = reg.predict(test_X.values)
		my_pred.append(pred_y[0])
		my_true.append(test_y)
		# print (pred_y,test_y)
		index_list.append(i)
	return my_true,my_pred,index_list

def get_top_features(reg,X,y,top_n):

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
	
def nested_cv_evaluation(model,params,X,y):
	"""
	X,y are np array
	
	"""
	outer = KFold(n_splits=10)
	my_pred=[]
	my_true=[]
	for train_index, test_index in outer.split(X):
		X_train, X_test = X.iloc[train_index], X.iloc[test_index]
		y_train, y_test = y.iloc[train_index], y.iloc[test_index]
		# print (X_train.head())
		# print (y_train.head())
		
		best_model=""
		best_score = -9999999999
		best_features =""
		for top_n in [5,10,20]:
			## feature selection
			top_features = get_top_features(dp(model),X_train,y_train,top_n)
			# top_features = X.columns.tolist()
			## parameter selection
			current_model = MAE_grid(dp(model),params,X_train[top_features].values,y_train)	
			print (top_n,current_model.best_params_ )
			if current_model.best_score_ > best_score:
				best_score = current_model.best_score_
				best_model = current_model
				best_features=top_features
		## current best model		
		print ("Best features:%s"%(",".join(best_features)))
		pred_y = best_model.predict(X_test[best_features].values)
		# print (pred_y)
		my_pred += list(pred_y)
		my_true += y_test.tolist()
		print (len(pred_y))
		print (len(y_test.tolist()))
	rho,p = scipy.stats.pearsonr(my_true,my_pred)
	print ("PCC: %s, %s"%(rho,p))
	rho,p = scipy.stats.spearmanr(my_true,my_pred)
	print ("SCC: %s, %s"%(rho,p))	
	df = pd.DataFrame()
	df['true']=my_true
	df['pred']=my_pred
	return df
	
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
from decimal import Decimal
import pandas as pd
import seaborn as sns
import scipy
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
	
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--input",  help="input data frame", required=True)
	mainParser.add_argument('-s',"--sep",  help="separator",default="\t")
	mainParser.add_argument('--index',  help=" index is true", action='store_true')
	mainParser.add_argument('--header',  help=" header is true", action='store_true')
	mainParser.add_argument('--target',  help="target column name, if no header, use column order, start from 0",required=True)
	mainParser.add_argument('-o','--output',  help="output file name prefix",default="regression_test_output")


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	df = general_df_reader(args)
	X = df.drop([args.target],axis=1)
	y = df[args.target]

	print ("sklearn_GBT")
	model,params=sklearn_GBT_reg()
	df = nested_cv_evaluation(model,params,X,y)
	df.to_csv("%s_prediction.csv"%(args.output),index=False)
	
	
	plot_top_features(dp(model),X,y,args.output)
	plot_correlation(args.output)
	

if __name__ == "__main__":
	main()



		





