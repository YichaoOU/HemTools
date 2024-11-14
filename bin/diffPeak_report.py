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

def send_email(jid_id,attachments):
	username = getpass.getuser()
	command = 'echo "Hi User_name,\n\nYour JOB_ID is finished. Please see the attachments for a summary of results. Your results have been generated in the following directory:\n RESULT_DIR" | mailx {{attachments}} -s "JOB_ID is finished" -- User_name@stjude.org'
	command = command.replace("JOB_ID",jid_id)
	attachments_string = map(lambda x: '-a "'+x+'" ',attachments)
	command = command.replace("{{attachments}}","".join(attachments_string))
	command = command.replace("User_name",username)
	command = command.replace("RESULT_DIR",os.getcwd()+"/"+jid_id+"/")
	# print (command)
	os.system(command)

def multi_replace(myString,myDict):
	for k in myDict:
		myString = myString.replace("{{"+k+"}}",str(myDict[k]))
	return myString

def create_gain_loss_ideogram_track(parameter_dict):
	JS_template = """
  <h2>{{title}}</h2>
  <h4>The number of differential peaks (FDR < 0.01): {{Num_diffPeaks}}</h4>
  <h4>The number of gain sites: {{Num_gainPeaks}}</h4>
  <h4>The number of loss sites: {{Num_lossPeaks}}</h4>
  <h4>Overview of the {{Num_displayed_gainPeaks}} gain sites and {{Num_displayed_lossPeaks}} loss sites. </h4>
  <div id="{{comparison_div_id}}"></div>
  <hr>
  <script type="text/javascript">
    var legend = [{
      name: 'Legend:', 
      rows: [ 
        {name: 'gain', color: 'red', shape: "triangle"},
        {name: 'loss', color: 'green', shape: "triangle"}
      ]
    }];
    var annotationTracks = [{id: 'gain',color: "red"},{id: 'loss', color: "green"}];
    var locations =  {"keys": ["name","start","length","trackIndex"],"annots": {{annots_list_dict}}};
    var config = {organism: 'human',assembly: 'GRCh37',container: '#{{comparison_div_id}}',chrHeight: 600,orientation: 'vertical',annotations: locations,annotationTracks: annotationTracks,legend: legend};
    var ideogram = new Ideogram(config);
  </script>  	
	"""
	JS_template = multi_replace(JS_template,parameter_dict)
	return JS_template
import json
def get_return_number(df,T=1000):
	# num gained, num loss, num display gain, num dispaly loss
	NumGain = df[df['logFC']<0].shape[0] 
	NumLoss = df[df['logFC']>0].shape[0]
	if df.shape[0] > T:
		tmp = df.head(T)
		NumDisplayedGain = tmp[tmp['logFC']<0].shape[0] 
		NumDisplayedLoss = tmp[tmp['logFC']>0].shape[0] 
		return [NumGain,NumLoss,NumDisplayedGain,NumDisplayedLoss,tmp]
	else:
		return [NumGain,NumLoss,NumGain,NumLoss,df]
def row_apply(r):
	if r['logFC'] < 0 :
		return [r['Geneid'],r['Start'],0,0]
	else:
		return [r['Geneid'],r['Start'],0,1]
def df_to_json(df):
	chr_list = df['Chr'].unique().tolist()
	my_dict_list = []
	for c in chr_list:
		tmp={}
		tmp['chr'] = c.split("chr")[-1]
		tmp['annots'] = df[df['Chr']==c].apply(row_apply,axis=1).tolist()
		my_dict_list.append(tmp)

	return json.dumps(my_dict_list)


def diffPeak_to_2tracks_json(bed_file):
	
	# transform bed files to list of dict so as to use ideogram.js to display an overview of diff peaks.
	# in my idea, each comparison will be displayed. Plus a figure of all gained sites and a figure of all loss sites if multiple comparison are given.
	# top 1000 diffPeaks will be shown
	# make a volcano plot, ask them to install enhanced volvaco
	df = pd.read_csv(bed_file,sep="\t")
	sig = df[df['adj.P.Val']<=0.01][['Geneid','Chr','Start','logFC','adj.P.Val']]
	sig = sig.sort_values('adj.P.Val')
	[NumGain,NumLoss,NumDisplayedGain,NumDisplayedLoss,sig] = get_return_number(sig,T=1000)
	annotationTracks = df_to_json(sig)

	return [NumGain,NumLoss,NumDisplayedGain,NumDisplayedLoss,annotationTracks]

def generate_report(parameter_dict,diffPeak_bed_files):
	HTML_template = """
<head>
  <script src="https://unpkg.com/ideogram@1.6.0/dist/js/ideogram.min.js"></script>
</head>
<body>
  <h1>{{JOB_ID}}</h1>
  <h4>Report generated on : {{generation_time}}</h4>
  <h4>Pipeline type: {{pipeline_type}}</h4>
  <h4>Steps: merge narrowPeak files, count raw reads, DESeq2, homer motif finding, ideogram visualization</h4>
  <h4>Contact: Yichao.Li@stjude.org or Yong.Cheng@stjude.org</h4>
  <hr>  
  {{IDEOGRAM_TRACKS}}
</body>	
	
	"""
	
	HTML_template = multi_replace(HTML_template,parameter_dict)
	IDEOGRAM_TRACKS_list = ""
	count = 1
	for f in diffPeak_bed_files:
		[NumGain,NumLoss,NumDisplayedGain,NumDisplayedLoss,annotationTracks] = diffPeak_to_2tracks_json(f)
		parameter_dict = {}
		parameter_dict['title'] = f.split("/")[-1]
		parameter_dict['Num_diffPeaks'] = NumGain+NumLoss
		parameter_dict['Num_gainPeaks'] = NumGain
		parameter_dict['Num_lossPeaks'] = NumLoss
		if parameter_dict['Num_diffPeaks'] > 1000:
			parameter_dict['Num_displayed_gainPeaks'] = "top 1000 differential peaks: "+str(NumDisplayedGain)
		else:
			parameter_dict['Num_displayed_gainPeaks'] = NumDisplayedGain
		parameter_dict['Num_displayed_lossPeaks'] = NumDisplayedLoss			
		parameter_dict['comparison_div_id'] = "container"+str(count)
		parameter_dict['annots_list_dict'] = annotationTracks
		IDEOGRAM_TRACKS_list = IDEOGRAM_TRACKS_list + create_gain_loss_ideogram_track(parameter_dict) + "\n"
		count += 1
	# print (IDEOGRAM_TRACKS_list)
	HTML_template = HTML_template.replace("{{IDEOGRAM_TRACKS}}",IDEOGRAM_TRACKS_list)
	return HTML_template
	
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()
	
	

parameter_dict = {}
parameter_dict['JOB_ID'] =  sys.argv[1]
parameter_dict['pipeline_type'] =  sys.argv[2]
parameter_dict['generation_time'] = str(datetime.date.today())
message = generate_report(parameter_dict,sys.argv[3].split(","))
outfile = parameter_dict['JOB_ID']+".report.html"
write_file(outfile,message)
attachments = sys.argv[4].split(",")
attachments.append(outfile)
send_email(parameter_dict['JOB_ID'],attachments)