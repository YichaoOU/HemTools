#!/usr/bin/env python
import sys
import os
import argparse

"""plot enrichment dotplot

calling ggplot2

http://yulab-smu.top/clusterProfiler-book/chapter11.html
https://github.com/YuLab-SMU/enrichplot/blob/3b43f30aeba526cecd2d3f6d07f0cb90f2f25423/R/dotplot.R

"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]


def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		if myDict[k] == None:
			value = ""
		else:
			value = myDict[k]
		myString = str(myString).replace("{{"+str(k)+"}}",str(value))
	return myString
def my_args():
	# username = getpass.getuser()
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="plot enrichment dotplot given dataframe.")



	mainParser.add_argument('-f',"--input",  help="data table input",required=True)
	mainParser.add_argument('-o',"--output",  help="output",required=True)
	mainParser.add_argument('-x',  help="X-axis",required=True)
	mainParser.add_argument('-y',  help="y-axis",required=True)
	mainParser.add_argument('-c',"--color_by",  help="color_by",required=True)
	mainParser.add_argument('-s',"--size_by",  help="size_by",required=True)
	mainParser.add_argument('-W',  help="width",required=True)
	mainParser.add_argument('-H',  help="heigh",required=True)
	# mainParser.add_argument('-o',  help="heigh",required=True)

	# mainParser.add_argument("--xlabel",default="")
	# mainParser.add_argument("--ylabel",default="")
	# mainParser.add_argument("--title",default="")

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():
	R_script="""

	library(ggplot2)
	library(DOSE)
	df = read.table("{{input}}",header=TRUE,sep="\t")
	head(df)
	ggplot(df, aes_string(x="{{x}}", y="{{y}}", size="{{size_by}}", color="{{color_by}}")) +
		geom_point() + scale_size_continuous(range = c(2, 20))+
		scale_color_continuous(low="blue", high="red", name = "{{color_by}}",
			guide=guide_colorbar(reverse=F)) +ylab(NULL)+theme_dose(10)
	ggsave("{{output}}",width={{W}},heigh={{H}})
	#data$Treatment <- factor(data$Treatment, levels=c("Y", "X", "Z"))
	#orderBy="logFDR"
	#idx <- order(df[[orderBy]], decreasing = T)
	#df$Y <- factor(df$Y,levels=rev(unique(df$Y[idx])))
	#df$peaks <- factor(df$peaks, levels=c("NFIX_open", "NFIX_close", "ATAC_near_NFIX_close"))

	"""
	args = my_args()
	if args.color_by[0] == " ":
		args.color_by = args.color_by[1:]
	argsDict = vars(args)
	
	print (argsDict)
	"""below is the same for very dataframe scripts
	
	by default our input dataframe is bed format, which is \t separated with no header no index 
	
	"""
	R_script = multireplace(R_script,argsDict)
	write_file("%s.R"%(args.output),R_script)
	command = "module load R/3.6.1;Rscript %s.R"%(args.output)
	os.system(command)

if __name__ == "__main__":
	main()




