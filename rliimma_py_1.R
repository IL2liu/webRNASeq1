require(biomaRt)
require(DESeq2)
require(reshape2)
require(ggplot2)
require(gplots)
require(plyr)
require(genefilter)
require(edgeR)

design = read.delim2("/Users/mitras/self/teleshova/Teleshova_Phenotype_csv_final.csv",sep = ",",as.is=T)
f1 <-factor(paste(design$Group,design$Condition,sep="."))

rownames(design)=design$Sample

design.limma <-model.matrix(~0+f1)

# cont.matrix <- makeContrasts("lowgel"="f1lowgel.postgel-f1lowgel.baseline","Placebo"="f1Placebo.postgel-f1Placebo.baseline","diff"="(f1lowgel.postgel-f1lowgel.baseline)-(f1Placebo.postgel-f1Placebo.baseline)","baseline_diff"="f1lowgel.baseline-f1Placebo.baseline","postgel_diff"="f1lowgel.postgel-f1Placebo.postgel",levels=design.limma)
# makeContrasts("lowgel=f1lowgel.postgel-f1lowgel.baseline","Placebo=f1Placebo.postgel-f1Placebo.baseline","diff=(f1lowgel.postgel-f1lowgel.baseline)-(f1Placebo.postgel-f1Placebo.baseline)","baseline_diff=f1lowgel.baseline-f1Placebo.baseline","postgel_diff=f1lowgel.postgel-f1Placebo.postgel",levels=design.limma)

cc <- c("lowgel=f1lowgel.postgel-f1lowgel.baseline", "Placebo=f1Placebo.postgel-f1Placebo.baseline")

cm <- makeContrasts(cc, levels=design.limma) 

for(i in 1:1) 
{
  #cmi <- paste(cm,i,sep="_") 
  print (cc[i])
  print(makeContrasts(eval(cc[i]), levels=design.limma))
  print(makeContrasts("Placebo=f1Placebo.postgel-f1Placebo.baseline", levels=design.limma))
  #print(cmi)
}

# cm1 <- makeContrasts("lowgel=f1lowgel.postgel-f1lowgel.baseline",levels=design.limma)
# cm2 <- makeContrasts("Placebo=f1Placebo.postgel-f1Placebo.baseline",levels=design.limma)

#cont.matrix<-makeContrasts(lowgel=lowgel.postgel-lowgel.baseline,Placebo=Placebo.postgel-Placebo.baseline,diff=(lowgel.postgel-lowgel.baseline)-(Placebo.postgel-Placebo.baseline),baseline_diff=lowgel.baseline-Placebo.baseline,postgel_diff=lowgel.postgel-Placebo.postgel,levels=design.limma)