#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold,StratifiedKFold
import matplotlib
matplotlib.use('agg')
from sklearn.metrics import roc_curve,roc_auc_score
import matplotlib.pyplot as plt


"""
module load gcc/6.3.0

nested CV on gkmSVM, for baseline comparison


"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument('-p','--pos_fa',  required=True)
	mainParser.add_argument('-n','--neg_fa',  required=True)
	mainParser.add_argument('-cv',  required=True,type=int)
	
	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def get_train_test_data(pos,neg,train_index,test_index):
	addon_string = str(uuid.uuid4()).split("-")[-1]
	pos_train_file = addon_string+"_pos_train_file.fa"
	neg_train_file = addon_string+"_neg_train_file.fa"
	pos_test_file = addon_string+"_pos_test_file.fa"
	neg_test_file = addon_string+"_neg_test_file.fa"


	write_fasta(pos_train_file,{k:v for k,v in pos.items() if k in train_index})
	write_fasta(pos_test_file,{k:v for k,v in pos.items() if k in test_index})
	write_fasta(neg_train_file,{k:v for k,v in neg.items() if k in train_index})
	write_fasta(neg_test_file,{k:v for k,v in neg.items() if k in test_index})

	
	
	return pos_train_file,neg_train_file,pos_test_file,neg_test_file,addon_string

def to_true_label(pos,neg):
	pos_fasta = read_fasta(pos)
	neg_fasta = read_fasta(neg)
	df = pd.DataFrame()
	df['true'] = [1]*len(pos_fasta.keys())+[-1]*len(neg_fasta.keys())
	df.index = pos_fasta.keys()+neg_fasta.keys()
	return df

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
	

def gkm_SVM_grid_search(pos_train_file,neg_train_file,scoring="roc_auc"):
	max_score = -999999
	best_d = -1
	#### have to be a maximization process
	pos_fasta = read_fasta(pos_train_file)
	neg_fasta = read_fasta(neg_train_file)
	Y = [1]*len(pos_fasta.keys())+[-1]*len(neg_fasta.keys())
	X = pos_fasta.keys()+neg_fasta.keys()
	
	"""
	>>> a=["asd","awse","dg","dt"]
	>>> b=[1,1,0,0]
	>>> train_test_split(a,b)
	[['awse', 'dt', 'asd'], ['dg'], [1, 0, 1], [0]]
	
	"""
	
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
	pos_train_file,neg_train_file,pos_test_file,neg_test_file,addon_string = get_train_test_data(pos_fasta,neg_fasta,X_train,X_test)
	for d in [1,2,3,4]:
		df = gkm_SVM_fit_transform(pos_train_file,neg_train_file,pos_test_file,neg_test_file,d)
		score = roc_auc_score(df['true'],df['pred'])
		if score > max_score:
			max_score = score
			best_d = d
	print ("best_d : %s. best score: %s"%(best_d,max_score))
	os.system("rm %s*"%(addon_string))
	return best_d

def plot_ROC(plot_df):
	plt.figure()
	score = roc_auc_score(plot_df['true'],plot_df['pred'])
	print ("AUC:%s"%(score))
	x_predict2,y_predict2,_ = roc_curve(plot_df['true'],plot_df['pred'])
	plt.plot([0, 1], [0, 1], 'k--')
	plt.plot(x_predict2, y_predict2, label='gkmSVM: %s'%(score))
	plt.xlabel('False positive rate')
	plt.ylabel('True positive rate')
	plt.title('ROC curve')
	plt.legend(loc='best')
	plt.savefig("gkmSVM_ROC_plot.pdf", bbox_inches='tight')

def main():

	args = my_args()
	## all the data
	pos_fasta = read_fasta(args.pos_fa)
	neg_fasta = read_fasta(args.neg_fa)
	
	## split data for CV
	outer = StratifiedKFold(n_splits=args.cv,random_state=0)
	X = pos_fasta.keys()+neg_fasta.keys()
	y = [1]*len(pos_fasta.keys())+[-1]*len(neg_fasta.keys())
	
	## evaluation df
	score_df_list = []
	
	## nested CV
	for train_index, test_index in outer.split(X,y):
		
		## step 1 create training testing files
		pos_train_file,neg_train_file,pos_test_file,neg_test_file,addon_string = get_train_test_data(pos_fasta,neg_fasta,[X[i] for i in train_index],[X[i] for i in test_index])

		## inner loop
		best_d = gkm_SVM_grid_search(pos_train_file,neg_train_file,scoring="roc_auc")
		
		## outer loop test
		score_df = gkm_SVM_fit_transform(pos_train_file,neg_train_file,pos_test_file,neg_test_file,best_d)
		score_df_list.append(score_df)
		os.system("rm %s*"%(addon_string))
		
	plot_df = pd.concat(score_df_list)
	print (plot_df.shape)
	print (plot_df.head())
	plot_df.to_csv("gkmSVM_ncv_prediction.csv")
	plot_ROC(plot_df)
	# return df
	

	
if __name__ == "__main__":
	main()

























