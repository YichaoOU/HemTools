#!/usr/bin/env Rscript

#Use Poisson/Negative Binominal regression remove systematic biases in Hi-C cis contact maps
#Adapt from MingHu

library("optparse")
options(scipen = 999)

option_list = list(
  make_option(c("-i", "--input"), type = "character", default = NA,
              help = "raw HiC matrix"),
  make_option(c("-o", "--output"), type = "character", default = NA,
              help = "normalized HiC matrix"),
  make_option(c("-f", "--genomic_feature"), type = "character", default = NA,
              help = "genomic feature file"),
  make_option(c("-c", "--cov"), type = "integer", default = 2,
              help = "minimum coverage [default %default]"),
  make_option(c("-l", "--len"), type = "double", default = 0.1,
              help = "minimum effective fragment length fraction of the bin [default %default]"),
  make_option(c("-s", "--gc"), type = "double", default = 0.3,
              help = "minimum gc content [default %default]"),
  make_option(c("-m", "--map"), type = "double", default = 0.8,
              help = "minimum mappability [default %default]"),
  make_option(c("-n", "--negative_binomial"), action = "store_true", default = TRUE,
              help = "use negative binomial regression")
)

opt_parser <- OptionParser(option_list=option_list)
opt <- parse_args(opt_parser)

if ( is.na(opt$input) | is.na(opt$output) | is.na(opt$genomic_feature) ) {
  stop("Missing required parameters. See usage (--help)")
}

map_in <- opt$input
genomic_features_in <- opt$genomic_feature
out <- opt$output
min_cov <- opt$cov
min_len <- opt$len
min_gc <- opt$gc
min_map <- opt$map

if ( !file.exists(genomic_features_in) ) {
  stop("Cannot open genomic feauture file.")
}
if ( !file.exists(map_in) ) {
  stop("Cannot open raw HiC matices.")
}

genomic_features <- read.table(genomic_features_in,head=F, sep="\t", colClasses=c("factor",rep("numeric",5)))
colnames(genomic_features) <- c('chr', 'bin1', 'bin2', 'len', 'gc', 'map')
genomic_features <- genomic_features[genomic_features$len>0 & genomic_features$gc>0 & genomic_features$map>0, ]

map <- read.table(map_in, head=F)
colnames(map) <- c('chr', 'bin1', 'bin2', 'raw')

chr_n <- table(map$chr)
chr_id <- names(chr_n)

final <- NULL

for (chr in chr_id) {
	tryCatch(
		{
			message(paste("normalizing",chr,sep=" "))

			genomic_features_chr <- genomic_features[which(genomic_features$chr==chr),]
			map_chr <- map[which(map$chr==chr),]
			#select bins with confident genomic features to build model
			conf_bins <- which(genomic_features_chr$len/(genomic_features_chr$bin2-genomic_features_chr$bin1)>=min_len & genomic_features_chr$gc>=min_gc & genomic_features_chr$map>=min_map) 
			
			ind1 <- match(map_chr$bin1,genomic_features_chr$bin1)
			ind2 <- match(map_chr$bin2,genomic_features_chr$bin1)

			map_chr$len <- log(genomic_features_chr$len[ind1] * genomic_features_chr$len[ind2])
			map_chr$gc <- log(genomic_features_chr$gc[ind1] * genomic_features_chr$gc[ind2])
			map_chr$map <- log(genomic_features_chr$map[ind1] * genomic_features_chr$map[ind2])

			res <- map_chr
    
			map_fit <- map_chr[!is.na(map_chr$len) & map_chr$raw >= min_cov & ind1 %in% conf_bins & ind2 %in% conf_bins,]
			map_chr$len <- (map_chr$len - mean(map_fit$len)) / sd(map_fit$len)
			map_chr$gc <- (map_chr$gc - mean(map_fit$gc)) / sd(map_fit$gc)
    
			map_fit$len <- (map_fit$len - mean(map_fit$len)) / sd(map_fit$len)
			map_fit$gc <- (map_fit$gc - mean(map_fit$gc)) / sd(map_fit$gc)
			
			if ( opt$negative_binomial ) {
			  library("MASS")
			  fit <- glm.nb(raw~len+gc+offset(map), data = map_fit)
			}
			else{
			  fit <- glm(raw~len+gc+offset(map), data = map_fit, family = "poisson")
			}
			coeff <- round(fit$coeff,4)
			res$nor <- round(map_chr$raw / exp(coeff[1] + coeff[2] * map_chr$len + coeff[3] * map_chr$gc + map_chr$map), 4)
			
			final <- rbind(final,res)
		},
		error = function(e) {
			message(e)
			message(paste("\nskip", chr, sep=" "))
		},
		warning = function(w){
			message(w)
			message(paste("\nskip", chr, sep=" "))
		}
  )
}

write.table(final[,c(1,2,3,8)], file=out, row.names=F, col.names=F, sep="\t", quote=F, na = "NaN")
