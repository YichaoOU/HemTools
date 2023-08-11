#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


"""process kallisto output and output transcript-level and gene-level differences

Input
-----

glob current kallisto dir

the kallisto output folder is named as sampleID_group_groupID.




sample_info example


sample	condition	path
F1	hudep1	1000000_RFR001_S1_kallisto
F2	hudep2	1000002_RFR003_S3_kallisto
F3	hudep1	1000004_RFR005_S5_kallisto
F4	hudep2	1000001_RFR002_S2_kallisto
F5	hudep1	1000003_RFR004_S4_kallisto
F6	hudep2	1000005_RFR006_S6_kallisto


Ref: https://pachterlab.github.io/sleuth_walkthroughs/pval_agg/analysis.html

"""


R_command_paired="""

#https://www.biostars.org/p/265777/

library("sleuth")
library("plyr")

sample_info <- read.table("{{sample_info}}", sep="\\t",header=T)
t2g <- read.table("{{gene_info}}", sep="\\t",header=T)
sample_info[,"path"]=file.path(sample_info[,"path"])

## transcript level expression
so <- sleuth_prep(sample_info, extra_bootstrap_summary = TRUE, target_mapping = t2g)
transcript_tpm = sleuth_to_matrix(so,"obs_raw","tpm")
treatment_mean = data.frame(treatment_mean=rowMeans(transcript_tpm[,c({{treatment_list}})]))
control_mean = data.frame(control_mean=rowMeans(transcript_tpm[,c({{control_list}})]))
transcript_tpm = cbind(transcript_tpm,treatment_mean,control_mean)
logFC = data.frame(logFC=log2((transcript_tpm[,"treatment_mean"]+1)/(transcript_tpm[,"control_mean"]+1)))
transcript_tpm = cbind(transcript_tpm,logFC)
write.csv(transcript_tpm, file="{{output_name}}.transcript.normalized.tpm.csv", row.names=T)

transcript_counts = sleuth_to_matrix(so,"obs_raw","est_counts")
treatment_mean = data.frame(treatment_mean=rowMeans(transcript_counts[,c({{treatment_list}})]))
control_mean = data.frame(control_mean=rowMeans(transcript_counts[,c({{control_list}})]))
transcript_counts = cbind(transcript_counts,treatment_mean,control_mean)
logFC = data.frame(logFC=log2((transcript_counts[,"treatment_mean"]+1)/(transcript_counts[,"control_mean"]+1)))
transcript_counts = cbind(transcript_counts,logFC)
write.csv(transcript_counts, file="{{output_name}}.transcript.normalized.est_counts.csv", row.names=T)

## gene level expression, num_cores=1 is important
so <- sleuth_prep(sample_info, ~condition, target_mapping = t2g, aggregation_column = 'ens_gene',gene_mode = TRUE,num_cores=1)
gene_tpm = sleuth_to_matrix(so,"obs_raw","tpm")
treatment_mean = data.frame(treatment_mean=rowMeans(gene_tpm[,c({{treatment_list}})]))
control_mean = data.frame(control_mean=rowMeans(gene_tpm[,c({{control_list}})]))
gene_tpm = cbind(gene_tpm,treatment_mean,control_mean)
logFC = data.frame(logFC=log2((gene_tpm[,"treatment_mean"]+1)/(gene_tpm[,"control_mean"]+1)))
gene_tpm = cbind(gene_tpm,logFC)
write.csv(gene_tpm, file="{{output_name}}.gene.normalized.tpm.csv", row.names=T)

gene_counts = sleuth_to_matrix(so,"obs_raw","est_counts")
treatment_mean = data.frame(treatment_mean=rowMeans(gene_counts[,c({{treatment_list}})]))
control_mean = data.frame(control_mean=rowMeans(gene_counts[,c({{control_list}})]))
gene_counts = cbind(gene_counts,treatment_mean,control_mean)
logFC = data.frame(logFC=log2((gene_counts[,"treatment_mean"]+1)/(gene_counts[,"control_mean"]+1)))
gene_counts = cbind(gene_counts,logFC)
write.csv(gene_counts, file="{{output_name}}.gene.normalized.est_counts.csv", row.names=T)


## main sleuth program
## https://pachterlab.github.io/sleuth/walkthroughs
# https://pachterlab.github.io/sleuth_walkthroughs/pval_agg/analysis.html
# so <- sleuth_prep(sample_info, ~condition+biologicalreplicate , target_mapping = t2g, aggregation_column = 'ens_gene',extra_bootstrap_summary = TRUE)
so <- sleuth_prep(sample_info, target_mapping = t2g, aggregation_column = 'ens_gene',extra_bootstrap_summary = TRUE)
# so <- sleuth_fit(so, ~condition, 'full')
# so <- sleuth_fit(so, ~biologicalreplicate , 'reduced')

so <- sleuth_fit(so, ~biologicalreplicate , 'reduced')
so <- sleuth_fit(so, ~biologicalreplicate+condition, 'full')

so <- sleuth_lrt(so, 'reduced', 'full')
sleuth_transcript <- sleuth_results(so, 'reduced:full', 'lrt', show_all = TRUE)
sleuth_transcript <- sleuth_transcript[order(sleuth_transcript[,"pval"]),c("target_id", "pval", "qval", "ext_gene","num_aggregated_transcripts")]

write.csv(sleuth_transcript, file="{{output_name}}.gene.sleuth.csv", row.names=FALSE)

sleuth_gene <- sleuth_results(so, 'reduced:full', 'lrt', show_all = TRUE,pval_aggregate = FALSE)
sleuth_gene <- sleuth_gene[order(sleuth_gene[,"pval"]),c("target_id", "pval", "qval", "ext_gene","ens_gene")]
write.csv(sleuth_gene, file="{{output_name}}.transcript.sleuth.csv", row.names=FALSE)

print (dim(sleuth_gene))
print (dim(gene_counts))
print (dim(sleuth_transcript))
print (dim(transcript_counts))

## combine data gene

df = read.csv("{{output_name}}.gene.sleuth.csv")
df2 = read.csv("{{output_name}}.gene.normalized.tpm.csv")
rownames(df2) = df2$X
rownames(df) = df$target_id
df3 = cbind(df,df2[rownames(df),])
write.csv(df3, file="{{output_name}}.gene.final.combined.tpm.csv", row.names=FALSE)

df = read.csv("{{output_name}}.gene.sleuth.csv")
df2 = read.csv("{{output_name}}.gene.normalized.est_counts.csv")
rownames(df2) = df2$X
rownames(df) = df$target_id
df3 = cbind(df,df2[rownames(df),])
write.csv(df3, file="{{output_name}}.gene.final.combined.est_counts.csv", row.names=FALSE)

## combine data transcript

df = read.csv("{{output_name}}.transcript.sleuth.csv")
df2 = read.csv("{{output_name}}.transcript.normalized.tpm.csv")
rownames(df2) = df2$X
rownames(df) = df$target_id
df3 = cbind(df,df2[rownames(df),])
write.csv(df3, file="{{output_name}}.transcript.final.combined.tpm.csv", row.names=FALSE)

df = read.csv("{{output_name}}.transcript.sleuth.csv")
df2 = read.csv("{{output_name}}.transcript.normalized.est_counts.csv")
rownames(df2) = df2$X
rownames(df) = df$target_id
df3 = cbind(df,df2[rownames(df),])
write.csv(df3, file="{{output_name}}.transcript.final.combined.est_counts.csv", row.names=FALSE)


"""

