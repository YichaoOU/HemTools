HemTools Tutorial 4-18-2019
===========================

.. contents::
    :local:

**Step 0: set up RSA authentication with HPC**

:doc:`How to ssh without password <../Linux_Art/ssh_without_password>`


Create a test run folder
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    cd ~

    mkdir my_test_run

    cd my_test_run

ATAC-seq example
^^^^^^^^^^^^^^^^

**Copy data**

.. code:: bash

    mkdir atac_seq

    cd atac_seq

    ln -s /research/dept/hem/common/sequencing/chenggrp/pipelines/example_data/atac_seq/*.gz .

**Run HemTools**

.. code:: bash

    module load python/2.7.13

    HemTools atac_seq --guess_input

    HemTools atac_seq -f fastq.tsv --short

.. note:: When using real data, do not use ``--short`` option, since it will submit all jobs to the short queue.

ATAC-seq example
^^^^^^^^^^^^^^^^

**Copy data**

.. code:: bash

    mkdir atac_seq

    cd atac_seq

    ln -s /research/dept/hem/common/sequencing/chenggrp/pipelines/example_data/atac_seq/*.gz .

**Run HemTools**

.. code:: bash

    module load python/2.7.13

    HemTools atac_seq --guess_input

    HemTools atac_seq -f fastq.tsv --short

.. note:: When using real data, do not use ``--short`` option, since it will submit all jobs to the short queue.

ATAC-seq example
^^^^^^^^^^^^^^^^

**Copy data**

.. code:: bash

    mkdir atac_seq

    cd atac_seq

    ln -s /research/dept/hem/common/sequencing/chenggrp/pipelines/example_data/atac_seq/*.gz .

**Run HemTools**

.. code:: bash

    module load python/2.7.13

    HemTools atac_seq --guess_input

    HemTools atac_seq -f fastq.tsv --short

.. note:: When using real data, do not use ``--short`` option, since it will submit all jobs to the short queue.

ATAC-seq example
^^^^^^^^^^^^^^^^

**Copy data**

.. code:: bash

    mkdir atac_seq

    cd atac_seq

    ln -s /research/dept/hem/common/sequencing/chenggrp/pipelines/example_data/atac_seq/*.gz .

**Run HemTools**

.. code:: bash

    module load python/2.7.13

    HemTools atac_seq --guess_input

    HemTools atac_seq -f fastq.tsv --short

.. note:: When using real data, do not use ``--short`` option, since it will submit all jobs to the short queue.

ATAC-seq example
^^^^^^^^^^^^^^^^

**Copy data**

.. code:: bash

    mkdir atac_seq

    cd atac_seq

    ln -s /research/dept/hem/common/sequencing/chenggrp/pipelines/example_data/atac_seq/*.gz .

**Run HemTools**

.. code:: bash

    module load python/2.7.13

    HemTools atac_seq --guess_input

    HemTools atac_seq -f fastq.tsv --short

.. note:: When using real data, do not use ``--short`` option, since it will submit all jobs to the short queue.




Report bug
^^^^^^^^^^

Once the job is finished, you will be notified by email with some attachments.  If no attachment can be found, it might be caused by an error. In such case, please go to the result directory (where the log_files folder is located) and type: 

.. code:: bash

    $ HemTools report_bug


Use different genome index
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    $ HemTools atac_seq -f fastq.tsv -i YOUR_GENOME_INDEX


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines




