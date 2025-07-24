#!/home/yli11/.conda/envs/jupyterlab_2024/bin/Rscript

library(crisprScore)
args <- commandArgs(trailingOnly=TRUE)

file=args[1]

# df = read.csv("candidate_gRNA.bed.off_targets.info.csv")
df = read.csv(file)
head(df)
results <- getAzimuthScores(df$seq1)
write.csv(results, paste0(file,".AzimuthScores.csv"), row.names = FALSE)

results <- getCRISPRaterScores(df$target)
write.csv(results, paste0(file,".CRISPRaterScores.csv"), row.names = FALSE)

results <- getDeepHFScores(df$seq)
write.csv(results, paste0(file,".DeepHFScores_df.csv"), row.names = FALSE)

results <- getRuleSet1Scores(df$seq1)
write.csv(results, paste0(file,".RuleSet1Scores_df.csv"), row.names = FALSE)

results <- getRuleSet3Scores(df$seq1)
write.csv(results, paste0(file,".RuleSet3Scores_df.csv"), row.names = FALSE)

results <- getDeepSpCas9Scores(df$seq1)
write.csv(results, paste0(file,".DeepSpCas9Scores_df.csv"), row.names = FALSE)

results <- getCRISPRscanScores(df$seq2)
write.csv(results, paste0(file,".CRISPRscanScores_df.csv"), row.names = FALSE)




