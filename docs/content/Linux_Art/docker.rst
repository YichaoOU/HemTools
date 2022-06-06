Docker notes
==========





File changes (add, delete, edit) can be done without re-build docker image
-----------------------------------------


https://stackoverflow.com/questions/56670437/add-a-file-in-a-docker-image


https://vsupalov.com/rebuilding-docker-image-development/



run docker in HPC
^^^^^^^^^^^^^^

::

	module load singularity/3.9.8
	# define download image location
	SINGULARITY_CACHEDIR=/research/dept/hem/common/sequencing/chenggrp/pipelines/docker
	singularity pull docker://tobneu/slamdunk
	# the following are the same thing, exec can run a bash script
	singularity exec slamdunk_latest.sif slamdunk -h
	singularity run slamdunk_latest.sif slamdunk -h
	# http://t-neumann.github.io/slamdunk/docs.html#document-Docker