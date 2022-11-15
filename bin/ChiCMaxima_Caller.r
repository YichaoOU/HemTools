#!/bin/env Rscript

options(warn=-1)
options(scipen=999)

#-----------Functions-----------------------------


#Function to retrieve arguments and options from the R script 

RetrieveAndDestroy=function(opt,root,stem,regexp,SearchNames,Out,isValue,NbFound,StockNames) {
  Bool=lapply(paste(root,SearchNames,stem,sep=""),grepl,opt)
  names(Bool)=StockNames
  Pos=lapply(Bool,which)
  names(Pos)=StockNames
  disable=c()
  for(i in StockNames) {
    nbmatch=length(Pos[[i]])
    if(nbmatch>0) {
      NbFound[[i]]=NbFound[[i]]+nbmatch
      disable=c(disable,-1*Pos[[i]])
      if(is.null(Out[[i]])) {
	if(isValue[[i]]!=0) {
	  if(regexp=="next") {
	    Out[[i]]=opt[Pos[[i]]+1]
	    disable=c(disable,-1*(Pos[[i]]+1))
	  }
	  else {
	    Out[[i]]=sub(regexp,"\\1",opt[Pos[[i]]])
	  }
	}
	else {
	  Out[[i]]=TRUE
	}
      }
      else {
	if(isValue[[i]]!=0) {
	  if(regexp=="next") {
	    Out[[i]]=c(Out[[i]],opt[Pos[[i]]+1])
	    disable=c(disable,-1*(Pos[[i]]+1))
	  }
	  else {
	    Out[[i]]=c(Out[[i]],sub(regexp,"\\1",opt[Pos[[i]]]))
	  }
	}
	else {
	  Out[[i]]=c(Out[[i]],TRUE)
	}
      }
    }
  }
  if(length(disable)>0) {
    opt=opt[disable]
  }
  Out[["ARGUMENT"]]=list()
  Out[["ARGUMENT"]][["opt"]]=opt
  Out[["ARGUMENT"]][["NbFound"]]=NbFound
  return(Out)
}

getopt=function (spec=NULL,opt=commandArgs()) {
  FindArgs=which(opt=="--args")
  if(length(FindArgs)!=1) {
    stop(length(FindArgs)," --args found where 1 expected.",call.=F)
  }
  ExecName=sub("--file=","",opt[FindArgs-1])
  
  if(FindArgs<length(opt)) {
    opt=opt[(FindArgs+1):length(opt)]
  }
  else {
    opt=""
  }
  
  min.columns=5
  colNames=c("LongName","ShortName","Flag","Mod","Default")
  max.columns=6
  DimSpec=dim(spec)
  if(DimSpec[2]>min.columns) {
    colNames=c(colNames,"Description")
  }
  
  if(is.null(spec) | !is.matrix(spec) | (DimSpec[2]<min.columns | DimSpec[2]>max.columns)) {
    stop('argument "spec" is required and must be a matrix with 4|5 columns.',call.=F)
  }
  colnames(spec)=colNames
  
  spec=as.data.frame(spec,stringsAsFactors=F)
  #spec validation
  if(length(unique(c(spec$ShortName,"ARGUMENT","args")))!=DimSpec[1]+2 | length(unique(spec$LongName))!=DimSpec[1]) {
    stop('Long|Short names for flags must be unique (Long name : "ARGUMENT" and "args" forbidden).',
	"\n","List of duplicated :",
	"\n","Short: ",paste(spec$ShortName[duplicated(c(spec$ShortName,"ARGUMENT","args"))],collapse=" "),
	"\n","Long:  ",paste(spec$ShortName[duplicated(spec$LongName)],collapse=" "),call.=F)
  }
  if(length(which(nchar(spec$ShortName)>1))!=0) {
    stop('Short names flags can\'t be longer than 1 character.')
  }
  
  #initialize 
  Out=list()
  Short2Long=list()
  NbFound=list()
  isValue=list()
  for(i in 1:DimSpec[1]) {
    Short2Long[[spec$ShortName[i]]]=spec$LongName[i]
    NbFound[[spec$LongName[i]]]=0
    isValue[[spec$LongName[i]]]=spec$Flag[i]
  }
  
  #Map, retrieve and suppress ARGUMENTs and arguments
  #Value ARGUMENT --example=value
  Out=RetrieveAndDestroy(opt,"^--","=.+$",".+=(.+)$",spec$LongName,Out,isValue,NbFound,spec$LongName)
  opt=Out[["ARGUMENT"]][["opt"]]
  NbFound=Out[["ARGUMENT"]][["NbFound"]]
  Out[["ARGUMENT"]]=NULL
  #boolean ARGUMENT --example
  Out=RetrieveAndDestroy(opt,"^--","$","$",spec$LongName,Out,isValue,NbFound,spec$LongName)
  opt=Out[["ARGUMENT"]][["opt"]]
  NbFound=Out[["ARGUMENT"]][["NbFound"]]
  Out[["ARGUMENT"]]=NULL
  #short name ARGUMENT -t value OR boolean -t
  Out=RetrieveAndDestroy(opt,"^-","$","next",spec$ShortName,Out,isValue,NbFound,spec$LongName)
  opt=Out[["ARGUMENT"]][["opt"]]
  NbFound=Out[["ARGUMENT"]][["NbFound"]]
  Out[["ARGUMENT"]]=NULL
  #Warn about non mapped ARGUMENTs
  if(length(opt)>0) {
    PosUnkArg=which(grepl("^-",opt))
    if(length(PosUnkArg)) {
      message("Error, argument unrecognized :","\n",paste(opt[PosUnkArg],collapse="\n"),"\n\n")
    }
    if(length(PosUnkArg)>0) {
      opt=opt[PosUnkArg*-1]
    }
  }
  #Arguments
  Out[["ARGUMENT"]]=opt
  
  #Validation of ARGUMENTs
  for(i in 1:DimSpec[1]) {
    if(spec$Flag[i]=="0") {#verify boolean arguments
      NbValue=length(Out[[spec$LongName[i]]])
      if(NbValue>1) {
	message("Warning : ",spec$LongName[i]," found ",NbValue," times")
      }
    }
    if(length(Out[[spec$LongName[i]]])==0) {
      Out[[spec$LongName[i]]]=spec$Default[i]
    }
    library("methods")
    Out[[spec$LongName[i]]]=as(Out[[spec$LongName[i]]],spec$Mod[i])
  }
  
  return(Out)
}



