#!/hpcf/apps/python/install/2.7.13/bin/python
from utils import *


def parse_config(x):
	myDict = {}
	with open(x) as f:
		for line in f:
			line = line.strip()
			if len(line) < 2:
				continue
			if line[0] == "#":
				continue
			line = line.split()
			## make sure it is case-insensitive
			myDict[line[0].lower()] = line[1]
			myDict[line[0]] = line[1]
	return myDict

def fastq_pair(x,y):
	length_difference = len(x)-len(y)
	# print x
	# print y
	item_differences = 0
	paired_flag = 0
	if length_difference!= 0:
		return 0
	for i in range(len(x)):
		item_x = x[i]
		item_y = y[i]
		# print item_x,item_y
		if item_x!=item_y:
			item_differences+=1
			if item_x == "R1" and item_y == "R2":
				paired_flag = 1
			if item_y == "R1" and item_x == "R2":
				paired_flag = 1
	# print "item_differences",item_differences
	# print "paired_flag",paired_flag
	if item_differences == 1 and paired_flag == 1:
		return 1
	else:
		return 0
def define_fastq_label(x):
	label = []
	for i in re.split('_|-|\.',x):
		if i.lower() in ['fastq','gz','bed']:
			continue
		if i == "R1" or i == "R2":
			return "_".join(label)
		label.append(i)
	return "_".join(label)



def prepare_paired_end_input():
	
	# observation:
	# 1. seperators are: - _ .
	# 2. the first element is often times unique for each sample
	# 	- 1631306_RFA001_R1.fastq.gz
	# 	- 110C-GATA1_S10_R1.fastq.gz
	# 	- 1047946_Hudep1_CTCFIP_R1.fastq.gz
	# 3. paired-end data, the only difference is R1 and R2
	# 	- all other items are the same 
	# 	- also, after spliting the seperators, the length of the array should be the same
	# logic: 
	# 1. split the string
	# 2. infer putative pairs
	# 	rules:
	# 		- length is the same 
	# 		- only difference is R1 and R2


	tmp_files = glob.glob("*.fastq.gz")+glob.glob("*.fastq")
	files = []
	for f in tmp_files:
		if "undetermined" in f.lower():
			continue
		files.append(f)
	files_array = map(lambda x:re.split('_|-|\.',x),files)
	myDict = {}
	
	for i in range(len(files_array)):
		myDict[files[i]] = []
		for j in range(len(files_array)):
			if fastq_pair(files_array[i],files_array[j]):
				myDict[files[i]].append(files[j])
	flag = False
	fname = "fastq.tsv"
	if isfile(fname):
		logging.warning(fname+" exists!")
		fname = "fastq."+str(uuid.uuid4()).split("-")[-1]+".tsv"
		logging.info( "Will use new file name: %s"%fname)
	f = open(fname,"wb")
	used_files = []
	# print myDict
	# print len(myDict)
	for k in myDict:
		if len(myDict[k]) != 1:
			logging.error ("FILE: "+k+" didn't find a pair "+" ".join(myDict[k]))
			flag = 	True
		else:

			f1 = k
			f2 = myDict[k][0]
			if f1 in used_files:
				continue
			if f2 in used_files:
				continue			
			label = define_fastq_label(f1)
			if len(label) == 0:
				label = f1[:5]
			## 7-9-2019, rna-seq variant call, input has to be order 
			mySeps = re.split('_|-|\.',f1)
			# print f1
			# print mySeps
			skip_flag = True
			for x in mySeps:
				if x == "R1":
					skip_flag = False
			if skip_flag:
				continue
			print >>f,"\t".join([f1,f2,label])
			used_files.append(f1)
			used_files.append(f2)
	unused_files = list(set(files) - set(used_files))	
	f.close()
	flag = False
	if len(unused_files) == 0:
		logging.info ("Input fastq files preparation complete! ALL GOOD!")
		logging.info ("Please check if you like the computer-generated labels in : "+fname)
		flag = True
	else:
		logging.info ("Input fastq files preparation complete! There are some unmatched files.")
		for f in unused_files:
			logging.error(f)
	return flag,fname

def prepare_single_end_input():
	
	tmp_files = glob.glob("*.fastq.gz")+glob.glob("*.fastq")
	files = []
	for f in tmp_files:
		if "undetermined" in f.lower():
			continue
		files.append(f)	
	fname = "fastq.tsv"
	if isfile(fname):
		logging.warning(fname+" exists!")
		fname = "fastq."+str(uuid.uuid4()).split("-")[-1]+".tsv"
		logging.info( "Will use new file name: "+fname)
	f = open(fname,"wb")
	for fastq in files:
		label = define_fastq_label(fastq)
		if len(label) == 0:
			label = fastq[:5]		
		print >>f,"\t".join([fastq,label])
	logging.info( "Input fastq files preparation complete! ALL GOOD!")
	f.close()
	return True,fname

def longestSubstringFinder(string1, string2):
	answers = {}
	s1 = re.split("\.|_|-",string1.upper())
	s2 = re.split("\.|_|-",string2.upper())
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



