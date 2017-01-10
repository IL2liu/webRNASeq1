contrasts_matrix <- function(basePath, filePath, factors, plotFactors, factorColumnValues, factorColumnValueSet,  samples, individuals, contrasts) {

           contrast = MAT_FN(filePath, basePlotPath, outputPath, robjects.StrVector(factors), robjects.StrVector(factorColumns),robjects.ListVector(factorColumnValuesMap), robjects.StrVector(factorColumnValueSet),robjects.StrVector(samples), robjects.StrVector(animals), robjects.StrVector(contrasts))

#contrasts_matrix <- function(f, contrasts) {
  
  # GIVEN: The counts matrix filePath in xls format, the factors which can be design matrix in a
  #        text file, and a string vector listing the contrasts.
  # RETURNS: 
  
  require(limma)

  require(biomaRt)
  require( "DESeq2" )
  require("reshape2")
  require("ggplot2")
  require("gplots")
  require("plyr")
  require("genefilter")

  library(Biobase)
  library(statmod)
  library(affy)
  library(edgeR)
  
  data = read.delim2(filePath,as.is=T,check.names=F)
  
  #data = read.delim2("/Users/mitras/self/teleshova/counts.matrix",as.is=T,check.names=F)
  col= sub("_S\\d+_R1_001", "", colnames(data),perl=TRUE)
  col.n = sub("\\.bam", "",col,perl=T)
  colnames(data)=col.n

  countTable=data[,-seq(1:6)]

  genenames=data$Geneid
  mart<-useMart(biomart = "ENSEMBL_MART_ENSEMBL", dataset="mmulatta_gene_ensembl",host="www.ensembl.org")
  genemap<-getBM(attributes=c("external_gene_name","ensembl_gene_id"), filters = "ensembl_gene_id",values=genenames,mart=mart)
  idx <- match(genenames, genemap$ensembl_gene_id )
  genesymbol <- genemap$external_gene_name[idx]
  
  #design = read.delim2("/Users/mitras/self/teleshova/Teleshova_Phenotype_csv_final.csv",sep = ",",as.is=T)
  #f <-factor(paste(design$Group,design$Condition,sep="."))  
  
  design_limma <-model.matrix(~0+factors)
  
  colnames(design_limma)<-levels(factor(factors))  
  
  contrasts_matrix <- makeContrasts(contrasts=contrasts, levels=design_limma)

  sedIdx = match(samples,colnames(countTable))
  countTable=countTable[,sedIdx]
  
  counts = DGEList(counts=countTable,genes=genesymbol)
  isexpr<-rowSums(cpm(counts)>1)>=3
  counts <- counts[isexpr,keep.lib.sizes=FALSE]
  counts <-calcNormFactors(counts)  

  #write.csv(counts,file="/Users/mitras/projects/webRNASeq/counts_matrix.csv")
  #write.csv(design_limma,file="/Users/mitras/projects/webRNASeq/design_limma.csv")

  y <- voom(counts,design_limma)
  corfit <- duplicateCorrelation(y,design_limma,block=individuals)
  v <- voom(counts,design_limma,plot=FALSE,block=samples,correlation=corfit$consensus)
  fit <- lmFit(v,design_limma)

  for (plotFactor in listPlotFactors){
    plotMDS(y,col=ifelse(plotFactor=="factor","blue","red"))
  }
  fit2<-contrasts.fit(fit,contrasts_matrix)
  fit2 <- eBayes(fit2)
  results <-decideTests(fit2,method="separate",adjust.method="none",p.value=0.05,lfc=0.585)
  write.csv(results,file = paste(basePath,"decideTests.csv", sep=""))
  #vennDiagram(results)

  for (contrast in contrasts){
    res=topTable(fit2,coef=contrast,number=length(which(isexpr==TRUE)),sort="p")
    write.csv(res,file=paste(basePath, contrast, ".csv", sep=""))
  }    

  return(contrasts_matrix)

}
