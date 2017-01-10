#!/usr/bin/env python

from rpy2 import robjects

MAT_FN = robjects.r("source('limma_analysis.R'); contrasts_matrix")

factors = ['Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel']

contrasts = ['lowgel.baseline-Placebo.baseline', 'lowgel.baseline-lowgel.postgel', 'lowgel.baseline-Placebo.postgel', 'Placebo.baseline-lowgel.postgel', 'Placebo.baseline-Placebo.postgel', 'lowgel.postgel-Placebo.postgel']

samples = ['DV13-BL', 'EL86-BL', 'HA05-BL', 'FF66-BL', 'DH91-BL', 'DV13-PG', 'EL86-PG', 'GI57-PG', 'HA05-PG', 'FF66-PG', 'DH91-PG', 'HI81-PG', 'HH91-BL', 'GC05-BL', 'HH78-BL', 'EJ42-BL', 'FH29-BL', 'FC50-BL', 'GK45-BL', 'FV47-BL', 'HH91-PG', 'GC05-PG', 'HH78-PG', 'EJ42-PG', 'FH29-PG', 'FC50-PG', 'GK45-PG', 'FV47-PG', 'IC87-PG', 'GB85-PG']

animals = ['DV13', 'EL86', 'HA05', 'FF66', 'DH91', 'DV13', 'EL86', 'GI57', 'HA05', 'FF66', 'DH91', 'HI81', 'HH91', 'GC05', 'HH78', 'EJ42', 'FH29', 'FC50', 'GK45', 'FV47', 'HH91', 'GC05', 'HH78', 'EJ42', 'FH29', 'FC50', 'GK45', 'FV47', 'IC87', 'GB85']

groups = ['Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel']

conditions = ['baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel']

listPlotFactors = []

listPlotFactors.append(groups)
listPlotFactors.append(conditions)

filePath = "/Users/mitras/self/teleshova/counts.matrix"

contrast = MAT_FN(filePath, robjects.StrVector(factors), robjects.StrVector(samples), robjects.StrVector(animals), robjects.StrVector(listPlotFactors),  robjects.StrVector(contrasts))

#contrast = MAT_FN(robjects.StrVector(factors), robjects.StrVector(samples), robjects.StrVector(animals), robjects.StrVector(listPlotFactors),  robjects.StrVector(contrasts))

print str(contrast)

#contrasts_matrix <- function(filePath, factors, samples, individuals, listPlotFactors, contrasts) {

##contrasts_matrix <- function(f, contrasts) {
  
  ## GIVEN: The counts matrix filePath in xls format, the factors which can be design matrix in a
  ##        text file, and a string vector listing the contrasts.
  ## RETURNS: 
  
  #require(limma)

  #require(biomaRt)
  #require( "DESeq2" )
  #require("reshape2")
  #require("ggplot2")
  #require("gplots")
  #require("plyr")
  #require("genefilter")
 
  #library(Biobase)
  #library(statmod)
  #library(affy)
  #library(edgeR)
  
  ##data = read.delim2("/Users/mitras/self/teleshova/counts.matrix",as.is=T,check.names=F)

  #data = read.delim2(filePath,as.is=T,check.names=F)

  #col= sub("_S\\d+_R1_001", "", colnames(data),perl=TRUE)
  #col.n = sub("\\.bam", "",col,perl=T)
  #colnames(data)=col.n

  #countTable=data[,-seq(1:6)]

  #genenames=data$Geneid
  #mart<-useMart(biomart = "ENSEMBL_MART_ENSEMBL", dataset="mmulatta_gene_ensembl",host="www.ensembl.org")
  #genemap<-getBM(attributes=c("external_gene_name","ensembl_gene_id"), filters = "ensembl_gene_id",values=genenames,mart=mart)
  #idx <- match(genenames, genemap$ensembl_gene_id )
  #genesymbol <- genemap$external_gene_name[idx]
  
  ##design = read.delim2("/Users/mitras/self/teleshova/Teleshova_Phenotype_csv_final.csv",sep = ",",as.is=T)
  ##f <-factor(paste(design$Group,design$Condition,sep="."))  
  
  #design_limma <-model.matrix(~0+factors)
  
  #colnames(design_limma)<-levels(factor(factors))  
  
  #contrasts_matrix <- makeContrasts(contrasts=contrasts, levels=design_limma)

  #sedIdx = match(samples,colnames(countTable))
  #countTable=countTable[,sedIdx]
  
  #counts = DGEList(counts=countTable,genes=genesymbol)
  #isexpr<-rowSums(cpm(counts)>1)>=3
  #counts <- counts[isexpr,keep.lib.sizes=FALSE]
  #counts <-calcNormFactors(counts)  

  ##write.csv(counts,file="/Users/mitras/projects/webRNASeq/counts_matrix.csv")
  ##write.csv(design_limma,file="/Users/mitras/projects/webRNASeq/design_limma.csv")

  #y <- voom(counts,design_limma)
  #corfit <- duplicateCorrelation(y,design_limma,block=individuals)
  #v <- voom(counts,design_limma,plot=FALSE,block=samples,correlation=corfit$consensus)
  #fit <- lmFit(v,design_limma)

  #for (plotFactor in listPlotFactors){
    #plotMDS(y,col=ifelse(plotFactor=="factor","blue","red"))
  #}
  #fit2<-contrasts.fit(fit,contrasts_matrix)
  #fit2 <- eBayes(fit2)
  #results <-decideTests(fit2,method="separate",adjust.method="none",p.value=0.05,lfc=0.585)
  #write.csv(results,file="/Users/mitras/projects/webRNASeq/voom_lowgel_2.csv")
  ##vennDiagram(results)

  #for (contrast in contrasts){
    #res=topTable(fit2,coef=contrast,number=length(which(isexpr==TRUE)),sort="p")
    #write.csv(res,file=paste("/Users/mitras/projects/webRNASeq/", contrast, "_2.csv", sep=""))
  #}    

  #return(contrasts_matrix)

#}
