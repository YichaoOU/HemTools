Convert BCL basecall files to FASTQ files
=========================================

The output from Illumina sequencing looks like the flowwing

.. code:: bash
	AnalysisError.txt                       Basecalling_Netcopy_complete.txt  ImageAnalysis_Netcopy_complete_Read1.txt  Logs                   RunCompletionStatus.xml
	AnalysisLog.txt                         CompletedJobInfo.xml              ImageAnalysis_Netcopy_complete_Read2.txt  Queued                 RunInfo.xml
	Basecalling_Netcopy_complete_Read1.txt  Config                            ImageAnalysis_Netcopy_complete_Read3.txt  QueuedForAnalysis.txt  RunParameters.xml
	Basecalling_Netcopy_complete_Read2.txt  Data                              ImageAnalysis_Netcopy_complete_Read4.txt  Recipe                 ``SampleSheet.csv``
	Basecalling_Netcopy_complete_Read3.txt  fastq_files                       ImageAnalysis_Netcopy_complete.txt        RTAComplete.txt        Thumbnail_Images
	Basecalling_Netcopy_complete_Read4.txt  GenerateFASTQRunStatistics.xml    InterOp                                   RunCheckDetail.txt

.. tip:: If you need to do demultiplexing, then you will need to provide ``SampleSheet.csv``.


**Step 1**

.. code:: python

	bsub -R 'rusage[mem=32000]' -Is -q interactive -P Genomics /bin/bash

**Step 2**

.. code:: bash

	module load bcl2fastq


**Step 3**

.. code:: bash

	bcl2fastq --no-lane-splittin

.. note:: Please note that there should be no spaces when naming sample_ID (e.g., highlighted examples below). A unique sample_ID is also preferred. 

.. image:: ../../images/no_space_bcl2fastq.png