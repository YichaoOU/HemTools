EGACryptor for EGA submission
======================

EGA submission requires users to encrypt data before uploading.


Reference
^^^^^^^

https://ega-archive.org/submission/tools/egacryptor

Input
^^^^^

Please put all of your files in one folder (your working dir).

Output
^^^^^^

By default, ``output-files`` contains all encrypted files to be uploaded.


Usage
^^^^^

Go to your working dir

.. code:: bash

	hpcf_interactive -q interactive -R "rusage[mem=40000]" # login to a compute node

	module load java/10.0.2

	java -jar /home/yli11/HemTools/share/script/jar/ega-cryptor-2.0.0.jar -i $PWD


