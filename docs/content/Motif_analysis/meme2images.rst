Generate Motif logo
^^^^^^^^^^^^^^^^^^^


.. code:: bash


	meme2images -eps Supp_File_motif_PWM.meme logo

	cd logo

	for i in *.eps; do sed -i 's/showFineprint true/showFineprint false/' $i;done

	for i in *.eps;do epstopdf $i -o=$i.pdf;done







