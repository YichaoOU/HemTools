eCLIP-seq differential peak
======================



Summary
^^^^^^^^

This pipeline is based on the input normalization code from ENCODE. 

::

	Input normalization: Compares the number of reads within the IP sample to the number of reads within the size-matched INPUT sample across Clipper-called peak clusters





Input
^^^^^^

3 input files. User should run this pipeline inside the eCLIP-seq jobID folder.

::

	WT sample
	KO sample
	Input sample



Usage
^^^^^

::

	hpcf_interactive.sh # login to compute node

	module load conda3/202011

	source activate /home/yli11/.conda/envs/captureC

	module load perl

	eclip_diff_peak.py $wt $ko $input

	# stderr
	Input is: 2472461_Nontarget_cd34_10_IP_S5_R1 2472462_M1_3_cd34_10_IP_S6_R1 2472458_Nontarget_cd34_10_Input_S2_R1
	reading peak file 2472461_Nontarget_cd34_10_IP_S5_R1_results/2472461_Nontarget_cd34_10_IP_S5_R1.bed
	now doing expt 2472461_Nontarget_cd34_10_IP_S5_R1.pri.bam
	now doing input 2472458_Nontarget_cd34_10_Input_S2_R1.pri.bam
	CLOSE
		(in cleanup) Internal error: could not get STATE from IPC::Run
	(1702, 6)
	reading peak file 2472461_Nontarget_cd34_10_IP_S5_R1.enriched_peak.bed
	now doing expt 2472461_Nontarget_cd34_10_IP_S5_R1.pri.bam
	now doing input 2472462_M1_3_cd34_10_IP_S6_R1.pri.bam
	CLOSE
		(in cleanup) Internal error: could not get STATE from IPC::Run
	(424, 6)


Output
^^^^^^^

Please see the ``*enriched_peak.final.bed`` file. The 4th and 5th columns are -log10 pvalue and logFC.



