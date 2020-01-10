Standard GATK variant calling for both human and non-human species
=========================================================

::

	usage: GATK_variant_call.py [-h] [-j JID] -f INPUT_LIST -s KNOWN_SNP
	                            [-g GENOME] [--genome_fasta GENOME_FASTA]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j JID, --jid JID     enter a job ID, which is used to make a new directory.
	                        Every output will be moved into this folder. (default:
	                        GATK_variant_call_yli11_2020-01-09)
	  -f INPUT_LIST, --input_list INPUT_LIST
	                        tsv 2 columns, bam file and output name (default:
	                        None)
	  -s KNOWN_SNP, --known_SNP KNOWN_SNP
	                        give a known snp vcf file. Known variants are used for
	                        base recalibration, without known SNPs, this pipeline
	                        will run GATK twice and use the first result as known
	                        variants. If no known SNPs are available, use NA. This
	                        is used for non-human species. (default: None)

	Genome Info:
	  -g GENOME, --genome GENOME
	                        genome version: hg19, hg38, mm9, mm10, custom. By
	                        default, specifying a genome version will
	                        automatically update index file, black list, chrom
	                        size and effectiveGenomeSize, unless a user explicitly
	                        sets those options. (default: hg19)
	  --genome_fasta GENOME_FASTA
	                        genome fasta file (default:
	                        /home/yli11/Data/Human/hg19/fasta/hg19.fa)

Summary
^^^^^^^

This germline variant calling pipeline is designed for non-human species but it also useful for human. Standard GATK pipeline includes `BWA-MEM mapping`, `bam sort and remove duplicates`, `GATK base recalibration`, `GATK haplotype caller`. Note that variant annotation is not included in this pipeline. 

Ref: https://wiki.stjude.org/pages/viewpage.action?pageId=53318458

For species without known variants, we have to perform GATK variant calling at least twice (till convergence), suggested in https://software.broadinstitute.org/gatk/documentation/article?id=11081, because base recalibration is a mandatory step in GATK pipeline and base recalibration can detect systematic sequencing errors and thus increase the accuracy of variant calling.

In practice, two step variant calling is probably enough. See: https://genome.cshlp.org/content/25/12/1921.full.html, "Given the lack of existing polymorphism data, a first round of conservative variant calling provided input to the quality score recalibration procedure. SNPs were then called using the GATK UnifiedGenotyper algorithm on all samples simultaneously." `UnifiedGenotyper` is later on replaced by `HaplotypeCaller` in GATK 3.3 or later.


Input
^^^^^

**bam.list**

A tsv file with 2 columns: path to bam file and a sample ID. Each line will produce a vcf file named as ``[sampleID].BSQR.vcf``.

::

	1659315_cell1_treat1_ATAC_S13_L001.rmdup.uq.bam	1659315_cell1_treat1
	1659316_cell1_control_ATAC_S14_L001.rmdup.uq.bam	1659316_cell1_control
	1659317_cell2_treat1_ATAC_S15_L001.rmdup.uq.bam	1659317_cell2_treat1
	1659318_cell2_control_ATAC_S16_L001.rmdup.uq.bam	1659318_cell2_control
	1659315_cell1_treat1_ATAC_S13_L002.rmdup.uq.bam	1659315_cell1_treat1_2
	1659316_cell1_control_ATAC_S14_L002.rmdup.uq.bam	1659316_cell1_control_2
	1659317_cell2_treat1_ATAC_S15_L002.rmdup.uq.bam	1659317_cell2_treat1_2
	1659318_cell2_control_ATAC_S16_L002.rmdup.uq.bam	1659318_cell2_control_2

Usage
^^^^^

For hg19, use

.. code:: bash

	hpcf_interactive

    module load python/2.7.13

    general_variant_calling.py -f bam.list

For all other species, you have to provide a SNP vcf file. If such file is not available, use `-s NA`. Not recommanded for hg39, mm9, mm10, because such vcf files are available, just not currently provided by this pipeline.

The following example is for green monkey.

.. code:: bash

    GATK_variant_call.py -f bam.list -g custom --genome_fasta chlsab2_myxoma.fa -s NA


Output
^^^^^^

Once the job is finished, you will be notified by email.

``*.BSQR.vcf`` contains the called variants, which is inside the `{{jid}}/[sample_id]` folder


Pipeline script
^^^^^^^^^^^^^^^


.. code-block:: shell


	=cut GATK 1

	inputFile=input_list

	ncore=1
	mem=16000


	module load picard/2.9.4 gatk/3.5 
	module load samtools/1.9

	genome_fasta={{genome_fasta}}
	bam=${COL1}
	output=${COL2}
	mkdir {{jid}}/$output

	cp $genome_fasta {{jid}}/$output/



	ref={{jid}}/$output/$(basename $genome_fasta)


	two_step_GATK={{no_known_SNPs}}

	known_SNP={{known_SNP}}



	    
	java -jar /hpcf/apps/picard/install/2.9.4/picard.jar CreateSequenceDictionary R= $ref  O= ${ref%.*}.dict

	samtools faidx $ref	
		

	java -jar /hpcf/apps/picard/install/2.9.4/picard.jar AddOrReplaceReadGroups I= $bam O= $output.bam RGID=test RGLB=test RGPL=illumina RGPU=Hart_Center RGSM=test

	java -jar /hpcf/apps/picard/install/2.9.4/picard.jar ReorderSam I= $output.bam O= $output.sorted.bam R= $ref CREATE_INDEX=TRUE


	if [ "$two_step_GATK" = true ] ; then

		echo -e "["$(date)"]\tStart two step GATK.."

	    java -jar /hpcf/apps/gatk/install/3.5/GenomeAnalysisTK.jar -T HaplotypeCaller -R $ref -I $output.sorted.bam -o $output.known.vcf 
		
		known_SNP=$output.known.vcf
		
		echo -e "["$(date)"]\tFiltering Variants.."
		java -jar /hpcf/apps/gatk/install/3.5/GenomeAnalysisTK.jar -T VariantFiltration -R $ref -V $known_SNP -filterName FS -filter "FS > 30.0" -filterName QD -filter "QD < 2.0" -o $output.filtered.known.vcf	
		
		known_SNP=$output.filtered.known.vcf
		
	fi



	#Perform BQSR
	echo -e "["$(date)"]\tPerforming BQSR.."
	java -jar /hpcf/apps/gatk/install/3.5/GenomeAnalysisTK.jar -T BaseRecalibrator -I $output.sorted.bam -R $ref -knownSites $known_SNP -o $output.Base.Recal.table

	#Print recalibrated reads
	echo -e "["$(date)"]\tPrinting recalibrated reads.."
	java -jar /hpcf/apps/gatk/install/3.5/GenomeAnalysisTK.jar -T PrintReads -R $ref -I $output.sorted.bam -BQSR $output.Base.Recal.table -o $output.BQSR.bam 


	#Run HaplotypeCaller
	echo -e "["$(date)"]\tRunning HaplotypeCaller.."
	java -jar /hpcf/apps/gatk/install/3.5/GenomeAnalysisTK.jar -T HaplotypeCaller -R $ref -I $output.BQSR.bam  -o $output.BQSR.vcf 

	mv $output*.vcf {{jid}}/$output/
	mv $output*.bam {{jid}}/$output/
	mv $output*.table {{jid}}/$output/








Report bug
^^^^^^^^^^

.. code:: bash

    $ HemTools report_bug

Comments
^^^^^^^^

.. disqus::
    :disqus_identifier: NGS_pipelines






























