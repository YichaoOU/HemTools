Optimal subset finding problem in mutagenesis studies
===================




Summary
^^^^^^

Finding a preferred subset from a given set of features is a common problem in biology. With different constraints, the problem can be mapped to set cover problem if user requires a minimal cardinality subset or mapped to feature selection problem if user wants to find the most distriminative subset between positive class and negative class. While the significance of individual feature can be quantified easily using statistical tests (e.g., DESEQ), the combination of features can't be evaluated over the entire space because of the curse of dimensionality. One common approach to reduce the computational cost is to solve the problem through some kind of heuristic algorithm. 

Here, we consider an optimal subset finding problem where the user has :math:`K` preferred features. The user would like to extend the :math:`K` features and find a superset that is of interest in terms of some metric. On the other direction, the user is also flexible on the "preferred" features; namely, the user would like to remove some feature(s) and find a subset that is of interest. In this study, we formally define the optimal subset finding problem and solve the problem via a greedy algorithm that finds sub-optimal solutions and a branch-and-bound algorithm that finds the exact optimal solution. We demonstrate the effectiveness of the solutions in mutagenesis studies.

.. todo::

	branch-and-bound algorithm


Problem definition
^^^^^

We consider a mutagenesis study where :math:`N` number of experiments have been sequenced and the total number of observed mutations is denoted by set :math:`M = \{M_1,M_2,...,M_m\}, m=|M|`. The number of reads in each experiments is denoted by :math:`R = \{R_1,R_2,...,R_N\}`.

Given $k$ number of candidate mutations (e.g., selected for DESEQ2 results), the biological question is to examine if the co-occurring of the $k$ mutations, and the subset of the $k$ mutations or the superset of the $k$ mutations are also significantly enriched in each sample. In other words, we ask if adding $t$ new mutations to the set or removing $t$ mutations ($t<k$) from the set can produce more biological meaningful mutation sets. 

A formal statement of this optimization problem is as follows. Let :math:`A^i` be a read count table for mutagenesis experiment $i$, $m$ be the number of observed mutations, and $r$ be the number of reads in sample $i$, where

.. math::

	\begin{equation*}
		A^i_{r,m} = 
		\begin{pmatrix}
			a_{1,1} & a_{1,2} & \cdots & a_{1,m} \\
			a_{2,1} & a_{2,2} & \cdots & a_{2,m} \\
			\vdots  & \vdots  & \ddots & \vdots  \\
			a_{r,1} & a_{r,2} & \cdots & a_{r,m} 
		\end{pmatrix}
	\end{equation*}

	and
	
	\begin{align*}
		a_{r,m} = \left\{ \begin{array}{rcl}
			1 & & \textrm{if mutation } m \textrm{ occurs in read } r \\
			0 &  & \textrm{otherwise}
		\end{array}\right.
	\end{align*}

Next, let $M = \{M_1,M_2,...,M_m\}$ be the mutation set and $K = \subset M$ be the set for user-defined $k$ mutations, where $|K|=k$. Let $C(K,A^i)$ be the number of reads that contains all mutations in $K$ and $t$ be an integer less than $k$. Then the objective is to find a subset of $K$, denoted by $S$ ($|S|=k-t$) or a superset of $K$, denoted by $S$ ($|S|=k+t$),  such that $$  D(K,t,A) = \sum_{i=1}^{n} \frac{C(K,A^i) - C(S,A^i)}{C(K,A^i)}  $$ is minimized. 

When finding the subset of $K$, the total number of reads containing the subset mutations will be larger than the total number of reads containing the $k$ mutations, therefore we would like to find a subset that maximize the difference (i.e., the gain by reducing some constraints), which is equivalent to minimize the negative gain. The denominator is a normalization factor. Similarly, when finding the superset of $K$, the total number of reads will decrease, therefore we would like to find a superset that minimize the number of dropped reads. Thus, both searching directions can be formulated as a minimization problem.

It is obvious that $D(K,t=1,A)$ is always better (i.e., smaller) than $D(K,t=2,A)$ because (1) for subset of $K$

Like other combinatorial problems, the $k$-mutation optimization problem is NP-hard. Here, we provide a branch-and-bound algorithm that solves the problem in a pseudo-polynomial time when $t$ is small (e.g., $t<=3$).






