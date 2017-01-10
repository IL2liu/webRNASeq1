#createPlots <- function(filePath, basePlotPath, factors, samples) {

  ## GIVEN: The counts matrix 
  ##        filePath
  ##        basePlotPath
  ##        factors
  ## 
  ## RETURNS: 
  
 factors <- c('Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel')
 
 samples <- c('DV13-BL_S1_R1_001.bam', 'EL86-BL_S3_R1_001.bam', 'HA05-BL_S6_R1_001.bam', 'FF66-BL_S4_R1_001.bam', 
              'DH91-BL_S5_R1_001.bam', 'DV13-PG_S3_R1_001.bam', 'EL86-PG_S2_R1_001.bam', 'GI57-PG_S9_R1_001.bam',
              'HA05-PG_S7_R1_001.bam', 'FF66-PG_S1_R1_001.bam', 'DH91-PG_S14_R1_001.bam', 'HI81-PG_S5_R1_001.bam', 
              'HH91-BL_S2_R1_001.bam', 'GC05-BL_S7_R1_001.bam', 'HH78-BL_S8_R1_001.bam', 'EJ42-BL_S9_R1_001.bam', 
              'FH29-BL_S10_R1_001.bam', 'FC50-BL_S11_R1_001.bam', 'GK45-BL_S12_R1_001.bam', 'FV47-BL_S13_R1_001.bam', 
              'HH91-PG_S14_R1_001.bam', 'GC05-PG_S13_R1_001.bam', 'HH78-PG_S10_R1_001.bam', 'EJ42-PG_S15_R1_001.bam',
              'FH29-PG_S4_R1_001.bam', 'FC50-PG_S6_R1_001.bam', 'GK45-PG_S12_R1_001.bam', 'FV47-PG_S15_R1_001.bam', 
              'IC87-PG_S11_R1_001.bam', 'GB85-PG_S8_R1_001.bam')

filePath <- "/Users/mitras/projects/webRNASeq/Project_3/ww.csv"
basePlotPath <- "/Users/mitras/projects/webRNASeq/static/img"

require(limma)

require("reshape2")
require("ggplot2")
require("gplots")
require("plyr")

library(Biobase)
library(statmod)
library(affy)
library(edgeR)

data = read.delim2(filePath,as.is=T,check.names=F)
countTable=data[,-seq(1:6)]
genenames=data$Geneid
design_limma <-model.matrix(~0+factors)

colnames(design_limma)<-levels(factor(factors))  

sedIdx = match(samples,colnames(countTable))
countTable=countTable[,sedIdx]

counts = DGEList(counts=countTable,genes=genenames)
isexpr<-rowSums(cpm(counts)>1)>=3
counts <- counts[isexpr,keep.lib.sizes=FALSE]
counts <-calcNormFactors(counts)  
countsn <- counts

df<-data.frame(counts2 = unlist(countsn))

write.csv(df,file=paste("/Users/mitras/projects/webRNASeq/Project_3/NormalizedData", ".csv", sep=""))

y <- voom(counts,design_limma)

#MDS plot
png(paste(basePlotPath, "/plotMDS.png", sep=""), width=4, height=4, units="in", res=300)
#print (paste("!!!!!!!!",basePlotPath, "/",listPlotFactorNames[counter], ".png", sep=""))
plotMDS(y)
dev.off()

#MA Plot

png(paste(basePlotPath, "/plotMA.png", sep=""), width=4, height=4, units="in", res=300)
#print (paste("!!!!!!!!",basePlotPath, "/",listPlotFactorNames[counter], ".png", sep=""))
limma::plotMA(y)
dev.off()

