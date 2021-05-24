#!/home/yli11/.conda/envs/share_url/bin/python

"""
rGREAT is the best if it works for you. But it doesn't work for me.

Motivation
----------

My work here at St. Jude is to develop pipelines and simplify user's effort for NGS analyses.
I don't want users, when finish running my HemTools pipeline, have to upload bed files to GREAT
server themselves.

Summary
-------

This tool uses Dropbox to create a sharable link and then use it for GREAT analysis. It will
print out a GREAT url. You then just need to copypaste the url to a browser to check out the results.


Installation
------------

module load conda3
conda create -n share_url
source activate share_url
conda install -c anaconda dropbox

Please follow the dropbox instruction below, mainly, you need a token.
The dropbox code is taken from: https://gist.github.com/Keshava11/d14db1e22765e8de2670b8976f3c7efb

Usage
-----

python pyGREAT.py test.bed

Return
------

http://great.stanford.edu/public/cgi-bin/greatStart.php?requestURL=https://www.dropbox.com/s/jd9q2489k91m8bj/test.bed?dl=0&requestSpecies=hg19&requestName=ensGene&requestSender=UCSC%20Table%20Browser

"""

# Prerequisites :
# 1.SetUp dropbox sdk to be able to use Dropbox Api's
# $ sudo pip install dropbox
# By default python dropbox sdk is based upon the python 3.5
#
# 2. Create an App on dropbox console (https://www.dropbox.com/developers/apps) which will be used and validated to do
# the file upload and restore using dropbox api. Mostly you need an access token to connect to Dropbox before actual file/folder operations.
#
# 3. Once done with code, run the script by following command
# $ python SFileUploader.py // if python3.5 is default

import uuid
import os
import sys
import dropbox
import argparse
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import getpass
username = getpass.getuser()
# Access token
TOKEN = 'KXA53e1kGzsAAAAAAAAAASNwHMFF_LTPhfIOyaHP8uwAHvE387Nreav8JioFMNVy'


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	mainParser.add_argument('--email',  help="send email", action='store_true')
	mainParser.add_argument('-f',"--bed",  help="bedfile",required=True)
	mainParser.add_argument('-g',"--genome",  help="bedfile",required=True)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


# Uploads contents of LOCALFILE to Dropbox
def backup():
	with open(LOCALFILE, 'rb') as f:
		# We use WriteMode=overwrite to make sure that the settings in the file
		# are changed on upload
		# print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
		try:
			dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
		except ApiError as err:
			# This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
			if (err.error.is_path() and
					err.error.get_path().error.is_insufficient_space()):
				sys.exit("ERROR: Cannot back up; insufficient space.")
			elif err.user_message_text:
				print(err.user_message_text)
				sys.exit()
			else:
				print(err)
				sys.exit()


# Adding few functions to check file details
def checkFileDetails():
	print("Checking file details")

	for entry in dbx.files_list_folder('').entries:
		print("File list is : ")
		print(entry.name)

def send_email_no_attachment(message,subject):
	command = ' echo "{{message}}" | mailx -s "{{subject}}" -- User_name@stjude.org '
	command = command.replace("{{message}}",message+"\n\nYour result is located at:\n"+os.getcwd())
	command = command.replace("{{subject}}",subject)
	command = command.replace("User_name",username)
	os.system(command)
	# print command
# Run this script independently
if __name__ == '__main__':
	# Check for an access token
	args = my_args()
	if (len(TOKEN) == 0):
		sys.exit("ERROR: Looks like you didn't add your access token. Open up backup-and-restore-example.py in a text editor and paste in your token in line 14.")
	addon_string = str(uuid.uuid4()).split("-")[-1]
	## process bed
	outfile_name = "%s.pyGREAT"%(addon_string)
	# LOCALFILE = "%s.pyGREAT"%(addon_string)
	LOCALFILE="/scratch_space/%s/%s"%(username,outfile_name)
	os.system("cut -f 1,2,3 %s > %s"%(args.bed,LOCALFILE))
	BACKUPPATH = '/%s'%(outfile_name) # Keep the forward slash before destination filename
	# Create an instance of a Dropbox class, which can make requests to the API.
	# print("Creating a Dropbox object...")
	dbx = dropbox.Dropbox(TOKEN)

	# Check that the access token is valid
	try:
		dbx.users_get_current_account()
	except AuthError as err:
		sys.exit(
			"ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

	# try:
		# checkFileDetails()
	# except Error as err:
		# sys.exit("Error while checking file details")

	# print("Creating backup...")
	# Create a backup of the current settings file
	backup()

	# print("Done!")
	
	result = dbx.sharing_create_shared_link_with_settings(BACKUPPATH).url
	
	# print (result)
	

	link = "http://great.stanford.edu/public/cgi-bin/greatStart.php?requestURL=%s&requestSpecies=%s&requestName=liyc-stjude&requestSender=HemTools"%(result,args.genome)
	print (link)
	if args.email:
		send_email_no_attachment(link,"pyGreat peak analysis link")
