Known motif finding given fasta sequences
============



::


	usage: find_motif_seq.py [-h] [-j JID] -f FASTA [-m MOTIF_FILE]
	                         [-p FIMO_CUTOFF]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        find_motif_seq_yli11_2020-09-27)
	  -f FASTA, --fasta FASTA
	                        input query fasta (default: None)
	  -m MOTIF_FILE, --motif_file MOTIF_FILE
	                        meme file (default:
	                        /home/yli11/Data/Motif_database/Human/human.meme)
	  -p FIMO_CUTOFF, --fimo_cutoff FIMO_CUTOFF



Summary
^^^^^^^

Identify known transcription factor binding sites on given sequences. Motif scanning is based on FIMO, default p-value is 1e-4. 

Default known motifs are from Human. For mouse, use: ``/home/yli11/Data/Motif_database/Mouse/mouse_TF.meme``


Input
^^^^^

Input fasta file.

::

	>seq1
	AAGTCGTA
	>seq2
	AAAAAAAAAAAAAAA

Usage
^^^^^


::

	hpcf_interactive.sh
	module load python/2.7.13
	find_motif_seq.py -f input.fa



Output
^^^^^^

Output is a tsv file. The first column is motif name, followed by sequence name. q-value column is empty. Last column is the matched sequence.

::

	#pattern name	sequence name	start	stop	strand	score	p-value	q-value	matched sequence
	motif1	seq1	12	26	-	15.9888	2.26e-06		GGAAGTCAGCCACCT
	motif1	seq1	19	37	+	15.1667	3.2e-06		TGACTTCCCACTGTGTCCT



