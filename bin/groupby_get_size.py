#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
"""




"""
current_file_base_name = __file__.split("/")[-1].split(".")[0]

def my_args():
	username = getpass.getuser()
	addon_string = str(uuid.uuid4()).split("-")[-1]
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description="groupby and print group size")
	mainParser.add_argument("-f","--input",  help="input bed",required=True)
	mainParser.add_argument("-g","--groupby",  help="separated by ,",required=True)
	mainParser.add_argument("-o","--output",  help="extend length",default="output.bed")


	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

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
				
	
def main():

	args = my_args()
	df = pd.read_csv(args.input,sep=guess_sep(args.input))
	groupby_list = args.groupby.split(",")
	tmp = pd.DataFrame(df.groupby(groupby_list).size())
	tmp =  tmp.sort_values(0,ascending=False)
	tmp.to_csv(args.output)

if __name__ == "__main__":
	main()






