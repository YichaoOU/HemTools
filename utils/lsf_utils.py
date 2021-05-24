#!/hpcf/apps/python/install/2.7.13/bin/python
from utils import *
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"


def parse_LSF_job_specification(x):
	"""parse LSF job specification file into job sections
	
	return
	------
	
	dict: [job name] = [job order, job dep, job commands, core, mem, input_file]
	
	list: sorted job name list
	
	"""
	## =cut
	
	## read into chunks
	
	myLSFjobs = {}
	with open(x) as f:
		for line in f:
			line = line.strip()
			if len(line) == 0:
				continue
			if line[0] == "#":
				if "#BSUB" in line:
					pass
				else:
					continue
			if "=cut" in line:
				# print line
				line = line.split()
				job_name = line[1]
				job_order = int(line[2])
				try:
					job_dep = line[3]
				except:
					job_dep = ""
				myLSFjobs[job_name] = [job_order,job_dep,[],"","","",""]
			else:
				try:
					if "core=" in line:
						core = line.split("=")[-1]
						myLSFjobs[job_name][3] = core
					if "mem=" in line:
						mem = line.split("=")[-1]
						myLSFjobs[job_name][4] = mem
					if "q=" in line: ## new Yichao 5/21/2020
						q = line.split("=")[-1]
						myLSFjobs[job_name][6] = q
					if "inputFile=" in line: ## do not add this line to script
						inputFile = line.split("=")[-1]
						myLSFjobs[job_name][5] = inputFile
					else:
						myLSFjobs[job_name][2].append(line)
				except:
					continue
			
	# for k in  myLSFjobs:
		# print "------------",k,"---------------"
		# print myLSFjobs[k]

	order_job_name_list = sorted(myLSFjobs,key=lambda x:myLSFjobs[x][0])
	
	# print order_job_name_list
	
	return order_job_name_list,myLSFjobs


