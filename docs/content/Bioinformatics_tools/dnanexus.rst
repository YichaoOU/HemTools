DNAnexus download and upload
============================

Summary
^^^^^^^

This post provides a method to download files from Stjude Could that is much faster than ``wget``.


Login account setup
^^^^^^^^^^^^^^^^^^^

.. note:: You just need to do this once.

**CREATE YOUR API TOKEN**

Following these 3 steps to get an API TOKEN. Maybe email this token to yourself, because you will once see it once. If you lost it, you will need to create it again (though it is quite easy to generate a new one).

.. image:: ../../images/DNAnexusAPI1.PNG
	:align: center

.. image:: ../../images/DNAnexusAPI2.PNG
	:align: center

.. image:: ../../images/DNAnexusAPI3.PNG
	:align: center

.. code:: bash

	module load dx-toolkit

	dx login --token [YOUR TOKEN]

Download a folder
^^^^^^^^^^^^^^^^^^^

You can find ``projectID`` by going to the folder and click ``Settings``. See the example below:

.. image:: ../../images/dx_download.png
	:align: center

The general usage is shown below.

.. code:: bash

	module load dx-toolkit

	dx cd projectID

	dx ls

	# replace projectID 

	dx download -r -f folder_name

	## or 

	dx download -f *.gz

	# -f option used to overwrite files with the same file name.

	# I sometimes see files with the same file name in Stjude cloud

	# and it can raise error when download the files.

For example, all your data is store in some folder inside ``chengLab`` dir, say ``RNA_seq_example00``. Then, by ``dx cd chengLab-projectID``, you are virtually inside ``chengLab`` dir, just like Linux command ``cd``. Next, do ``dx download -r RNA_seq_example00``, it will download the whole folder to your current dir in HPC. Now, suppose I want to download ``RNA_seq_example00`` inside my ``sequencing`` folder, you should first go to that dir and then do dx download.

.. note:: ProjectID is for each project, it is the root of your directory tree. If your target folder is in the third-level or more, you need to do more than one ``cd`` command.

The following example will assume that the directory structure is::

.. image:: ../../images/stj_cloud_example_tree.png

Example 1 - download seq_data1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Option 1: This option will create ``seq_data1`` folder inside your current dir.

.. code:: bash

	module load dx-toolkit

	dx cd projectID

	dx download -r -f seq_data1

Option 2: This option will download every file inside your current dir.

.. code:: bash

	module load dx-toolkit

	dx cd projectID

	dx download -f *.gz

Example 2 - download seq_data2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Option 1: This option will create ``seq_data2`` folder inside your current dir.

.. code:: bash

	module load dx-toolkit

	dx cd projectID

	dx cd Banana

	dx download -r -f seq_data1

Option 2: This option will download every file inside your current dir.

.. code:: bash

	module load dx-toolkit

	dx cd projectID

	dx cd Banana

	dx download -f *.gz

Upload a dir
^^^^^^^^^^^^

.. image:: ../../images/stj_cloud_tree.png

In this example, my root dir is ``Share_with_PSU``. My sub-dir is ``test``. In the ``test`` dir, I have ``test1`` folder. In the HPC, I have created a folder called ``test2`` and I want to upload this folder to ``test``. 

So the first step to do is to go to the root dir:


.. code:: bash

	module load dx-toolkit

	dx cd projectID


Then go to the ``test`` dir:

.. code:: bash

	dx cd test

Finally, upload your ``test2`` folder

.. code:: bash

	dx upload -r test2

Note that ``dx upload -r test2/`` will upload all files in ``test2``. If you want to upload the dir, you should not include the back slash char.	