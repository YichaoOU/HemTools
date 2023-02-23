Quantify mutations
==================


Variant calling (e.g., GATK, mutect2) contains a lot of filterings, which can't give you a raw variant count matrix. This makes sense because variant calling, even with many filterings, base quality corrections, can still have many false positives.

In some cases, for example, a time-seires amplicon sequencing data, where we do want to have the raw variant frequency, then we need to have this raw count table. And what tools can we use? The answer is ``bam-readcount``


I have tried ``bcltools mpileup``, not good for indels.

bam-readcount can give you both SNP and indel counts in one table, the insertion will looks like ``+ACGTAGTTGA``, for example ``G->GACGTAGTTGA``, will be a line for that reference ``G`` and a column for that alternative ``+ACGTAGTTGA``, followed by read count. You have to give ``-f ref.fa``

I also created some simulated data to test bcftools and bam-readcount.

::

	# this is HBB 5utr/exon sequence
	seq="TGCCCCACAGGGCAGTAACGGCAGACTTCTCCTCAGGAGTCAGATGCACCATGGTGTCTGTTTGAGGTTGCTAGTGAACACAGTTGT"
	pos=10 # 0index

	myDict={}
	# case 1 SNP, G to T
	myDict["SNP"]="TGCCCCACAGTGCAGTAACGGCAGACTTCTCCTCAGGAGTCAGATGCACCATGGTGTCTGTTTGAGGTTGCTAGTGAACACAGTTGT"

	# case 2 indel, G to ACGTAGTTGAC
	myDict["ins"]="TGCCCCACAGACGTAGTTGACGCAGTAACGGCAGACTTCTCCTCAGGAGTCAGATGCACCATGGTGTCTGTTTGAGGTTGCTAGTGAACACAGTTGT"


	# case 3 deletion, GGCAGTAACGGCA to G
	myDict["del"]="TGCCCCACAGGGACTTCTCCTCAGGAGTCAGATGCACCATGGTGTCTGTTTGAGGTTGCTAGTGAACACAGTTGT"

But I can't get bwa to align correctly for the deletion case. It either create soft clips, or when I added ``-L 100,100``, it create an insertion!