#Geometric_mean function to identify background level for each bait

Geometric_mean=function(table=table,cis_window=1500000) {
	# start=seq(0,cis_window-20000,by=20000)
	# end=seq(20000,cis_window,by=20000)
	start=seq(0,cis_window-50000,by=50000)
	end=seq(50000,cis_window,by=50000)
	# start=seq(0,cis_window-10000,by=10000)
	# end=seq(10000,cis_window,by=10000)
	distance=GRanges(seqnames=Rle(table$chr_Bait[1]),ranges=IRanges(start,end),strand=rep("*",length(start)))
	distance_d=as.data.frame(distance)
	distance_d$RefBinMean=1

	#Remove closest distance bins with no supporting reads, which otherwise causes bugs in table allocation
	for (i in 1:length(start(distance))) {
		firstbins=table[abs(table$end_OE-table$start_Bait[1]) <= end(distance)[i] & abs(table$end_OE-table$start_Bait[1]) > start(distance)[i],]
		if (dim(firstbins)[1]>0) { break }
		distance_d=distance_d[2:dim(distance_d)[1],]
	}
	
	for(j in 1:length(distance_d$start)){
			
		bins=table[abs(table$end_OE-table$start_Bait[1]) <= distance_d$end[j] & abs(table$end_OE-table$start_Bait[1]) > distance_d$start[j] ,]
		# print (bins)
		distance_d$RefBinMean[j]=geometric.mean(bins[,"N"])
		if (is.na(distance_d$RefBinMean[j]) & length(distance_d$RefBinMean[j-1])!=0 ) {distance_d$RefBinMean[j]=distance_d$RefBinMean[j-1]}
	}
  if(length(distance_d[distance_d$RefBinMean==0,]$RefBinMean)<=length(distance_d[distance_d$RefBinMean!=0,]$RefBinMean) & dim(distance_d)[1] >= 10){
		
	  function_distance <- glm.nb( distance_d$RefBinMean ~ distance_d$start,link="log") #Negative Binomial regression 
	  distance_d$predicted=fitted(function_distance)
   } else {
     distance_d$predicted=distance_d$RefBinMean
   }
	# print (distance_d)
	return (distance_d)

}

