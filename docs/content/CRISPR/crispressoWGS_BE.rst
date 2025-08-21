Quantify base editing efficiency/cas9 indel frequency for Hybrid-Capture assay
====================================

::

	usage: crispressoWGS_BE.py [-h] [-j JID] -r REGION_FILE -f BAM_LIST
	                           [--ref REF] [--alt ALT] [--center CENTER]
	                           [--addon_parameters ADDON_PARAMETERS]
	                           [--queue QUEUE] [-g GENOME]
	                           [--genome_fasta GENOME_FASTA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        crispressoWGS_BE_yli11_2024-11-20)
	  -r REGION_FILE, --region_file REGION_FILE
	                        gRNA_bed required (default: None)
	  -f BAM_LIST, --bam_list BAM_LIST
	                        gRNA_bed required (default: None)
	  --ref REF             reference base (default: A)
	  --alt ALT             alternative base (default: G)
	  --center CENTER       center (default: -10)
	  --addon_parameters ADDON_PARAMETERS
	                        additional paramteeres, such as
	                        --min_paired_end_reads_overlap for crispresso
	                        (default: )
	  --queue QUEUE         which queue to use (default: standard)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10. By default,
	                        specifying a genome version will automatically update
	                        index file, black list, chrom size and
	                        effectiveGenomeSize, unless a user explicitly sets
	                        those options. (default: hg19)
	  --genome_fasta GENOME_FASTA
	                        genome fasta file (default:
	                        /home/yli11/Data/Human/hg19/fasta/hg19.fa)



Summary
^^^^^^

Code is designed to analyze Hybrid-Capture assay based on ``crispressoWGS``, but should be generic.


Hybrid-Capture is a cost-effective assay comparing to ``rhAmp-seq`` if you have >500 regions. In our data, >90% region have at least 1000 UMI-deduplicated reads.

Updates for Cas9 samples, 2/24/2025
^^^^^

For cas9 samples, we still use the same pipeline, but we can ignore the ref to alt base conversion stats, and just focus on indel freqeuncy. Some key parameters need to be changed. 

First, the input region file, instead of extending +/- 2bp. Users need to add more bases to the PAM side, for example, 2bp to 5end but 10bp added to the 3end. 

Seconding, quantification window and window size, we will change to cas9 setting. See below.

::

	crispressoWGS_BE.py -r gRNA.bed -f bam.tsv -g hg38 --ref A --alt G --w_size 1 --center "-3" --addon_parameters " --exclude_bp_from_right 0 --exclude_bp_from_left 0 --plot_window_size 12" --queue priority


Input
^^^^^

Target region bed file
-----------------------------

5-col tsv, chr, start, end, name, gRNA spacer sequence

``name``, the 4-th col name should start with gRNA name, required to use my chi-square test script to do treatment-control comparison

::

	chr17	82316684	82316712	gRNAName1_OT1_any_name	GAGGTCAATGTCTACGGCTC
	chrX	10739958	10739986	gRNAName1_OT2	GAGGTCAATGCCTACGCTTG
	chr21	27717636	27717664	gRNAName2_OT3	GATGTCAATGTCTACAGCTT

gRNA spacer length can only be 18nt to 22nt. Adjust your gRNA if not in this range.

Note, ``crispressoWGS`` requires bam read to cover the entire given region, so your input region file better not too big. We recommand ``start`` and ``end`` to be 2bp flanking the spacer sequence. ``crispressoWGS`` uses ``samtools faidx hg38.fa chr1:55555559-55555561`` to extract fasta, all start and end are 1-index. 

Also ``crispressoWGS`` has a "bug" when extract fasta sequence, the ``end-1`` position is used, instead of ``end``.

So you need to make sure your start and end is also 1-index. So if your spacer is 3-22 (1-index), the start and end should be 1 and 25.

Output
^^^^^^

For each sample, it outputs a tsv file containing the gRNA name, gRNA sequence, base editing efficiency for each position (only consider the 20bp gRNA length), and 'indel_frequency','total_indel','Reads_total'. So totally 25 columns.

file name: ``$sample_id.gRNA_length.edit_eff.tsv`` contain indel infomation and edit% each position
file name: ``$sample_id.allele.edit.tsv`` contain allele edit information
file name: ``$sample_id.max_edit.tsv (pdf)`` max edit each position

If editing efficiency is -1, meaning no reads mapped to the amplicon sequence. or total reads < 50


Usage
^^^^^

Copy fastq files, target bed file  in the working dir and run the following:

::

	hpcf_interactive

	PATH=/home/yli11/HemTools/bin:/hpcf/lsf/lsf_prod/10.1/linux3.10-glibc2.17-x86_64/etc:/hpcf/lsf/lsf_prod/10.1/linux3.10-glibc2.17-x86_64/bin:/usr/lpp/mmfs/bin:/usr/lpp/mmfs/lib:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/ibutils/bin:/sbin:/cm/local/apps/environment-modules/3.2.10/bin:/opt/puppetlabs/bin
	export PATH=$PATH:"/home/yli11/HemTools/bin"


	module load python/2.7.13

	run_lsf.py --guess_input

	crispressoWGS_BE.py -r ABE.target.bed -f ABE.bam.list -g hg38 --ref A --alt G --addon_parameters " --exclude_bp_from_right 0 --exclude_bp_from_left 0 --plot_window_size 12 " --queue standard


Chi-square test
^^^^^^^^^^^^^^

1. Prepare a design tsv
-------------

sample label, group label, replicates

each design.tsv file corresponse to the same control file, if you have two groups using two different control, then create two design.tsv, because ``Control`` is a keywork in design.tsv

::

	==> D2.design.tsv <==
	GM_VK484_S1	Control	1
	GM_VK485_S2	P27_D2	1
	GM_VK486_S3	P26_D2	1
	GM_VK487_S4	Control	2
	GM_VK488_S5	P27_D2	2
	GM_VK489_S6	P26_D2	2
	GM_VK490_S7	P27_D2	3
	GM_VK491_S8	P26_D2	3

	==> D3.design.tsv <==
	GM_VK492_S9	Control	1
	GM_VK493_S10	P27_D3	1
	GM_VK494_S11	P26_D3	1
	GM_VK495_S12	Control	2
	GM_VK496_S13	P27_D3	2
	GM_VK497_S14	P26_D3	2
	GM_VK498_S15	P27_D3	3
	GM_VK499_S16	P26_D3	3


2. Run the code
-------------

In the crispresso jid folder, where you have allele_edit.tsv and eff_edit.tsv

::

	hpcf_interactive

	module load conda3/202402

	source activate /home/yli11/.conda/envs/jupyterlab_2024

	hybrid_capture_chi_square.py design.tsv


3. Outputs
-----------

The stats tables are provided for ABE and Cas9 (indel%). You should select one of them based on your assay.

Outputs are ``Your_group_label.hybrid_capture.pivot_tabe.add_chi_square_stats.ABE.csv`` and ``Your_group_label.hybrid_capture.pivot_tabe.add_chi_square_stats.Cas9.csv``

