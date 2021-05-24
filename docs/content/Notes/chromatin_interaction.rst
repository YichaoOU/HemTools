Chromatin Interaction data analysis
=========




TAD calling
^^^^^^^^^^^

TAD variation between replicates
--------------------------------

https://github.com/deeptools/HiCExplorer/issues/445

Please do the following:

take the cool matrix without KR applied
normalize them with mode 'smallest'
apply hicCorrectMatrix with KR correction
rerun hicFindTads
consider now what Gautier wrote.
If you cannot make sure the value ranges are equal it is quite likely to have different boundaries in replicates.


The difficulty with TAD calling is that it is really parameter dependent. I would highly recommend you to visualize your data and check for the boundaries you called and those that you compared you boundries with. You might need to tweak the parameters quite a bit to matches your data. For example you want to avoid seeing very tiny domains or unusually big ones, this can be improved by adjusting the parameters. The format shouldn't matter.

If it is a matter of QC, please use the Zscore for each sample calculated by hicFindTADs and compare them using for instance multiBigwigSummary from deeptools (https://deeptools.readthedocs.io/en/develop/content/tools/multiBigwigSummary.html) followed by plotCorrelation (https://deeptools.readthedocs.io/en/develop/content/tools/plotCorrelation.html).

Alternatively you can plot the different samples Hi-C tracks and their respective hicFindTADs Zscore on top of each other using hicPlotTADs and check the overall similarity of signals distribution. It is also a good way to check for "differential" loci that can be identified from comparing the Zscores (dots outside of the diagonal on the plotCorrelation plots).

The overlap of the exact position of TAD boundaries is rarely giving a significant measure of reproducibility of TAD calling because, more often than not, TAD boundaries position is shifted +-1 to 2 bins depending on the sample because of how hicFindTADs work. Zscores are much more robust because they depend on much less parameters and are less stochastic.

The best is to use as I said the zscore between samples, and if you want to have a consensus on the TAD boundaries position, the simplest is to merge all replicates (if applicable) and tweak the parameters until the TADs distribution is satisfying enough for given regions... (hence "by eye").

On a side note, "TADs" being often nested structures, there's no "ground truth" in their definition (until you perfectly know the underlying mechanisms of their definition), i.e., different set of parameters will give satisfying TADs distribution depending on the resolution of the matrix. Hence it can be a good idea to define different set of TADs (from large to small "TADs") and check if your hypothesis still stand independently of the TADs set used.


I agree with @LeilyR , to get your consensus TAD boundaries position, the more contacts available the better. So it's definitely the way to go:

Call TADs on unnormalized corrected control matrix to get the BED file of TAD boundaries: control_TADs.bed.

Normalize the control and the treated samples matrices, correct the matrices, and call TADs again, but this time, try to plot the newly computed Zscores norm_control_zscore.bw and norm_treatment_zscore.bw around the previously called control_TADs.bed using deeptools computeMatrix and plotHeatmap. With some clustering you should be able to spot "lost" TAD boundaries, if there are any.

For "newly formed" TAD boundaries (which are pretty rare, but it depends on your experiments), you can try to compare the norm_control_zscore.bw and norm_treatment_zscore.bw values and extract the specific spots of the genome where the value in norm_treatment_zscore.bw is way below norm_control_zscore.bw (the lower the value, the more likely a TAD boundary is present). You can then verify these spots using pyGenomeTracks by creating a bed file of all the regions you want to verify. pyGenomeTracks will create one image for each spot, and thus you can check by eye if the topology is different enough or not: https://github.com/deeptools/pyGenomeTracks .

You can apply a similar method for "lost TADs" too, by extracting the coordinates of the spots with high values in norm_treatment_zscore.bw compared to norm_control_zscore.bw ...

The difference of the two bigwigs should give a nice and informative 2D track about potential differential TAD boundaries. Ranking that bigwig from lowest to highest should give you "lost" and "newly acquired" TADs. Most of the time it's more like "mostly affected" and "not affected", but well it depends on your genome topology phenotype.

I don't know if what you propose would change something or not, but I would convert the unbalanced coolers to h5 with hicConvertFormat then hicNormalize and hicCorrectMatrix.

Normalization might have an effect only if the difference of coverage is rather important between samples... But if it's too important (Fold Change of the sum of contacts > 2 between samples), then it's better to downsample the high coverage FASTQ to the level of the least covered FASTQ and build the matrices from scratch from those downsampled FASTQs.

But as I said earlier: get your consensus boundaries from the control and compare the zscore / insulation score (same thing) between control and treatment globally to see if you really have TAD distribution modifications and validate them with pyGenomeTracks. This is the best way to avoid some spurious TAD detection between samples...

bedtools fisher on TAD boundaries extended +- 1 bin can also help you, but I'm not sure it's the best way to check TAD calling consistency.

You also have to remember that Hi-C is not only about TADs, it's also about A/B compartments, contacts distribution (hicPlotDistVsCounts) and contacts aggregation for instance. TADs are somewhat boring since they rarely change 😃



bin size for TAD calling
--------------

In theory for a deep enough data one could be able to call TADs on the restriction fragment resolution, however in reality one might need to merge few bins to compensate for the data sparsity. Sometime it is a good practice if one tries to visualize TADs of several resolutions and compare. Your second plot shows how sparse your data, so you might need to consider merging some bins, however 10kb might be a bit too much, if you are looking for high resolution TADs. You could try merging less number bins and see how your matrix look for something like 2 or 3kb resolution.