#Function local maxima To find peaks
FindPeaks <- function(table=table,w=50,span=0.05,d=0,cis_window=1500000) {
  y=table[,"N"]
	x=table[,"start_OE"]
	n <- length(y)
	# y.smooth <- loess(y ~ x, span=span)$fitted
	y.smooth <- y
	# print (y.smooth)
	y.max <- rollapply(zoo(y.smooth), 2*w+1,max,align="center")
	y.max2 <- rollapply(zoo(y), 2*w+1,max,align="center")
	delta2 <- y.max2 - y[-c(1:w, n+1-1:w)]
	i.max2 <- which(delta2 <= 0) + w
	delta <- y.max - y.smooth[-c(1:w, n+1-1:w)]
	i.max <- which(delta <= d) + w
	N_filter = which(y >=5)
	# i.max = intersect(i.max2,N_filter)
	i.max = i.max2
	# i.max = intersect(i.max,i.max2)
	# print (i.max)
	if (length(i.max)==0) {
		return(NULL)
	}
	final=data.frame()
	distance_d=Geometric_mean(table,cis_window)
	# print (distance_d)
	for (j in 1:length(i.max)){
		peak=table[i.max[j],]	
		dist=abs(peak$start_OE-peak$start_Bait[1])
		value=distance_d[dist >distance_d$start & dist <= distance_d$end,]
		value=value[!is.na(value$predicted),]
		if ( dim(value)[1] !=0 & dim(peak)[1] !=0 ) {
			if ( peak[,"N"]  > value$RefBinMean ) {
				final[j,1]=peak$ID_Bait
				final[j,2]=peak$ID_OE
				# print (value$predicted)
				# final[j,3]=log2(peak$N/value$predicted)
				final[j,3]=peak$N/value$RefBinMean
				counter <<- counter+1
			}
			
		}
		
	}
 final=na.omit(final)
	# print (final)
 if( dim(final)[1] !=0) {
   Final_coordinates=data.frame()
   for (i in 1:dim(final)[1]) {
   	Final_coordinates=rbind(Final_coordinates,table[table$ID_OE == final[i,2] & table$ID_Bait==final[i,1],])
    }
			# print (final[,3])
			# print (Final_coordinates)
   Final_coordinates$Enrichment = final[,3]
			
   return(Final_coordinates)
  }
}

#Main Function of identifying interactions 
IdentifyPeaks=function(gene=gene,table=ibed,window_size=window_size,loess_span=loess_span,cis_window=cis_window) {	
	
  table=table[table$Bait_name==gene,]
	table=table[order(table$start_OE),]
	ref=table$start_Bait[1]
	table=table[abs(table$end_OE -ref) <= cis_window,]
	cat(paste(gene,"\n"))
	peaks=NULL
  if (length(table$start_OE) == 0 | length(table$start_OE) < 2*window_size+1) {
		poor <<- c(poor,gene)
	}
  else {	
    	peaks=FindPeaks(table=table,w=window_size,span=loess_span,d=0,cis_window=cis_window)
	}
	if (!is.null(peaks)) { return(peaks) }
}

#Function wrapper for IdentifyPeaks
wrapeIdentifyPeaks=function(i) {

	Peaks_coordinates=IdentifyPeaks(gene=genes[i],table=ibed,window_size=window_size,loess_span=loess_span,cis_window=cis_window)
	
	return(Peaks_coordinates)
  
}




#
### =========================================================================
### ChiCMaxima Caller version beta 0.9
### -------------------------------------------------------------------------
###

