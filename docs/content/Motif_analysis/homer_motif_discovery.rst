Homer motif discovery
==================



Usage
^^^^^


I usually search motifs with multiple parameter combinations, for example:


::

	homer_motif_discovery.py -f input.list -g mm9 -s 200 -m 2 -n 50

	homer_motif_discovery.py -f input.list -g mm9 -s 500 -m 2 -n 50

	homer_motif_discovery.py -f input.list -g mm9 -s given -m 2 -n 50

	homer_motif_discovery.py -f input.list -g mm9 -s 1000 -m 2 -n 50



You can reduce ``-n 50`` to ``-n 10`` when you use homer on the same input the second time, because you have an idea of what the motifs would look like. In this case, I usually increase the number of mismatches to 3.

::

	homer_motif_discovery.py -f input.list -g mm9 -s 200 -m 3 -n 10

	homer_motif_discovery.py -f input.list -g mm9 -s 500 -m 3 -n 10

	homer_motif_discovery.py -f input.list -g mm9 -s given -m 3 -n 10

	homer_motif_discovery.py -f input.list -g mm9 -s 1000 -m 3 -n 10

Sometimes I only want to search on one strand, for NFIX motif, because it is a palindromic motif:

::

	homer_motif_discovery.py -f input.list -g mm9 -s 200 --homer_addon " -norevopp" -m 2

	homer_motif_discovery.py -f input.list -g mm9 -s 500 --homer_addon " -norevopp" -m 2

	homer_motif_discovery.py -f input.list -g mm9 -s given --homer_addon " -norevopp" -m 2

	homer_motif_discovery.py -f input.list -g mm9 -s 200 --homer_addon " -norevopp" -m 3

	homer_motif_discovery.py -f input.list -g mm9 -s 500 --homer_addon " -norevopp" -m 3

	homer_motif_discovery.py -f input.list -g mm9 -s given --homer_addon " -norevopp" -m 3





Notes
^^^^

