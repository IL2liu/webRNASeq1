contrasts_matrix <- function(counts_matrix_xls, design_matrix_txt, contrasts) {
  # GIVEN: The counts matrix filename in xls format, the design matrix in a
  #        text file, and a string vector listing the contrasts.
  # RETURNS: THe contrasts matrix as specified by limma::makeContrasts.
  require(limma)

  data <- read.delim2(counts_matrix_xls, as.is=TRUE, check.names=FALSE)

  design <- read.delim2(design_matrix_txt, as.is=TRUE)
  rownames(design) <- design$Sample

  f <- factor(paste(design$Group, design$Condition, sep="."))

  design_limma <- model.matrix(~ 0 + f)
  colnames(design_limma) <- levels(f)

  return(makeContrasts(contrasts=contrasts, levels=design_limma))
}
