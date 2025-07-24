#!/home/yli11/.conda/envs/jupyterlab_2024/bin/Rscript

# Load required libraries
library(crisprScore)
library(parallel)
library(tools)

# Get the input file from the command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]

if (!file.exists(input_file)) {
  stop("Input file does not exist.")
}

cat("Reading input file:", input_file, "\n")
df <- read.csv(input_file)

# Verify that required columns are present
required_cols <- c("seq1", "target", "seq", "seq2")
if (!all(required_cols %in% colnames(df))) {
  stop("One or more required columns are missing: ", 
       paste(setdiff(required_cols, colnames(df)), collapse = ", "))
}

n_rows <- nrow(df)
cat("Total rows:", n_rows, "\n")

# Define the number of cores to use
n_cores <- 2
cat("Using", n_cores, "cores for parallel processing.\n")

# Split indices into n_cores groups (roughly equal)
group_size <- ceiling(n_rows / n_cores)
index_list <- split(seq_len(n_rows), ceiling(seq_len(n_rows) / group_size))

# Define a function to process a chunk of the data frame
process_chunk <- function(idx) {
  chunk <- df[idx, ]

  safe_score <- function(func, arg) {
    tryCatch({
      func(arg)
    }, error = function(e) {
      paste0("ERROR: ", e$message)
    })
  }

  chunk$Azimuth    <- safe_score(getAzimuthScores, chunk$seq1)
  chunk$CRISPRater <- safe_score(getCRISPRaterScores, chunk$target)
  chunk$DeepHF     <- safe_score(getDeepHFScores, chunk$seq)
  chunk$RuleSet1   <- safe_score(getRuleSet1Scores, chunk$seq1)
  chunk$RuleSet3   <- safe_score(getRuleSet3Scores, chunk$seq1)
  chunk$DeepSpCas9 <- safe_score(getDeepSpCas9Scores, chunk$seq1)
  chunk$CRISPRscan <- safe_score(getCRISPRscanScores, chunk$seq2)

  return(chunk)
}

# Process the chunks in parallel using mclapply
cat("Processing chunks in parallel...\n")
results_list <- mclapply(index_list, process_chunk, mc.cores = n_cores)

# Combine all processed chunks into a single data frame
results_combined <- do.call(rbind, results_list)

# Construct output file name based on input file name
prefix <- file_path_sans_ext(basename(input_file))
output_file <- paste0(prefix, "_AllScores.csv")

# Save the combined results to a CSV file
write.csv(results_combined, output_file, row.names = FALSE)
cat("All scores have been saved to:", output_file, "\n")
