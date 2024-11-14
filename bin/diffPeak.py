#!/hpcf/apps/python/install/2.7.12/bin/python
from __future__ import print_function,division
import sys
print ("Your python version is :",sys.version_info[0])
import logging
import argparse
import os
import subprocess 
import re
import getpass
import datetime
import uuid
import pandas as pd
from joblib import Parallel, delayed
import numpy as np

# module load subread bedtools R/3.6.1 homer/4.9.1

username = getpass.getuser()

parser = argparse.ArgumentParser(prog='DiffPeak')

parser.add_argument('-b',"--bams",  help="list of bam files (include path to file)")

parser.add_argument('-d', "--design_matrix", help="Each line is a group. Every group will be compared against the 'control' group. So you have to specify a control group in your input. The format for each line is: group_id:file_name_1,file_name_2. Just need file name, no need for the path to file.")

parser.add_argument('-p','--peaks',  help="list of narrowPeak files (include path to file), need the last line to be empty (i.e. so as to have the newline character).")

parser.add_argument('-x','--dry_run',  help=" 1 or 0. 1: dry run, to check system commands", default=0)

parser.add_argument('-z','--submit_job',  help=" 1 or 0. 1: submit this job to HPC", default=0)

parser.add_argument('-r','--flag',  help=" 1 or 0. 1: run this job in terminal. 0: submit this job.", default=1)

parser.add_argument('--include_unmapped_reads',  help="Expecting global change, need normalization by total reads", action='store_true')

parser.add_argument('-s','--single', help="run featureCount in single-end mode", action='store_true')

parser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='DiffPeak_'+username+"_"+str(datetime.date.today()))

args = parser.parse_args()

if len(sys.argv)==1:
	parser.print_help(sys.stderr)
	sys.exit(1)

if os.path.isdir(args.jid):
	addon_string = str(uuid.uuid4()).split("-")[-1]
	print ("The input job id is not available!")
	args.jid = args.jid+"_"+addon_string
	print ("The new job id is:",args.jid)
else:
	print ("The job id is:",args.jid)

def dry_run(files1):
	print("DRY RUN: check if all input files exist")
	file_exist_flag = True
	for fname in files1:
		if not os.path.isfile(fname):
			print(fname+" NOT FOUND. Please check your input file: "+args.input)
			file_exist_flag = False
	if file_exist_flag:
		print ("LOOKS GOOD! Dry run PASSED! Please proceed without -x option!")
	else:
		print ("Something is wrong! Please check the above error messages.")
def parse_list_files(file):
	my_list = []
	with open(file) as f:
		for line in f:
			line = line.strip()
			if len(line) >= 1:
				my_list.append(line)
	return my_list
def parse_design_matrix(file):
	my_dict = {}
	with open(file) as f:
		for line in f:
			try:
				line = line.strip().split(":")
				my_dict[line[0]] = line[1].split(",")
			except:
				continue
	return my_dict	

bam_list = parse_list_files(args.bams)
peaks_list = parse_list_files(args.peaks)
design_matrix = parse_design_matrix(args.design_matrix)
if args.dry_run:
	dry_run(bam_list+peaks_list)
	exit()

if int(args.submit_job):
	if args.include_unmapped_reads:
		command = 'bsub -P DiffPeak -q priority -J '+args.jid+' -n 4 -R "rusage[mem=10000] span[hosts=1]" -o ' + args.jid + "/log_files/DiffPeak.out -e " + args.jid + "/log_files/DiffPeak.err " + '"module purge;module load python/2.7.12;module load subread bedtools R/3.6.1 homer/4.9.1; diffPeak.py'+' -b '+args.bams+' -d '+args.design_matrix+'  -p '+args.peaks + ' --include_unmapped_reads"' 
	else:
		command = 'bsub -P DiffPeak -q priority -J '+args.jid+' -n 4 -R "rusage[mem=10000] span[hosts=1]" -o ' + args.jid + "/log_files/DiffPeak.out -e " + args.jid + "/log_files/DiffPeak.err " + '"module purge;module load python/2.7.12;module load subread bedtools R/3.6.1 homer/4.9.1; diffPeak.py'+' -b '+args.bams+' -d '+args.design_matrix+'  -p '+args.peaks + '"'
	command = command + " -j " + args.jid
	os.system(command)
	print ("Once the job is finished, you will be notified by email, with a summary of differential peaks, all motif discovery results from Homer2, and bedgraph files of differential peaks (logFC and logFDR).")
	exit()
	