def prepare_single_end_input_with_group_infer():
	
	## get all files
	tmp_files = glob.glob("*.fastq.gz")+glob.glob("*.fastq")
	files = {}
	for f in tmp_files:
		if "undetermined" in f.lower():
			continue
		label = f.replace(".fastq.gz","")
		files[label] = f
	fname = "fastq.tsv"
	if isfile(fname):
		logging.warning(fname+" exists!")
		fname = "fastq."+str(uuid.uuid4()).split("-")[-1]+".tsv"
		logging.info( "Will use new file name: "+fname)
	dname = "design_matrix.tsv"
	if isfile(dname):
		logging.warning(dname+" exists!")
		dname = "design_matrix."+str(uuid.uuid4()).split("-")[-1]+".tsv"
		logging.info( "Will use new file name: "+dname)


	# infer group
	lines = []
	for i in files:
		
		for j in files:
			if j == i:
				continue
			current = [files[i],i]
			current+=longestSubstringFinder(i,j)
			lines.append(current)
	df = pd.DataFrame(lines)
	# print (df)
	df = df.sort_values(3,ascending=False)
	df = df.drop_duplicates(1)
	groups = df[2].unique().tolist()
	if df.shape[0]!=len(files) or len(groups) == 1:
		logging.error("Failed to guess fastq.tsv and design_matrix.tsv")
		return False,fname
	
	df = df[[0,1,2]]
	df.to_csv(fname,sep="\t",header=False,index=False)
	logging.info( "Input fastq files and design.tsv preparation complete! ALL GOOD!")
	logging.info( "The following are infered fastq.tsv \n %s"%(df.to_string(index=False,header=False)))
	
	combos = list(itertools.combinations(groups, 2))
	df = pd.DataFrame(combos)
	df[2] = df[0].astype(str)+".vs."+df[1].astype(str)
	df.to_csv(dname,sep="\t",header=False,index=False)
	

	return True,fname



def find_control(myList):
	return_list = []
	for x in myList:
		if "igg" in x.lower():
			return_list.append(x)
		if 'input' in x.lower():
			return_list.append(x)
	return return_list
def prepare_design_matrix(file):
	# 4-10, adjust for multiple controls
	# any item matched to "igg" or "input" will be used as control, all other samples will be treatment
	items = map(lambda x:x.strip().split()[-1],open(file).readlines())
	control = find_control(items)
	# print len(control)
	if len(control) == 0:
		logging.error( "No control sample found.")
		return 0
	fname = "peakcall.tsv"
	if isfile(fname):
		logging.warning( fname+" exists!")
		fname = "peakcall."+str(uuid.uuid4()).split("-")[-1]+".tsv"
		logging.info( "Will use new file name: "+fname)
	f = open(fname,"wb")

	if len(control) > 1:
		logging.info( "Multiple control files found. Computer-generated design matrix could be inaccurate.")
		treatment_list = list(set(items)-set(control))
		df = pd.DataFrame()
		for c in control:
			myList = map(lambda x:similar(c, x),treatment_list)
			df[c] = myList
		df.index = treatment_list
		df['Max'] = df.idxmax(axis=1)
		for i in df.index:
			c = df.at[i,'Max']
			print >>f,"\t".join([i,c,i+".vs."+c])
	else:
		for i in items:
			if i == control[0]:
				continue	
			print >>f,"\t".join([i,control[0],i+".vs."+control[0]])
	logging.info( "Input peakcall file preparation complete! File name: "+fname)	
	f.close()
	pass

def check_input_tsv_isfile(x):
	"""the last column is always assumed to be uid"""
	flag = True
	with open(x) as f:
		for line in f:
			line = line.strip().split()
			if len(line) > 1:
				for item in line[:-1]:
					if not isfile(item):
						logging.error (item,"not exist")
						flag = False
	return flag
	
def check_input_tsv_numCols_uid_uniqueness(x):
	"""the last column is always assumed to be uid"""
	myList = []
	uidList = []
	with open(x) as f:
		for line in f:
			line = line.strip().split()
			if len(line) > 1:
				myList.append(len(line))
				uidList.append(line[-1])
	myList = list(set(myList))
	if len(myList) == 1:
		return True,uidList
	else:
		logging.error ("You have unequal number of cols!")
		return False,uidList

def check_NGS_input(args):
	"""perform general input files check
	
	applicable to fastq tsv and peakcall tsv
	
	"""
	flag1,fastq_tsv = check_input_tsv_numCols_uid_uniqueness(args.fastq_tsv)
	try:
		flag2,peakcall_tsv = check_input_tsv_numCols_uid_uniqueness(args.peakcall_tsv)
	except:
		flag2 = True
		peakcall_tsv = fastq_tsv
	flag3 = check_input_tsv_isfile(args.fastq_tsv)
	myList = list(set(fastq_tsv) - set(peakcall_tsv))
	if len(myList) != 0:
		flag4 = False
		logging.error ("unmatched UID found! See below:")
		logging.info ("\n".join(myList))
	else:
		flag4 = True
	if flag1 and flag2 and flag3 and flag4:
		return True
	else:
		logging.error ("input files contain errors, please see above messages!")
		logging.error ("Program existing...")
		return False
		
def check_diffPeak_input(args):

	return 1