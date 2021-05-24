Generate Motif logo
^^^^^^^^^^^^^^^^^^^


The following commands provide examples to covert eps to pdf / png.

.. code:: bash

	module load meme

	module load texlive/20190410

	meme2images -eps Supp_File_motif_PWM.meme logo

	cd logo

	for i in *.eps; do sed -i 's/showFineprint true/showFineprint false/' $i;done

	for i in *.eps;do epstopdf $i -o=$i.pdf;done

	for i in *.pdf;do convert -density 300 -trim $i -quality 100 $i.png;done





