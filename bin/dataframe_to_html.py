#!/hpcf/apps/python/install/2.7.13/bin/python
import os
import argparse
import subprocess
import glob
import pandas as pd
import uuid
import base64
import sys
import PIL
from PIL import Image
import cStringIO
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
cwd = os.getcwd()

"""Convert pandas dataframe to html

usage
-----

dataframe_to_html.py your_dataframe.csv output.html

There should be a header in your dataframe

"""
def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		myString = str(myString).replace("{{"+str(k)+"}}",str(myDict[k]))
	return myString

def resize_image(file,w,h):
	img = Image.open(file) # image extension *.png,*.jpg
	img = img.resize((w, h), Image.ANTIALIAS)
	buffer = cStringIO.StringIO()
	img.save(buffer, format="PNG")
	return base64.b64encode(buffer.getvalue())

html_template="""
<html>
<head>
<script type="text/javascript" src="https://code.jquery.com/jquery-1.12.1.min.js"></script> 
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/js/jquery.tablesorter.min.js"></script> 
<script type="text/javascript" src="https://raw.githubusercontent.com/YichaoOU/YichaoOU.github.io/9bd18765cc77a855b71dc491d895bf0968c7fe89/js/liyc.js"></script> 
<link rel="stylesheet" href="https://raw.githubusercontent.com/YichaoOU/YichaoOU.github.io/9bd18765cc77a855b71dc491d895bf0968c7fe89/css/liyc.css" type="text/css" media="print, projection, screen">
<style type="text/css">
	
td {
    height: 250px;
}
</style>
</head>
<body>
<p class="tip">
		<em>TIP!</em> Sort multiple columns simultaneously by holding down the shift key and clicking a second, third or even fourth column header!
</p>
<table id="myTable" class="tablesorter"> 
<col width="10">
<col width="10">
<thead> 
<tr> 
{{header_content}}
</tr> 
</thead> 
<tbody> 
{{table_content}}
</tbody> 
</table> 
</body>
</html>
"""

html_template2="""
<html>
<head>
<script type="text/javascript" src="https://code.jquery.com/jquery-1.12.1.min.js"></script> 
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/js/jquery.tablesorter.min.js"></script> 
<script type="text/javascript" src="https://raw.githubusercontent.com/YichaoOU/YichaoOU.github.io/9bd18765cc77a855b71dc491d895bf0968c7fe89/js/liyc.js"></script> 
<link rel="stylesheet" href="https://raw.githubusercontent.com/YichaoOU/YichaoOU.github.io/9bd18765cc77a855b71dc491d895bf0968c7fe89/css/liyc.css" type="text/css" media="print, projection, screen">
<style type="text/css">
table {
  table-layout: fixed;
  width: 500px;
}
td{
    word-wrap:break-word
}

</style>
</head>
<body>

<table id="myTable" class="tablesorter"> 
<thead> 
<tr> 
{{header_content}}
</tr> 
</thead> 
<tbody> 
{{table_content}}
</tbody> 
</table> 
</body>
</html>
"""


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)


	mainParser.add_argument('-f',"--input",  help="dataframe",required=True)
	mainParser.add_argument('-o',"--output",  help="output name",default="output.html")
	mainParser.add_argument('-s',"--sep",  help="output name",default="\t")
	mainParser.add_argument('-w',"--width",  help="output name",default=200,type=int)
	mainParser.add_argument('-H',"--height",  help="output name",default=200,type=int)
	mainParser.add_argument("--sort",  help="sort by column name",default="None")
	mainParser.add_argument("--motif",  help="generate motif html", action='store_true')
	


	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
	
	
def output_header(df):
	ss = list(map(lambda x:"<th>"+str(x)+"</th>",df.columns))
	return "\n".join(ss)

def encode_figure(x,w,h):
	try:
		file_ending = x.split(".")[-1]
	except:
		return "file not exist"
	
	if file_ending == "png":
		try:
			# encoded = base64.b64encode(open(x, "rb").read())
			encoded = resize_image(x,w,h)
			item = ''' <img style="display:block;" width="%s" height="%s" src="data:image/png;base64,%s"  /> ''' % ("100%","100%",encoded)
			# item = ''' <img src="%s" width=%s height=%s  > </img> ''' % (x,w,h)
			return item
		except:
			return "file not exist"
	return str(x)
	
def encode_motif(x,w,h):
	file_ending = x.split(".")[-1]
	
	if file_ending == "png":
		try:
			# encoded = base64.b64encode(open(x, "rb").read())
			# encoded = resize_image(x,w,h)
			# item = ''' <img style="display:block;" width="%s" height="%s" src="data:image/png;base64,%s"  /> ''' % ("100%","100%",encoded)
			item = ''' <img src="%s" width=%s height=%s  > </img> ''' % (x,w,h)
			return item
		except:
			return "file not exist"
	return str(x)
	
def output_row(x,w,h):
	out = "<tr>"
	ss = list(map(lambda x:"<td>"+encode_figure(x,w,h)+"</td>",x.tolist()))
	out += "\n".join(ss)
	out += "</tr>"
	return out
def output_row2(x,w,h):
	out = "<tr>"
	ss = list(map(lambda x:"<td>"+encode_motif(x,w,h)+"</td>",x.tolist()))
	out += "\n".join(ss)
	out += "</tr>"
	return out
	
def df_to_html(df,w,h,html_template):
	
	content = df.apply(lambda x:output_row(x,w,h),axis=1)
	content = "".join(list(map(lambda x:"".join(x),content.values.tolist())))
	header = output_header(df)
	return multireplace(html_template, {'header_content':header,'table_content':content})
def df_to_html2(df,w,h,html_template):
	
	content = df.apply(lambda x:output_row2(x,w,h),axis=1)
	content = "".join(list(map(lambda x:"".join(x),content.values.tolist())))
	header = output_header(df)
	return multireplace(html_template, {'header_content':header,'table_content':content})
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()
	
def run_dataframe():
	args = my_args()
	df = pd.read_csv(args.input,sep=args.sep,dtype=str)
	if not args.sort == "None":
		df[args.sort] = df[args.sort].astype(float)
		df = df.sort_values(args.sort)
		df[args.sort] = df[args.sort].astype(str)
	if args.motif:
		template_html = df_to_html2(df,args.width,args.height,html_template2)
	else:
	
		template_html = df_to_html(df,args.width,args.height,html_template)
	write_file(args.output,template_html)

if __name__ == "__main__":
	run_dataframe()









