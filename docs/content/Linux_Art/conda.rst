conda cheatsheet
================

You may want to create a Conda environment to share with all your group members. In this case you will need to create the environment in a new location. You can do this with the --prefix command. For example:

conda create --prefix $SCRATCH/../conda/envs/<environment_name>
This will create the environment in the root of your group's scratch directory. To activate this environment requires a little more typing since it's not in the standard location for Conda environments

source activate /panfs/pfs.local/scratch/<your_group>/conda/envs/<environment_name>

::
	jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password=''