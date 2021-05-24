#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *

'''
upload bw files by types
generate tracks.json for:
- all.bw
- rmdup.uq.bw
- rmdup.bw
- treat_pvalue.bw
- logRE.bw
- FE.bw

upload tracks in the current dir

'''
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="a folder name, used to upload tracks", default=current_file_base_name+'_'+username+"_"+str(datetime.date.today()))	
	mainParser.add_argument('-g','--genome',  help="genome version: hg19, hg38, mm9, mm10.", default='hg19',type=str)
	mainParser.add_argument('--current_dir',  help="Upload .bedpe .mango .bed .narrowPeak .broadPeak and .bw files",action='store_true' )
	# mainParser.add_argument('--interaction',  help="Upload .bedpe and .mango files",action='store_true' )
	##------- add parameters above ---------------------
	
	args = mainParser.parse_args()	
	return args

def main():

	args = my_args()
	
	if args.current_dir:
	
		url = upload_bed_bw(args.jid+str(uuid.uuid4()).split("-")[-1],True,args.genome)
		print "Please copy the following url to your genome browser. Note that protein paint genome browser is only accessible inside stjude network."
		print url
		exit()

	flag = True
	files = glob.glob("*.bw")
	myDict = {}
	keywords = ["markdup.bw","rmdup.uq.bw","rmdup.bw","treat_pvalue.bw","logLR.bw","FE.bw"]
	for k in keywords:
		myDict[k] = []
	for f in files:
		for k in keywords:
			if k in f:
				myDict[k].append(f)
				break
	f = open(args.jid+"_ppr.url","wb")
	for k in myDict:
		if len(myDict[k]) == 0:
			continue
		try:
			logging.info( "uploading "+k)
			url = run_upload_tracks(args.jid,myDict[k],k,flag,args.genome)
			print url
			flag = False
			logging.info( "finish uploading "+k)
		except Exception as e:
			logging.error(str(e))
			continue
		print >>f,k,url
	f.close()


	
if __name__ == "__main__":
	main()

























