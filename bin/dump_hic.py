#!/home/yli11/.conda/envs/py2/bin/python
from joblib import Parallel, delayed

import sys
import os
import glob


hic_file_list = glob.glob("*.hic")
chrom_size = sys.argv[1]
resolution = 250000
resolution2 = 100000
chr_list = []
with open(chrom_size) as f:
    for line in f:
        line = line.strip().split()
        chr_list.append(line[0].replace("chr","").upper())
print (chr_list)

def dump_oe(hic,chr,bedgraph):
    # for O/E please use 500 - 100kb resolution, depending on the chromsome size, KR norm gives better look
    command = f"module load juicer_tools;java -jar /home/yli11/HemTools/share/script/jar/juicer_tools_1.21.01.jar dump oe KR {hic} {chr} {chr} BP {resolution} {hic.replace('.hic','')}_{chr}_oe.mat -d"
    # command = f"module load juicer_tools;java -jar /home/yli11/HemTools/share/script/jar/juicer_tools_1.21.01.jar pearsons NONE {hic} {chr} {chr} BP {resolution} {hic.replace('.hic','')}_{chr}_pcc.mat -d"
    print (command)
    os.system(command)
    command = f"module load python/2.7.13;/hpcf/apps/python/install/2.7.13/bin/python /home/yli11/HemTools/bin/HiCPlotter_oe.py -f {hic.replace('.hic','')}_{chr}_oe.mat -n {chr} -chr {redefine_chr_name(chr)} -o {hic.replace('.hic','')}_{chr}_oe -r {resolution} -fh 0  -ext pdf -nl 1 -hmc 3 -hist {bedgraph} -hl PC1 -hc e03822 -fhist 1"
    print (command)
    os.system(command)
    
def dump_observed(hic,chr,bedgraph):
    # for observed please use 100kb resolution
    command = f"module load juicer_tools;java -jar /home/yli11/HemTools/share/script/jar/juicer_tools_1.21.01.jar dump observed KR {hic} {chr} {chr} BP {resolution2} {hic.replace('.hic','')}_{chr}_observed.mat -d"
    print (command)
    os.system(command)
    command = f"module load python/2.7.13;/hpcf/apps/python/install/2.7.13/bin/python /home/yli11/HemTools/bin/HiCPlotter.py -f {hic.replace('.hic','')}_{chr}_observed.mat -n {chr} -chr {redefine_chr_name(chr)} -o {hic.replace('.hic','')}_{chr}_observed -r {resolution2} -fh 0  -ext pdf -hmc 3 -hist {bedgraph} -hl PC1 -hc e03822 -fhist 1"
    print (command)
    os.system(command)
def redefine_chr_name(x):
    p1,p2 = x.split("_")
    return "chr"+p1+"_"+p2.lower()
def dump_pcc(hic,chr,bedgraph):
    # for PCC, please use 500 - 250kb resolution.
    command = f"module load juicer_tools;java -jar /home/yli11/HemTools/share/script/jar/juicer_tools_1.21.01.jar pearsons -p NONE {hic} {chr} BP {resolution} {hic.replace('.hic','')}_{chr}_pcc.mat -d"
    print (command)
    os.system(command)
    command = f"module load python/2.7.13;/hpcf/apps/python/install/2.7.13/bin/python /home/yli11/HemTools/bin/HiCPlotter_pcc.py -f {hic.replace('.hic','')}_{chr}_pcc.mat -n {chr} -chr {redefine_chr_name(chr)} -o {hic.replace('.hic','')}_{chr}_pcc -r {resolution} -fh 0  -ext pdf -nl 1 -hmc 3 -hist {bedgraph} -hl PC1 -hc e03822 -fhist 1"
    print (command)
    os.system(command)
input_list=[]
for h in hic_file_list:
    for c in chr_list:
        input_list.append([h,c,h.split("_homer")[0]+".PC1.bedGraph.sorted"])
# Parallel(n_jobs=10,verbose=10)(delayed(dump_observed)(x[0],x[1],x[2]) for x in input_list)
# Parallel(n_jobs=10,verbose=10)(delayed(dump_oe)(x[0],x[1],x[2]) for x in input_list)
# Parallel(n_jobs=10,verbose=10)(delayed(dump_pcc)(x[0],x[1],x[2]) for x in input_list)


### compare
input_list2 = []
for c in chr_list:
    r1 = hic_file_list[0]
    b1 = r1.split("_homer")[0]+".PC1.bedGraph.sorted"
    r2 = hic_file_list[1]
    b2 = r2.split("_homer")[0]+".PC1.bedGraph.sorted"
    input_list2.append([r1,b1,r2,b2,c])


def hic_compare(r1,b1,r2,b2,chr):
    print (r1,b1,r2,b2,chr)
    command = f"module load python/2.7.13;/hpcf/apps/python/install/2.7.13/bin/python /home/yli11/HemTools/bin/HiCPlotter.py -f {r1.replace('.hic','')}_{chr}_observed.mat {r2.replace('.hic','')}_{chr}_observed.mat -n {r1} {r2} -chr {redefine_chr_name(chr)} -o HiCCompre_{chr} -r {resolution2} -fh 0  -ext pdf -c 1 -hmc 3 -hist {b1} {b2}  -hl PC1 PC1 -hc e03822 e03822 -fhist 1 1"
    print (command)
    os.system(command)

# Parallel(n_jobs=10,verbose=10)(delayed(hic_compare)(*x) for x in input_list2)


def call_selfish(r1,r2,chr):
    command = f"selfish -f1 {r1} -f2 {r2} -ch {chr} -r 10kb -o diff_{chr}.tsv -t 0.01 -sz 10 -i 20"
    print (command)
    os.system(command)
Parallel(n_jobs=10,verbose=10)(delayed(call_selfish)(x[0],x[2],x[4]) for x in input_list2)

