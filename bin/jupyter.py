#!/home/yli11/.conda/envs/py2/bin/python


import os
import io 
import numpy as np
import subprocess
import random

a = subprocess.Popen("ip addr show | grep 220",stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
b=a.communicate()
# print (b)
b = str(b[0])
b = b.split()[2]
# print (b)
IP = b.split("/")[0]
print (IP)

port = random.randint(49152,65530)
import getpass

username = getpass.getuser()
def send_email_no_attachment(IP,port):
	command = ' echo "{{message}}" | mailx -s "jupyter notebook links" -- %s@stjude.org '%(username)
	message = "Please click http://%s:%s to access the jupyter notebook. This link is only accessible within stjude."%(IP,port)
	command = command.replace("{{message}}",message)
	os.system(command)


send_email_no_attachment(IP,port)
command = "jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password='' --no-browser --port %s"%(port)
os.system(command)


# command = "chmod -R 777 /home/yli11/.local/share/;rm -r /home/yli11/.local/share/jupyter/;mkdir /run/user/1018339;chmod 777 -R /run/user/1018339;jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password='' --no-browser --port %s --allow-root --notebook-dir ."%(port)
# command = "chmod -R 777 /home/yli11/.local/share/;rm -r /home/yli11/.local/share/jupyter/;mkdir /run/user/1018339;chmod 777 -R /run/user/1018339;jupyter notebook --port %s "%(port)