cas9ENG
======



Input
^^^^^

Copy fastq files in the working dir and prepare the manifest file:

.. code-block:: shell

	amplicon_seq: TTTCGGGTTTATTACAGGGACAGCAGAGATCCACTTTGGCGCCGGCGGATCCGGCATCGACTTCAAGGAGGANNNNNGGCTTAAGTAGGTACCGCACGTCGATATCTTCGAANNNNNNNNNNCCGGGTGCAAAGATGGATAAAGTTTTAAACAGAGAGGAATCTTTGCAGCTAATGGACCTTCTAGGTCTTGAAAGGAGTGGGAATTGGCTCCGGTGCCCGTCAGTGGGCAGAGCGCACATCGCCCACAG
	gRNA_seq: GGCATCGACTTCAAGGAGGA
	barcode_seq: NNNNNNNNNN
	PAM_seq: NNNNN
	min_read_count: 5
	input: 134_052820_input_merge.fastq.gz
	cas9sso7d_rep2: 134_Cas9Sso7d_repB_S61_R1_001.fastq.gz.merge.extendedFrags.fastq.gz
	cas9_rep1: 134_Cas9_repA_S40_R1_001.fastq.gz.merge.extendedFrags.fastq.gz
	control_rep1: 134_Control_repA_S39_R1_001.fastq.gz.merge.extendedFrags.fastq.gz
	cas9_rep2: 134_Cas9_repB_S60_R1_001.fastq.gz.merge.extendedFrags.fastq.gz
	control_rep2: 134_Control_repB_S59_R1_001.fastq.gz.merge.extendedFrags.fastq.gz
	cas9sso7d_rep1: 134_Cas9Sso7d_repA_S41_R1_001.fastq.gz.merge.extendedFrags.fastq.gz


Usage
^^^^^

.. code:: bash

	export PATH=$PATH:"/home/yli11/HemTools/bin"

	hpcf_interactive.sh

	module load conda3

	source activate /home/yli11/.conda/envs/crispresso2_env/

	cas9ENG.py -m input.yaml


Output
^^^^^^

1.raw_barcode_PAM.count.csv
----

This output is generated for each input and control file. Fist two columns are aligned sequences between the input amplicon sequence and read. Only alignment passed the default CrisprESSO cutoff (60) is used and outputed. 

``PAM_count.csv`` output is generated for cas9 and cas9sso7d files.  The following columns are different: 

- ``2`` is either "Reference_MODIFIED" or "Reference_UNMODIFIED", crisprEsso output.

- ``PAM_seq2`` is the detected PAM sequence in the reads. 

- ``PAM_seq`` is the final assigned PAM. The priority of assignment is : (1) use PAM_seq2 if possible (e.g., no deletion in PAM_seq2) (2) assign PAM according to the barcode (3) assign PAM to barcode within maximal mismatch=1.

- ``PAM`` is the second and third bp of PAM_seq, ``PAM_seq[1:3]``


2.barcode_PAM.filter.csv
----

The barcode dictionary after filtering (default min_read_count=5)


3. editing frequency
-----

- edit.freq.csv
- cutting_freq_heatmap.pdf








