Convert bed files to vcf
==================

::

	usage: bed2vcf.py [-h] -f TSV --required_cols REQUIRED_COLS --info_cols
	                  INFO_COLS --info_types INFO_TYPES [-o OUTPUT]
	                  [--column_number COLUMN_NUMBER] [--add_chr]
	                  [--remove_cols REMOVE_COLS] [--log10_cols LOG10_COLS]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f TSV, --tsv TSV     input tsv file (default: None)
	  --required_cols REQUIRED_COLS
	                        input the chr, pos, ID, ref, alt col names in order
	                        (default: None)
	  --info_cols INFO_COLS
	                        input col names (please make sure no spaces in the col
	                        names) to be put in the info column (default: None)
	  --info_types INFO_TYPES
	                        input col types for the info columns, should match
	                        info cols in order. choose from Integer, Float, String
	                        (default: None)
	  -o OUTPUT, --output OUTPUT
	                        output file name (default: bed2vcf.vcf)
	  --column_number COLUMN_NUMBER
	                        if no header, then columns will be named as numbers,
	                        start from 0 (default: None)
	  --add_chr             add string chr to the chrom column (default: False)
	  --remove_cols REMOVE_COLS
	                        remove columns not used in the vcf file (default:
	                        None)
	  --log10_cols LOG10_COLS
	                        convert a col to -np.log10 (default: None)


Summary
^^^^^^^

This program converts any tsv to vcf file (tabix index).

The output vcf file can be visualized on protein paint with the following json:

``"locusinfo":{ "key":"P" },`` is the key option to show variants spreading on different values.

::

	{"type":"vcf",
	"name":"TableS3",
	"file":"yli11/CRM_gRNA/SGP/TableS3.hg19.vcf.gz",
	"itemlabelname":"variant",
	"axisheight":200,
	"vcfinfofilter":{
		"lst":[
			{ "name":"-log10 P value", 
			"locusinfo":{ "key":"P" },
			"numericfilter":[{"side":">","value":2},{"side":">","value":10}] 
			}

			],
		"setidx4numeric":0
		}
	}

Input
^^^^^

::

chr2	60724085	60724086	rs1896295	BCL11A	T	C	37/201/307	0.25229	-11.0735	1.02e-25	-0.6421	0.05798	0.1917
chr2	60718042	60718043	rs1427407	BCL11A	T	G	35/186/324	0.23485999999999999	-11.0656	1.09e-25	-0.6471	0.05848	0.1915



Usage
^^^^^


.. code:: bash

	hpcf_interactive.sh

	module load python/2.7.13

	bed2vcf.py -f input.bed --required_cols 0,2,3,5,6  --column_number 4,7,8,9,10,11,12,13  --info_types String,String,Float,Float,Float,Float,Float,Float  --info_cols Nearest_gene,GENO,MAF,STAT,P,BETA,SEBETA,R2 --remove_cols 1 --log10_cols 10 --output TableS3.hg19.vcf


In the example input file, we have 14 columns, the required columns for vcf file is ``chr, pos, id, ref, alt``, which corresponds to column ``0,2,3,5,6``. We also want to include the ``INFO`` column for vcf file, which includes column ``4,7,8,9,10,11,12,13``, the corresponding labels are ``Nearest_gene,GENO,MAF,STAT,P,BETA,SEBETA,R2`` and the types are ``String,String,Float,Float,Float,Float,Float,Float``. Lastly, the pvalue is column 10 and we want to convert it to -np.log10. ``--remove_cols 1`` will delete column 1 from out input, which is the "start" position in the bed file.

The output is ``TableS3.hg19.vcf.gz`` and ``TableS3.hg19.vcf.gz.tbi``