if(version$major !="3" & version$minor !="0.2") {
  warning("Optimised for R version >= 3.0.2")
}
arg=commandArgs(TRUE)
if(length(arg)==0) {
  cat("CHiCMaxima pipeline for analyzing Capture-HiC data: 
Usage:
    ./ChiCMaxima_Caller.r [options] 
  Options:
    -i/--input			    <string>	[default:input]
    -o/--output                     <string>    [default:./output/]
    -w/--window_size                <string>    [default: 20    ]
    -s/--loess_span                 <string>    [default: 0.05  ]
    -c/--cis_window		    <string>    [default: 1500000 ]
   \n\n")
  q("no")

}else {
  tmp=suppressPackageStartupMessages(require("GenomicRanges"))
  if(!tmp) {
    stop("Package GenomicRanges required !!")
  }
  tmp=suppressPackageStartupMessages(require("MASS"))
  if (!tmp) {
	stop("Package MASS required !!")
  }
  tmp=suppressPackageStartupMessages(require("data.table"))	
  if (!tmp) {
	stop("Package data.table required !!")
  }
  tmp=suppressPackageStartupMessages(require("zoo"))
  if (!tmp) {
	stop("Package zoo required !!")
  }
  tmp=suppressPackageStartupMessages(require("psych"))
  if (!tmp) {
	stop("Package psych required !!")
  }
# w=20, s=0.05, b=30 kb, c=1.5 Mb.
  optArgs=getopt(
	rbind(
	    c('output','o', 1, 'character',"output.ibed"),
	    c('window_size', 'w', 1, 'integer', 20),
	    c('loess_span','s',1,'numeric',0.05),
	    c('input','i',1,'character',"chr1_mESCs.ibed"),
	    c('cis_window','c',1,'integer',1500000)
	    )
	)
}


#################################################################################
# ARGUMENTS
#################################################################################
file=optArgs$input
output=optArgs$output
window_size=optArgs$`window_size`
loess_span=optArgs$`loess_span`
cis_window=optArgs$`cis_window`





###################################################################################
# MAIN
###################################################################################

ibed=as.data.frame(fread(file,header=TRUE,fill=TRUE,check.names=TRUE),stringsAsFactors=FALSE)
# ibed$N = as.integer(ibed$N)
#Check presence of headers and appropriate ibed format
if(dim(ibed)[2]!=11) {
	stop("Wrong ibed format - ID_Bait, chr_Bait, start_Bait, end_Bait, Bait_name, ID_OE, chr_OE, start_OE, end_OE, OE_name, N\n")
}

if(colnames(ibed)[1] != "ID_Bait") {
  stop("Wrong ibed header or Missing header","\n")
}

colnames(ibed)=c("ID_Bait","chr_Bait","start_Bait","end_Bait","Bait_name","ID_OE","chr_OE","start_OE","end_OE","OE_name","N")

if (!is.numeric(ibed$ID_Bait) | !is.numeric(ibed$start_Bait) | !is.numeric(ibed$end_Bait) | !is.numeric(ibed$ID_OE) | !is.numeric(ibed$start_OE) | !is.numeric(ibed$end_OE) | !is.numeric(ibed$N)) {
	stop("Wrong ibed format - ID_Bait, chr_Bait, start_Bait, end_Bait, Bait_name, ID_OE, chr_OE, start_OE, end_OE, OE_name, N\n")
}

oe=as.factor(ibed$OE_name)
if(length(names(summary(oe)))!=1 & names(summary(oe))!=".") {
	cat ("Warning: some bait to bait interactions included in ibed\n")
} else {
	cat("No bait to bait interactions in ibed\n")
}

cis=(ibed$chr_Bait==ibed$chr_OE)
if (sum(cis)!=dim(ibed)[1]) {
	cat("Warning: trans interactions included in ibed\n")
} else {
	cat("All cis interactions in ibed\n")
}

genes=unique(ibed$Bait_name)
genes=genes[order(genes)]

#List of poorly covered genes; may help in optimisation of window_size
poor=c()
		
#Identifying Peaks
counter = 0
Peaks_final=data.frame()

Peaks_final=invisible(lapply(1:length(genes),wrapeIdentifyPeaks))

if(length(poor)>0) {
    
    cat(paste(length(poor),"genes insufficiently covered to compute interactions\n"))
    poor.fn = paste0(output,"_poorlycovered.txt")
    write.table(poor, poor.fn, sep="\t",quote=F,col.names=F,row.names=F )
}

# hits.fn = paste0(output,"_interactions.ibed")
hits.fn = paste0(output)
cat(file=hits.fn,"ID_Bait","\t","chr_Bait","\t","start_Bait","\t","end_Bait","\t","Bait_name","\t","ID_OE","\t","chr_OE","\t",  "start_OE","\t","end_OE","\t","OE_name","\t","N","\t","Enrichment","\n")
invisible(lapply(Peaks_final, function(x) write.table( data.frame(x), hits.fn  , append= T, sep="\t",quote=F,col.names=F,row.names=F )))
cat(paste(counter,"interactions found\n"))
				



