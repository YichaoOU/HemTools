Weird called peaks
===================


Example 1: most of the called peaks are chrY
^^^^^^^^^^^

In one user case, for GATA1, totally called 47 peaks where 46 of them are in chrY. Since chrY has many repeats, many downstream analyses will filter out these peaks (e.g., homer motif analysis), leading to empty results of many pipelines.

::


	chr8	100508135	100508136	NA_peak_1	11.54111
	chrY	58822212	58822213	NA_peak_2	5.15772
	chrY	58822659	58822660	NA_peak_3	2.56477
	chrY	58824885	58824886	NA_peak_4	5.31885
	chrY	58825522	58825523	NA_peak_5	11.31443
	chrY	58826294	58826295	NA_peak_6	5.31885
	chrY	58827264	58827265	NA_peak_7	4.21362
	chrY	58829125	58829126	NA_peak_8	6.88079
	chrY	58832739	58832740	NA_peak_9	6.52889
	chrY	58834784	58834785	NA_peak_10	9.67788


In this case, likely the very beginning input is not correct. Here, the initial input is fastq files, we can inspect the following things:

- 1. Number of reads
- 2. Number of valid reads (properly paired reads for PE data, non-chrM reads, etc.)
- 3. QC reports (like cross-correlation score for chip-seq, number of called peaks, etc.)


