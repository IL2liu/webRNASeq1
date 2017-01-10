import rpy2.robjects as robjects
import pandas as pd
import numpy
import itertools
import sys, traceback

def pythonR():

    try:
        
        df = pd.DataFrame.from_csv("/Users/mitras/self/teleshova/Teleshova_Phenotype_csv_final.csv")
	
	groupCol = "Group"
	conditionCol = "Condition"
	
	group = df[groupCol]
	condition = df[conditionCol]

	groupList = list(df[groupCol])
	conditionList = list(df[conditionCol])
	
	factorList = []
	
	factorList.append(groupList)
	factorList.append(conditionList)
	
	newList = [groupList, conditionList ]
	
	#print str(zip(newList))

	combinationStringList = [".".join(x) for x in zip (*newList)]
	
	print ":::: " + str(combinationStringList)
	
	rfactorList = robjects.StrVector(combinationStringList)
	
	robjects.globalenv["rf"] = rfactorList
	
	#combinationStringList = [".".join(x) for x in combinationStringList]
	
	print " combinationStringList *** " + str(combinationStringList)	
	
	robjects.r('design.limma <-model.matrix(~0+rf)')

	designpy = robjects.globalenv["design.limma"]
	
	robjects.r('colnames(design.limma)<-levels(rf)')
	
	print str("****** &&& from Python " + str(designpy.r_repr()))	
	
    except:

	traceback.print_exc(file=sys.stdout)

def robjectsR():

    try:
        
	robjects.r('design <- read.csv(file = "/Users/mitras/self/teleshova/Teleshova_Phenotype_csv_final.csv", header=TRUE, sep=",")')
	
	robjects.r('f <-factor(paste(design$Group,design$Condition,sep="."))')
	
	fpy = robjects.globalenv["f"]
	
	print str(fpy.r_repr())
	
	robjects.r('design.limma <-model.matrix(~0+f)')

	designpy = robjects.globalenv["design.limma"]
	
	print str(designpy.r_repr())
	
	robjects.r('colnames(design.limma)<-levels(rf)')

    except:

	traceback.print_exc(file=sys.stdout)
	
pythonR()
robjectsR()