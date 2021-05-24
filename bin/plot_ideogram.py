#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
import json


"""
Every python wrapper is supposed to be similar, since they are using the same convention.

The only thing need to be changed is the guess_input function and the argparser function.

look for ## CHANGE THE FUNCTION HERE FOR DIFFERENT WRAPPER

variable inherents from utils:
myData
myPars
myPipelines
"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',"--output",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today())+".html")
	mainParser.add_argument("--organism", help="possible choice: Human,Mouse,Arabidopsis thaliana", default="Human")
	mainParser.add_argument("--assembly", help="GRCh38,GRCh37,GRCm38,MGSCv37,TAIR10", default="GRCh38")
	mainParser.add_argument('file', type=str, nargs='+',help="input bed files, the first 3 columns should be chr, start, end, additional columns will be ignored. Multiple files should be separated by space, you can use *.bed to include all bed filess in the current dir.")

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
def send_email(attachments):
	username = getpass.getuser()
	command = 'echo "Hi User_name,\n\nSee attachment. Your results have been generated in the following directory:\n RESULT_DIR" | mailx {{attachments}} -s "plot ideogram is finished" -- User_name@stjude.org'
	attachments_string = map(lambda x: '-a "'+x+'" ',attachments)
	command = command.replace("{{attachments}}","".join(attachments_string))
	command = command.replace("User_name",username)
	command = command.replace("RESULT_DIR",os.getcwd())
	# print (command)
	os.system(command)
def multi_replace(myString,myDict):
	for k in myDict:
		myString = myString.replace("{{"+k+"}}",str(myDict[k]))
	return myString
def row_apply(r):
	return [r['name'],r['start'],0,r['index']]

	
def df_to_json(df):
	chr_list = df['chr'].unique().tolist()
	my_dict_list = []
	for c in chr_list:
		tmp={}
		tmp['chr'] = c.split("chr")[-1]
		tmp['annots'] = df[df['chr']==c].apply(row_apply,axis=1).tolist()
		my_dict_list.append(tmp)
	return json.dumps(my_dict_list)


def create_ideogram_track(f,organism,assembly):

	JS_template = """
  <h2>File: {{FileName}} has {{Total_number}} regions.</h2>
  <div id="{{FileID}}"></div>
  <hr>
  <script type="text/javascript">

    var annotationTracks = [{id: 'red_arrow1',color: "red"},{id: 'red_arrow2', color: "red"},{id: 'red_arrow3', color: "red"},{id: 'red_arrow4', color: "red"}];
    var locations =  {"keys": ["name","start","length","trackIndex"],"annots": {{annots_list_dict}}};
    var config = {organism: '{{organism}}',assembly: '{{assembly}}',container: '#{{FileID}}',chrHeight: 600,orientation: 'vertical',annotations: locations,annotationTracks: annotationTracks};
    var ideogram = new Ideogram(config);
  </script>  	
	"""
	df = read_bed(f)
	df = find_index(df)
	# print (df.head())
	parameter_dict = {}
	parameter_dict['FileName'] = f
	parameter_dict['FileID'] = "C"+str(uuid.uuid4()).split("-")[-1]
	parameter_dict['Total_number'] = df.shape[0]
	parameter_dict['organism'] = organism
	parameter_dict['assembly'] = assembly
	parameter_dict['annots_list_dict'] = df_to_json(df)
	JS_template = multi_replace(JS_template,parameter_dict)
	# print (JS_template)
	return JS_template


def generate_html(ideogram_list):
	HTML_template = """
<head>
  <script src="https://unpkg.com/ideogram@1.12.0/dist/js/ideogram.min.js"></script>
</head>
<body>
  <hr>  
  {{IDEOGRAM_TRACKS}}
</body>	
	
	"""
	HTML_template = HTML_template.replace("{{IDEOGRAM_TRACKS}}",ideogram_list)
	return HTML_template
	
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()
def read_bed(f):
	df = pd.read_csv(f,sep="\t",header=None)
	df['chr'] = df[0]
	df['start'] = df[1]
	df['end'] = df[2]
	df['name'] = df[0]+":"+df[1].astype(str)+"-"+df[2].astype(str)
	return df	
def find_index(df):
	df = df.sort_values([0,1])
	df['index'] = 0
	tmp = df.copy()
	tmp[1] = tmp[1].diff(periods=1) 
	# df.loc[df.A==0, 'B'] = np.nan
	cutoff = 2000
	df.loc[tmp[(tmp[1]>0)&(tmp[1]<=20*cutoff)].index,'index'] = 1
	# print (df.loc[tmp[(tmp[1]>0)&(tmp[1]<=20*cutoff)].index,'index'])
	# tmp[(tmp[1]>20*cutoff)&(tmp[1]<=40*cutoff)]['index'] = 2
	df.loc[tmp[(tmp[1]>20*cutoff)&(tmp[1]<=40*cutoff)].index,'index'] = 2
	# tmp[(tmp[1]>40*cutoff)&(tmp[1]<=60*cutoff)]['index'] = 3
	df.loc[tmp[(tmp[1]>40*cutoff)&(tmp[1]<=60*cutoff)].index,'index'] = 3
	# print tmp[(tmp[1]>0)&(tmp[1]<=20*cutoff)]
	# df['index'] = tmp['index']
	# print (df)
	return df
def main():

	args = my_args()
	ideogram_list = []
	for f in args.file:
		# print (f)
			
		html_div = create_ideogram_track(f,args.organism,args.assembly)
		ideogram_list.append(html_div)

	html_string = generate_html("\n<hr>".join(ideogram_list))	

	write_file(args.output,html_string)
	send_email([args.output])

	
if __name__ == "__main__":
	main()


















