## set up logging system, please use rootLogger to send messages to users
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
fileHandler = logging.FileHandler(args.jid+".log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.INFO)
run_flag = args.flag

def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()


def multireplace(string, replacements):
	substrs = sorted(replacements, key=len, reverse=True)
	regexp = re.compile('|'.join(map(re.escape, substrs)))
	return regexp.sub(lambda match: replacements[match.group(0)], string)

def merge_bed(narrowPeaks,UID):
	command = 'cat sample_list | while read i;do cat $i;done | sort -k1,1 -k2,2n | bedtools merge -c 4 -o collapse -i - > UID_name.merged.bed'
	command = command.replace("sample_list",narrowPeaks)
	command = command.replace("UID_name",UID)
	# print (command)
	if run_flag:
		os.system(command)
		return 1
	else:
		return [command]

def count_reads(bamfile_list,UID,flag):
	command_list = []
	command = """echo "GeneID Chr Start End Strand" | sed 's/ /\\t/g' > UID_name.merged.saf; awk '{print "region_"NR"\\t"$1"\\t"$2"\\t"$3"\\t+"}' UID_name.merged.bed >> UID_name.merged.saf ; featureCounts -p -F SAF -T 8 -Q 0 -a UID_name.merged.saf -o UID_name.count_table.bed bamfile_list"""
	if args.single:
		command = command.replace("featureCounts -p ","featureCounts ")
	command = command.replace("UID_name",UID)
	command = command.replace("bamfile_list"," ".join(bamfile_list))
	# print (command)
	# os.system(command)
	command_list.append(command)
	input_file = "UID_name.count_table.bed".replace("UID_name",UID)
	if flag:
		command = """python -c 'import pandas as pd;df = pd.read_csv("{{UID}}.count_table.bed",sep="\\t",skiprows=1);df2 = pd.read_csv("{{UID}}.count_table.bed.summary",sep="\\t",index_col=0);df.columns = map(lambda x:x.split("/")[-1],df.columns.tolist());nrows = df.shape[0];df.loc[nrows+1]=["Unassigned_Ambiguity","chr1","1","2","+","2"]+df2.loc["Unassigned_Ambiguity"].tolist();df.loc[nrows+2]=["Unassigned_NoFeatures","chr1","3","4","+","2"]+df2.loc["Unassigned_NoFeatures"].tolist();df.to_csv("{{UID}}.count_table.bed",index=False,sep="\\t")'"""
	else:
		command = """python -c 'import pandas as pd;df = pd.read_csv("{{UID}}.count_table.bed",sep="\\t",skiprows=1);df.columns = map(lambda x:x.split("/")[-1],df.columns.tolist());df.to_csv("{{UID}}.count_table.bed",index=False,sep="\\t")'"""
	
	# command = command.replace("{{input_file}}",input_file)
	command = command.replace("{{UID}}",UID)
	print (command)
	command_list.append(command)
	if run_flag:
		map(lambda x:os.system(x),command_list)
		return 1
	else:
		return command_list	
	

def split_called_DiffPeaks(file):

	df = pd.read_csv(file,sep="\t",index_col=0)
	df['Strand'] = 0
	# logFC > 0 is loss in treatment
	bdg_files = to_bed_graph(df,file.split(".diffRegions")[0])
	df[(df['adj.P.Val']<=1)&(df['logFC']>0)][['Chr','Start','End','Strand']].head(n=100).to_csv(file+".loss.bed",sep="\t",header=False)
	df[(df['adj.P.Val']<=1)&(df['logFC']<0)][['Chr','Start','End','Strand']].head(n=100).to_csv(file+".gain.bed",sep="\t",header=False)
	return bdg_files
	

def run_hommer(design_matrix):
	command_list = []
	diffPeak_files = []
	bdg_files = []
	homer_html_files = []
	for k in design_matrix:
		if k == 'control':
			continue
		file = 'control-'+k+".diffRegions.txt"
		diffPeak_files.append(file)
		bdg_files += split_called_DiffPeaks(file)
		
		tmp_file1 = str(uuid.uuid4()).split("-")[-1]
		tmp_file2 = str(uuid.uuid4()).split("-")[-1]
		command = "findMotifsGenome.pl " + file + ".loss.bed hg19 "+ 'control-'+k +"_loss_Motifs_results -size 200 -mask -p 8 -preparsedDir /tmp/"+tmp_file1
		command_list.append(command)
		command = "findMotifsGenome.pl " + file + ".gain.bed hg19 "+ 'control-'+k +"_gain_Motifs_results -size 200 -mask -p 8 -preparsedDir /tmp/"+tmp_file2
		command_list.append(command)
		command_list.append("rm -rf /tmp/"+tmp_file1)
		command_list.append("rm -rf /tmp/"+tmp_file2)
		old_loss_html = 'control-'+k +"_loss_Motifs_results/homerResults.html"
		new_loss_html = 'control-'+k +"_loss_Motifs_results/"+'control-'+k+".loss.homerMotifs.html"
		command_list.append("mv "+old_loss_html + " " +new_loss_html)
		old_gain_html = 'control-'+k +"_gain_Motifs_results/homerResults.html"
		new_gain_html = 'control-'+k +"_gain_Motifs_results/"+'control-'+k+".gain.homerMotifs.html"
		command_list.append("mv "+old_gain_html+ " "  + new_gain_html)
		homer_html_files.append(new_loss_html)
		homer_html_files.append(new_gain_html)
	if run_flag:
		map(lambda x:os.system(x),command_list)
		print ("\n".join(command_list))
		return 1,diffPeak_files,bdg_files,homer_html_files
	else:
		return command_list,diffPeak_files,bdg_files,homer_html_files



def run_DESEQ2(design_matrix,UID):
	input_list = []
	for k in design_matrix:
		if k == 'control':
			continue
		tmp = 'control ' + k + " " + ",".join(design_matrix['control']) + " " + ",".join(design_matrix[k]) + " 0.01 .  UID_name.count_table.bed".replace("UID_name",UID)
		input_list.append(tmp)
	command = "/hpcf/authorized_apps/rhel7_apps/R/install/3.6.1/bin/Rscript --version;/hpcf/authorized_apps/rhel7_apps/R/install/3.6.1/bin/Rscript --vanilla /research/dept/hem/common/sequencing/chenggrp/pipelines/misc/DESeq2.R args"
	#print input_list
	for args in input_list:
		print (command.replace('args',args))
	#print run_flag
	if run_flag:
		Parallel(n_jobs=8)(delayed(os.system)(command.replace('args',args)) for args in input_list)
		return 1
	else:
		return map(lambda x:x.replace('args',args),input_list)


def to_bed_graph(df,prefix):
	header = 'track type=bedGraph name="{{track_name}}" description="BedGraph" visibility=full color=255,0,0 altColor=0,0,255 priority=20 smoothingWindow=10'
	df['adj.P.Val'] = df['adj.P.Val'].fillna(1)
	df = df[df['adj.P.Val'] < 0.01]
	df['logFC'] = df['logFC'].fillna(0)
	df['logFC'] = -df['logFC']
	df['log10FDR'] = -np.log10(df['adj.P.Val'])
	bdg_files = []
	for col in ['logFC','log10FDR']:
		out_file = prefix+"."+col+".bdg"	
		df[['Chr','Start','End']+[col]].to_csv(out_file,sep="\t",header=False,index=False)
		command = """sed -i '1s/^/HEADER\\n/' """.replace("HEADER",header.replace("{{track_name}}",out_file))+out_file
		os.system(command)	
		bdg_files.append(out_file)
	return bdg_files

if run_flag:
	rootLogger.info("merge_bed")
	merge_bed(args.peaks,args.jid)
	if args.include_unmapped_reads:
		rootLogger.info("count_reads: include_unmapped_reads")
	count_reads(bam_list,args.jid,args.include_unmapped_reads)
	rootLogger.info("run_DESEQ2")
	run_DESEQ2(design_matrix,args.jid)
	rootLogger.info("run_hommer")
	tmp,diffPeak_files,bdg_files,homer_html_files=run_hommer(design_matrix)
	commands = []
	commands.append("zip "+args.jid+".IGV.bdg.zip " + " ".join(bdg_files))
	
	html_command = 'python /research/dept/hem/common/sequencing/chenggrp/pipelines/misc/diffPeak_report.py '+args.jid+' diffPeak '+",".join(diffPeak_files) + " " + ",".join(homer_html_files+[args.jid+".IGV.bdg.zip"])
	commands.append(html_command)	
	commands.append("mkdir "+args.jid)
	commands.append("mkdir "+args.jid+"/homer_motifs")
	commands.append("mkdir "+args.jid+"/DEseq2_results")
	commands.append("mkdir "+args.jid+"/bdg_files")
	commands.append("mkdir "+args.jid+"/log_files")
	
	for k in design_matrix:
		if k == 'control':
			continue
		gain = 'control-'+k+"_gain_Motifs_results "
		loss = 'control-'+k+"_loss_Motifs_results "
		command = "mv -f " +gain+ args.jid+"/homer_motifs"
		commands.append(command)		
		command = "mv -f " +loss+ args.jid+"/homer_motifs"
		commands.append(command)
		command = "mv " +'control-'+k + ".diffRegions.* " + args.jid+"/homer_motifs"
		commands.append(command)
		command = "mv " +'control-*pdf ' + args.jid+"/homer_motifs"
		commands.append(command)
		command = "mv " +'control-'+k + "*.bdg " + args.jid+"/bdg_files"
		commands.append(command)
	command = "mv " + args.jid+".IGV.bdg.zip " + args.jid
	commands.append(command)
	command = "mv "+ args.jid+".merged.bed " + args.jid
	commands.append(command)
	command = "mv "+ args.jid+".count_table.bed* " + args.jid+"/DEseq2_results"
	commands.append(command)
	commands.append("rm "+args.jid+".merged.saf")	
	outfile = args.jid+".report.html"
	commands.append("mv "+outfile+" "+args.jid)


	commands.append("mv "+args.jid+".log "+args.jid+"/log_files")

	map(lambda x:os.system(x),commands)








