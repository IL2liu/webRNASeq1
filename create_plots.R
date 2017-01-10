createPlots <- function(filePath, basePlotPath, factors, plotFactors, factorColumnValues,  factorColumnValueSet, samples, sampleNames, factorSetMap, projectId, userId, startingColumn, commaOrTabDelimitedFlag) {

  # GIVEN: The counts matrix 
  #        filePath
  #        basePlotPath
  #        factors
  # 
  # RETURNS: 

  require(limma)

  require("reshape2")
  require("ggplot2")
  require("gplots")
  require("plyr")

  library(Biobase)
  library(statmod)
  library(affy)
  library(edgeR)
  
  
  print (paste(" in comma 222 ", commaOrTabDelimitedFlag,sep=","))  
  if (commaOrTabDelimitedFlag )  
  {
    data = read.delim2(filePath,as.is=T,check.names=F, sep=",")
    print (paste(" in comma", filePath,sep=","))  
  }
  else{
    data = read.delim2(filePath,as.is=T,check.names=F)
  }
  countTable=data[,-seq(1:startingColumn)]
  genenames=data$Geneid
  
  print (startingColumn)
  design_limma <-model.matrix(~0+factors)
  
  colnames(design_limma)<-levels(factor(factors))  

  sedIdx = match(samples,colnames(countTable))
  print  (paste(" colnames ", colnames(countTable),sep=","))  
  print  (paste(" samples ", samples,sep=","))    
  print  (paste(" in sedIdx ", sedIdx,sep=","))  
  countTable=countTable[,sedIdx]
  
  colnames(countTable) = sampleNames
  
  print (samples)
  
  counts = DGEList(counts=countTable,genes=genenames)
  isexpr<-rowSums(cpm(counts)>1)>=3
  counts <- counts[isexpr,keep.lib.sizes=FALSE]
  counts <-calcNormFactors(counts)  
 
  #normalizedCountsMatrix = cpm(counts)
  #write.csv(normalizedCountsMatrix,file=paste(outputPath, "/NormalizedData", ".csv", sep="")) 
 
  y <- voom(counts,design_limma)
  
  #MDS plot
  
  counter = 1
  for (plotFactor in plotFactors) {  
  
    #print (paste("plotFactor:",plotFactor, sep = ""))
    #print (paste("counter",counter, sep = " = "))
    #print (paste("factorColumnValues[counter]" , eval(parse(text=factorColumnValues[plotFactor])) , sep = " !!!!!! = !!!!! "))
    #print (paste("factorColumnValueSet[counter]" , factorColumnValueSet[counter] , sep = " ********* = ************ "))
    
    #print (paste("factorSetMap[factor]",eval(parse(text=(factorSetMap[plotFactor]))), counter, sep = " *^^* = *^^* "))
    
    #png(paste(basePlotPath, "/plotMDS_", plotFactor, ".png", sep=""), width=550, height=300, units = "px", units="in", res=300)

    #plotMDS(y,col=ifelse(eval(parse(text=factorColumnValues [plotFactor])) == factorColumnValueSet[counter],"blue","red"))
    
    png(paste(basePlotPath, "/plotMDS_", plotFactor, "_Project_", projectId, "_user_", userId, ".png", sep=""), width=6, height=4, units = "in", res=300)  
    
     # title  main = paste( "plotMDS_", plotFactor, sep="")
    
    plotMDS(y,col=ifelse(eval(parse(text=factorColumnValues [plotFactor])) == factorColumnValueSet[counter],"blue","red"), xlab = NA, ylab = NA, main=paste( "plotMDS_", plotFactor, sep=""))
    
    legend("topleft", legend=eval(parse(text=(factorSetMap[plotFactor]))), col=c("red", "blue"), pch=15)
    
    dev.off()
    
    counter = counter + 1

  }

  #MA Plot
  png(paste(basePlotPath, "/plotMA", "_Project_", projectId, "_user_", userId, ".png", sep=""), width=4, height=4, units="in", res=300)
  #print (paste("!!!!!!!!",basePlotPath, "/",listPlotFactorNames[counter], ".png", sep=""))
  limma::plotMA(y, main=paste( "plotMA", sep=""))
  dev.off()

  return

}
