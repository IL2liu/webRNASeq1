find_levels <- function( factors) {

  require(limma)

  columnNames <- levels(factor(factors))
  
  return(columnNames)

}
