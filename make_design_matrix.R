design_matrix <- function( factors) {

  require(limma)

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
  
  design_limma <-model.matrix(~0+factors)
  
  colnames(design_limma)<-levels(factor(factors))
  
  return(design_limma)

  #return(factors)

}
