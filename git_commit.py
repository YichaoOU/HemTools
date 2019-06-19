
import sys
import os

comment = sys.argv[1]

os.system("git add *")

os.system("git commit -m %s"%(comment))

os.system("git push")













