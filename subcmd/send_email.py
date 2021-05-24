#!/hpcf/apps/python/install/2.7.13/bin/python
from utils import *
import glob
import pickle
import sys
import os
import getpass
'''
sometimes, the email won't be sent because of the attached files do not exist. 

This is a stand-alone script ot overcome that issue by checking the existence of attachments.



'''

username = getpass.getuser()
def send_email_command(attachments,jid,urlDict):
	command = 'echo "Hi User_name,\n\nYour JOB_ID is finished. Please see the attachment for a summary of results. The results have been generated the following directory:\n RESULT_DIR \n\n If no attachment can be found, it might be caused by an error. In such case, please go to the result directory (above) and do HemTools report_bug. \n\n BigWiggle_URL" | mailx {{attachments}} -s "JOB_ID is finished" -- User_name@stjude.org'
	# attachments = attachments.split(",")
	command = command.replace("JOB_ID",jid)
	# print attachments
	real_attachments = []
	for item in attachments:
		if os.path.isfile(item):
			real_attachments.append(item)
	attachments_string = map(lambda x: '-a "'+x+'" ',real_attachments)
	# attachments_string = map(lambda x: '-a "'+x+'" ',attachments)
	command = command.replace("{{attachments}}","".join(attachments_string))
	# command = command.replace("attachment_file",attachments)
	command = command.replace("User_name",username)
	command = command.replace("RESULT_DIR",os.getcwd()+"/"+jid+"/")
	if len(urlDict) > 0:
		outlines = []
		for k in urlDict:
			outlines.append(k+" tracks can be viewed at: "+urlDict[k])
		command = command.replace("BigWiggle_URL","\n\n".join(outlines))
	else:
		command = command.replace("BigWiggle_URL","")
	os.system(command)


file = open(sys.argv[1], 'rb')
[attachments,jid,urlDict] = pickle.load(file)
send_email_command(attachments,jid,urlDict)
file.close()