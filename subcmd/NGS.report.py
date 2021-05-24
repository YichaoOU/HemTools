#!/hpcf/apps/python/install/2.7.13/bin/python
from __future__ import print_function,division
import re
import pandas as pd
import glob
import datetime
import os
import getpass
import sys
import zipfile
# suppose to work on Python 2
flagstat_regexes = {
	'total':		 r"(\d+) \+ (\d+) in total \(QC-passed reads \+ QC-failed reads\)",
	'secondary':	 r"(\d+) \+ (\d+) secondary",
	'supplementary': r"(\d+) \+ (\d+) supplementary",
	'duplicates':	r"(\d+) \+ (\d+) duplicates",
	'mapped':		r"(\d+) \+ (\d+) mapped \((.+):(.+)\)",
	'paired in sequencing': r"(\d+) \+ (\d+) paired in sequencing",
	'read1':		 r"(\d+) \+ (\d+) read1",
	'read2':		 r"(\d+) \+ (\d+) read2",
	'properly paired': r"(\d+) \+ (\d+) properly paired \((.+):(.+)\)",
	'with itself and mate mapped': r"(\d+) \+ (\d+) with itself and mate mapped",
	'singletons':	r"(\d+) \+ (\d+) singletons \((.+):(.+)\)",
	'with mate mapped to a different chr': r"(\d+) \+ (\d+) with mate mapped to a different chr",
	'with mate mapped to a different chr (mapQ >= 5)': r"(\d+) \+ (\d+) with mate mapped to a different chr \(mapQ>=5\)",
}

def send_email(jid_id,attachment):
	username = getpass.getuser()
	command = 'echo "Hi User_name,\n\nYour JOB_ID is finished. Please see the attachment for QC reports. The results have been generated the following directory:\n RESULT_DIR" | mailx -a "attachment_file" -s "JOB_ID is finished" -- User_name@stjude.org'
	command = command.replace("JOB_ID",jid_id)
	command = command.replace("attachment_file",attachment)
	command = command.replace("User_name",username)
	command = command.replace("RESULT_DIR",os.getcwd()+"/"+jid_id+"/")
	os.system(command)

class Fadapa(object):
	def __init__(self, file_name):
		self.file_name = file_name
		archive = zipfile.ZipFile(file_name, 'r')
		# print (archive.namelist())
		self._content = archive.read(file_name.replace(".zip","")+'/fastqc_data.txt').splitlines()
		self._m_mark = '>>'
		self._m_end = '>>END_MODULE'
	def summary(self):
		modules = [line.split('\t') for line in self._content
				   if self._m_mark in line and self._m_end not in line]
		data = [[i[2:], j] for i, j in modules]
		data.insert(0, ['Module Name', 'Status'])
		return data
def parse_fastqc(fname):
	f = Fadapa(fname)
	df = pd.DataFrame(f.summary())
	df.columns = df.loc[0]
	df = df.loc[1:]
	df = df.set_index('Module Name')
	del df.index.name
	df.columns = [fname]
	return df
def parse_single_report(file_obj):
	"""
	Take a filename, parse the data assuming it's a flagstat file
	Returns a dictionary {'lineName_pass' : value, 'lineName_fail' : value}
	"""
	parsed_data = {}

	re_groups = ['passed', 'failed', 'passed_pct', 'failed_pct']
	for k, r in flagstat_regexes.items():
		# print r
		r_search = re.search(r, file_obj, re.MULTILINE)
		if r_search:
			for i,j in enumerate(re_groups):
				try:
					key = "{}_{}".format(k, j)
					val = r_search.group(i+1).strip('% ')
					parsed_data[key] = float(val) if ('.' in val) else int(val)
				except IndexError:
					pass # Not all regexes have percentages
				except ValueError:
					parsed_data[key] = float('nan')
	# Work out the total read count
	try:
		parsed_data['flagstat_total'] = parsed_data['total_passed'] + parsed_data['total_failed']
	except KeyError:
		pass
	
	
	parsed_data['duplication_rate_pct'] = (float(parsed_data['duplicates_passed']+parsed_data['duplicates_failed'])/parsed_data['flagstat_total'] )*100
	# for k in parsed_data:
		# if "" in k:
			# parsed_data[k]  = str(parsed_data[k]) + "%"
	return parsed_data


