Average signal and heatmap over a bed file
==========================================



::

	usage: signal_plot.py [-h] [-j JID] [--pipeline_type PIPELINE_TYPE]
	                      [--figure_type FIGURE_TYPE] [--bed BED]
	                      [--computeMatrix_addon_parameters COMPUTEMATRIX_ADDON_PARAMETERS]
	                      [--plotHeatmap_addon_parameters PLOTHEATMAP_ADDON_PARAMETERS]
	                      [-u U] [-d D] [--commands_list COMMANDS_LIST]
	                      [--max_value MAX_VALUE] [--min_value MIN_VALUE]
	                      [--region_plot] [--one_plot_per_bw]
	                      (--bw BW | --one_to_one ONE_TO_ONE)

	plot bigwiggle signals and heatmaps given a list of bed files

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        signal_plot_yli11_2019-07-12)
	  --pipeline_type PIPELINE_TYPE
	                        Not for end-user. (default: signal_plot)
	  --figure_type FIGURE_TYPE
	                        pdf or png (default: png)
	  --bed BED             a list of bed files, any number of columns, the first
	                        three columns have to be chr, start, end (default:
	                        None)
	  --computeMatrix_addon_parameters COMPUTEMATRIX_ADDON_PARAMETERS
	                        add user-defined parameters to computeMatrix (default:
	                        )
	  --plotHeatmap_addon_parameters PLOTHEATMAP_ADDON_PARAMETERS
	                        add user-defined parameters to plotHeatmap (default: )
	  -u U                  upstream flanking length (default: 5000)
	  -d D                  downstream flanking length (default: 5000)
	  --region_plot         By default, only the centers in bed files with
	                        extended regions are used. This option enables
	                        plotting signals on the given regions plus extended
	                        flanking regions (default: False)
	  --one_plot_per_bw     Use this option when you want to edit the generated
	                        pdf by yourself. (default: False)
	  --bw BW               a list of bigwiggle files (default: None)
	  --one_to_one ONE_TO_ONE
	                        5 columns tsv, path_to_bed, bed_label, path_to_bw,
	                        bw_file_label, output_name. Most common usage.
	                        (default: None)


.. note:: ``--bw`` and ``--bed`` options are not implemented.

Summary
^^^^^^^

Given a bed file and a bigwiggle file, plot the average signals (line plot) and heatmap.


Example
^^^^^^^

.. image:: ../../images/signal_plot.png
	:align: center


Input
^^^^^

A tsv file containing 5 columns: 

::

	path_to_bed	bed_file_label	path_to_bw	bw_file_label	output_name

You can input multiple lines, each line will produce two figures: one is the center (of your input regions) with extended flanking regions; the other is the actual region plus extended regions. Unless you are looking at gene structure

Usage
^^^^^

Go to your data directory and type the following.

**Step 0: Load python version 2.7.13.**

.. code:: bash

    module load python/2.7.13

**Step 1: Prepare input parameters**

.. code:: bash

    signal_plot.py --one_to_one input.list

You can remove legend by adding ``--plotHeatmap_addon_parameters "--legendLocation none"``. 

.. code:: bash

    signal_plot.py --one_to_one input.list --plotHeatmap_addon_parameters "--legendLocation none"

Output
^^^^^^

Once the job is finished, you will receive a notification email with figures attached.

FAQ
^^^


**1.	In couple of runs there are files losing of the final picture figures.**

We need to look at the log files. You can do HemTools report_bug, inside the [job ID] (e.g., signal_plot_yli11_2019-07-12) folder.

.. code:: bash

	module load python/2.7.13

	cd [path_to_job_ID]

	HemTools report_bug

**2.	Is that possible to adjust the distance from center from 5Kb to 1 or 2 Kb?**

There are two parameters for that, see below

::

	-u U                  upstream flanking length (default: 5000)
	-d D                  downstream flanking length (default: 5000)


**3.	For the blue color bar right to the main plot, is it possible to make all the plots in the same range? For example, From 1-8?**

For heatmap scale, use ``--zMin 1 --zMax 8``.

.. code:: bash

	signal_plot.py --one_to_one input.list --plotHeatmap_addon_parameters " --zMin 1 --zMax 8"

For y-axis range (line plot), use ``--yMin 1 --yMax 8``.

.. code:: bash

	signal_plot.py --one_to_one input.list --plotHeatmap_addon_parameters " --yMin 1 --yMax 8"


Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines








