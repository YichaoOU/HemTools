Generate base editor score tracks
=========================


::

	usage: Base_editor_score.py [-h] [-o OUTPUT] [-j JID] -f1 MAGECK_RRA -f2
	                            MAGECK_NORM_COUNT -b GRNA_BED -e EDIT_BASE
	                            [--edit_freq EDIT_FREQ] [-g GENOME]
	                            [-s CHROM_SIZE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -o OUTPUT, --output OUTPUT
	                        output file name for FDR bw (default:
	                        base_editor_score)
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        Base_editor_score_yli11_2020-09-22)
	  -f1 MAGECK_RRA, --mageck_RRA MAGECK_RRA
	                        mageck_RRA sgRNA summary file (default: None)
	  -f2 MAGECK_NORM_COUNT, --mageck_norm_count MAGECK_NORM_COUNT
	                        mageck sgRNA normalized count file (default: None)
	  -b GRNA_BED, --gRNA_bed GRNA_BED
	                        gRNA bed file, need strand info (default: None)
	  -e EDIT_BASE, --edit_base EDIT_BASE
	                        A for ABE and C for CBE (default: None)
	  --edit_freq EDIT_FREQ
	                        known editing frequency to adjust position effect
	                        (default: /home/yli11/HemTools/share/misc/editing_freq
	                        uency.list)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  -s CHROM_SIZE, --chrom_size CHROM_SIZE
	                        chrome size (default: /home/yli11/Data/Human/hg19/anno
	                        tations/hg19.chrom.sizes)




Summary
^^^^^^

Motivation: Base editor sgRNAs can generate precise single nucleotide modifications that distrupt or introduce new TF binding sites. A score track for the entire 20bp sgRNA is obviously less informative than a score for each editable bases.

This script uses MaGeCK RRA results and assign the original FDR or merged FDR to each editable base. The FDR is then adjusted for positional effects. The final base editor is -log10 transformed. 

The editing frequency for each position is calculated from our own ABE amplicon sequencing data: https://github.com/YichaoOU/ABE_NonCoding_functional_score/blob/master/per_A_base_score/editing_frequency/average_model/editing_frequecy_barplot.pdf 


.. note:: An example input is provided in "/home/yli11/HemTools/test/""

Input
^^^^^

.. note:: The ``sgRNA`` column from MAGECK output should contain the sgRNA sequence at the end of each sgRNA ID. For example ``chr19:13190675-TGCTGCCTGTGTAGAGGGCC``, this sgRNA sequence ``TGCTGCCTGTGTAGAGGGCC`` also matches to the 4th column in the gRNA bed file.

1. MAGeCK RRA sgRNA significance output

::

	sgrna	Gene	control_count	treatment_count	control_mean	treat_mean	LFC	control_var	adj_var	score	p.low	p.high	p.twosided	FDR	high_in_treatment
	chr19:13190675-TGCTGCCTGTGTAGAGGGCC	chr19:13190380-13190550	2.3734/6.9212	272.09/293.85	4.6473	282.97	5.652	10.342	11.686	81.417	1	0	0	0	True
	chr11:5306112-TACTCATGGTCTATCTCTCC	chr11:5305920-5306090	252.76/250.89	2342.7/2282.8	251.83	2312.8	3.194	1.7444	1243.7	58.439	1	0	0	0	True
	chr2:57948343-ACGAGGCCAGGAAGACACAG	chr2:57948080-57948230	386.86/415.27	2447.9/2378.2	401.07	2413	2.586	403.76	2167	43.221	1	0	0	0	True
	chr11:5173389-TATCTGAATGACAAGCTGGT	chr11:5173040-5173250	59.334/50.179	623.5/674.32	54.756	648.91	3.543	41.907	204.44	41.554	1	0	0	0	True
	chr11:5248516-AGGGCTGGGCATAAAAGTCA	chr11:5248300-5248490	192.24/174.76	1285.7/1348.1	183.5	1316.9	2.8366	152.79	853.54	38.795	1	0	0	0	True
	chr11:5264509-GCACTGTAACAAGCTGCACG	chr11:5264320-5264470	315.66/176.49	1586.4/1585.5	246.07	1585.9	2.6832	9683.4	1210	38.519	1	0	0	0	True
	chr11:5646581-TATCAGTGTGCACTCAAAGC	chr11:5646340-5646490	354.82/304.53	1641.8/1828.3	329.68	1735.1	2.3923	1264.2	1714.7	33.939	1	8.893e-253	1.7786e-252	1.5791e-249	True
	chr11:5256103-TGCGGTGGGGAGATATGTAG	chr11:5255800-5255990	325.15/389.32	1837.3/1794.9	357.23	1816.1	2.3427	2058.9	1887.2	33.582	1	1.5248e-247	3.0495e-247	2.3691e-244	True
	chr19:12952224-GCGGGGCCTATAAGAAGGCG	chr19:12952024-12952190	176.82/257.82	1332.8/1270.8	217.32	1301.8	2.5771	3280.6	1043.6	33.57	1	2.3175e-247	4.635e-247	3.2007e-244	True

2. MAGeCK normalized count
------------------

Count data is used to calculate variance. Please remove additional groups that are not used in the RRA FDR calculation. Keep sgRNA and Gene columns.


::

	sgRNA	Gene	ABE_HBF_LOW_R1.fastq.gz	ABE_HBF_LOW_R2.fastq.gz	ABE_HBF_HIGH_R1.fastq.gz	ABE_HBF_HIGH_R2.fastq.gz
	chr11:5705274-GCTGGTCCCCTTCCACACTA	chr11:5705000-5705150	288.3628041275524	273.3886306364796	193.6910583239117	180.36707688061983
	chr19:13049006-TCTAGGGGCAGAAGGAGGAG	chr19:13048760-13048950	186.30847838693717	209.3672424494559	159.5645385239844	94.2952499193514
	chr19:13700400-TGGCCAGTCTTAGCAGCGGC	chr19:13700160-13700310	144.77474116691934	162.64893215081696	632.7241238581115	602.502788728879
	chr6:135552289-ATGGGGTGGGGTGAGCTCTC	chr6:135552020-135552170	666.9131519328579	576.1924936832133	403.0618689883305	466.5421958219072
	chr11:5621934-ATAAGGGTAAGAAAAAGTCA	chr11:5621640-5621810	469.9245696893447	420.4647926877502	343.109874745215	373.89163049417243
	chr11:4629322-AGTTAGGACCCCAGCGGGAA	chr11:4629070-4629290	296.669551571556	375.4767901779498	305.29400145340367	304.2666494490699
	chr2:57987373-GGGAACTGGACAGGACCATT	chr2:57987080-57987250	481.79135175220694	354.71309671188806	228.73991649681	242.31686316484488
	chr19:13049980-CAACCTCTAGTTTGACACGT	chr19:13049660-13049830	415.3373722001784	254.3552449592563	478.69361557195316	453.93294728618
	chr19:13831016-GGGAATTGCTTGAACTTGGG	chr19:13830800-13830970	524.511767178511	468.91341077522765	408.5958992261566	411.719376101354


3. gRNA bed file

This should be a bed6 format: chr, start, end, gRNA sequence, value, strand. The value column is not used.

::

	chr19	13215423	13215443	CTATGCGCAAGCCCGTGGCC	0	+
	chr6	135501700	135501720	GACATGTGACAATACGACGG	0	+
	chr6	135495884	135495904	GCCTGTAATCACAACACTTT	0	+
	chr6	135376041	135376061	CGCATGCGCACTGCTGTGCA	0	+
	chr19	12983928	12983948	AGTGGCCAAAGGGGGTGGGT	0	+
	chr2	58274505	58274525	CGGCTTCTGGGTACCTTCCC	0	-
	chr6	135376614	135376634	TCTCACTCACTTTGTCGCCC	0	-
	chr19	13207639	13207659	GGCCCGGGCCGGAGCGTGCC	0	+


Usage
^^^^^


.. code:: bash

    hpcf_interactive -q standard -R "rusage[mem=10000]"

    module load conda3

    source activate /home/yli11/.conda/envs/py2/

	Base_editor_score.py -f1 ABE_high_vs_low_mageck_RRA_results.sgrna_summary.txt -f2 ABE_RRA_results.normalized.txt -b gRNA.all.bed -e A -g hg19

Use ``-e A`` to specify ABE or CBE

Use ``-g hg19`` to specify genome version.




Output
^^^^^^

Base editor score is provided in the jid folder, ``Editable_scores.tsv``

Example track:

https://ppr.stjude.org/?study=HemPipelines/yli11/create_tracks_yli11_2020-09-22bd628e9af53b/tracks.json









