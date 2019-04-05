#converts a Homer .motif PWM/PFM into MEME format
motif2meme <- function(inFile) {
    library(tools)
    #establishing the number of distinct motifs in the file and parsing it accordingly
    stopifnot(is.character(inFile))
    outFile <- paste(inFile,"meme",sep=".")
    thisFile <- file(outFile)
    fileName <- file_path_sans_ext(inFile)
    #reading the input file
    motif.file <- scan(file=inFile,character(0), sep="\n",quote=NULL)
    motif.index <- grep(pattern="^>",motif.file)
    n.motifs <- length(motif.index)
    total.len <-  length(motif.file)
    #print(n.motifs)
    sink(thisFile,append=TRUE)
    cat("MEME version 4\n\n",file=thisFile,append=TRUE)
    cat("ALPHABET= ACGT\n\n",file=thisFile,append=TRUE)
    cat("strands: + -\n\n")
    nameSplit <- strsplit(fileName,"_")
    nameNum <- nameSplit[[1]][1]
    motifNum <- sub("^.....(..).*", "\\1", nameNum)  # fifth
    for (i in 1:(n.motifs-1)) {
        #print(i)
        #print(" ")
        (motif.index[i]+1) -> index.start
        ((motif.index[i+1])-1) -> index.end
        motif.file[index.start:index.end] -> this_motif
                   strsplit(this_motif,split="\t") -> motif_split
                   #print(head(motif_split))
                   length(this_motif) -> motif_row
                   array(NA,c(motif_row,4)) -> motif_array
                   for (n in 1:motif_row) {
                       as.numeric(motif_split[[n]]) -> motif_array[n,]
                   }
                   motif_array <- as.data.frame(motif_array)
                   motif.file[motif.index[i]] -> header.string
                   strsplit(header.string,split="[\t]") -> prob.string
                   prob.string[[1]][6] -> prob.string2
                   strsplit(prob.string2,"[:]") -> prob.string3
                   prob.string3[[1]][4] -> this.p.val
                   prob.string[[1]][2] -> name.string
                   strsplit(name.string,split=",") -> name.string2
                   name.string2[[1]][1] -> name.string3
                   motif_name <- paste("motif",motifNum,i,sep="_")
                   cat("MOTIF",motif_name,name.string3,"\n",file=thisFile, append=TRUE)
                   cat("letter-probability matrix: ",file=thisFile, append=TRUE)
                   cat("alength= 4 w=", motif_row, file=thisFile, append=TRUE)
                   cat(" nsites= 20 ",file=thisFile, append=TRUE)
                   cat("E= 0\n",file=thisFile, append=TRUE)
                   #cat(this.p.val,"\n",file=thisFile, append=TRUE)
                   write.table(motif_array,file=thisFile,append=TRUE,col.names=FALSE,row.names=FALSE,sep="\t")
                   cat("\n",file=thisFile, append=TRUE)
    }
        (motif.index[n.motifs]+1) -> index.start
        total.len -> index.end
        motif.file[index.start:index.end] -> this_motif
                   strsplit(this_motif,split="\t") -> motif_split
                   #print(head(motif_split))
                   length(this_motif) -> motif_row
                   array(NA,c(motif_row,4)) -> motif_array
                   for (n in 1:motif_row) {
                       as.numeric(motif_split[[n]]) -> motif_array[n,]
                   }
                   motif_array <- as.data.frame(motif_array)
                   motif.file[motif.index[i]] -> header.string
                   strsplit(header.string,split="[\t]") -> prob.string
                   prob.string[[1]][6] -> prob.string2
                   strsplit(prob.string2,"[:]") -> prob.string3
                   prob.string3[[1]][4] -> this.p.val
                   prob.string[[1]][2] -> name.string
                   strsplit(name.string,split=",") -> name.string2
                   name.string2[[1]][1] -> name.string3
                   motif_name <- paste("motif",motifNum,i,sep="_")
                   cat("MOTIF",motif_name,name.string3,"\n",file=thisFile, append=TRUE)
                   cat("letter-probability matrix: ",file=thisFile, append=TRUE)
                   cat("alength= 4 w=", motif_row, file=thisFile, append=TRUE)
                   cat(" nsites= 20 ",file=thisFile, append=TRUE)
                   cat("E= ",file=thisFile, append=TRUE)
                   cat(this.p.val,"\n",file=thisFile, append=TRUE)
                   write.table(motif_array,file=thisFile,append=TRUE,col.names=FALSE,row.names=FALSE,sep="\t")
                   cat("\n",file=thisFile, append=TRUE)
   sink()
   close(thisFile) 
   print("matrix has been converted to MEME")
}
                       
args <- commandArgs(trailingOnly=TRUE)
motif2meme(args[1])
