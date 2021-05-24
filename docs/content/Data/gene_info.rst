Processed gene info data in HemTools
====================================


Summary
^^^^^^^

Both kallisto and STAR indices were built using Ensembl data. mm10 and hg38 kallisto indices were directly downloaded from kallisto github repo. 

For sleuth, we need t2g table, namely gene ID, transcript ID and gene name.

For gene ID conversion between Entrez ID, Ensembl ID, HGNC ID, and others, we have another table.

Note that during every conversion, you can definitely lose some genes. 

We will use ``Ensembl transcript ID`` as the primary key.


Kallisto/Sleuth and STAR
^^^^^^^^^^^^^^^^^^^^^^^^

We provide 3 tables:

**1. [genome].ensembl_[version].txt --- mm9.ensembl_v67.txt**

Genomic location was obtained from Ensembl ftp, ``cnda.all``: e.g., ftp://ftp.ensembl.org/pub/release-67/fasta/mus_musculus/cdna/Mus_musculus.NCBIM37.67.cdna.all.fa.gz.

Current Ensembl version is v96; for hg19, the highest version is v75; for mm9, it is v67.

::

	ENSMUST00000176802	ENSMUSG00000067978	Vmn2r-ps113	chr17	18186448	18211184	1
	ENSMUST00000097386	ENSMUSG00000067978	Vmn2r-ps113	chr17	18201001	18211184	1

**2. [genome].ensembl_[version].bed --- mm9.ensembl_v67.bed**

This is bed6 format. Strand is denoted as 1 or -1. For human tables, they are + or -.

::

	chr17	18186448	18211184	.	ENSMUST00000176802	1
	chr17	18201001	18211184	.	ENSMUST00000097386	1

**3. [hg19].ensembl_[version].t2g --- hg19.ensembl_v75.t2g**

This is for Sleuth.

::

	target_id		ens_gene		ext_gene
	ENST00000387314 ENSG00000210049    MT-TF
	ENST00000389680 ENSG00000211459  MT-RNR1
















