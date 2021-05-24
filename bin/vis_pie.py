
import argparse
import pandas as pd
import uuid
from os.path import isfile,isdir
import os
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import glob


"""Matplotlib for pie chart





"""

##---------------------- Config --------------------------
email_domain = "@stjude.org"

def multireplace(myString, myDict):
	## keywords format is {{string}}
	for k in myDict:
		myString = myString.replace("{{"+str(k)+"}}",str(myDict[k]))
	return myString

def send_email_command(url):
	username = getpass.getuser()
	command = 'echo "Your GREAT result is ready, please click on the url below\n\n{{url}}" | mailx -s "pyGREAT analysis" -- User_name%s'%(email_domain)
	command = command.replace("User_name",username)
	command = command.replace("{{url}}",url)
	os.system(command)

current_file_base_name = __file__.split("/")[-1].split(".")[0]
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--input",  help="input your count table", required=True)
	mainParser.add_argument('-s',"--separator",  help='Tab, comma, or space: "/\t", ",", or " ".',default="\t")
	mainParser.add_argument('-t',"--treatment",  help="treatment column names, separated by ,", required=True)
	mainParser.add_argument('-c',"--control",  help="control column names, separated by ,", required=True)
	mainParser.add_argument("--skip",  help="skip the first N lines in your count table",default=0)
	mainParser.add_argument("--no_header",  help="If used, column names will be assign just as 0,1,2,... Then you should modify -t, -c accordingly",action='store_true')
	mainParser.add_argument('-o',"--output",  help="output file name. Default: input file name.t.vs.c.DESEQ2.out and input file name.t.vs.c.DESEQ2.R. First 8 letter of -t and -c will be used if -t or -c is a long string.")
	mainParser.add_argument('--email',  help="send email", action='store_true')
	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

R_command = """

###------------------ data pre-processing ---------------------------------
treatment <- as.character(unlist(strsplit({{treatment}}, ",")))
control <- as.character(unlist(strsplit({{control}}, ",")))
group_label <- c(rep("treatment", length(treatment)), rep("control", length(control)))
count_table <- read.table({{input}}, sep="\t", header={{no_header}}, check.names=FALSE, skip={{skip}})
region_info <- count_table
if(!all(c(treatment, control) %in% colnames(count_table))){
	treatment <- paste("X", treatment, sep="")
	control <- paste("X", control, sep="")
}
count_table <- count_table[,c(treatment, control)]
sample_info <- data.frame(sampleName=c(treatment, control), Group=group_label)


###------------------ DESEQ2 command ---------------------------------------
#ref: https://www.bioconductor.org/packages/devel/bioc/vignettes/DESeq2/inst/doc/DESeq2.html
dds <- DESeqDataSetFromMatrix(countData=count_table, colData=sample_info, design = ~ Group)
dds <- DESeq(dds)
res <- lfcShrink(dds, coef="Group_treatment_vs_control", type="apeglm")

###------------------ output result ----------------------------------------
d <- data.frame(region_info, logFC=res[,"log2FoldChange"], AveExpr=res[,"lfcSE"], t=res[,"stat"], P.Value=res[,"pvalue"], adj.P.Val=res[,"padj"])
d <- d[order(d[,"padj"]),]
write.table(d, file={{output}}, sep="\t", quote=FALSE, row.names=FALSE)

"""


def main():
	## initial parameters
	args =  my_args()
	argsDict = vars(args)
	
	
	
	pass



if __name__ == "__main__":
	main()
	
## ---------------- misc ------------------------------
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import glob
files = glob.glob("*/*anno*")
def parse_file(x,myList):
	with open(x) as f:
		for line in f:
			line = line.strip().split("\t")
			elem = line[-2].split()[0]
			myList.append(elem)
	return 1
myList = []
for f in files:
	parse_file(f,myList)
from collections import Counter
c = Counter(myList)
occ = [[i, c[i] / float(len(myList)) * 100.0] for i in c]
plt.figure()
plt.pie([x[1] for x in occ], labels=[x[0] for x in occ], autopct='%1.1f%%',shadow=True, startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.savefig("pie.png")









