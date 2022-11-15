#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='Methyl_seq_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-f',"--input",  help="fastq_tsv",required=True)
	mainParser.add_argument('-q',"--queue",  help="submit queue",default="standard")
	mainParser.add_argument('-g',"--genome",  help="genome version: hg19, hg38, mm9, mm10",default=None)
	mainParser.add_argument('-fa',"--fasta",  help="only map to a small region",default=None)
	mainParser.add_argument("--fasta_index",  help="fasta_index samtools .fai",default="/home/yli11/Data/Human/hg19/mask_genome/hg19.hbg_mask.fa.fai")
	mainParser.add_argument("--bwa_meth_index",  help="bwa_meth_index .fa",default="/home/yli11/Data/Human/hg19/mask_genome/hg19.hbg_mask.fa")

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args
# _JAVA_OPTIONS="-Djava.io.tmpdir=`pwd`/tmp" # not working

# nextflow run /home/yli11/.nextflow/assets/nf-core/methylseq --input '*_R{1,2}.fastq.gz' -profile singularity --fasta /home/yli11/Data/Human/hg19/mask_genome/hg19.hbg_mask.fa --fasta_index /home/yli11/Data/Human/hg19/mask_genome/hg19.hbg_mask.fa.fai --bwa_meth_index /home/yli11/Data/Human/hg19/mask_genome/hg19.hbg_mask.fa --save_reference --accel --aligner bwameth -resume


def main():

	args = my_args()
	##------- check if jid exist  ----------------------
	if isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		logging.warning ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		logging.info ("The new job id is: "+args.jid)
	else:
		logging.info ("The job id is: "+args.jid)		
	os.system("mkdir %s"%(args.jid))
	df = pd.read_csv(args.input,sep="\t",header=None)
	for i,r in df.iterrows():
		R1_abs = os.path.abspath(r[0])
		R2_abs = os.path.abspath(r[1])
		out_dir = "%s/%s"%(args.jid,r[2])
		if args.genome:
			command = """mkdir -p {0};cd {0}; ln -s {1} .;ln -s {2} .;module load nextflow/21.10.5 singularity;bsub -q {3} -n 16 -P Methy -R 'span[hosts=1] rusage[mem=15000]' -J Methy "nextflow run nf-core/methylseq --input '*_R{{1,2}}.fastq.gz' -profile singularity  --genome {4} --save_reference --accel --aligner bwameth" """.format(out_dir,R1_abs,R2_abs,args.queue,args.genome)
		elif args.fasta:
			command = """mkdir -p {0};cd {0}; ln -s {1} .;ln -s {2} .;module load nextflow/21.10.5 singularity;bsub -q {3} -n 16 -P Methy -R 'span[hosts=1] rusage[mem=15000]' -J Methy "nextflow run nf-core/methylseq --input '*_R{{1,2}}.fastq.gz' -profile singularity  --fasta {4} --save_reference --accel --aligner bwameth" """.format(out_dir,R1_abs,R2_abs,args.queue,args.fasta)
		else:
			command = """mkdir -p {0};cd {0}; ln -s {1} .;ln -s {2} .;module load nextflow/21.10.5 singularity;bsub -q {3} -n 16 -P Methy -R 'span[hosts=1] rusage[mem=15000]' -J Methy "nextflow run nf-core/methylseq --input '*_R{{1,2}}.fastq.gz' -profile singularity --fasta {4} --fasta_index {5} --bwa_meth_index {4} --save_reference --accel --aligner bwameth" """.format(out_dir,R1_abs,R2_abs,args.queue,args.bwa_meth_index,args.fasta_index)
		# print (command)
		subprocess.call(command,shell=True)



if __name__ == "__main__":
	main()


















