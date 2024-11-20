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

We also require ``start`` and ``end`` to be 2bp flanking the spacer sequence. ``crispressoWGS`` uses ``samtools faidx hg38.fa chr1:55555559-55555561`` to extract fasta, all start and end are 1-index. 

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

sample label, gRNA, replicates

If you have 3 replicates for gRNA, you better have 3 replicates of control, otherwise you have to modify my code.

::

	VK2447	B2M	1
	VK2448	CBLB	1
	VK2449	CD7	1
	VK2450	CIITA	1
	VK2451	PDCD1	1
	VK2452	Control	1
	VK2455	B2M	2
	VK2456	CBLB	2
	VK2457	CD7	2

Save as ``design_label``.info.tsv

2. Run the code
-------------

In the crispresso jid folder, where you have allele_edit.tsv and eff_edit.tsv

``hybrid_capture_chi_square.py design_label``