def submit_job(myDict):
	"""myDict contains parameters to be replaced"""
	# most jobs should be split and then submit

	# prepare job lsf
	# output_lsf_file_name = myDict['job_name']+".lsf"
	# Yichao Li avoid file being rewrite 
	output_lsf_file_name = myDict['jid']+"/"+myDict['job_name']+".lsf"
	content = multireplace(lsf_job_template,myDict)
	write_file(output_lsf_file_name,content)
	dos2unix(output_lsf_file_name)
	# submit job and extract submission id
	job_id_regex = b"Job <([0-9]+)>"
	if myDict['number_lines'] == 0:
		return "No input, skip"
	# if "cas" in output_lsf_file_name:
		# pipe = subprocess.Popen('bsub -m nodegpu120 < '+output_lsf_file_name, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	# else:
	pipe = subprocess.Popen('bsub < '+output_lsf_file_name, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output = pipe.communicate()[0]
	match = re.match(job_id_regex,output)
	submission_id = match.group(1).decode('utf-8')
	return submission_id

def run_interative_jobs(pipeline_file,args):
	"""run the specified pipeline interatively, designed for debug purposes

	use subprocess.call to run bash script

	Pseudo code
	-----------
	
	1. generate args define file name
	
	for each LSF job section
		find input file name
		define myDict:
			replace with args define file name
			replace core, mem
			replace keywords with real names in commands
		replace LSF job template using myDict

	Note
	----
	
	we have two dicts.
	
	myDict is used to replace lsf_job_template
	
	args will be converted into a dict, used to replace current_command.

	"""

	tempDict = {}	
	tempDict['project_name'] = str(args.jid).split(".py")[0]
	argsDict = vars(args)
	# print argsDict
	myList,myJobs = parse_LSF_job_specification(pipeline_file)
	myJobID_list = [] ## for backtrack if any job failed to submit
	for x in myList:
		### x = job_name
		
		current_command = "\n".join(myJobs[x][2])
		current_command = multireplace(current_command,argsDict)

		myDict = dp(tempDict)
		myDict['job_name'] = x
		myDict['jid'] = args.jid
		
		try:
			myDict['sample_list'] = argsDict[myJobs[x][5]]
			dos2unix(myDict['sample_list'])
		except:
			pass
		try:
			myDict['sample_list'] = argsDict[myJobs[x][5]]
			myDict['number_lines'] = get_number_lines(myDict['sample_list'])
		except:
			myDict['sample_list'] = p_dir+"../share/misc/sample.tsv"
			myDict['number_lines'] = 1

		myDict['commands'] = current_command

		logging.info("%s is running"%(x))
		
		df = pd.read_csv(myDict['sample_list'],sep="\t",header=None)
		print (df)
		Ncols = df.shape[1]
		if myDict['sample_list']  == p_dir+"../share/misc/sample.tsv":

			# subprocess.call(current_command,shell=True)
			run_as_bash_script(current_command)
		
		for i,r in df.iterrows():
			temp = dp(current_command)
			for j in range(1,Ncols+1):
				temp = temp.replace("${COL%s}"%(j),r[j-1])
			logging.info("running the following command: \n %s"%(temp))
			# subprocess.call(temp,shell=True)
			run_as_bash_script(temp)
			
		
def run_as_bash_script(commands):
	write_file("temp.sh",commands)
	subprocess.call("bash temp.sh",shell=True)

def submit_pipeline_jobs(pipeline_file,args):
	"""submit a pipeline job specified in share/lsf/

	Pseudo code
	-----------
	
	1. generate args define file name
	
	for each LSF job section
		find input file name
		define myDict:
			replace with args define file name
			replace core, mem
			replace keywords with real names in commands
		replace LSF job template using myDict

	Note
	----
	
	we have two dicts.
	
	myDict is used to replace lsf_job_template
	
	args will be converted into a dict, used to replace current_command.

	"""

	tempDict = {}	
	tempDict['project_name'] = str(args.jid).split(".py")[0][:10] ## project name too long. Job not submitted.
	argsDict = vars(args)
	# print argsDict
	myList,myJobs = parse_LSF_job_specification(pipeline_file)
	myJobID_list = [] ## for backtrack if any job failed to submit
	for x in myList:
		### x = job_name
		
		current_command = "\n".join(myJobs[x][2])
		current_command = multireplace(current_command,argsDict)
		number_cores = myJobs[x][3]
		if number_cores == "":
			number_cores = 1
		memory_request = myJobs[x][4]
		bqueue = myJobs[x][6]
		if memory_request == "":
			memory_request = 4000
		if bqueue == "":
			bqueue = 'standard'
		myDict = dp(tempDict)
		myDict['job_name'] = x
		myDict['jid'] = args.jid
		
		myDict['number_cores'] = number_cores
		myDict['bqueue'] = bqueue
		# myDict['memory_request'] = memory_request
		# print memory_request
		myDict['memory_request'] = multireplace(memory_request,argsDict)
		myDict['bqueue'] = multireplace(bqueue,argsDict)
		try:
			myDict['sample_list'] = argsDict[myJobs[x][5]]
			dos2unix(myDict['sample_list'])
		except:
			pass
		try:
			myDict['sample_list'] = argsDict[myJobs[x][5]]
			myDict['number_lines'] = get_number_lines(myDict['sample_list'])
		except:
			myDict['sample_list'] = p_dir+"../share/misc/sample.tsv"
			myDict['number_lines'] = 1
		if myJobs[x][1] == "":
			myDict['dependencies'] = ""
		else:
			## two types:
			dep_job_name = myJobs[x][1]
			# print ("###DEBUG##",myJobs)
			# print ("###DEBUG##",myJobs[x])
			if dep_job_name=="all":
				dep_all_list = ["ended(%s)"%(var) for var in myJobID_list]
				myDict['dependencies'] = '#BSUB -w "%s"'%(" && ".join(dep_all_list))
			elif "[*]" in dep_job_name:
				myDict['dependencies'] = lsf_job_dep_template%(myJobs[dep_job_name.replace("[*]","")][-1]+"[*]")
			else:
				myDict['dependencies'] = lsf_job_dep_template%(myJobs[dep_job_name][-1])
		myDict['commands'] = current_command
		try:
			jobID = submit_job(myDict)
			# os.system("mv %s.lsf %s"%(x,args.jid))
			if not "skip" in jobID:
				myJobID_list.append(jobID)
		except:
			logging.error("%s is failed to submit. The failing is likely to be caused by incorrect input format."%(x))
			for k in myDict:
				print (k,myDict[k])
			for k in myJobs:
				print (k,myJobs[k])
			# print myDict['sample_list'],(get_number_lines(myDict['sample_list']))
			print ("-------------------see info above-----------------")
			for j in myJobID_list:
				os.system("bkill %s"%(j))
			logging.error("Program exiting! Please check input!")
			sys.exit(1)
		myJobs[x].append(jobID)
		logging.info("%s has been submitted; JobID: %s"%(x,jobID))
	send_user_command(getpass.getuser(),args.jid)
lsf_job_template = """

#BSUB -P {{project_name}}
#BSUB -o {{jid}}/log_files/{{job_name}}_%J_%I.out -e {{jid}}/log_files/{{job_name}}_%J_%I.err
#BSUB -n {{number_cores}}
#BSUB -q {{bqueue}}
#BSUB -R "span[hosts=1] rusage[mem={{memory_request}}]"
#BSUB -J "{{job_name}}[1-{{number_lines}}]"

{{dependencies}}

module purge

id=$LSB_JOBINDEX
COL1=`head -n $id {{sample_list}}|tail -n1|awk -F "\t" '{print $1}'`
COL2=`head -n $id {{sample_list}}|tail -n1|awk -F "\t" '{print $2}'`
COL3=`head -n $id {{sample_list}}|tail -n1|awk -F "\t" '{print $3}'`
COL4=`head -n $id {{sample_list}}|tail -n1|awk -F "\t" '{print $4}'`
COL5=`head -n $id {{sample_list}}|tail -n1|awk -F "\t" '{print $5}'`
COL6=`head -n $id {{sample_list}}|tail -n1|awk -F "\t" '{print $6}'`
COL7=`head -n $id {{sample_list}}|tail -n1|awk -F "\t" '{print $7}'`
COL8=`head -n $id {{sample_list}}|tail -n1|awk -F "\t" '{print $8}'`
COL9=`head -n $id {{sample_list}}|tail -n1|awk -F "\t" '{print $9}'`
LINE=`head -n $id {{sample_list}}|tail -n1`

{{commands}}

"""

lsf_job_dep_template = '#BSUB -w "ended(%s)"'


