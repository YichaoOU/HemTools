bjobs related commands
==========================



check output from a job
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	bpeek jid[array_id]


check memory usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

	bjobs -l jid[array_id]

Kill all by queue name or job name
^^^^^^^^^^^^^^^^^^^^^^^^^

when job_ID is 0, it means for all jobs, otherwise only the most recent submission will be killed

https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=reference-bkill

.. code:: bash

	bkill -J *_*

	bkill -q standard 0