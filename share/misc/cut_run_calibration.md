graph TB 
	fastq[fastq files] --> fastqc(fastqc/0.11.5)
	fastq --> BWA1(human bwa/0.7.16a)
	fastq --> BWA2(E.coli bwa/0.7.16a)
	BWA1 --> filter(properly paired: -f 2 -F 4 -F 8 -F 256 -F 512 -F 2048)
	BWA2 --> filter
	filter --> output1[BAM output: .st.bam]
	filter --> filter2(uniquely mapped: -q 1)
	filter2 --> output2[BAM output: .uq.st.bam]
	output2 --> MACS(macs2/2.1.2 callpeak, fragment length: 0-2000, 0-120, 150-2000)
	output1 --> MACS
	output1 --> QC_plots(deepTools/3.2.0, QC or enrichment plots)
	output2 --> QC_plots
	output1 --> calibrated_bw(bedtools/2.29.2, calibrated bigwiggle)
	output2 --> calibrated_bw


	classDef green fill:#9f6,stroke:#333,stroke-width:2px;
	class output1,output2,QC_plots,calibrated_bw,MACS green;

