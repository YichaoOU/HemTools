#!/usr/bin/env python

import numpy as np
import pandas as pd
import h5py
import os
import torch
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler, BatchSampler
from scipy import stats
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
import numpy as np
import scipy.stats as sts
import gzip as gz
import pysam
import pandas as pd
import numpy as np
import scipy
import glob
from joblib import Parallel, delayed
import sys
import argparse
import os
import swifter
import sys
from Levenshtein import distance
pd.options.display.max_columns = 100
pd.options.display.max_rows = 100
def wm_prediction(on_target,off_target,MODEL_PATH):
	import numpy as np
	import pandas as pd
	import matplotlib.pyplot as plt
	import seaborn as sns
	import h5py
	import os
	import torch
	from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler, BatchSampler
	from scipy import stats
	import torch.nn as nn
	import torch.nn.functional as F
	import torch.optim as optim
	# MODEL_PATH = '/research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/projects/GUIDEseq/02172023_GUIDEseq2_GV_Novaseq/ML/all_large_5_11062024_ollision_Avoidance_cutadaptv2_1mM_rep1_6layer_128_3linear.pth'
	BATCH_SIZE = 8192
	NUM_EPOCHS = 300
	def get_free_gpu():
		os.system('nvidia-smi -q -d Memory |grep -A5 GPU|grep Free > ./tmp')
		memory_available = [int(x.split()[2]) for x in open('tmp', 'r').readlines()]
		return int(np.argmax(memory_available))

	# id = get_free_gpu()
	# device = torch.device("cuda:%d" % id) 
	device = 'cpu'

	class CNN(nn.Module):
		def __init__(self):
			super().__init__()
			self.layers = nn.ModuleList()
			dropout = 0.2
			hidden_dim = 128
			
			self.seq_length = 23
			self.layers.append(nn.Conv1d(in_channels = 8, out_channels = hidden_dim, kernel_size = 3, padding = 1))
			self.layers.append(nn.BatchNorm1d(hidden_dim, track_running_stats = True))
			self.layers.append(nn.LeakyReLU())
			self.layers.append(nn.Dropout(dropout))

			self.layers.append(nn.Conv1d(in_channels = hidden_dim, out_channels = hidden_dim, kernel_size = 3, padding = 1))
			self.layers.append(nn.BatchNorm1d(hidden_dim, track_running_stats = True))
			self.layers.append(nn.LeakyReLU())
			self.layers.append(nn.Dropout(dropout))
			
			self.layers.append(nn.Conv1d(in_channels = hidden_dim, out_channels = hidden_dim, kernel_size = 3, padding = 1))
			self.layers.append(nn.BatchNorm1d(hidden_dim, track_running_stats = True))
			self.layers.append(nn.LeakyReLU())
			self.layers.append(nn.Dropout(dropout))
			
			self.layers.append(nn.Conv1d(in_channels = hidden_dim, out_channels = hidden_dim, kernel_size = 5, padding = 2))
			self.layers.append(nn.BatchNorm1d(hidden_dim, track_running_stats = True))
			self.layers.append(nn.LeakyReLU())
			self.layers.append(nn.Dropout(dropout))
			
			self.layers.append(nn.Conv1d(in_channels = hidden_dim, out_channels = hidden_dim, kernel_size = 5, padding = 2))
			self.layers.append(nn.BatchNorm1d(hidden_dim, track_running_stats = True))
			self.layers.append(nn.LeakyReLU())
			self.layers.append(nn.Dropout(dropout))
			
			self.layers.append(nn.Conv1d(in_channels = hidden_dim, out_channels = 10, kernel_size = 5, padding = 2))
			self.layers.append(nn.BatchNorm1d(10, track_running_stats = True))
			self.layers.append(nn.LeakyReLU())
			self.layers.append(nn.Dropout(dropout))
			
			self.layers.append(nn.Flatten())
			
			self.layers.append(nn.Linear(self.seq_length * 10, 128))
			self.layers.append(nn.LeakyReLU())
			self.layers.append(nn.Linear(128, 32))
			self.layers.append(nn.LeakyReLU())
			self.layers.append(nn.Linear(32, 1))
			
			

		def forward(self, x):
			out = x
			for layer in self.layers:
				out = layer(out)
			return out
			
	model = CNN()
	checkpoint = torch.load(MODEL_PATH,  map_location=torch.device('cpu'))
	model.load_state_dict(checkpoint['model_state_dict'])
	model.to(device)
	model.eval()
	def genome_onehot_encoding_pair_with_genotype(ref, genotype):
		ref = list(ref.upper())
		genotype = genotype.upper()
		D = {'A': [1,0,0,0], 'C': [0,1,0,0], 'G': [0,0,1,0], 'T': [0,0,0,1], 'N': [1/4,1/4,1/4,1/4], '-': [0,0,0,0]}
		mat1 = np.array([D[i] for i in ref])
		haplotype = genotype.split('_')
		if len(haplotype) == 1:
			if len(haplotype[0]) != 23:
				return None
			mat2 = np.array([D[i] for i in haplotype[0]])
		else:
			if len(haplotype[0]) != 23 or len(haplotype[1]) != 23:
				return None
			mat2_1 = np.array([D[i] for i in haplotype[0]])
			mat2_2 = np.array([D[i] for i in haplotype[1]])
			mat2 = (mat2_1 + mat2_2) / 2
		return np.hstack((mat1, mat2)).astype(float)

	seq_list=[on_target,off_target]
	X = np.array([genome_onehot_encoding_pair_with_genotype(on_target, seq_list[i]) for i in range(len(seq_list))])
	X = torch.tensor(X, dtype = torch.float32).to(device)
	X = torch.transpose(X, 1, 2)
	preds = model(X).cpu().detach().numpy().reshape(-1)
	on,off = preds
	return 2**off-1

MODEL_PATH = f'/research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/projects/GUIDEseq/02172023_GUIDEseq2_GV_Novaseq/ML/all_large_training_log21p_activity_05272025_NGG_filtering5_6layer_128_3linear.pth'
# on_target="GTCCCCTGAGCCCATTTCCTNGG"
# ref="GTCACCTGAACCCATTTCCTATG"
# var="GTCACCTGAACCCATTTCCTAGG"
# print (f"NEW model REF: {wm_prediction2(on_target, ref, MODEL_PATH)}")
# print (f"NEW model ALT: {wm_prediction2(on_target, var, MODEL_PATH)}")

import sys
input=sys.argv[1]
on_target=int(sys.argv[2])
off_target=int(sys.argv[3])

df = pd.read_csv(input,sep="\t",header=None)
df[on_target] = df[on_target].str.upper()
df[off_target] = df[off_target].str.upper()

def get_wm_score(r,on_target,off_target,MODEL_PATH):
	return wm_prediction(r[on_target], r[off_target], MODEL_PATH)
df['changenet'] = df.apply(lambda r: get_wm_score(r,on_target,off_target,MODEL_PATH),axis=1)
df.to_csv(f"{input}.changenet.tsv",sep="\t",header=False,index=False)
