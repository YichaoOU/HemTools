#!/usr/bin/env python


import glob
import argparse

hic_files = glob.glob("*hic")
interaction_files = glob.glob("*iced.st.bed.gz")+glob.glob("*bedpe*gz")+glob.glob("*mango*gz")
bed_files = glob.glob("*gz")
bw_files = glob.glob("*bw")
bed_files = list(set(bed_files)-set(interaction_files))

hic_template = """
{
        "type":"hicstraw",
        "name":"{{name}}",
        "mode_arc":false,
        "mode_hm":true,
        "pyramidup":true,
        "color":"#a80000",
        "file":"{{dir}}/{{file}}",
        "enzyme":"MboI"
}
"""

bw_template = """
{"type":"bigwig","scale":{"auto": 1},"file": "{{dir}}/{{file}}","height":40,"stackspace":1,"onerow":1,"name":"{{name}}"}

"""

interaction_template = """
{
        "type":"hicstraw",
        "name":"{{name}}",
        "mode_arc":true,
        "mode_hm":false,
        "pyramidup":true,
        "color":"#1a60d1",
        "bedfile":"{{dir}}/{{file}}",
        "enzyme":"MboI"
}

"""

bed_template = """
{
"type":"bedj",
"name":"{{name}}",
"file":"{{dir}}/{{file}}",
"height":20,
"stackspace":1
}

"""

json_template = """

{
  "genome": "{{genome}}",
  "disable_sampletable": 1,
  "browserview": {
      "nativetracks": [
      "RefGene"
    ],

    "position": {
      "chr": "chr11",
      "start": 5247530,
      "stop": 5302902,
      "gene": "HBG2"
    },
	"tracks":[

{{tracks_json_list}}			


	]
  },
  "show_browser": 1
}

"""
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument("-d","--dir",  help="genome browser dir",required=True)
	mainParser.add_argument("-o","--output",  help="output_file_name",required=True)

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10.", default='hg19',type=str)

	##------- add parameters above ---------------------
	# args = mainParser.parse_args()	
	args,unknown = mainParser.parse_known_args()
	for i in range(0,len(unknown),2):
		mainParser.add_argument(unknown[i],default=unknown[i+1])
	args = mainParser.parse_args()
	return args

def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		if myDict[k] == None:
			value = ""
		else:
			value = myDict[k]
		myString = str(myString).replace("{{"+str(k)+"}}",str(value))
	return myString

def fill_template(file_list,template,dir=None):
	out = []
	for f in file_list:
		myDict = {}
		myDict['dir'] = dir
		myDict['name'] = f.replace(".hic","").replace(".gz","").replace(".bed","").replace(".st","")
		myDict['file'] = f
		out.append(multireplace(template, myDict))
	return out
def main():
	args = my_args()
	dir = args.dir
	out = fill_template(hic_files,hic_template,dir)+ \
		fill_template(interaction_files,interaction_template,dir)+ \
		fill_template(bw_files,bw_template,dir)+ \
		fill_template(bed_files,bed_template,dir)
	myDict = {}
	myDict['genome'] = args.genome
	myDict['tracks_json_list'] = ",\n".join(out)
	out_json =  multireplace(json_template, myDict)
	write_file(args.output,out_json)
if __name__ == "__main__":
	main()



