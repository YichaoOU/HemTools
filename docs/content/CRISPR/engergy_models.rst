CRISPR-cas9 energy models for gRNA efficiency prediction
===========






uCRISPR
^^^^^

This tool can predict on-target activity given 23bp gRNA.


https://github.com/Vfold-RNA/uCRISPR


Input
-----

AGTCGT(23bp with PAM)

Usage
-----

::

	module load gcc/5.4.0

	export DATAPATH=/home/yli11/HemTools/share/script/RNAstructure/data_tables

	uCRISPR -on input.list > output




DNA_melting_bubbles_TIDD
^^^^^

This tool can predict destabilization score for each bp from the input sequence. The higher the score, the higher instability.


https://github.com/JanZrimec/DNA_melting_bubbles_TIDD

Input
-----

any sequences > 10bp

Usage
-----

::

	module load conda3

	source activate /home/yli11/.conda/envs/py2

	module load matlab

	module load java

	DNA_melting -s "AGTAGTAGTAGTAGATAGTA"




