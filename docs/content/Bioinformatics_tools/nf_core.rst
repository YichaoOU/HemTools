Using nf-core pipelines on HPC
===================================


Input
^^^^^

Please provide a metadata table described here:
https://nf-co.re/rnaseq/3.8.1/usage



Usage
^^^^^

::

	module load nextflow/21.10.5 singularity

	bsub -n 20 -q priority -P Genomics -R 'span[hosts=1] rusage[mem=6000]' -J NGS nextflow run nf-core/rnaseq --save_merged_fastq --input input.csv --outdir nf_core_rnaseq --genome GRCh38 -profile singularity --aligner star_rsem --pseudo_aligner salmon --save_unaligned


