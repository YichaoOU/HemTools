Merge Images
===========




Merge pdf files
^^^^^^^^^^^^

::

	module load texlive/20190410
	pdfjam 9_29_AF043.pdf 512_AF005.pdf 719_AF026.pdf 725_AF026.pdf --nup 2x2 --landscape --outfile out.pdf




Merge png files
^^^^^^^^^^^


::

	montage -tile 5 -mode concatenate  *png merged.png
