Upload colorful bed files to protein paint
==============================







Assign colors to each unique name in the bed file
^^^^^^^^^^^^^^^^^^^^^^^^^


Input
-----

::

	chr10	10376029	10376040	MA0035.3.GATA1	11.9388	+
	chr4	22866505	22866523	MA0140.2.GATA1.TAL1	12.3636	+
	chr6	128962975	128962986	MA0035.3.GATA1	13.3878	-
	chr1	223888603	223888621	MA0140.2.GATA1.TAL1	10.4545	-
	chr10	72923272	72923290	MA0140.2.GATA1.TAL1	12.5455	+
	chr11	44257011	44257022	MA0035.3.GATA1	12.6531	-
	chr8	57564294	57564313	GATA1_HUMAN.H11MO.0	13.1364	-
	chr14	66544756	66544774	MA0140.2.GATA1.TAL1	11.6727	-
	chr2	14866278	14866289	MA0035.3.GATA1	11.2449	-
	chr7	105075524	105075543	GATA1_HUMAN.H11MO.0	11.5909	-

Usage
-----

::

	hpcf_interactive

	module load conda3

	source activate /home/yli11/.conda/envs/py2

	bed_to_bedjs_withName_category_color.py input.bed


Output: input.bed.bedjs.sorted.gz


json format for protein paint
---------

::


	{
	"type":"bedj",
	"name":"GATA1",
	"file":"PATH/TO/input.bed.bedjs.sorted.gz",
	"stackheight":20,
	"stackspace":1,
	"onerow":1
	}











