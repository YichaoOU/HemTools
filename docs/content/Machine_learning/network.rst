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