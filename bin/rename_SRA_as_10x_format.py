#!/hpcf/apps/python/install/2.7.13/bin/python


"""

data downloaded from SRA is like:

SRR7295265_2.fastq.gz
SRR7295265_1.fastq.gz

without R1 or R2, --guess_input won't work

This script helps to add R1 and R2

replace _1. to _R1.
"""

import glob
import os
import sys
import pandas as pd
import re
fastq_files = glob.glob("*.fq")+glob.glob("*.fq.gz")+glob.glob("*.fastq")+glob.glob("*.fastq.gz")

for f in fastq_files:
	new_name = f.replace("_1.","_R1.")
	new_name = new_name.replace("_2.","_R2.")
	if f != new_name:
		command = "mv %s %s"%(f,new_name)
		os.system(command)

try:
	file=sys.argv[1]
except:
	exit()

def guess_sep(x):
	with open(x) as f:
		for line in f:
			tmp1 = len(line.strip().split(","))
			tmp2 = len(line.strip().split("\t"))
			# print (tmp1,tmp2)
			if tmp1 > tmp2:
				return ","
			if tmp2 > tmp1: 
				return "\t"
			else:
				print ("Can't determine the separator. Please input manually")
				exit()
				

df = pd.read_csv(file,sep=guess_sep(file))
# print (df.head())
try:
	df.index = df['Run']
except:
	df.index = df['Comment[ENA_RUN]']
fastq_files = glob.glob("*.fq")+glob.glob("*.fq.gz")+glob.glob("*.fastq")+glob.glob("*.fastq.gz")

df.columns = [re.sub(r'[^.a-zA-Z0-9]', "_", x).lower() for x in df.columns]
print (df.columns)

for f in fastq_files:
	# print (f)
	# print (re.split(r'_|-|.',f))
	sra_id = re.split('_|-|\.',f)[0]
	# print (sra_id)
	final_name = []
	try:
		cell_type = df.at[sra_id,'cell_type']
		cell_type = cell_type.replace("+","plus")
		cell_type = cell_type.replace("-","minus")
		cell_type = re.sub(r'[^.a-zA-Z0-9]', "_", cell_type)
		final_name.append(cell_type)
	except:
		pass
	try:
		cell_type = df.at[sra_id,'cell_line']
		cell_type = cell_type.replace("+","plus")
		cell_type = cell_type.replace("-","minus")
		cell_type = re.sub(r'[^.a-zA-Z0-9]', "_", cell_type)
		final_name.append(cell_type)
	except:
		pass		
	try:
		source_name = df.at[sra_id,'source_name']
		source_name = source_name.replace("+","plus")
		source_name = source_name.replace("-","minus")
		source_name = re.sub(r'[^.a-zA-Z0-9]', "_", source_name)
		final_name.append(source_name)
	except:
		pass
	try:
		source_name = df.at[sra_id,'chromatin_state']
		source_name = source_name.replace("+","plus")
		source_name = source_name.replace("-","minus")
		source_name = re.sub(r'[^.a-zA-Z0-9]', "_", source_name)
		final_name.append(source_name)
	except:
		pass
	try:
		if "Antibody" in df.columns:
			antibody = df.at[sra_id,'Antibody']
		elif "antibody" in df.columns:
			antibody = df.at[sra_id,'antibody']
		elif "chip_antibody" in df.columns:
			antibody = df.at[sra_id,'chip_antibody']
		elif "chip-antibody" in df.columns:
			antibody = df.at[sra_id,'chip-antibody']
		else:
			print ("no antibody column")
		antibody = antibody.replace("+","plus")
		antibody = antibody.replace("-","minus")
		antibody = re.sub(r'[^.a-zA-Z0-9]', "_", antibody)
		final_name.append(antibody)
	except:
		pass
	try:
		digestion_time = df.at[sra_id,'digestion_time']
		digestion_time = digestion_time.replace("+","plus")
		digestion_time = digestion_time.replace("-","minus")
		digestion_time = re.sub(r'[^.a-zA-Z0-9]', "_", digestion_time)
		final_name.append(digestion_time)
	except:
		pass
	try:
		population = df.at[sra_id,'population']
		population = population.replace("+","plus")
		population = population.replace("-","minus")
		population = re.sub(r'[^.a-zA-Z0-9]', "_", population)
		final_name.append(population)
	except:
		pass		
	try:
		population = df.at[sra_id,'chip']
		population = population.replace("+","plus")
		population = population.replace("-","minus")
		population = re.sub(r'[^.a-zA-Z0-9]', "_", population)
		final_name.append(population)
	except:
		pass		
	try:
		population = df.at[sra_id,'treatment']
		population = population.replace("+","plus")
		population = population.replace("-","minus")
		population = re.sub(r'[^.a-zA-Z0-9]', "_", population)
		final_name.append(population)
	except:
		pass		
	try:
		population = df.at[sra_id,'library_name']
		population = population.replace("+","plus")
		population = population.replace("-","minus")
		population = re.sub(r'[^.a-zA-Z0-9]', "_", population)
		final_name.append(population)
	except:
		pass		
	try:
		population = df.at[sra_id,'extract_name']
		population = population.replace("+","plus")
		population = population.replace("-","minus")
		population = re.sub(r'[^.a-zA-Z0-9]', "_", population)
		final_name.append(population)
	except:
		pass		
	try:
		population = df.at[sra_id,'assay_type']
		population = population.replace("+","plus")
		population = population.replace("-","minus")
		population = re.sub(r'[^.a-zA-Z0-9]', "_", population)
		final_name.append(population)
	except:
		pass		
	try:
		population = df.at[sra_id,'selection_marker']
		population = population.replace("+","plus")
		population = population.replace("-","minus")
		population = re.sub(r'[^.a-zA-Z0-9]', "_", population)
		final_name.append(population)
	except:
		pass		
	try:
		population = df.at[sra_id,'LibrarySelection']
		population = population.replace("+","plus")
		population = population.replace("-","minus")
		population = re.sub(r'[^.a-zA-Z0-9]', "_", population)
		final_name.append(population)
	except:
		pass		
	try:
		population = df.at[sra_id,'time']
		population = population.replace("+","plus")
		population = population.replace("-","minus")
		population = re.sub(r'[^.a-zA-Z0-9]', "_", population)
		final_name.append(population)
	except:
		pass		
	# print (final_name)
	if len(final_name) == 0:
		continue
	new_name = f
	new_name = new_name.replace(sra_id,"_".join([x.replace(".","_") for x in final_name]))
	new_name = new_name.replace("__","_")
	new_name = new_name.replace("_.fastq.gz",".fastq.gz")
	new_name = sra_id+"_"+new_name
	# print (new_name)

	if "R1.fastq.gz" in new_name:
		new_name = new_name.replace("R1.fastq.gz","S1_L001_R1_001.fastq.gz")
	if "R2.fastq.gz" in new_name:
		new_name = new_name.replace("R2.fastq.gz","S1_L001_R2_001.fastq.gz")
	new_name = new_name.replace("._","_")
	new_name = new_name.replace("_.","_")
	new_name = new_name.replace("__","_")
	new_name = new_name.replace("__","_")
	command = "mv %s %s"%(f,new_name)
	# print (command)
	os.system(command)








