#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


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
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--atac_list",  help="tsv 2 columns, cell type and path to bam file (abs or relative to current working dir)",required=True)
	mainParser.add_argument('-c',"--conserved_peak",  help="path to IDR peak",required=True)
	mainParser.add_argument('-r',"--relaxed_peak",  help="path to union MACS2 peak",required=True)
	mainParser.add_argument('-t',"--training_cell_type",  help="training cell type label, must match to names in atac.list",required=True)
	mainParser.add_argument("--override_jid",  help="continue working on the same jid folder",action='store_true')		
	mainParser.add_argument("--predict_only",  help="continue working on the same jid folder",action='store_true')		
	mainParser.add_argument("--train_predict",  help="train_predict",action='store_true')		
	mainParser.add_argument("--bw",  help="ATAC bw input",action='store_true')		

	mainParser.add_argument('-m',"--motif_list",  help="tsv 2 columns, motif name and path to motif file (abs or relative to current working dir)",default=None)
	mainParser.add_argument('-q',"--queue",  help="submit queue",default="standard")
	mainParser.add_argument('-b',"--bin_size",  help="bin_size",default=50,type=int)
	# mainParser.add_argument("--Catchitt_path",  help="submit queue",default="/home/yli11/HemTools/share/script/jar/Catchitt-0.1.3.jar")
	mainParser.add_argument("--Catchitt_path",  help="submit queue",default="/home/yli11/HemTools/share/script/jar/Catchitt-0.1.4b.jar")
	mainParser.add_argument("--atac_list2",default=None, help=argparse.SUPPRESS)
	mainParser.add_argument("--training_chromosomes",default=None, help=argparse.SUPPRESS)
	mainParser.add_argument('--motif_features',  help=argparse.SUPPRESS,default="m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/Ctcf_H1hesc_shift20_bdeu_order-20_comp1-model-1/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/intersect_all_relaxed_filtered_lslim3-model-3/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/intersect_all_relaxed_filtered_lslim3-model-7/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/Jund_K562_shift20_bdeu_order-20_comp1-model-1/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/ENCSR000BHK_SP1-human_1_hg19-model-2/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/intersect_all_relaxed_filtered_lslim3-model-4/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/intersect_all_relaxed_filtered_pwm-model-1/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/Max_K562_shift20_bdeu_order-20_comp1-model-1/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/intersect_all_relaxed_filtered_lslim3-model-1/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/intersect_all_relaxed_filtered_lslim3-model-5/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/intersect_all_relaxed_filtered_pwm-model-2/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/NFIX.homer/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/intersect_all_relaxed_filtered_lslim3-model-2/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/intersect_all_relaxed_filtered_lslim3-model-6/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/intersect_all_relaxed_filtered_pwm-model-3/Motif_scores.tsv.gz m=/home/yli11/Data/Motif_database/Catchitt/motifs/NFIX_motif_model/model/PU1.homer/Motif_scores.tsv.gz ")
	
	
	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='mm9',type=str)
	genome.add_argument('--faidx',  help="fasta index", default=myData['mm9_faidx'])
	genome.add_argument('--fasta',  help="fasta index", default=myData['mm9_fasta'])


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def get_motif_features(f,jid):
	df = pd.read_csv(f,sep="\t",header=None)
	out = []
	for i in df[0].tolist():
		out.append("m=%s/Motif/%s/Motif_scores.tsv.gz"%(jid,i))
	return " ".join(out)
	
	
	pass

def get_atac_list2(f,jid):
	df = pd.read_csv(f,sep="\t",header=None)
	chr_list = "chr1,chr2,chr3,chr4,chr5,chr6,chr7,chr9,chr10,chr11,chr12,chr13,chr14,chr15,chr16,chr17,chr18,chr19,chr20,chr21,chr22,chrX,chrY"
	chr_list = chr_list.split(",")
	out = []
	for a in df[0].unique().tolist():
		for c in chr_list:
			out.append([a,c])
	out = pd.DataFrame(out)
	name = "%s.list"%(jid)
	out.to_csv(name,sep="\t",header=False,index=False)
	return name

def main():

	args = my_args()
	check_file([args.atac_list,args.conserved_peak,args.relaxed_peak])
	if not args.genome=="custom":
		args.fasta = myData['%s_fasta'%(args.genome)]	
		args.faidx = myData['%s_faidx'%(args.genome)]	
	if "hg" in args.genome:
		args.training_chromosomes = "chr1,chr2,chr3,chr4,chr5,chr6,chr7,chr9,chr10,chr11,chr12,chr13,chr14,chr15,chr16,chr17,chr18,chr19,chr20,chrX,chrY"
	else:
		args.training_chromosomes = "chr1,chr2,chr3,chr4,chr5,chr6,chr7,chr9,chr10,chr11,chr12,chr13,chr14,chr15,chr16,chr17,chr18,chr19"
	##------- check if jid exist  ----------------------
	if isdir(args.jid) and not args.override_jid:
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)			
	
	##------- add functions below ----------------------
	
	#-------------- run jobs ----------------------
	
	os.system("mkdir -p %s"%(args.jid))
	os.system("mkdir -p %s/log_files"%(args.jid))
	os.system("mkdir -p %s/ATAC"%(args.jid))
	os.system("mkdir -p %s/Motif"%(args.jid))
	os.system("mkdir -p %s/prediction"%(args.jid))
	os.system("mkdir -p %s/trained_model"%(args.jid))
	pipeline_name = current_file_base_name
	args.atac_list2 = get_atac_list2(args.atac_list,args.jid)
	if args.predict_only:
		# print (args)
		submit_pipeline_jobs(myPipelines[pipeline_name+"_last_step"],args)
		exit()
	if args.motif_list:
		args.motif_features = get_motif_features(args.motif_list,args.jid)
	if args.bw:
		submit_pipeline_jobs(myPipelines[pipeline_name+"_bw"],args)
		exit()
	if args.train_predict:
		submit_pipeline_jobs(myPipelines[pipeline_name+"_train_predict"],args)
		exit()
	if not args.motif_list:
		submit_pipeline_jobs(myPipelines[pipeline_name+"_skip_motif"],args)
		exit()
	
	submit_pipeline_jobs(myPipelines[pipeline_name],args)


	
if __name__ == "__main__":
	main()

























