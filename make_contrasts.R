contrasts_matrix <- function( factors, contrasts) {

  require(limma)

  design_limma <-model.matrix(~0+factors)
  
  colnames(design_limma)<-levels(factor(factors))  
  
  contrasts_matrix <- makeContrasts(contrasts=contrasts, levels=design_limma)

  return(contrasts_matrix)

}