R_command = """

library("sleuth")
library("plyr")

sample_info <- read.table("{{sample_info}}", sep="\\t",header=T)
t2g <- read.table("{{gene_info}}", sep="\\t",header=T)
sample_info[,"path"]=file.path(sample_info[,"path"])

## transcript level expression
so <- sleuth_prep(sample_info, extra_bootstrap_summary = TRUE, target_mapping = t2g)
transcript_tpm = sleuth_to_matrix(so,"obs_raw","tpm")
treatment_mean = data.frame(treatment_mean=rowMeans(transcript_tpm[,c({{treatment_list}})]))
control_mean = data.frame(control_mean=rowMeans(transcript_tpm[,c({{control_list}})]))
transcript_tpm = cbind(transcript_tpm,treatment_mean,control_mean)
logFC = data.frame(logFC=log2((transcript_tpm[,"treatment_mean"]+1)/(transcript_tpm[,"control_mean"]+1)))
transcript_tpm = cbind(transcript_tpm,logFC)
write.csv(transcript_tpm, file="{{output_name}}.transcript.normalized.tpm.csv", row.names=T)

transcript_counts = sleuth_to_matrix(so,"obs_raw","est_counts")
treatment_mean = data.frame(treatment_mean=rowMeans(transcript_counts[,c({{treatment_list}})]))
control_mean = data.frame(control_mean=rowMeans(transcript_counts[,c({{control_list}})]))
transcript_counts = cbind(transcript_counts,treatment_mean,control_mean)
logFC = data.frame(logFC=log2((transcript_counts[,"treatment_mean"]+1)/(transcript_counts[,"control_mean"]+1)))
transcript_counts = cbind(transcript_counts,logFC)
write.csv(transcript_counts, file="{{output_name}}.transcript.normalized.est_counts.csv", row.names=T)

## gene level expression, num_cores=1 is important
so <- sleuth_prep(sample_info, ~condition, target_mapping = t2g, aggregation_column = 'ens_gene',gene_mode = TRUE,num_cores=1)
gene_tpm = sleuth_to_matrix(so,"obs_raw","tpm")
treatment_mean = data.frame(treatment_mean=rowMeans(gene_tpm[,c({{treatment_list}})]))
control_mean = data.frame(control_mean=rowMeans(gene_tpm[,c({{control_list}})]))
gene_tpm = cbind(gene_tpm,treatment_mean,control_mean)
logFC = data.frame(logFC=log2((gene_tpm[,"treatment_mean"]+1)/(gene_tpm[,"control_mean"]+1)))
gene_tpm = cbind(gene_tpm,logFC)
write.csv(gene_tpm, file="{{output_name}}.gene.normalized.tpm.csv", row.names=T)

gene_counts = sleuth_to_matrix(so,"obs_raw","est_counts")
treatment_mean = data.frame(treatment_mean=rowMeans(gene_counts[,c({{treatment_list}})]))
control_mean = data.frame(control_mean=rowMeans(gene_counts[,c({{control_list}})]))
gene_counts = cbind(gene_counts,treatment_mean,control_mean)
logFC = data.frame(logFC=log2((gene_counts[,"treatment_mean"]+1)/(gene_counts[,"control_mean"]+1)))
gene_counts = cbind(gene_counts,logFC)
write.csv(gene_counts, file="{{output_name}}.gene.normalized.est_counts.csv", row.names=T)


## main sleuth program
## https://pachterlab.github.io/sleuth/walkthroughs
so <- sleuth_prep(sample_info, ~condition, target_mapping = t2g, aggregation_column = 'ens_gene',extra_bootstrap_summary = TRUE)
so <- sleuth_fit(so, ~condition, 'full')
so <- sleuth_fit(so, ~1, 'reduced')
so <- sleuth_lrt(so, 'reduced', 'full')
sleuth_transcript <- sleuth_results(so, 'reduced:full', 'lrt', show_all = TRUE)
sleuth_transcript <- sleuth_transcript[order(sleuth_transcript[,"pval"]),c("target_id", "pval", "qval", "ext_gene","num_aggregated_transcripts")]

write.csv(sleuth_transcript, file="{{output_name}}.gene.sleuth.csv", row.names=FALSE)

sleuth_gene <- sleuth_results(so, 'reduced:full', 'lrt', show_all = TRUE,pval_aggregate = FALSE)
sleuth_gene <- sleuth_gene[order(sleuth_gene[,"pval"]),c("target_id", "pval", "qval", "ext_gene","ens_gene")]
write.csv(sleuth_gene, file="{{output_name}}.transcript.sleuth.csv", row.names=FALSE)

print (dim(sleuth_gene))
print (dim(gene_counts))
print (dim(sleuth_transcript))
print (dim(transcript_counts))

## combine data gene

df = read.csv("{{output_name}}.gene.sleuth.csv")
df2 = read.csv("{{output_name}}.gene.normalized.tpm.csv")
rownames(df2) = df2$X
rownames(df) = df$target_id
df3 = cbind(df,df2[rownames(df),])
write.csv(df3, file="{{output_name}}.gene.final.combined.tpm.csv", row.names=FALSE)

df = read.csv("{{output_name}}.gene.sleuth.csv")
df2 = read.csv("{{output_name}}.gene.normalized.est_counts.csv")
rownames(df2) = df2$X
rownames(df) = df$target_id
df3 = cbind(df,df2[rownames(df),])
write.csv(df3, file="{{output_name}}.gene.final.combined.est_counts.csv", row.names=FALSE)

## combine data transcript

df = read.csv("{{output_name}}.transcript.sleuth.csv")
df2 = read.csv("{{output_name}}.transcript.normalized.tpm.csv")
rownames(df2) = df2$X
rownames(df) = df$target_id
df3 = cbind(df,df2[rownames(df),])
write.csv(df3, file="{{output_name}}.transcript.final.combined.tpm.csv", row.names=FALSE)

df = read.csv("{{output_name}}.transcript.sleuth.csv")
df2 = read.csv("{{output_name}}.transcript.normalized.est_counts.csv")
rownames(df2) = df2$X
rownames(df) = df$target_id
df3 = cbind(df,df2[rownames(df),])
write.csv(df3, file="{{output_name}}.transcript.final.combined.est_counts.csv", row.names=FALSE)




"""

