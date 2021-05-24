Community detection
=============












::

	module load conda3
	source activate /home/yli11/.conda/envs/network2020/




Reference
^^^^^^^^

Core difference between each method is their objective function. In other words, how they define community.

Modularity score is a common idea. Two most popular methods are:

1. Louvian method

https://github.com/taynaud/python-louvain

2. Markov clustering method

https://github.com/GuyAllard/markov_clustering

3. Graph embedding (e.g., deepwalk)

Karateclub python package implements 20+ advanced community detection algorithms:

https://github.com/benedekrozemberczki/karateclub

4. Graph neural network

https://github.com/stellargraph/stellargraph

Drawback is the GNN is a supervised method.

graphSAGE provides unsupervided learning, node embedding.

https://github.com/stellargraph/stellargraph/blob/master/demos/community_detection/attacks_clustering_analysis.ipynb

some review papers:

https://www.nature.com/articles/srep30750



https://nbviewer.jupyter.org/github/saibalmars/GraphRicciCurvature/blob/master/notebooks/tutorial.ipynb


Networkx layout
^^^^^^^^^^^^^^


https://stackoverflow.com/questions/21978487/improving-python-networkx-graph-layout


https://github.com/bhargavchippada/forceatlas2


https://hvplot.holoviz.org/user_guide/NetworkX.html



Ego-splitting method for community detection
^^^^^^^^^^^^^^^^^^^^^^^^^

Only one parameter in the Ego-splitting method, ``resolution``, which is the ``time`` resolution parameter mentioned in the Louvian method, intuitively, it relates to the probablity (e.g., average times) that in a random walk process, the first step and the ``time t`` step are being in the same community.

https://www.eecs.yorku.ca/course_archive/2017-18/F/6412/reading/kdd17p145.pdf

https://arxiv.org/pdf/0812.1770.pdf





