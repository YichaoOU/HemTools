Using Git version control
=========================


.. code:: bash


	$ git config credential.helper store

	$ git push http://example.com/repo.

	Username: <type your username>
	Password: <type your password>

	[several days later]
	
	$ git push http://example.com/repo.git

	[your credentials are used automatically]


https://stackoverflow.com/questions/11403407/git-asks-for-username-every-time-i-push


Git to permenantly delete a file
----------------------------



.. code:: bash

	pip install git-filter-repo
	git filter-repo --path bin/GEO_shengdar.sh --invert-paths --force
	git reflog expire --expire=now --all
	# SLOW
	git gc --prune=now --aggressive
	git remote add origin https://github.com/YichaoOU/HemTools
	# SLOW
	git push origin --force --all
	git push origin --force --tags







Add existing project to github
------------


https://help.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line


.. code:: bash

	cd Tools/easy_prime/
	git init
	git add *
	git commit -m "easy prime working in progress"
	git remote add origin https://github.com/YichaoOU/easy_prime.git
	git remote -v
	git push -u origin master


Add large files to gitignore
-------------

git prohibit uploading files > 100M, the following code automatically ignore large files.

.. code:: bash

	find . -size +99M | sed "s|^./||g" | cat > .gitignore

Fix large files in the commit causing error when push
-------------

make a copy before start

::

	git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch ./GSE9891/GSE9891_classification/data_matrix.tsv' HEAD

	git stash # if uncommitted 

	git add .

	git commit -m "update"

	git push --force





