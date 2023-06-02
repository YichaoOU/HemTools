GTF operations
==============


Get gene bed
--------------

::
	
	module load pygtftk
	gtftk select_by_key -i Homo_sapiens.add_chr.GRCh38.96.gtf -k feature -v gene | gtftk convert -n gene_name  -f bed6| head -n 3


REF: https://dputhier.github.io/pygtftk/conversion.html#convert

