graph TB 
	input1[Undetermined fastq] --> demultiplex(Sample barcode demultiplexing based on hamming distance)
	demultiplex --> demultiplex2(Cell barcode demultiplexing based on edit distance)
	demultiplex2 --> umiextract(umi_tools extract)
	umiextract --> filterpolyT(will skip this filter by default)
	filterpolyT --> fastq[individual sample fastq, read name containing cell barcode and UMI]
	fastq --> BWA(BWA mem mapping for ATAC-seq)
	BWA --> QC(QC based on RSEQC and ATACseqQC)
	fastq --> STAR(STAR mapping for RNA-seq)
	fastq --> collision(collision analysis based on hybrid genome)
	collision --> STAR
	collision --> BWA
	STAR --> QC

	classDef green fill:#9f6,stroke:#333,stroke-width:2px;
	class fastq,input1 green;