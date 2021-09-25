Predicting in vivo TFBS using Catchitt
=======================


This group from German, called J-Team, won the shared first place in the ENCODE-DREAM competetion in the final phase. It was also the second place in the initial phase. They also provided the best documented and workable tutorial for their algorithm. I tried other teams methods, including the XGboost method (shared-first place) and the Deep Learning method (second place), they don't seem to work. 

The learning algorithm used by J-team is adoptied from the team leader's Ph.D thesis on discriminative Baysian learning. I would say probably XGboost and DL are better learning algorithms, but both algirhtms need a good work on parameter tunining. Parameter tuning and feature engineering are usually much important than the learning algorithm itself. So on ML competitions, sometimes when you stick to one algorithm, you become reluctant to switch to another algorithm because all the work you have spent.

 

Learning motif features
^^^^^^^^^^^^^^^^^

These motif features are usually fixed. so you only need to do it once.

Input.list
---------

2-col tsv specifing the input motif model (SLIM model .xml or JASPAR pfm) and the output tranformed model.

::

	d=Ctcf_H1hesc_shift20_bdeu_order-20_comp1-model-1.xml	model/Ctcf_H1hesc_shift20_bdeu_order-20_comp1-model-1
	d=ENCSR000BHK_SP1-human_1_hg19-model-2.xml	model/ENCSR000BHK_SP1-human_1_hg19-model-2
	d=intersect_all_relaxed_filtered_lslim3-model-1.xml	model/intersect_all_relaxed_filtered_lslim3-model-1
	d=intersect_all_relaxed_filtered_lslim3-model-2.xml	model/intersect_all_relaxed_filtered_lslim3-model-2
	d=intersect_all_relaxed_filtered_lslim3-model-3.xml	model/intersect_all_relaxed_filtered_lslim3-model-3
	d=intersect_all_relaxed_filtered_lslim3-model-4.xml	model/intersect_all_relaxed_filtered_lslim3-model-4
	d=intersect_all_relaxed_filtered_lslim3-model-5.xml	model/intersect_all_relaxed_filtered_lslim3-model-5
	d=intersect_all_relaxed_filtered_lslim3-model-6.xml	model/intersect_all_relaxed_filtered_lslim3-model-6
	d=intersect_all_relaxed_filtered_lslim3-model-7.xml	model/intersect_all_relaxed_filtered_lslim3-model-7
	d=intersect_all_relaxed_filtered_pwm-model-1.xml	model/intersect_all_relaxed_filtered_pwm-model-1
	m=Jaspar j=NFIX.homer.pfm	model/NFIX.homer
	m=Jaspar j=PU1.homer.pfm	model/PU1.homer


Usage
-----

::

	run_lsf.py -f input.list -p Catchitt_motif -g mm9

Usually it takes less than 3 hours to finish with 3 threads and 64G memory.



