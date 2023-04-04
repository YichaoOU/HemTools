Notes on how to use plink
======================

I found PLINK is really fast.

``module load plink/2.0``


subset by individuals
^^^^^^^^^^^^^^^^^^^

My sample ID is named like ``NA06985_NA06985``, so the keep list just need one column.

::

	[yli11@noderome203 test]$ head 2.list
	NA06985_NA06985
	[yli11@noderome203 test]$ plink2 --vcf chrAll.95samples.withinRegions.v2.03282023.vcf --keep 2.list --out test --export vcf


	[yli11@noderome203 test]$ head 3.list 
	NA06985
	NA06986
	[yli11@noderome203 test]$ plink2 --vcf $f --keep 3.list --out test2 --export vcf


subset by region
^^^^^^^^^^^^^^^^^^^










