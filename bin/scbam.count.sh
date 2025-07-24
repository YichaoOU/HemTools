module load subread/2.0.5
featureCounts -p --countReadPairs -t gene -g gene_name -a /home/yli11/dirs/pipelines/hg38/cellranger_arc/GRCh38-2020-A-reference-sources/gencode.v32.primary_assembly.annotation.rmHBGnoise.gtf -o merged_counts.rmHBGnoise.tsv *markdup.uq.bam

