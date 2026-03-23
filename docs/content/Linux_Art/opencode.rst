Setup opencode on HPC
=======================



Usage
--------

my example working dir is set to /home/yli11/test/AIflow/test_data



I've added stjude local qwen model to ``/home/yli11/.config/opencode/opencode.jsonc``

::

	hpcf_interactive.sh # go to compute node

	module load conda3/202402 

	source activate jupyterlab_2024 # setup good python env for opencode

	module load nodejs/22.20.0

	export NODE_TLS_REJECT_UNAUTHORIZED=0

	# cd to your dir

	git init

	export OPENCODE_CONFIG_DIR=$PWD # export to current dir, so that skills in project dir can be loaded

	opencode web --port 45713 --hostname 0.0.0.0

	API_URL=http://10.220.17.11:45713 PORT=45710 DEFAULT_DIRECTORY=$PWD serve-ui

https://opencode.ai/docs/skills/


You might need to remove old session in order to get to the current dir easier

::

	mkdir ~/tmp/opencode

	cd ~/.local/share/opencode

	mv -f snapshot/ ~/tmp/opencode
	mv -f bin/ ~/tmp/opencode
	mv -f tool-output/ ~/tmp/opencode
	mv -f storage/ ~/tmp/opencode
	mv -f opencode* ~/tmp/opencode
	mv -f log/ ~/tmp/opencode




::

	{
	  "permission": {
	    "bash": "allow",
	    "read": "allow",
	    "edit": "allow",
	    "external_directory": "allow"
	  },
	  "model": "stjude-qwen/Qwen/Qwen3.5-27B-FP8"
	}
	opencode run --model "stjude-qwen/Qwen/Qwen3.5-27B-FP8"  "summary current folder and save to summary.md"






Build opencode for QWEN
-----------------

There is an important bug fix, currently not in any release, for QWEN models, https://github.com/anomalyco/opencode/pull/16981. I have patched it and build a local opencode version.

::

	module load conda3/202402

	source activate jupyterlab_2024

	git clone https://github.com/anomalyco/opencode.git\ncd opencode

	conda install -c conda-forge gh

	gh pr checkout 15018

	module load nodejs/22.20.0

	npm install -g bun

	bun install

	cd /research/rgs01/home/clusterHome/yli11/Programs/opencode/packages/opencode

	bun run build

	#binary is /research/rgs01/home/clusterHome/yli11/Programs/opencode/packages/opencode/dist/opencode-linux-x64
