conda cheatsheet
================

You may want to create a Conda environment to share with all your group members. In this case you will need to create the environment in a new location. You can do this with the --prefix command. For example:

conda create --prefix $SCRATCH/../conda/envs/<environment_name>
This will create the environment in the root of your group's scratch directory. To activate this environment requires a little more typing since it's not in the standard location for Conda environments

source activate /panfs/pfs.local/scratch/<your_group>/conda/envs/<environment_name>

.. code:: bash

	jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password=''

Commonly used python libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	import pandas as pd
	import seaborn as sns
	%matplotlib inline
	import matplotlib.pyplot as plt
	import matplotlib.colors as clr
	import numpy as np
	from matplotlib.colors import ListedColormap
	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib import cm
	from matplotlib.colors import ListedColormap, LinearSegmentedColormap
	import pandas as pd
	import matplotlib.pylab as plt
	import numpy as np
	import scipy
	import seaborn as sns
	import glob

Ignore python warning

export PYTHONWARNINGS="ignore"