def prepare_sample_info(conditions,paired):
	if paired:
		df = pd.read_csv("paired.info",sep="\t",header=None,index_col=0)[1].to_dict()
	files = glob.glob("*_group_*")
	out = []
	# out.append("\t".join(["sample","condition","path"]))
	treatment_list = []
	control_list = []
	for f in files:
		if isdir(f):
			name1 = f.split("_group_")[0]
			name2 = f.split("_group_")[1]
			if not name2 in conditions:
				continue
			if name2 == conditions[0]:
				treatment_list.append(name1)
			if name2 == conditions[1]:
				control_list.append(name1)

			# out.append("\t".join([name1,name2,f]))
			out.append([name1,name2,f])
	out = pd.DataFrame(out)
	out.columns = ["sample","condition","path"]
	if paired:
		out['biologicalreplicate'] = out['sample'].map(df)
	file_name = "_".join(conditions)+".sample_info.txt"
	# write_file(file_name,"\n".join(out))
	out.to_csv(file_name,sep="\t",index=False)
	treatment_list = list(set(treatment_list))
	control_list = list(set(control_list))
	return file_name,",".join(['"'+x+'"' for x in treatment_list]),",".join(['"'+x+'"' for x in control_list])

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	# mainParser.add_argument('-f','--sample_info',  help="a tsv table | if -t and -c not used, you need to provide this sample info file",default="None")
	mainParser.add_argument('-o','--output_name', default=username+"_"+str(datetime.date.today()))
	mainParser.add_argument('-c','--control',  help="input control group",default="None")
	mainParser.add_argument('--treatment_list',  help="input treatment samples",default="None")
	mainParser.add_argument('--control_list',  help="input control samples",default="None")
	group = mainParser.add_mutually_exclusive_group(required=True)
	group.add_argument('-t','--treatment',  help="input treatment group",default="None")
	group.add_argument('-f','--sample_info',  help="a tsv table | if -t and -c not used, you need to provide this sample info file",default="None")
	mainParser.add_argument('--paired',  help="paired.info file should exist", action='store_true')
	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. Testing mm9", default='hg19',type=str)
	genome.add_argument('-i','--gene_info',  help="gene info t2g file for sleuth", default=myData['hg19_t2g'])

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main(R_command):

	args = my_args()
	
	if args.sample_info == "None":
		args.sample_info,args.treatment_list,args.control_list = prepare_sample_info([args.treatment,args.control],args.paired)
	if not args.genome == "custom":
		args.gene_info = myData['%s_t2g'%(args.genome)]
	if args.paired:
		R_command = multireplace(R_command_paired,vars(args))
	else:
		R_command = multireplace(R_command,vars(args))
	write_file(args.output_name+".sleuth.R",R_command)
	os.system("Rscript --vanilla "+args.output_name+".sleuth.R")

	
if __name__ == "__main__":
	main(R_command)


