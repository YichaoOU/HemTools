Optimal subset finding problem in mutagenesis studies
===================




Summary
^^^^^^

Finding a preferred subset from a given set of features is a common problem in biology. With different constraints, the problem can be mapped to set cover problem if user requires a minimal cardinality subset or mapped to feature selection problem if user wants to find the most distriminative subset between positive class and negative class. While the significance of individual feature can be quantified easily using statistical tests (e.g., DESEQ), the combination of features can't be evaluated over the entire space because of the curse of dimensionality. One common approach to reduce the computational cost is to solve the problem through some kind of heuristic algorithm. 

Here, we consider an optimal subset finding problem where the user has :math:`K` preferred features. The user would like to extend the :math:`K` features and find a superset that is also of interest in terms of some metric. On the other direction, the user is also flexible on the "preferred" features; namely, the user would like to remove some feature(s) and find a subset that is of interest. In this study, we formally define the optimal subset finding problem and solve the problem via a greedy algorithm that finds sub-optimal solutions and a branch-and-bound algorithm that finds the exact optimal solution. We demonstrate the effectiveness of the solutions in mutagenesis studies.

.. todo::

	branch-and-bound algorithm
	

Problem definition
^^^^^

We consider a mutagenesis study where :math:`N` number of experiments have been sequenced and the total number of observed mutations found is denoted by set :math:`M = \{M_1,M_2,...,M_m\}, m=|M|`. The number of reads in each experiments is denoted by :math:`R = \{R_1,R_2,...,R_N\}`.

Given :math:`k` number of candidate mutations (e.g., selected for DESEQ2 results), the biological question is to examine if the co-occurring of the $k$ mutations, and the subset of the $k$ mutations or the superset of the $k$ mutations are also significantly enriched in each sample. 







