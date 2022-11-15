#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
file_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument('-f',"--input",  help="file name like:Alleles_frequency_table_around_sgRNA_CTTGTCAAGGCTATTGGTCA")
	mainParser.add_argument('-o',"--output",  help="output file")

	genome=mainParser.add_argument_group(title='Genome Info')
	genome.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10. By default, specifying a genome version will automatically update index file, black list, chrom size and effectiveGenomeSize, unless a user explicitly sets those options.", default='hg38',type=str)
	genome.add_argument('--fasta',  help="fasta ", default=myData['hg38_fasta'])

	##------- add parameters above ---------------------
	# args = mainParser.parse_args()	
	args,unknown = mainParser.parse_known_args()
	for i in range(0,len(unknown),2):
		mainParser.add_argument(unknown[i],default=unknown[i+1])
	args = mainParser.parse_args()
	return args
def revcomp(seq):
	try: ## python2
		tab = string.maketrans(b"ACTG-", b"TGAC-")
	except:  ## python3
		tab = bytes.maketrans(b"ACTG-", b"TGAC-")
	return seq.translate(tab)[::-1]
def find_variant_sequence(q,r,first_letter_pos,strand):
    if strand == "+":
        return find_variant_sequence_pos_strand(q,r,first_letter_pos)
    else:
        q = revcomp(q)
        r = revcomp(r)
        # print (q)
        # print (r)
        return find_variant_sequence_pos_strand(q,r,first_letter_pos)
def find_variant_sequence_pos_strand(q,r,first_letter_pos):
    insertion=[]
    deletion=[]
    insertion_pos = []
    deletion_pos = []
    coord = "Complex"
    ref = "Complex"
    variant = "Complex"
    var_type = "Complex"
    variant_size = "Complex"
    for i in range(len(q)):
        if q[i]=="-":
            if len(deletion)==0:
                deletion.append(r[i-1])    
                deletion_pos.append(i-1)
            deletion.append(r[i])
            deletion_pos.append(i)
        if r[i]=="-":
            if len(insertion)==0:
                insertion.append(r[i-1])  
                insertion_pos.append(i-1)
            insertion.append(q[i])
            insertion_pos.append(i)
    # insertion case
    if len(deletion)==0:
        if len(insertion)==0:
            return coord,ref,variant,var_type,variant_size
        coord = str(insertion_pos[0]+first_letter_pos)
        ref = insertion[0]
        variant = "".join(insertion)
        var_type = "insertion"
        variant_size = len(insertion)-1
        return coord,ref,variant,var_type,variant_size
    # deletion case
    if len(insertion)==0:
        coord = "%s-%s"%(deletion_pos[0]+first_letter_pos,deletion_pos[-1]+first_letter_pos)
        variant = deletion[0]
        ref = "".join(deletion)
        var_type = "deletion"
        variant_size = len(deletion)-1
        return coord,ref,variant,var_type,variant_size
    return coord,ref,variant,var_type,variant_size
# find_variant_sequence_pos_strand(df.at[0,"Aligned_Sequence"],df.at[0,"Reference_Sequence"],5254917)
# find_variant_sequence(df.at[0,"Aligned_Sequence"],df.at[0,"Reference_Sequence"],5254876+1,"-")
def row_apply(r,pos,strand):
    return pd.Series(find_variant_sequence(r.Aligned_Sequence,r.Reference_Sequence,pos,strand))
def main():

	args = my_args()
	if not args.genome == "custom":
		args.fasta = myData['%s_fasta'%(args.genome)]	

	
	df = pd.read_csv(args.input,sep="\t")
	
	# get reference location
	blat_query=df[df.Unedited==True].Reference_Sequence.tolist()[0]
	write_fasta("tmp.query.fa",{"Reference_Sequence":blat_query})
	blat = "module load blat;blat %s tmp.query.fa tmp.query.out"%(args.fasta)
	print (blat)
	print ("Running BLAT, this can take several minites or several hours")
	os.system(blat)
	t = pd.read_csv("tmp.query.out",sep="\t",header=None,skiprows=5)
	strand = t.loc[0].T[8]
	start = t.loc[0].T[15]
	chr = t.loc[0].T[13]
	df[["coord","ref","variant","var_type","variant_size"]] = df.apply(lambda r:row_apply(r,start+1,strand),axis=1)
	df['chr'] = chr
	df.to_csv(args.output,index=False)
	os.system("rm tmp.query.*")

if __name__ == "__main__":
	main()





# df = pd.read_csv("Alleles_frequency_table_around_sgRNA_CTTGTCAAGGCTATTGGTCA.txt",sep="\t")



