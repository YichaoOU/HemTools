Log in to compute node
======================


.. code:: bash

	hpcf_interactive.sh



command to submit and kill jobs
-------------

.. code:: bash

	ls split* |head -n 5 | parallel bsub -q rhel7_short -P Genomics -R 'rusage[mem=4000]' easy_prime -f {} -c config.yaml -o {}

	for i in `bjobs | grep rhel7 | cut -d" " -f 1`;do bkill $i;done


