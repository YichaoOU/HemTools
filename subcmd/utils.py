#!/hpcf/apps/python/install/2.7.13/bin/python
import os
# import paramiko
import pickle
import getpass
import sys
import uuid
import glob
import subprocess
import re
import datetime
# useful sub functions
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
username = getpass.getuser()
def dos2unix(file):
	os.system(p_dir+"../bin/dos2unix "+file)
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()
def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		myString = myString.replace("{{"+str(k)+"}}",str(myDict[k]))
	return myString

class NGS_pipeline:

	# private variable, not accessible by users
	outputs_dict = {}
	outputs_dict['log_files'] = []
	outputs_dict['peak_files'] = []
	outputs_dict['bam_files'] = []
	outputs_dict['figures_tables'] = []
	outputs_dict['bdg_files'] = []
	outputs_dict['bw_files'] = []
	outputs_dict['QC_files'] = []
	submission_id_dict = {}
	parameter_dict = {}
	attachments = []
	urlDict = {}
	
	def __init__(self,args,logger,dep=1):
		self.args = args
		self.logger = logger
		self.parameter_dict['project_name']=args.subcmd
		self.dep = dep
		if args.short:
			self.Num_cores = "2"
		else:
			self.Num_cores = "6"
		# parameter_dict has 10 additional parameters that need to be specified for every run

	def submit_array_job(self):
		# most jobs should be split and then submit
		header="""

#BSUB -P {{project_name}}
#BSUB -o {{output_message}}_%J_%I.out -e {{output_message}}_%J_%I.err
#BSUB -n {{number_cores}}
#BSUB -q {{queue}}
#BSUB -R "span[hosts=1] rusage[mem={{memory_request}}]"
#BSUB -J "{{job_id}}[1-{{number_lines}}]"

{{dependencies}}

id=$LSB_JOBINDEX
COL1=`head -n $id {{sample_list}}|tail -n1|awk '{print $1}'`
COL2=`head -n $id {{sample_list}}|tail -n1|awk '{print $2}'`
COL3=`head -n $id {{sample_list}}|tail -n1|awk '{print $3}'`
LINE=`head -n $id {{sample_list}}|tail -n1`
{{commands}}

		"""
		if self.args.debug:
			self.submission_id_dict[self.parameter_dict['job_id']] = "123"
			return 1
		if self.args.short:
			self.parameter_dict['queue']="short"	
		if ".bw" in self.parameter_dict['job_id']:
			self.parameter_dict['queue']="standard"	
		# prepare job lsf
		header = multireplace(header,self.parameter_dict)
		write_file(self.parameter_dict['job_script_file'],header)
		dos2unix(self.parameter_dict['job_script_file'])
		# submit job and extract submission id
		job_id_regex = b"Job <([0-9]+)>"
		pipe = subprocess.Popen('bsub < '+self.parameter_dict['job_script_file'], shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		output = pipe.communicate()[0]
		match = re.match(job_id_regex,output)
		try:
			submission_id = match.group(1).decode('utf-8')
		except:
			self.logger.error(self.parameter_dict['job_script_file']+' Job is failed to submit. Exit program...')
			exit()

		# organize outputs
		# every lsf job will have:
		# - .lsf
		# - .err
		# - .out
		self.outputs_dict['log_files'].append(self.parameter_dict['job_script_file'])
		for i in range(1,int(self.parameter_dict['number_lines'])+1):
			self.outputs_dict['log_files'].append(self.parameter_dict['output_message']+"_"+submission_id+"_"+str(i)+".out")
			self.outputs_dict['log_files'].append(self.parameter_dict['output_message']+"_"+submission_id+"_"+str(i)+".err")
		self.logger.info(self.parameter_dict['job_id']+" has been submitted. Job ID: "+submission_id)
		self.submission_id_dict[self.parameter_dict['job_id']] = submission_id
		pass


	def run_fastqc(self):
		commands = "fastqc ${COL1}"

		# prepare input list, the LSF job is to go through every line
		fastqc_input = self.args.jid + ".fastqc.input"
		write_file(fastqc_input,"\n".join(self.fastq_input_list))
		dos2unix(fastqc_input)
		self.outputs_dict['log_files'].append(fastqc_input)

		# define LSF parameters
		self.parameter_dict['output_message']=self.args.jid +".fastqc.message"
		self.parameter_dict['number_cores']=1
		self.parameter_dict['queue']="short"
		self.parameter_dict['memory_request']=4000
		self.parameter_dict['job_id']="QC1"
		self.parameter_dict['sample_list']=fastqc_input
		self.parameter_dict['number_lines']=len(self.fastq_input_list)
		self.parameter_dict['dependencies']='module load fastqc/0.11.5'
		self.parameter_dict['commands']=commands
		self.parameter_dict['job_script_file']=self.args.jid +".fastqc.lsf"

		# submit job
		self.submit_array_job()

		# organize output
		for i in self.fastq_input_list:
			self.outputs_dict['QC_files'].append(i.replace(".fastq.gz","_fastqc.html"))
			self.outputs_dict['QC_files'].append(i.replace(".fastq.gz","_fastqc.zip"))


		pass

	def submit_single_command(self,command,output_dict={},attachments=[],queue="standard",number_cores=1,memory_request=4000):

		# most jobs should be split and then submit
		header="""

#BSUB -P {{project_name}}
#BSUB -o {{output_message}}_%J_%I.out -e {{output_message}}_%J_%I.err
#BSUB -n {{number_cores}}
#BSUB -q {{queue}}
#BSUB -R "span[hosts=1] rusage[mem={{memory_request}}]"
#BSUB -J "{{job_id}}[1-{{number_lines}}]"

{{commands}}

		"""

		# define LSF parameters
		self.parameter_dict['output_message']=self.args.jid +"."+self.args.subcmd+".message"
		self.parameter_dict['number_cores']=number_cores
		self.parameter_dict['queue']=queue
		self.parameter_dict['memory_request']=memory_request
		self.parameter_dict['job_id']=self.args.subcmd
		self.parameter_dict['number_lines']=1
		self.parameter_dict['commands']=command
		self.parameter_dict['job_script_file']=self.args.jid +"."+self.args.subcmd+".lsf"
		if self.args.short:
			self.parameter_dict['queue']="short"	
		# prepare job lsf
		header = multireplace(header,self.parameter_dict)
		write_file(self.parameter_dict['job_script_file'],header)
		dos2unix(self.parameter_dict['job_script_file'])
		# submit job and extract submission id
		job_id_regex = b"Job <([0-9]+)>"
		pipe = subprocess.Popen('bsub < '+self.parameter_dict['job_script_file'], shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		output = pipe.communicate()[0]
		match = re.match(job_id_regex,output)
		try:
			submission_id = match.group(1).decode('utf-8')
		except:
			self.logger.error(self.parameter_dict['job_script_file']+' Job is failed to submit. Exit program...')
			exit()

		# lsf outputs
		# every lsf job will have:
		# - .lsf
		# - .err
		# - .out
		self.outputs_dict['log_files'].append(self.parameter_dict['job_script_file'])
		for i in range(1,int(self.parameter_dict['number_lines'])+1):
			self.outputs_dict['log_files'].append(self.parameter_dict['output_message']+"_"+submission_id+"_"+str(i)+".out")
			self.outputs_dict['log_files'].append(self.parameter_dict['output_message']+"_"+submission_id+"_"+str(i)+".err")
		self.logger.info(self.parameter_dict['job_id']+" has been submitted. Job ID: "+submission_id)
		self.submission_id_dict[self.parameter_dict['job_id']] = submission_id

		# commmand-specific outputs
		for k in output_dict:
			try:
				self.outputs_dict[k] += output_dict[k]
			except:
				self.outputs_dict[k] = output_dict[k]
		self.attachments+=attachments

		pass		

	def run_skewer(self):
		Num_cores = "4"
		commands = p_dir+"../bin/skewer-0.2.2-linux-x86_64 -t {{Num_cores}} -x {{adaptor_x}} -y {{adaptor_y}} ${COL1} \
		${COL2} -z yes -o ${COL3}"
		# If trimming adapters from Nextera runs should cut the reads at CTGTCTCTTATACACATCT instead of the usual AGATCGGAAGAGC. Use of cutadapt, trim_galore or similar program is recommended with custom adapter specified.
		# prepare input list, the LSF job is to go through every line
		commands = multireplace(commands, {'Num_cores':Num_cores,\
			'adaptor_x':self.args.adaptor_x,\
			'adaptor_y':self.args.adaptor_y})


		# define LSF parameters
		self.parameter_dict['output_message']=self.args.jid +".skewer.message"
		self.parameter_dict['number_cores']=Num_cores
		self.parameter_dict['queue']="standard"
		self.parameter_dict['memory_request']=4000
		self.parameter_dict['job_id']="trim"
		self.parameter_dict['sample_list']=self.args.input
		self.parameter_dict['number_lines']=len(self.fastq_input_lines)
		self.parameter_dict['dependencies']=''
		self.parameter_dict['commands']=commands
		self.parameter_dict['job_script_file']=self.args.jid +".skewer.lsf"

		# submit job
		self.submit_array_job()
		
		# organize output
		for i in self.fastq_input_lines:
			self.outputs_dict['log_files'].append(i[-1]+"-trimmed.log")
	

		pass

	def run_BWA(self):

		Num_cores = self.Num_cores
		read1 = "${COL1}"
		read2 = "${COL2}"
		uid = "${COL3}"
		commands = []
		command_read1 = "bwa mem -t "+Num_cores+" "+self.args.index_file+" " + read1 + " |samtools view -@ "+Num_cores+" -bS - > " + uid + ".read1.bam"
		command_single = "bwa mem -t "+Num_cores+" "+self.args.index_file+" " + read1 + " |samtools view -@ "+Num_cores+" -bS - > " + uid + ".bam"
		command_pair = "bwa mem -t "+Num_cores+" "+self.args.index_file+" " + read1 + " " + read2 + " |samtools view -@ "+Num_cores+" -bS - > " + uid + ".bam"
		bwa_input = self.args.jid + ".bwa.input"
		outlines = []
		if self.args.subcmd == "atac_seq":				
			for i in self.fastq_input_lines:
				outlines.append("\t".join(map(lambda x:i[-1]+x,['-trimmed-pair1.fastq.gz','-trimmed-pair2.fastq.gz',''])))
		else:				
			for i in self.fastq_input_lines:
				outlines.append("\t".join(i))
		write_file(bwa_input,"\n".join(outlines))
		dos2unix(bwa_input)
		self.outputs_dict['log_files'].append(bwa_input)


		## DESIGN: if new API uses BWA, this might need to be adjusted
		if self.args.subcmd == "chip_seq_pair":
			commands.append(command_pair)
			commands.append(command_read1)
		elif self.args.subcmd == "chip_seq_single":
			commands.append(command_single.replace("{COL3}","{COL2}"))
		else:
			commands.append(command_pair)
		if self.args.subcmd == "atac_seq":	
			commands.append("rm ${COL1}")
			commands.append("rm ${COL2}")


		# define LSF parameters
		self.parameter_dict['output_message']=self.args.jid +".BWA.message"
		self.parameter_dict['number_cores']=Num_cores
		self.parameter_dict['queue']="standard"
		self.parameter_dict['memory_request']=4000
		self.parameter_dict['job_id']="BWA"
		self.parameter_dict['sample_list']=bwa_input
		self.parameter_dict['number_lines']=len(self.fastq_input_lines)
		# depends on trimming
		dependencies = ['module load bwa/0.7.16a','module load samtools/1.7']
		if self.args.subcmd == "atac_seq":
			dependencies=['#BSUB -w "ended('+self.submission_id_dict['trim']+'[*])"']+dependencies
		self.parameter_dict['dependencies']="\n".join(dependencies)


		# self.parameter_dict['dependencies']="\n".join(['module load bwa/0.7.16a','module load samtools/1.7'])
		self.parameter_dict['commands']="\n".join(commands)
		self.parameter_dict['job_script_file']=self.args.jid +".BWA.lsf"

		# submit job
		self.submit_array_job()

		# organize output
		for i in self.fastq_input_lines:
			self.outputs_dict['bam_files'].append(i[-1]+".bam")
			if self.args.subcmd == "chip_seq_pair":
				self.outputs_dict['bam_files'].append(i[-1]+".read1.bam")

		pass

	def run_samtools_markdup_rmdup(self):
		commands = []
		Num_cores = self.Num_cores
		command_samtools = "samtools command -@ "+str(Num_cores)
		command_sort_by_name = command_samtools.replace("command","sort") + " -n -o UID.name.st.bam UID.bam"
		command_fixmate = command_samtools.replace("command","fixmate") + " -m UID.name.st.bam UID.fixmate.bam"
		command_sort2 = command_samtools.replace("command","sort") + " -o UID.fixmate.st.bam UID.fixmate.bam"
		command_markdup = command_samtools.replace("command","markdup") + " UID.fixmate.st.bam UID.markdup.bam"
		command_markdup_r = command_samtools.replace("command","markdup") + " -r UID.markdup.bam UID.rmdup.bam"
		command_delete = "rm UID.name.st.bam UID.fixmate.bam UID.fixmate.st.bam"
		command_flagstat = command_samtools.replace("command","flagstat") + " UID.markdup.bam > UID.markdup.report"
		command_index_markdup = command_samtools.replace("command","index") + " UID.markdup.bam"
		command_index_rmdup = command_samtools.replace("command","index") + " UID.rmdup.bam"
		command_unique_rmdup = command_samtools.replace("command","view") + " -q 1 -b UID.rmdup.bam > UID.rmdup.uq.bam"
		command_index_unique_rmdup = command_samtools.replace("command","index") + " UID.rmdup.uq.bam"
		command_chrm = command_samtools.replace("command","view") + " UID.markdup.bam chrM -b > UID.markdup.chrM.bam"
		command_flagstat_chrM = command_samtools.replace("command","flagstat") + " UID.markdup.chrM.bam > UID.markdup.chrM.report"
		command_rmchrM = "samtools idxstats UID.rmdup.uq.bam | cut -f 1 | grep -v  chrM| xargs samtools view -@ "+str(Num_cores)+\
		" -b UID.rmdup.uq.bam > UID.rmdup.uq.rmchrM.bam"
		command_rmchrM_raw = "samtools idxstats UID.markdup.bam | cut -f 1 | grep -v  chrM| xargs samtools view -@ "+str(Num_cores)+\
			" -b UID.markdup.bam > UID.markdup.rmchrM.bam"
		command_rmchrM_raw_flagstat = command_samtools.replace("command","flagstat") + " UID.markdup.rmchrM.bam > UID.markdup.rmchrM.report"
		commands.append(command_sort_by_name)
		commands.append(command_fixmate)
		commands.append(command_sort2)
		commands.append(command_markdup)
		commands.append(command_markdup_r)
		commands.append(command_delete)
		commands.append(command_flagstat)
		commands.append(command_index_markdup)
		commands.append(command_index_rmdup)
		commands.append(command_unique_rmdup)
		commands.append(command_index_unique_rmdup)
		commands.append(command_chrm)
		commands.append(command_flagstat_chrM)
		commands.append(command_rmchrM)
		commands.append(command_rmchrM_raw)
		commands.append(command_rmchrM_raw_flagstat)
		if "single" in self.args.subcmd:
			uid = "${COL2}"
		else:
			uid = "${COL3}"
		myList1 = map(lambda x:x.replace("UID",uid),commands)
		myList2 = map(lambda x:x.replace("UID",uid+".read1"),commands)
		commands = myList1
		## DESIGN: if new API uses BWA, this might need to be adjusted
		if self.args.subcmd == "chip_seq_pair":
			commands = myList1 + myList2

		# define LSF parameters
		self.parameter_dict['output_message']=self.args.jid +".markdup.rmdup.message"
		self.parameter_dict['number_cores']=Num_cores
		self.parameter_dict['memory_request']=4000
		self.parameter_dict['job_id']="rmdup"
		self.parameter_dict['queue']="standard"
		self.parameter_dict['number_lines']=str(len(self.fastq_input_lines))
		self.parameter_dict['sample_list']=self.args.input
		# depends on BWA
		dependencies = ['module load samtools/1.7']
		if self.dep:
			dependencies=['#BSUB -w "ended('+self.submission_id_dict['BWA']+'[*])"']+dependencies
		self.parameter_dict['dependencies']="\n".join(dependencies)
		self.parameter_dict['commands']="\n".join(commands)
		self.parameter_dict['job_script_file']=self.args.jid +".mk.rm.lsf"


		# submit job
		self.submit_array_job()

		# organize output
		for i in self.fastq_input_lines:
			self.outputs_dict['bam_files'].append(i[-1]+".markdup.bam")
			self.outputs_dict['bam_files'].append(i[-1]+".markdup.bam.bai")
			self.outputs_dict['bam_files'].append(i[-1]+".markdup.chrM.bam")
			self.outputs_dict['bam_files'].append(i[-1]+".rmdup.bam")
			self.outputs_dict['bam_files'].append(i[-1]+".rmdup.bam.bai")
			self.outputs_dict['bam_files'].append(i[-1]+".rmdup.uq.bam")
			self.outputs_dict['bam_files'].append(i[-1]+".rmdup.uq.bam.bai")
			self.outputs_dict['QC_files'].append(i[-1]+".markdup.report")
			self.outputs_dict['QC_files'].append(i[-1]+".markdup.chrM.report")
			self.outputs_dict['bam_files'].append(i[-1]+".rmdup.uq.rmchrM.bam")
			self.outputs_dict['bam_files'].append(i[-1]+".markdup.rmchrM.bam")
			self.outputs_dict['QC_files'].append(i[-1]+".markdup.rmchrM.report")

			if self.args.subcmd == "chip_seq_pair":
				self.outputs_dict['bam_files'].append(i[-1]+".read1.markdup.bam")
				self.outputs_dict['bam_files'].append(i[-1]+".read1.markdup.bam.bai")
				self.outputs_dict['bam_files'].append(i[-1]+".read1.markdup.chrM.bam")
				self.outputs_dict['bam_files'].append(i[-1]+".read1.rmdup.bam")
				self.outputs_dict['bam_files'].append(i[-1]+".read1.rmdup.bam.bai")
				self.outputs_dict['bam_files'].append(i[-1]+".read1.rmdup.uq.bam")
				self.outputs_dict['bam_files'].append(i[-1]+".read1.rmdup.uq.bam.bai")
				self.outputs_dict['QC_files'].append(i[-1]+".read1.markdup.report")
				self.outputs_dict['QC_files'].append(i[-1]+".read1.markdup.chrM.report")
				self.outputs_dict['bam_files'].append(i[-1]+".read1.rmdup.uq.rmchrM.bam")
				self.outputs_dict['bam_files'].append(i[-1]+".read1.markdup.rmchrM.bam")
				self.outputs_dict['QC_files'].append(i[-1]+".read1.markdup.rmchrM.report")				
		pass

	def run_spp(self):
		Num_cores = 2
		command = "Rscript "+p_dir+"../bin/run_spp.R -c=UID.rmdup.uq.bam -p="+str(Num_cores)+" -savp -odir=. -rf > UID.spp.log" 

		## DESIGN: if new API uses BWA, this might need to be adjusted
		if self.args.subcmd == "chip_seq_pair":
			command = command.replace("UID","${COL3}.read1")
		elif self.args.subcmd == "chip_seq_single":
			command = command.replace("UID","${COL2}")
		else:
			command = command.replace("UID","${COL3}")


		# define LSF parameter
		self.parameter_dict['output_message']=self.args.jid +".spp.message"
		self.parameter_dict['number_cores']=Num_cores
		self.parameter_dict['queue']="standard"
		self.parameter_dict['memory_request']="4000"
		self.parameter_dict['job_id']="spp"
		self.parameter_dict['sample_list']=self.args.input
		self.parameter_dict['number_lines']=str(len(self.fastq_input_lines))
		# depends on rmdup
		dependencies = ['module load R/3.4.0','module load samtools/1.7']
		if self.dep:
			dependencies=['#BSUB -w "ended('+self.submission_id_dict['rmdup']+'[*])"']+dependencies
		self.parameter_dict['dependencies']="\n".join(dependencies)

		self.parameter_dict['commands']=command
		self.parameter_dict['job_script_file']=self.args.jid +".spp.lsf"


		# submit job
		self.submit_array_job()

		# organize output
		for i in self.fastq_input_lines:
			if self.args.subcmd == "chip_seq_pair":
				self.outputs_dict['peak_files'].append(i[-1]+".read1.rmdup.uq.pdf")
				self.attachments.append(i[-1]+".read1.rmdup.uq.pdf")
				self.outputs_dict['peak_files'].append(i[-1]+".read1.spp.log")
			else:
				self.outputs_dict['peak_files'].append(i[-1]+".rmdup.uq.pdf")
				self.attachments.append(i[-1]+".rmdup.uq.pdf")
				self.outputs_dict['peak_files'].append(i[-1]+".spp.log")
		pass

	def run_bamCoverage(self,input,output,type):
		Num_cores = self.Num_cores
		command = "bamCoverage -b "+input+" -o "+output+" --smoothLength=200 --ignoreForNormalization chrX chrM   --effectiveGenomeSize "+self.args.effectiveGenomeSize+" --numberOfProcessors "+Num_cores
		# paired-end data will add --centerReads parameter
		if not "single" in self.args.subcmd:
			command += " --centerReads"

		# define LSF parameter	
		self.parameter_dict['output_message']=self.args.jid +"."+type+".bw.message"
		self.parameter_dict['number_cores']=Num_cores
		self.parameter_dict['queue']="standard"
		self.parameter_dict['memory_request']=2000
		self.parameter_dict['job_id']=type+".bw"
		self.parameter_dict['sample_list']=self.args.input
		self.parameter_dict['number_lines']=str(len(self.fastq_input_lines))
		# depends on rmdup
		dependencies = ['#BSUB -R "select[rhel7]"','module load python/2.7.15-rhel7']
		if self.dep:
			dependencies=['#BSUB -w "ended('+self.submission_id_dict['rmdup']+'[*])"']+dependencies
		self.parameter_dict['dependencies']="\n".join(dependencies)
		self.parameter_dict['commands']=command
		self.parameter_dict['job_script_file']=self.args.jid +"."+type+".bw.lsf"

		# submit job
		self.submit_array_job()

		# organize output
		for i in self.fastq_input_lines:
			self.outputs_dict['bw_files'].append(i[-1]+"."+type+".bw")
		pass

	def run_lib_complexity(self):
		command_lib_complexity = """bedtools bamtobed -i UID.bam | awk 'BEGIN{OFS="\\t"}{print $1,$2,$3,$6}' | grep -v 'chrM' | sort | uniq -c | awk 'BEGIN{mt=0;m0=0;m1=0;m2=0} ($1==1){m1=m1+1} ($1==2){m2=m2+1} {m0=m0+1} {mt=mt+$1} END{printf "%d\\t%d\\t%d\\t%d\\t%f\\t%f\\t%f\\n",mt,m0,m1,m2,m0/mt,m1/m0,m1/m2}' > UID.lib.complexity"""

		self.parameter_dict['output_message']=self.args.jid +".lib.complexity.message"
		self.parameter_dict['number_cores']=1
		self.parameter_dict['queue']="standard"
		self.parameter_dict['memory_request']=10000
		self.parameter_dict['job_id']="libx"
		self.parameter_dict['sample_list']=self.args.input
		self.parameter_dict['number_lines']=str(len(self.fastq_input_lines))
		# depends on rmdup
		dependencies = ['module load bedtools/2.25.0']
		if self.dep:
			dependencies=['#BSUB -w "ended('+self.submission_id_dict['BWA']+'[*])"']+dependencies
		self.parameter_dict['dependencies']="\n".join(dependencies)
		if "single" in self.args.subcmd:
			uid = "${COL2}"
		else:
			uid = "${COL3}"
		self.parameter_dict['commands']=command_lib_complexity.replace("UID",uid)
		self.parameter_dict['job_script_file']=self.args.jid +".libx.lsf"
		# submit job
		self.submit_array_job()

		# organize output
		for i in self.fastq_input_lines:
			self.outputs_dict['QC_files'].append(i[-1]+".lib.complexity")
		pass

	def run_macs2_narrowPeak(self):
		commands = []
		# atac-seq parameter is different
		# paired-end and single-end are different
		# paired-end data will call twice, one for raw bam (atac-seq will be raw.rmchrM.bam), one for uq.rmdup.bam
		# single-end data will always use raw bam
		if self.args.subcmd == "atac_seq":
			# ref: https://www.biostars.org/p/209592/
			# ref: https://docs.google.com/document/d/1f0Cm4vRyDQDu0bMehHD7P7KOMxTOP-HiNoIvL1VcBt8/edit
			macs2_pealcall = "macs2 callpeak --nomodel --shift -100 --extsize 200 -t treatment_uid.bam -B -n NAME"
		elif "single" in self.args.subcmd:
			macs2_pealcall = "macs2 callpeak -t treatment_uid.bam -c control_uid.bam -g hs --keep-dup all -n NAME -B"
		else:
			macs2_pealcall = "macs2 callpeak -t treatment_uid.bam -c control_uid.bam -f BAMPE -g hs -B --keep-dup all -n NAME"
		# local bias track and call peak
		# ref: https://github.com/taoliu/MACS/wiki/Build-Signal-Track#Run_MACS2_bdgcmp_to_generate_foldenrichment_and_logLR_track
		# ref: https://github.com/taoliu/MACS/wiki/Advanced%3A-Call-peaks-using-MACS2-subcommands#Step_2_Decide_the_fragment_length_d
		macs2_bdgcmp_qpois = "macs2 bdgcmp -t NAME_treat_pileup.bdg -c NAME_control_lambda.bdg -m qpois -o NAME_treat_pvalue.bdg"
		macs2_bdgcmp_FE = "macs2 bdgcmp -t NAME_treat_pileup.bdg -c NAME_control_lambda.bdg -m FE -o NAME_FE.bdg"
		macs2_bdgcmp_logLR = "macs2 bdgcmp -t NAME_treat_pileup.bdg -c NAME_control_lambda.bdg -m logLR -o NAME_logLR.bdg"
		macs2_bdgpeakcall = "macs2 bdgpeakcall -i NAME_treat_pvalue.bdg -c 1.301 -l 100 -g 75 -o NAME_bdgpeaks.bed"
		in_files = ['NAME_treat_pvalue.bdg','NAME_FE.bdg','NAME_logLR.bdg']
		out_files = ['NAME_treat_pvalue.bw','NAME_FE.bw','NAME_logLR.bw']
		
		# have to manually adjust , because the short queue is rhel6, and by default, the node is rhel7.
		if self.args.short:
			command_wigToBigWig = p_dir+"../bin/wigToBigWig INFILE " + self.args.chrom_size + " OUTFILE"
		else:
			command_wigToBigWig = p_dir+"../bin/wigToBigWig.rhel7 INFILE " + self.args.chrom_size + " OUTFILE"
		remove_backlist1 = "intersectBed -a NAME_peaks.narrowPeak -b "+self.args.Blacklist+" -v -wa > NAME_peaks.rmblck.narrowPeak"
		remove_backlist2 = "intersectBed -a NAME_bdgpeaks.bed -b "+self.args.Blacklist+" -v -wa > NAME_bdgpeaks.rmblck.bed"
		
		commands.append(macs2_pealcall)
		commands.append(macs2_bdgcmp_qpois)
		commands.append(macs2_bdgcmp_FE)
		commands.append(macs2_bdgcmp_logLR)
		commands.append(macs2_bdgpeakcall)
		commands.append(remove_backlist1)
		commands.append(remove_backlist2)
		for i in [0,1,2]:
			tmp = command_wigToBigWig.replace("INFILE",in_files[i])
			tmp = tmp.replace("OUTFILE",out_files[i])
			commands.append(tmp)

		myList1 = map(lambda x:x.replace("treatment_uid","${COL1}").replace("control_uid","${COL2}").replace("NAME","${COL3}"),commands)	
		myList_atac = map(lambda x:x.replace("treatment_uid","${COL3}.markdup.rmchrM").replace("control_uid","${COL2}.markdup.rmchrM").replace("NAME","${COL3}.markdup.rmchrM"),commands)	
		myList2 = map(lambda x:x.replace("treatment_uid","${COL1}.rmdup.uq.rmchrM").replace("control_uid","${COL2}.rmdup.uq.rmchrM").replace("NAME","${COL3}.rmdup.uq.rmchrM"),commands)	

		## DESIGN: if new API uses BWA, this might need to be adjusted
		if self.args.subcmd == "atac_seq":
			commands = myList_atac + map(lambda x:x.replace("treatment_uid","${COL3}.rmdup.uq.rmchrM").replace("NAME","${COL3}.rmdup.uq.rmchrM"),commands)	
		elif "single" in self.args.subcmd:
			commands = myList1
		else:
			commands = myList1 + myList2

		# define LSF parameters
		self.parameter_dict['output_message']=self.args.jid +".macs2.message"
		self.parameter_dict['number_cores']=1
		self.parameter_dict['queue']="standard"
		self.parameter_dict['memory_request']=30000
		self.parameter_dict['job_id']="macs2"
		try:
			self.parameter_dict['sample_list']=self.args.design_matrix
			self.parameter_dict['number_lines']=len(self.design_matrix)			
		except:
			self.parameter_dict['sample_list']=self.args.input
			self.parameter_dict['number_lines']=len(self.fastq_input_lines)
		# depends on rmdup
		dependencies = ['module load macs2/2.1.1','module load bedtools/2.25.0']
		if self.dep:
			dependencies=['#BSUB -w "ended('+self.submission_id_dict['rmdup']+')"']+dependencies
		self.parameter_dict['dependencies']="\n".join(dependencies)
		self.parameter_dict['commands']="\n".join(commands)
		self.parameter_dict['job_script_file']=self.args.jid +".macs2.lsf"

		# submit job
		self.submit_array_job()

		# organize output
		try:
			myList = self.design_matrix
		except:
			myList = self.fastq_input_lines
		for i in myList:
			self.outputs_dict['peak_files'].append(i[-1]+"*.bed")
			self.outputs_dict['peak_files'].append(i[-1]+"*.xls")
			self.outputs_dict['peak_files'].append(i[-1]+"*.narrowPeak")
			self.outputs_dict['bdg_files'].append(i[-1]+"*.bdg")
			if self.args.subcmd == "atac_seq":
				self.outputs_dict['bw_files'].append(i[-1]+".markdup.rmchrM_FE.bw")
				self.outputs_dict['bw_files'].append(i[-1]+".markdup.rmchrM_logLR.bw")
				self.outputs_dict['bw_files'].append(i[-1]+".markdup.rmchrM_treat_pvalue.bw")	
				self.outputs_dict['bw_files'].append(i[-1]+".rmdup.uq.rmchrM_FE.bw")
				self.outputs_dict['bw_files'].append(i[-1]+".rmdup.uq.rmchrM_logLR.bw")
				self.outputs_dict['bw_files'].append(i[-1]+".rmdup.uq.rmchrM_treat_pvalue.bw")							
			elif "single" in self.args.subcmd:
				self.outputs_dict['bw_files'].append(i[-1]+"_FE.bw")
				self.outputs_dict['bw_files'].append(i[-1]+"_logLR.bw")
				self.outputs_dict['bw_files'].append(i[-1]+"_treat_pvalue.bw")	
			else:
				self.outputs_dict['bw_files'].append(i[-1]+"_FE.bw")
				self.outputs_dict['bw_files'].append(i[-1]+"_logLR.bw")
				self.outputs_dict['bw_files'].append(i[-1]+"_treat_pvalue.bw")			
				self.outputs_dict['bw_files'].append(i[-1]+".rmdup.uq.rmchrM_FE.bw")
				self.outputs_dict['bw_files'].append(i[-1]+".rmdup.uq.rmchrM_logLR.bw")
				self.outputs_dict['bw_files'].append(i[-1]+".rmdup.uq.rmchrM_treat_pvalue.bw")			
			self.outputs_dict['log_files'].append(i[-1]+"*.r")

		pass

	def run_hommer(self):

		pass

	def run_mEpigram(self):

		pass

	def send_email_command2(self):
		# this function should be applied for any API
		command = 'echo "Hi User_name,\n\nYour JOB_ID is finished. Please see the attachment for a summary of results. The results have been generated the following directory:\n RESULT_DIR \n\n If no attachment can be found, it might be caused by an error. In such case, please go to the result directory (above) and do HemTools report_bug. \n\n BigWiggle_URL" | mailx {{attachments}} -s "JOB_ID is finished" -- User_name@stjude.org'
		command = command.replace("JOB_ID",self.args.jid)
		# print self.attachments
		# real_attachments = []
		# for item in self.attachments:
			# if os.path.isfile(item):
				# real_attachments.append(real_attachments)
		# attachments_string = map(lambda x: '-a "'+x+'" ',real_attachments)
		attachments_string = map(lambda x: '-a "'+x+'" ',self.attachments)
		command = command.replace("{{attachments}}","".join(attachments_string))
		# command = command.replace("attachment_file",self.attachments)
		command = command.replace("User_name",username)
		command = command.replace("RESULT_DIR",os.getcwd()+"/"+self.args.jid+"/")
		if len(self.urlDict) > 0:
			outlines = []
			for k in self.urlDict:
				outlines.append(k+" tracks can be viewed at: "+self.urlDict[k])
			command = command.replace("BigWiggle_URL","\n\n".join(outlines))
		else:
			command = command.replace("BigWiggle_URL","")
		return 	command
		
	def send_email_command(self):
		# this function should be applied for any API
		outFile = str(uuid.uuid4()).split("-")[-1]+".bwDict"
		out = open(outFile,"wb")
		pickle.dump([self.attachments,self.args.jid,self.urlDict],out)			
		out.close()
		commands = p_dir+'send_email.py '+outFile
		
		self.outputs_dict['log_files'].append(outFile)	
		return 	commands


		

	def gather_email_attachments(self):

		pass

	def QC_report_command(self):
		commands = p_dir+'NGS.report.py '+self.args.jid + " "+self.args.subcmd+" "+",".join(self.fastq_input_list) + " " + ",".join(list(map(lambda x:x[-1],self.fastq_input_lines)))

		# step 4
		# organize output

		self.outputs_dict['figures_tables'].append(self.args.jid+".report.html")
		self.attachments.append(self.args.jid+".report.html")			

		return commands

		

	def run_output_organization(self,report_flag=True):
		# this function should be the most generalized function
		# add send email, html report command here
		# Should be the last step of NGS_pipeline
		# print "report_flag",report_flag
		# print "last step"
		
		if report_flag:
			commands = [self.QC_report_command(),self.send_email_command(),'mkdir '+self.args.jid]
		else:
			commands = [self.send_email_command(),'mkdir '+self.args.jid]
		# print "attachments",self.attachments
		for k in self.outputs_dict:
			if len(self.outputs_dict[k]) == 0:
				continue
			commands.append('mkdir '+self.args.jid+"/"+k)
			for v in self.outputs_dict[k]:
				commands.append('mv '+v+" "+self.args.jid+"/"+k)


		# step 2 
		# define 10 LSF parameters
		self.parameter_dict['job_script_file']=self.args.jid +".html.lsf"
		commands.append('mv '+self.parameter_dict['job_script_file']+" "+self.args.jid+"/log_files")
		commands.append('mv '+self.args.jid+".log "+self.args.jid+"/log_files")
		self.parameter_dict['output_message']=self.args.jid+"/log_files/"+self.args.jid +".html.message"
		self.parameter_dict['number_cores']=1
		self.parameter_dict['memory_request']=4000
		self.parameter_dict['job_id']="html"
		self.parameter_dict['queue']="short"
		self.parameter_dict['number_lines']=1
		self.parameter_dict['sample_list']=self.args.input
		# depends on rmdup
		dependencies = ['module load python/2.7.13']
		if self.dep:
			tmp = []
			for v in self.submission_id_dict.values():
				tmp.append('ended('+v+')')
			dependencies=['"'+" && ".join(tmp)+'"']+dependencies
		self.parameter_dict['dependencies']='#BSUB -w '+"\n".join(dependencies)

		self.parameter_dict['commands']="\n".join(commands)
		# self.parameter_dict['job_script_file']=self.args.jid +".html.lsf"

		# step 3
		# submit job
		self.submit_array_job()
		
		self.logger.info("All jobs are submitted. You will be notified by email with the final report attached! Bye!")

		
		pass


	def run_STJtracks(self):
		# dump bw files
		myURL = "https://ppr.stjude.org/?study=HemPipelines/UserName/UserJobID/{{tracks}}.json"
		myURL = myURL.replace("UserName",username)
		myURL = myURL.replace("UserJobID",self.args.jid)
				
		myDict = {}
		myDict['treat_pvalue.bw'] = []
		myDict['FE.bw'] = []
		myDict['logLR.bw'] = []
		myDict['all.bw'] = []
		myDict['rmdup.bw'] = []
		myDict['rmdup.uq.bw'] = []
		bw_files = self.outputs_dict['bw_files']
		
		for k in myDict:
			tmp = myURL.replace("{{tracks}}",k)
			self.urlDict[k] = tmp
			for n in bw_files:
				if k in n:
					myDict[k].append(n)
					continue

		outFile = str(uuid.uuid4()).split("-")[-1]+".bwDict"
		out = open(outFile,"wb")
		pickle.dump([self.args.jid,myDict],out)			
		out.close()

		commands = p_dir+'STJtracks.py '+outFile


		# step 2 
		# define 10 LSF parameters
		self.parameter_dict['output_message']=self.args.jid +".tracks.message"
		self.parameter_dict['number_cores']=1
		self.parameter_dict['memory_request']=4000
		self.parameter_dict['job_id']="tracks"
		self.parameter_dict['queue']="standard"
		self.parameter_dict['number_lines']=1
		self.parameter_dict['sample_list']=self.args.input
		# depends on rmdup
		dependencies = ['module load python/2.7.13']
		# if self.dep:
			# tmp = []
			# for v in self.submission_id_dict.values():
				# tmp.append('#BSUB -w "done('+v+')"')
			# dependencies=tmp+dependencies
		if self.dep:
			tmp = []
			for v in self.submission_id_dict.values():
				tmp.append('ended('+v+')')
			dependencies=['"'+" && ".join(tmp)+'"']+dependencies
		self.parameter_dict['dependencies']='#BSUB -w '+"\n".join(dependencies)			
			
		# self.parameter_dict['dependencies']="\n".join(dependencies)

		self.parameter_dict['commands']=commands
		self.parameter_dict['job_script_file']=self.args.jid +".tracks.lsf"

		# step 3
		# submit job
		self.submit_array_job()		

		# step 4
		# organize output

		self.outputs_dict['log_files'].append(outFile)			
		self.outputs_dict['log_files'].append(self.args.jid+".url")			

		return commands

	def run_DESEQ2(self):

		pass

	def parse_paired_fastq(self):
		# In paired-end input tsv, only len(cols) == 3 will be accepted
		# len(cols) == 2 won't raise Error, but it will be ignored
		my_list = []
		my_paired_files = []
		dos2unix(self.args.input)
		with open(self.args.input) as f:
			for line in f:
				line = line.strip().split()
				if len(line) == 3:
					my_paired_files.append([line[0],line[1],line[2]])
					my_list.append(line[0])
					my_list.append(line[1])
		self.fastq_input_list = my_list	
		self.fastq_input_lines = my_paired_files	

		pass

	def parse_single_fastq(self):
		# In single-end input tsv, only len(cols) == 2 will be accepted
		# len(cols) == 3 won't raise Error, but it will be ignored
		my_list = []
		my_single_files = []
		dos2unix(self.args.input)
		with open(self.args.input) as f:
			for line in f:
				line = line.strip().split()
				if len(line) == 2:
					my_single_files.append([line[0],line[1]])
					my_list.append(line[0])
		self.fastq_input_list = my_list	
		self.fastq_input_lines = my_single_files	
		pass

	def parse_treatment_control(self):
		my_list = []
		dos2unix(self.args.design_matrix)
		with open(self.args.design_matrix) as f:
			for line in f:
				line = line.strip().split()
				if len(line) == 3:
					my_list.append([line[0],line[1],line[2]])
		self.design_matrix = my_list
		self.pairwise_comparisons={}
		try:			
			for row in my_list:
				if not self.pairwise_comparisons.has_key(row[0]):
					self.pairwise_comparisons[row[0]] = {}
					self.pairwise_comparisons[row[0]]['control'] = []
					self.pairwise_comparisons[row[0]]['treatment'] = []
				self.pairwise_comparisons[row[0]][row[1]]=row[2]
		except:
			pass
		pass

	def dry_run(self):
		# subcmd independent check-up
		# only check for file existence and sample ID matches
		self.logger.info("DRY RUN: check if all input files exist")
		file_exist_flag = True
		for fname in self.fastq_input_list:
			if not os.path.isfile(fname):
				self.logger.info(fname+" NOT FOUND. Please check your input file: "+self.args.input)
				file_exist_flag = False
		try:
			self.design_matrix
			flag = True
		except:
			flag = False
		if flag:
			self.logger.info("DRY RUN: check if sample IDs match in the input fastq tsv and design matrix.")
			reference = list(map(lambda x:x[-1],self.fastq_input_lines))
			sample_id_match_flag = True
			for i in self.design_matrix:
				if not i[0] in reference:
					sample_id_match_flag = False
					self.logger.info(i[0]+" can't be found in "+self.args.input)
				if not i[1] in reference:
					sample_id_match_flag = False
					self.logger.info(i[1]+" can't be found in "+self.args.input)
			good_flag = file_exist_flag and sample_id_match_flag
		good_flag = file_exist_flag
		if good_flag:
				self.logger.info("LOOKS GOOD! Dry run PASSED! Analyses continue...")
		else:
			self.logger.info("Something is wrong! Please check the above error messages.")
			self.logger.close()
			os.system("rm "+self.args.jid+".log")		
			exit()
		

	def run_example(self):

		# step 1
		# Note: all the commands should be directly executable in bash
		commands = ""

		# step 1.5 adjust commands to different subcmd
		## DESIGN: if new API uses BWA, this might need to be adjusted
		if self.args.subcmd == "chip_seq_pair":
			commands = myList1 + myList2		

		# step 2 
		# define 10 LSF parameters
		self.parameter_dict['output_message']=self.args.jid +".BWA.message"
		self.parameter_dict['number_cores']=Num_cores
		self.parameter_dict['queue']="standard"
		self.parameter_dict['memory_request']=4000
		self.parameter_dict['job_id']="BWA"
		self.parameter_dict['sample_list']=self.args.input
		self.parameter_dict['number_lines']=len(self.fastq_input_lines)
		# depends on rmdup
		dependencies = ['module load bedtools/2.25.0']
		if self.dep:
			dependencies=['#BSUB -w "ended('+self.submission_id_dict['BWA']+'[*])"']+dependencies
		self.parameter_dict['dependencies']="\n".join(dependencies)
		self.parameter_dict['commands']="\n".join(commands)
		self.parameter_dict['job_script_file']=self.args.jid +".BWA.lsf"

		# step 3
		# submit job
		self.submit_array_job()

		# step 4
		# organize output
		for i in self.fastq_input_lines:
			self.outputs_dict['bam_files'].append(i[-1]+".bam")
			if self.args.subcmd == "chip_seq_pair":
				self.outputs_dict['bam_files'].append(i[-1]+".read1.bam")			


		pass

	def run_mageck_count(self):

		# step 1
		# Note: all the commands should be directly executable in bash
		files = glob.glob("*.gz")
		commands = "mageck count --output-prefix "+self.args.jid+"_raw_counts -l "+self.args.gRNA_library+" --fastq "+",".join(files)+"  --pdf-report --sample-label "+",".join(files)	
		# outputs
		# all.count_normalized.txt  all_countsummary.R  all_countsummary.Rnw  all.countsummary.txt  all.count.txt  all.log
		# step 2 
		# define 10 LSF parameters
		self.parameter_dict['output_message']=self.args.jid +".mageck_count.message"
		self.parameter_dict['number_cores']=1
		self.parameter_dict['queue']="standard"
		self.parameter_dict['memory_request']=8000
		self.parameter_dict['job_id']="mageck_count"
		self.parameter_dict['sample_list']=self.args.design_matrix
		self.parameter_dict['number_lines']=1
		# depends on rmdup
		dependencies = ['module load python/2.7.5']
		self.parameter_dict['dependencies']="\n".join(dependencies)
		self.parameter_dict['commands']=commands
		self.parameter_dict['job_script_file']=self.args.jid +".mageck_count.lsf"

		# step 3
		# submit job
		self.submit_array_job()

		# step 4
		# organize output

		self.outputs_dict['log_files'].append(self.args.jid+"_raw_counts_countsummary.R")
		self.outputs_dict['log_files'].append(self.args.jid+"_raw_counts_countsummary.Rnw")
		self.outputs_dict['log_files'].append(self.args.jid+"_raw_counts.log")
		self.outputs_dict['mageck_count_files'] = []
		self.outputs_dict['mageck_count_files'].append(self.args.jid+"_raw_counts.countsummary.txt")
		self.outputs_dict['mageck_count_files'].append(self.args.jid+"_raw_counts.count.txt")
		self.outputs_dict['mageck_count_files'].append(self.args.jid+"_raw_counts.count_normalized.txt")



		pass		
	def run_mageck_RRA(self):

		# step 1
		# Note: all the commands should be directly executable in bash
		commands=[]
		command = "mageck test --count-table "+self.args.jid+"_raw_counts.count.txt"+" --norm-method control --output-prefix {{name}}_RRA_results --control-sgrna "+self.args.gRNA_library+" -t {{treatment_col_names}} -c {{control_col_names}}"	
		for k in self.pairwise_comparisons:
			t = self.pairwise_comparisons[k]['treatment']
			c = self.pairwise_comparisons[k]['control']
			name = k
			tmp = multireplace(command, {'name':name,\
				'treatment_col_names':t,\
				'control_col_names':c\
				})
			commands.append(tmp)

		# prepare input list, the LSF job is to go through every line
		command_input = self.args.jid + ".RRA.input"
		write_file(command_input,"\n".join(commands))
		dos2unix(command_input)
		self.outputs_dict['log_files'].append(command_input)

		# outputs
		
		# step 2 
		# define 10 LSF parameters
		self.parameter_dict['output_message']=self.args.jid +".mageck_RRA.message"
		self.parameter_dict['number_cores']=1
		self.parameter_dict['queue']="standard"
		self.parameter_dict['memory_request']=8000
		self.parameter_dict['job_id']="mageck_RRA"
		self.parameter_dict['sample_list']=command_input
		self.parameter_dict['number_lines']=len(commands)
		# depends on mageck_count
		dependencies = ['module load python/2.7.5']
		if self.dep:
			dependencies=['#BSUB -w "ended('+self.submission_id_dict['mageck_count']+')"']+dependencies
		self.parameter_dict['dependencies']="\n".join(dependencies)
		self.parameter_dict['commands']="${LINE}"
		self.parameter_dict['job_script_file']=self.args.jid +".mageck_RRA.lsf"

		# step 3
		# submit job
		self.submit_array_job()

		# step 4
		# organize output
		self.outputs_dict['mageck_RRA_files'] = []
		for k in self.pairwise_comparisons:
			name = k
			self.outputs_dict['log_files'].append(name+"_RRA_results.log")
			self.outputs_dict['log_files'].append(name+"_RRA_results_summary.Rnw")
			self.outputs_dict['log_files'].append(name+"_RRA_results.R")
			self.outputs_dict['mageck_RRA_files'].append(name+"_RRA_results.gene_summary.txt")
			self.outputs_dict['mageck_RRA_files'].append(name+"_RRA_results.sgrna_summary.txt")



		pass		

	def run_mageck_MLE(self):

		# step 1
		# Note: all the commands should be directly executable in bash
		commands=[]
		command = "mageck mle -d {{design_matrix}} --count-table "+self.args.jid+"_raw_counts.count.txt"+" --norm-method control --output-prefix {{name}}_MLE_results --control-sgrna "+self.args.gRNA_library	+ " -i {{selected_samples}}" 
		# to_mageck_design_matrix(treatment_list,control_list,count_df,comparison_id):

		for k in self.pairwise_comparisons:
			t = self.pairwise_comparisons[k]['treatment']
			c = self.pairwise_comparisons[k]['control']
			design_matrix = ['1,0']*len(c.split(","))+['1,1']*len(t.split(","))
			design_matrix = '"'+";".join(design_matrix)+'"'
			
			name = k
			tmp = multireplace(command, {'name':name,\
				'design_matrix':design_matrix,\
				'selected_samples':t+","+c\
				})
			commands.append(tmp)

		# prepare input list, the LSF job is to go through every line
		command_input = self.args.jid + ".MLE.input"
		write_file(command_input,"\n".join(commands))
		dos2unix(command_input)
		self.outputs_dict['log_files'].append(command_input)
		
		# step 2 
		# define 10 LSF parameters
		self.parameter_dict['output_message']=self.args.jid +".mageck_MLE.message"
		self.parameter_dict['number_cores']=8
		self.parameter_dict['queue']="standard"
		self.parameter_dict['memory_request']=2000
		self.parameter_dict['job_id']="mageck_MLE"
		self.parameter_dict['sample_list']=command_input
		self.parameter_dict['number_lines']=len(commands)
		# depends on mageck_count
		dependencies = ['module load python/2.7.5']
		if self.dep:
			dependencies=['#BSUB -w "ended('+self.submission_id_dict['mageck_count']+')"']+dependencies
		self.parameter_dict['dependencies']="\n".join(dependencies)
		self.parameter_dict['commands']="${LINE}"
		self.parameter_dict['job_script_file']=self.args.jid +".mageck_MLE.lsf"

		# step 3
		# submit job
		self.submit_array_job()

		# step 4
		# organize output
		# test_MLE.gene_summary.txt  test_MLE.log  test_MLE.sgrna_summary.txt

		self.outputs_dict['mageck_MLE_files'] = []
		for k in self.pairwise_comparisons:
			name = k
			self.outputs_dict['log_files'].append(name+"_MLE_results.log")
			self.outputs_dict['log_files'].append(name+"_MLE_results.sgrna_summary.txt")
			self.outputs_dict['mageck_MLE_files'].append(name+"_MLE_results.gene_summary.txt")





		pass

	# def run_fastqc(self):

	# 	pass



def run_upload_tracks(jid,bw_files,bw_types,dir=False):
	# username = getpass.getuser()
	file = open(p_dir+"../misc/AT847CE", 'rb')
	password = pickle.load(file)
	file.close()

	# print "connecting to server"
	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname="10.220.19.239",username="yli11",password=password)

	if dir:
		# print "creating user's dir"
		stdin,stdout,stderr=ssh_client.exec_command("mkdir /research/rgs01/resgen/legacy/gb_customTracks/tp/HemPipelines/"+username)
		stdin,stdout,stderr=ssh_client.exec_command("mkdir /research/rgs01/resgen/legacy/gb_customTracks/tp/HemPipelines/"+username+"/"+jid)
	user_dir = "/research/rgs01/resgen/legacy/gb_customTracks/tp/HemPipelines/"+username+"/"+jid+"/"

	# print "generating json file"
	tracks_template = '{"type":"bigwig","scale":{"auto": 1},"file": "{{relative_path}}","stackheight":20,"stackspace":1,"onerow":1,"name":"{{track_name}}"}'
	tmp_file = "/tmp/"+str(uuid.uuid4()).split("-")[-1]
	tmp_file_handle = open(tmp_file,"wb")
	tracks_json_list=[]
	for b in bw_files:
		tmp = tracks_template.replace("{{relative_path}}","HemPipelines/"+username+"/"+jid+"/"+b)
		tmp = tmp.replace("{{track_name}}",b.replace("."+bw_types,""))
		tracks_json_list.append(tmp)
	lines = open(p_dir+"../misc/template_browser.json").readlines()
	lines = "".join(lines)
	lines = lines.replace("{{study_name}}",jid)	
	lines = lines.replace("{{tracks_json_list}}",",\n".join(tracks_json_list))	
	print >>tmp_file_handle,lines
	tmp_file_handle.close()
	# print "transfering file"
	ftp_client=ssh_client.open_sftp()
	for b in bw_files:
		ftp_client.put(b,user_dir+b)
	ftp_client.put(tmp_file,user_dir+bw_types+".json")
	ftp_client.close()

	myURL = "https://ppr.stjude.org/?study=HemPipelines/UserName/UserJobID/{{tracks}}.json"
	myURL = myURL.replace("UserName",username)
	myURL = myURL.replace("UserJobID",jid)
	myURL = myURL.replace("{{tracks}}",bw_types)
	return myURL	


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


	files = glob.glob("*.fastq.gz")
	files_array = map(lambda x:re.split('_|-|\.',x),files)
	myDict = {}
	
	for i in range(len(files_array)):
		myDict[files[i]] = []
		for j in range(len(files_array)):
			if fastq_pair(files_array[i],files_array[j]):
				myDict[files[i]].append(files[j])
	flag = False
	fname = "fastq.tsv"
	if os.path.isfile(fname):
		# print fname,"exists!"
		fname = "fastq."+str(uuid.uuid4()).split("-")[-1]+".tsv"
		# print "Will use new file name:",fname
	f = open(fname,"wb")
	used_files = []
	for k in myDict:
		if len(myDict[k]) != 1:
			# print "FILE:",k,"didn't find a pair",myDict[k]
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
			print >>f,"\t".join([f1,f2,label])
			used_files.append(f1)
			used_files.append(f2)
	unused_files = list(set(files) - set(used_files))	
	f.close()
	flag = False
	if len(unused_files) == 0:
		# print "Input fastq files preparation complete! ALL GOOD!"
		# print "Please check if you like the computer-generated labels in :",fname
		flag = True
	else:
		# print "Input fastq files preparation complete! There are some unmatched files."
		for f in unused_files:
			print (f)
	# return flag,fname

def prepare_single_end_input():
	
	files = glob.glob("*.fastq.gz")
	fname = "fastq.tsv"
	if os.path.isfile(fname):
		# print fname,"exists!"
		fname = "fastq."+str(uuid.uuid4()).split("-")[-1]+".tsv"
		# print "Will use new file name:",fname
	f = open(fname,"wb")
	for fastq in files:
		label = define_fastq_label(fastq)
		if len(label) == 0:
			label = fastq[:5]		
		print >>f,"\t".join([fastq,label])
	# print "Input fastq files preparation complete! ALL GOOD!"
	f.close()
	# return True,fname

def find_control(myList):
	for x in myList:
		if "igg" in x.lower():
			return x
		if 'input' in x.lower():
			return x
	return "no_control_found"
def prepare_design_matrix(file):
	# any item matched to "igg" or "input" will be used as control, all other samples will be treatment
	items = map(lambda x:x.strip().split()[-1],open(file).readlines())
	control = find_control(items)
	if control == "no_control_found":
		# print "No control sample found."
		return 1
	fname = "peakcall.tsv"
	if os.path.isfile(fname):
		# print fname,"exists!"
		fname = "peakcall."+str(uuid.uuid4()).split("-")[-1]+".tsv"
		# print "Will use new file name:",fname
	f = open(fname,"wb")


	for i in items:
		if i == control:
			continue	
		print >>f,"\t".join([i,control,i+".vs."+control])
	# print "Input peakcall file preparation complete! File name:",fname	
	f.close()
	pass




