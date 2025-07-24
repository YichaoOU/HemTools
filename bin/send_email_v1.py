#!/hpcf/apps/python/install/2.7.13/bin/python
import sys
import os
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path.append(os.path.abspath(p_dir+"../utils/"))
from utils import *
'''
sometimes, the email won't be sent because of the attached files do not exist. 

This is a stand-alone script ot overcome that issue by checking the existence of attachments.



'''

def send_email_with_template_body(attachments,body_file,subject):
	command = ' mailx {{attachments}} -s "{{subject}}" -- User_name@stjude.org < {{body_file}}'
	command = command.replace("{{body_file}}",body_file)
	command = command.replace("{{subject}}",subject)
	command = command.replace("User_name",username)
	real_attachments = []
	for item in attachments:
		if os.path.isfile(item):
			real_attachments.append(item)
	attachments_string = map(lambda x: '-a "'+x+'" ',real_attachments)
	command = command.replace("{{attachments}}","".join(attachments_string))
	os.system(command)
	# print command
	os.system("rm %s"%(body_file))
	
def send_email_with_message(attachments,message,subject):
	command = ' echo "{{message}}" | mailx {{attachments}} -s "{{subject}}" -- User_name@stjude.org '
	command = command.replace("{{message}}",message+"\n\nYour result is located at:\n"+os.getcwd())
	command = command.replace("{{subject}}",subject)
	command = command.replace("User_name",username)
	real_attachments = []
	for item in attachments:
		if os.path.isfile(item):
			real_attachments.append(item)
		else:
			item = glob.glob("%s"%item)[0]
			if os.path.isfile(item):
				real_attachments.append(item)
	attachments_string = map(lambda x: '-a "'+x+'" ',real_attachments)
	command = command.replace("{{attachments}}","".join(attachments_string))
	os.system(command)
	# print command
	
def send_email_no_attachment(message,subject):
	command = ' echo "{{message}}" | mailx -s "{{subject}}" -- User_name@stjude.org '
	command = command.replace("{{message}}",message+"\n\nYour result is located at:\n"+os.getcwd())
	command = command.replace("{{subject}}",subject)
	command = command.replace("User_name",username)
	os.system(command)
	# print command

	
def parse_pyGREAT_url():
	url_files = glob.glob("*_pyGREAT.url")
	if len(url_files) == 0:
		return ""
	outline = ['Identified peaks have been annotated (e.g., GO enrichment analysis) using GREAT, see results below:']
	for f in url_files:
		url = open(f).readlines()[0].strip().split()[-1]
		outline.append('%s: %s'%(f.replace("_pyGREAT.url",""),url))
	return "\n\n".join(outline)
	
def parse_ppr_url():
	url_file = glob.glob("*_ppr.url")[0]
	outline = ['Protein Paint tracks have been generated, see links below:']
	try:
		for line in open(url_file).readlines():
			type,url = line.strip().split()
			outline.append('%s: %s'%(type,url))
		return "\n\n".join(outline)
	except:
		return ""
	
def find_failed_jobs():
	try:
		
		files = read_file_to_list("lsf_job_status.log")
		if len(files) > 0:
			outline = ['ERROR! The following jobs were terminated unexpectedly:']
			outline+=files
			return "\n".join(outline)
		else:
			return "All jobs ran successfully!"
	except:
		return ""

def NGS_pipeline_email(args):
	jid = args.jid
	attachments = str(args.attachments).split(",")
	template_file = p_dir+"../share/NGS_pipeline/email.template"
	result_dir = os.getcwd()+"/"+jid+"/"
	myDict = {
	"jid":jid,
	"username":username,
	"result_dir":result_dir,
	"peak_url":parse_pyGREAT_url(),
	"failed_jobs":find_failed_jobs(),
	"track_url":parse_ppr_url()
	}
	body = multireplace("".join(open(template_file).readlines()), myDict)
	write_file(args.jid+".email.log",body)
	send_email_with_template_body(attachments,args.jid+".email.log",jid)


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-j',"--jid",  help="this is your subject. for NGS pipelines, it is your jobID.")	
	mainParser.add_argument('-a',"--attachments",  help="attachments")	
	mainParser.add_argument('-m',"--message",  help="message")	
	mainParser.add_argument('--common',  help="message", action='store_true')	
	
	mainParser.add_argument('--NGS',  help="Not for end-user.", action='store_true')

	
	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def main():
	args = my_args()
	if args.NGS:
		NGS_pipeline_email(args)
	elif args.common:
		send_email_with_message(str(args.attachments).split(","),args.message,args.jid)
	else:
		send_email_no_attachment(args.message,args.jid)

	
if __name__ == "__main__":
	main()