def generate_report(job_id,pipeline_type,fastq_file_list,uid_list):
	HTML_template = """
	
<html>
	<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js">	</script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js">	</script>
	<style  type="text/css" >  

		.blank.level0 {
			display: none;
		}
		.row_heading {
			display: none;
		}
	</style>
	</head>
	<body>
		<div name="content" class="container">
			<div class="row">
				<div class="col-xs-9">
					<h1>{{JOB_ID}}</h1>
					<h4>Number of samples: {{Num_sample}}</h4>
					<h4>Report generated at : {{generation_time}}</h4>
					<h4>Pipeline type: {{pipeline_type}}</h4>
					<h4>Aligner: BWA 0.7.16a</h4>
					<h4>Peak caller: macs2 2.1.1</h4>
					<h4>Contact: Yichao.Li@stjude.org or Yong.Cheng@stjude.org</h4>
					<hr>
					<h1>FASTQC report</h1>
					{{fastqc_df}}
					<hr>
					<h1>Alignment report</h1>
					<h2>Flagstat (raw BAM)</h2>
					{{raw_bam_df}}
					<h2>Flagstat (chrM BAM)</h2>
					{{chrm_bam_df}}
					<h2>Flagstat (non-chrM BAM)</h2>
					{{nonchrm_bam_df}}
					<h2>Library complexity (filtered non-mito BAM)</h2>
					{{complexity_df}}

				</div>	
			</div>
		</div>
	</body>
</html>	
	"""

	# fastqc
	df_list = map(lambda x:parse_fastqc(x.replace(".fastq.gz","_fastqc.zip").replace(".fastq","_fastqc.zip")),fastq_file_list)
	fastqc_df = pd.concat(df_list,axis=1)
	HTML_template = HTML_template.replace("{{fastqc_df}}",fastqc_df.to_html().replace("dataframe","table table-striped table-hover").replace("_"," ").replace("fastqc","").replace(".zip","").replace("fail",'<span style="color:red;font-weight:bold">fail</span>').replace("warn",'<span style="color:orange">warn</span>'))	
	
	# raw bam
	file_list = map(lambda x:x+".markdup.report",uid_list)
	df_list = []
	for i in range(len(file_list)):
		file = file_list[i]
		df = parse_single_report("".join(open(file).readlines()))
		df = pd.DataFrame.from_dict(df,orient='index')
		df.columns  = [uid_list[i]]
		df_list.append(df.loc[['mapped_passed', 'total_passed', 'total_failed', 'mapped_passed_pct', 'read1_passed','read2_passed', 'properly paired_failed', 'properly paired_passed_pct','duplicates_passed','duplicates_failed', 'duplication_rate_pct','secondary_passed', 'paired in sequencing_failed',   'read1_failed', 'with mate mapped to a different chr_passed',  'singletons_passed', 'supplementary_passed', 'singletons_passed_pct', 'mapped_failed_pct', 'supplementary_failed', 'with itself and mate mapped_failed', 'mapped_failed', 'flagstat_total', 'with mate mapped to a different chr (mapQ >= 5)_passed', 'properly paired_failed_pct', 'with mate mapped to a different chr (mapQ >= 5)_failed', 'with itself and mate mapped_passed', 'read2_failed', 'with mate mapped to a different chr_failed', 'properly paired_passed', 'paired in sequencing_passed', 'singletons_failed', 'secondary_failed', 'singletons_failed_pct']])
	raw_bam_df = pd.concat(df_list,axis=1)	
	# print raw_bam_df.head()
	raw_bam_df = raw_bam_df.loc[['mapped_passed', 'total_passed','mapped_passed_pct','properly paired_passed','properly paired_passed_pct','duplicates_passed','duplication_rate_pct']]
	
	
	file_list = map(lambda x:x+".markdup.chrM.report",uid_list)
	df_list = []
	for i in range(len(file_list)):
		file = file_list[i]
		df = parse_single_report("".join(open(file).readlines()))
		df = pd.DataFrame.from_dict(df,orient='index')
		df.columns  = [uid_list[i]]
		df_list.append(df.loc[['mapped_passed', 'total_passed', 'total_failed', 'mapped_passed_pct', 'read1_passed','read2_passed', 'properly paired_failed', 'properly paired_passed_pct','duplicates_passed','duplicates_failed', 'duplication_rate_pct','secondary_passed', 'paired in sequencing_failed',   'read1_failed', 'with mate mapped to a different chr_passed',  'singletons_passed', 'supplementary_passed', 'singletons_passed_pct', 'mapped_failed_pct', 'supplementary_failed', 'with itself and mate mapped_failed', 'mapped_failed', 'flagstat_total', 'with mate mapped to a different chr (mapQ >= 5)_passed', 'properly paired_failed_pct', 'with mate mapped to a different chr (mapQ >= 5)_failed', 'with itself and mate mapped_passed', 'read2_failed', 'with mate mapped to a different chr_failed', 'properly paired_passed', 'paired in sequencing_passed', 'singletons_failed', 'secondary_failed', 'singletons_failed_pct']])
	chrm_bam_df = pd.concat(df_list,axis=1)	
	# print (chrm_bam_df)
	chrm_bam_df = chrm_bam_df.loc[['mapped_passed', 'total_passed','mapped_passed_pct','properly paired_passed','properly paired_passed_pct','duplicates_passed','duplication_rate_pct']]
	
		
	
	nonchrm_bam_df = raw_bam_df - chrm_bam_df
	nonchrm_bam_df = pd.DataFrame(columns=uid_list)
	nonchrm_bam_df.loc['total_passed'] = raw_bam_df.loc['total_passed'] - chrm_bam_df.loc['total_passed']
	nonchrm_bam_df.loc['duplicates_passed'] = raw_bam_df.loc['duplicates_passed'] - chrm_bam_df.loc['duplicates_passed']
	nonchrm_bam_df.loc['mapped_passed'] = raw_bam_df.loc['mapped_passed'] - chrm_bam_df.loc['mapped_passed']
	nonchrm_bam_df.loc['properly paired_passed'] = raw_bam_df.loc['properly paired_passed'] - chrm_bam_df.loc['properly paired_passed']
	nonchrm_bam_df.loc['duplication_rate'] = nonchrm_bam_df.loc['duplicates_passed']/nonchrm_bam_df.loc['total_passed']
	nonchrm_bam_df.loc['mapped_passed_pct'] = nonchrm_bam_df.loc['mapped_passed']/nonchrm_bam_df.loc['total_passed']
	nonchrm_bam_df.loc['properly paired_passed_pct'] = nonchrm_bam_df.loc['properly paired_passed']/nonchrm_bam_df.loc['total_passed']
	# nonchrm_bam_df['total_passed'] = raw_bam_df[''] - chrm_bam_df['']
	# print nonchrm_bam_df.head()
	
	file_list = map(lambda x:x+".lib.complexity",uid_list)
	df_list = []
	for i in range(len(file_list)):
		file = file_list[i]
		df = pd.read_csv(file,sep="\t",header=None)
		df.columns = ["Total Reads","Distinct Reads","One Read","Two Reads","NRF = Distinct/Total","PBC1 = OneRead/Distinct","PBC2 = OneRead/TwoReads"]
		df.index = [uid_list[i]]
		df_list.append(df)
	complexity_df = pd.concat(df_list)	
	complexity_df = complexity_df.T
	# print complexity_df.head()
	
	for k in raw_bam_df:
		if "_pct" in k:
			raw_bam_df[k]  = str(raw_bam_df[k]) + "%"	
	for k in chrm_bam_df:
		if "_pct" in k:
			chrm_bam_df[k]  = str(chrm_bam_df[k]) + "%"	
	for k in nonchrm_bam_df:
		if "_pct" in k:
			nonchrm_bam_df[k]  = str(nonchrm_bam_df[k]*100) + "%"	
			
	HTML_template = HTML_template.replace("{{raw_bam_df}}",raw_bam_df.astype(str).to_html(float_format=lambda x: '%10.2f' % x).replace("dataframe","table table-striped table-hover").replace("_"," ").replace("fastq","").replace(".report",""))
	HTML_template = HTML_template.replace("{{chrm_bam_df}}",chrm_bam_df.astype(str).to_html(float_format=lambda x: '%10.2f' % x).replace("dataframe","table table-striped table-hover").replace("_"," ").replace("fastq","").replace(".report",""))
	HTML_template = HTML_template.replace("{{nonchrm_bam_df}}",nonchrm_bam_df.astype(str).to_html(float_format=lambda x: '%10.2f' % x).replace("dataframe","table table-striped table-hover").replace("_"," ").replace("fastq","").replace(".report",""))
	HTML_template = HTML_template.replace("{{complexity_df}}",complexity_df.astype(str).to_html(float_format=lambda x: '%10.2f' % x).replace("dataframe","table table-striped table-hover").replace("_"," ").replace("fastq","").replace(".report",""))
	HTML_template = HTML_template.replace("{{Num_sample}}",str(nonchrm_bam_df.shape[1]))
	HTML_template = HTML_template.replace("{{generation_time}}",str(datetime.date.today()))
	HTML_template = HTML_template.replace("{{JOB_ID}}",job_id)
	HTML_template = HTML_template.replace("{{pipeline_type}}",pipeline_type)
	
	return HTML_template
	
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()
	
	
	
	
	
job_id = sys.argv[1]
pipeline_type = sys.argv[2]
fastq_file_list = sys.argv[3].split(",")
uid_list = sys.argv[4].split(",")
message = generate_report(job_id,pipeline_type,fastq_file_list,uid_list)
outfile = job_id+".report.html"
write_file(outfile,message)