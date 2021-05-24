#!/hpcf/apps/python/install/2.7.13/bin/python
import os
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
try:
	import paramiko
except:
	pass
import pickle
import getpass
import sys
import uuid
import glob
import subprocess
import re
import datetime
import time
from difflib import SequenceMatcher
import pandas as pd
import argparse
import logging
import Colorer
import numpy as np
from copy import deepcopy as dp
from os.path import isfile,isdir
from Bio.Seq import Seq
from Bio import SeqIO
import itertools
import string
"""Main utils to import

Single Responsibility Principle
-------------------------------

module listed below are used by other xxx_utils.py

however, individual xxx_utils.py only has dependencies on utils.py.

This is trying to organize utils while avoiding circular dependencies.

Note
----

I believe only paramiko depends on python/2.7.13.

So except that, any python2 should work.

In case of HPC changes, one might want to change shebang to other python versions


6-11 replace print with logging.info

"""
def revcomp(seq):
	try: ## python2
		tab = string.maketrans(b"ACTG", b"TGAC")
	except:  ## python3
		tab = bytes.maketrans(b"ACTG", b"TGAC")
	return seq.translate(tab)[::-1]


def guess_label(names):
	lines = []
	for i in names:
		
		for j in names:
			if j == i:
				continue
			current = [i,j]
			current+=longestSubstringFinder(i,j)
			lines.append(current)
	df = pd.DataFrame(lines)
	# print (df)
	df = df.sort_values(3,ascending=False)
	df = df.drop_duplicates(0)
	return df[3].tolist()
def longestSubstringFinder(string1, string2):
	answers = {}
	s1 = re.split("\.|_|-",string1)
	s2 = re.split("\.|_|-",string2)
	flag = False
	count = 0
	
	for i in range(len(s1)):
		try:
			if not count in answers:
				answers[count] = []
			if s1[i] == s2[i]:
				answers[count].append(s1[i])
			else:
				count += 1
		except:
			break
	for k in answers:
		answers[k] = "_".join(answers[k])
	df = pd.DataFrame.from_dict(answers,orient="index")
	# print (df)
	df['len'] = [len(x.split("_")) for x in df[0]]
	df = df.sort_values("len",ascending=False)
	
	return [df[0].tolist()[0],df['len'].tolist()[0]]



def toBed4(input,output):
	
	command = """awk -F "\t" '{print $1"\t"$2"\t"$3"\t"$1":"$2"-"$3}' %s > %s"""%(input,output)
	os.system(command)
	
def guess_sep(x):
	with open(x) as f:
		for line in f:
			tmp1 = len(line.strip().split(","))
			tmp2 = len(line.strip().split("\t"))
			# print (tmp1,tmp2)
			if tmp1 > tmp2:
				return ","
			if tmp2 > tmp1: 
				return "\t"
			else:
				print ("Can't determine the separator. Please input manually")
				exit()
				
def dos2unix(file):
	os.system("dos2unix -q "+file)

def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		if myDict[k] == None:
			value = ""
		else:
			value = myDict[k]
		myString = str(myString).replace("{{"+str(k)+"}}",str(value))
	return myString

def get_number_lines(x):
	count = 0
	if not isfile(x):
		logging.error("%s not found"%(x))
	with open(x) as f:
		for line in f:
			line = line.strip().split()
			if line == []:
				continue
			if len(line)>=1 or len(line[0]) >= 1:
				count += 1
	return count
	
def read_file_to_list(x):
	myList = []
	with open(x) as f:
		for line in f:
			line = line.strip()
			if len(line)>1:
				myList.append(line)
	return myList

def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()




def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

def write_fasta(file_name,myDict):
	out = open(file_name,"wt")
	for k in myDict:
		out.write(">"+k+"\n")
		out.write(myDict[k]+"\n")
	out.close()
def read_fasta(f):
	my_dict = {}
	for r in SeqIO.parse(f, "fasta"):
		my_dict[r.id] = str(r.seq).upper()
	return my_dict	
	
def setup_custom_logger(jid):
	logFormatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
	rootLogger = logging.getLogger("root")
	fileHandler = logging.FileHandler(jid+".log")
	fileHandler.setFormatter(logFormatter)
	rootLogger.addHandler(fileHandler)
	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	rootLogger.addHandler(consoleHandler)
	rootLogger.setLevel(logging.INFO)
	return rootLogger
def send_user_command(username,subject):
	message = "Your Job has been submitted. The jobID is: %s. \n\n Your command is : %s. "%(subject," ".join(sys.argv))
	command = ' echo "{{message}}" | mailx -s "{{subject}}" -- User_name@stjude.org '
	command = command.replace("{{message}}",message+"\n\nYour job work directory is:\n"+os.getcwd())
	command = command.replace("{{subject}}",subject)
	command = command.replace("User_name",username)
	command2 = 'attr -s command -V "%s" %s > /dev/null 2>&1'%(" ".join(sys.argv),subject)
	# print (command2)
	os.system(command2)
	if "no_email" in subject:
		return 1
	os.system(command)


from input_utils import *
from lsf_utils import *
from protein_paint_tracks import *








p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
username = getpass.getuser()
myData = parse_config(p_dir+"../config/data.config")
myPars = parse_config(p_dir+"../config/parameters.config")
myPipelines = parse_config(p_dir+"../config/pipeline.config")






