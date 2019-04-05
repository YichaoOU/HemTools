#!/hpcf/apps/python/install/2.7.13/bin/python
from utils import *
import glob
import pickle
import sys
# module load python/2.7.13
'''
upload bw files
generate tracks.json for:
- all.bw
- rmdup.uq.bw
- treat_pvalue.bw
- logRE.bw
- FE.bw



upload_tracks.py will upload any .bw files in the current DIR to protein paint and email you the link (HemTools upload_tracks) 

This script is a stand-alone program.
STJtracks.py is designed for NGS pipeline to create tracks.json for different types of bw files 
'''
file = open(sys.argv[1], 'rb')
[jid,myDict] = pickle.load(file)
# print jid
# print myDict
# exit()
file.close()
f = open(jid+".url","wb")
flag = True
for k in myDict:
	if len(myDict[k]) == 0:
		continue
	try:
		url = run_upload_tracks(jid,myDict[k],k,dir=flag)
		flag = False
	except:
		continue
	print >>f,k,url
f.close()