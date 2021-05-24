#!/hpcf/apps/python/install/2.7.13/bin/python
import pandas as pd
import sys
TF_query = sys.argv[1]
def get_TF_name(lines):
	TF_list = {}
	for line in lines:
		if "JASPA_MA" in line:
			tmp = line.split("_")
			TF_list[line] = "_".join(tmp[2:])
		elif "_HUMAN.H11MO" in line:
			tmp = line.split("_")
			if tmp[1] == "TAL1":
				TF_list[line] = "GATA1"
			else:
				TF_list[line] = tmp[1]
		elif "homer_MOTIF_HOMER" in line:
			if "-CHIP-SEQ" in line:
				tmp = line.split("-CHIP-")[0]
				tmp1 = tmp.split("-")[-1]
				TF_list[line] = tmp1.replace(".GFP","")
			else:
				tmp = line.split("_")
				TF_list[line] = "_".join(tmp[4:])
		elif "HSAPIENS-ENCODE-MOTIFS-" in line:
			tmp = line.replace("HSAPIENS-ENCODE-MOTIFS-","")
			TF_list[line] = tmp.split("_")[0]		
		elif "HSAPIENS-FACTORBOOK-" in line:
			tmp = line.replace("HSAPIENS-FACTORBOOK-","")
			TF_list[line] = tmp
		elif "CIS-B_" in line:
			tmp = line.split("_")
			TF_list[line] = tmp[3]
			
		else:
			print ("something wrong")
	return TF_list
	
motif_list = pd.read_csv("/home/yli11/Data/Motif_database/Human/motif.list",header=None)
motif_list = motif_list[0].tolist()
TF_list = get_TF_name(motif_list)
df=pd.DataFrame.from_dict(TF_list,orient="index")
# print (df.head())
pwm_list = df[df[0]==TF_query].index.tolist()

print ("Number of identified pwm is: %s"%(len(pwm_list)))

import re


OutPutpwmFileName = "%s.pwm"%(TF_query)
allPwmFile = "/home/yli11/Data/Motif_database/Human/human.meme"

selected_motifs_name = pwm_list
pwmFile = open(OutPutpwmFileName, 'wb')				
pwmFile.write('MEME version 4.4\nALPHABET= ACGT\nstrands: + -\nBackground letter frequencies (from web form):\nA 0.25000 C 0.25000 G 0.25000 T 0.25000\n\n')				

#read the allPWM file and get the sol PWMs and write them to a file				
flag = 0				
with open(allPwmFile, 'rb') as handler:				
		
	for line in handler:			
			
		line = line.strip()		
		# print "This is the line in allpwm",line	
		if re.search(r'MOTIF', line):		
			# print "asd"	
			split = line.split()	
			motifName  = split[1]
			# print	motifName		
			if motifName in selected_motifs_name:	
				# print "In :",motifName
				flag = 1
				pwmFile.write(line + '\n')
				continue
			else:	
				flag = 0
				
		if flag == 1:		
			pwmFile.write(line + '\n')	
#close the file				
pwmFile.close()				




	