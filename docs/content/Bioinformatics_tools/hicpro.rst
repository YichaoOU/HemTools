HiC-Pro
=======




.. code:: bash

	module load hic-pro/2.10.0 
	
	sparseToDense.py -b GSM3489136/raw/20000/GSM3489136_20000_abs.bed GSM3489136/iced/20000/GSM3489136_20000_iced.matrix --perchr

::

	-rwxrwx--- 1 yli11 chenggrp    0 Jun 26 17:43 01-S10_S8_hg19.bwt2pairs.SinglePairs
	-rwxrwx--- 1 yli11 chenggrp    0 Jun 26 17:43 01-S10_S8_hg19.bwt2pairs.FiltPairs
	-rwxrwx--- 1 yli11 chenggrp 513M Jun 26 17:49 01-S10_S8_hg19.bwt2pairs.DEPairs
	-rwxrwx--- 1 yli11 chenggrp  64M Jun 26 17:49 01-S10_S8_hg19.bwt2pairs.REPairs
	-rwxrwx--- 1 yli11 chenggrp 966K Jun 26 17:49 01-S10_S8_hg19.bwt2pairs.SCPairs
	-rwxrwx--- 1 yli11 chenggrp 1.9M Jun 26 17:49 01-S10_S8_hg19.bwt2pairs.DumpPairs
	-rwxrwx--- 1 yli11 chenggrp  315 Jun 26 17:49 01-S10_S8_hg19.bwt2pairs.RSstat
	-rwxrwx--- 1 yli11 chenggrp 197M Jun 26 17:50 01-S10_S8_hg19.bwt2pairs.validPairs
	-rwxrwx--- 1 yli11 chenggrp 130M Jun 26 17:50 S10_S8.allValidPairs

``.allValidPairs`` is a subset of ``.bwt2pairs.validPairs``, duplicate pairs were remove. Although in my test, there is still 8 reads that were not present in ``.allValidPairs``, but it should not be a big deal.


::

	>>> import pandas as pd
	>>> df = pd.read_csv("01-S10_S8_hg19.bwt2pairs.validPairs",sep="\t",header=None)
	df.head()
	>>> df.head()
	                                          0     1      2  3      4   \
	0   NB551526:94:HWGJCAFXY:3:11608:15104:6190  chr1  46758  -  chr20
	1   NB551526:94:HWGJCAFXY:4:21407:26485:9909  chr1  47311  -  chr19
	2  NB551526:94:HWGJCAFXY:2:11112:13155:18714  chr1  54539  +  chr12
	3   NB551526:94:HWGJCAFXY:4:21504:1612:13700  chr1  54560  +  chr12
	4    NB551526:94:HWGJCAFXY:1:11110:7058:7312  chr1  55163  -  chr11

	          5  6    7             8                 9   10  11  12
	0   62896985  -  380   HIC_chr1_87  HIC_chr20_155036  12  42 NaN
	1   38776303  -  470   HIC_chr1_89  HIC_chr19_107037  30  42 NaN
	2  125027356  +  418  HIC_chr1_104  HIC_chr12_309792  32  42 NaN
	3  133749376  +  227  HIC_chr1_104  HIC_chr12_331541  34  42 NaN
	4    5305858  -  217  HIC_chr1_108   HIC_chr11_12428  30  42 NaN
	>>> df['name'] = df[1]+df[2].astype(str)+df[3]+df[4]+df[5].astype(str)+df[6]
	df.sha>>> df.shape
	(1758798, 14)
	>>> df2 = df.drop_duplicates('name')
	d>>> df2.shape
	(1154108, 14)
	>>> df3 = pd.read_csv("S10_S8.allValidPairs",sep="\t")
	df>>> df3.shape
	(1154099, 13)
	>>> df3.head()
	    NB551526:94:HWGJCAFXY:3:11608:15104:6190  chr1  46758  -  chr20  \
	0   NB551526:94:HWGJCAFXY:4:21407:26485:9909  chr1  47311  -  chr19
	1  NB551526:94:HWGJCAFXY:2:11112:13155:18714  chr1  54539  +  chr12
	2   NB551526:94:HWGJCAFXY:4:21504:1612:13700  chr1  54560  +  chr12
	3    NB551526:94:HWGJCAFXY:1:11110:7058:7312  chr1  55163  -  chr11
	4   NB551526:94:HWGJCAFXY:2:21305:7748:12626  chr1  57020  -   chr3

	    62896985 -.1  380   HIC_chr1_87  HIC_chr20_155036  12  42  Unnamed: 12
	0   38776303   -  470   HIC_chr1_89  HIC_chr19_107037  30  42          NaN
	1  125027356   +  418  HIC_chr1_104  HIC_chr12_309792  32  42          NaN
	2  133749376   +  227  HIC_chr1_104  HIC_chr12_331541  34  42          NaN
	3    5305858   -  217  HIC_chr1_108   HIC_chr11_12428  30  42          NaN
	4  164831235   -  211  HIC_chr1_111   HIC_chr3_389134  37  42          NaN
	>>> df3 = pd.read_csv("S10_S8.allValidPairs",sep="\t",header=None)
	df3.shape
	>>> df3.shape
	(1154100, 13)
	>>> df3['name'] = df3[1]+df3[2].astype(str)+df3[3]+df3[4]+df3[5].astype(str)+df3[6]
	>>> set(df2['name'])-set(df3['name'])
	set(['chr115301553+chr115306194+', 'chr115305918-chr115306815+', 'chr11118726979+chr11118727287+', 'chr115306032-chr115319515+', 'chr115305923-chr115306776-', 'chr44699704-chr44699999-', 'chr115297821-chr115306182+', 'chr173812666+chr173964964+'])






