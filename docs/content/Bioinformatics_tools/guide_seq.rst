Running GUIDE-seq in HPC
===============




::

	hpcf_interactive
	export PATH=$PATH:/research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/anaconda3/condabin/
	eval "$(conda shell.bash hook)"
	conda activate /research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/anaconda3/envs/changeseq_py3/
	module load bwa
	module load samtools/1.7
	module load homer/4.10
	python /research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/src/guideseq_V3/guideseq/guideseq.py parallel -m test.yaml
	# Below is an example to just run identify and visualization when sam files are already generated, will overwrite existing results
	# python /research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/src/guideseq_V3/guideseq/guideseq.py parallel -m test.yaml --step identify+visualize



::

	hpcf_interactive
	export PATH=$PATH:/research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/anaconda3/condabin/
	eval "$(conda shell.bash hook)"
	conda activate /research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/anaconda3/envs/changeseq_py3/
	module load bwa
	module load samtools/1.7
	module load homer/4.10
	python /research_jude/rgs01_jude/groups/tsaigrp/projects/Genomics/common/src/guideseq_pool/guideseq/guideseq.py parallel -m test.yaml