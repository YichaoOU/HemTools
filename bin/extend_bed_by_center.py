#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
"""get bed center and extend with defined length




"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="get bed center and extend with defined length")
	mainParser.add_argument("-f","--input",  help="input bed",required=True)
	mainParser.add_argument("-e","--extend",  help="extend length",type=int,default=0)
	mainParser.add_argument("--extend_left",  help="extend left length",type=int,default=0)
	mainParser.add_argument("--extend_right",  help="extend right length",type=int,default=0)
	mainParser.add_argument("-o","--output",  help="extend length",default="output.bed")


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	df = pd.read_csv(args.input,sep="\t",header=None)
	df['center'] = (df[1]+df[2])/2
	df['center'] = df['center'].astype(int)
	if args.extend != 0:
		df['start'] = df['center']-args.extend
		df['end'] = df['center']+args.extend
	else:
		df['start'] = df['center']-args.extend_left
		df['end'] = df['center']+args.extend_right	
	df['name'] = df[0]+df['start'].astype(str)+df['end'].astype(str)
	df = df.drop_duplicates('name')
	df[[0,'start','end']].to_csv(args.output,sep="\t",header=False,index=False)
	
	

if __name__ == "__main__":
	main()




