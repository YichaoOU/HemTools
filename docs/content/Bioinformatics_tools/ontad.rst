OnTAD
=====





Installation
^^^^^^^^^^^^

.. code:: bash

	/home/yli11/Programs/test/OnTAD/src


	module load gcc/6.3.0

	module load gsl/1.9

	g++ -I /nfs_exports/apps/64-bit/gnu-apps/gsl-1.9/include/ -c main.cpp step1.cpp step2.cpp step3.cpp step4.cpp common.cpp

	g++ main.o step1.o step2.o step3.o step4.o common.o -lm -o OnTAD

	rm main.o step1.o step2.o step3.o step4.o common.o


Usage
^^^^^

.. code:: bash

	module load gcc/6.3.0

	OnTAD

	OnTAD chr18_KR.matrix -penalty 0.1 -maxsz 200 -o OnTAD_KRnorm_pen0.1_max200_chr18.tad


	for i in *.matrix;do OnTAD $i -o $i.ontad;done
