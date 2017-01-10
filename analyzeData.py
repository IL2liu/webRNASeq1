from pathway.models import *
from pathway.pathwayObjs import *
from pathway.settings import STATIC_DOC_ROOT
from pymongo import MongoClient
import numpy as np
import pandas as pd
from scipy import stats, integrate
import matplotlib.pyplot as plt
import seaborn as sns
import sys, traceback, os , time
import datetime
from time import mktime
from spectrum import *
import pandas as pd
from pandas import * 
import datetime
from datetime import datetime
from pandas.tools.plotting import andrews_curves
from pandas.tools.plotting import autocorrelation_plot
from pandas.tools.plotting import radviz
from scipy import stats
from statsmodels.formula.api import ols
import seaborn as sns
from django.conf import settings

basefilePath = "/Users/mitras/self/alex/data/"

dataFileMap = {}

FOLD_CHANGE_CUT_OFF = 1.5

def loadFileData():

    try:

	topTableDataFrame = pd.read_csv (settings.PROJECT_BASE_FOLDER + "projects/webBrainPathway/topTable_NAC_IP_vs_NAC_IN.csv")
	
	#if analysisResultFilterObj.topTableFoldChangeCutOff != 0:	
	
	topTableDataFrame = topTableDataFrame.loc[topTableDataFrame['logFC'] >= FOLD_CHANGE_CUT_OFF]
	
	# get top 1000 genes
	
	geneUpList = list(topTableDataFrame.sort('logFC',ascending = False).values)
	    
	geneDownList = list(topTableDataFrame.sort('logFC',ascending = True).values)
	
	geneUpSummaryObjList = []
	geneDownSummaryObjList = []
	    
	for geneIndex, data in enumerate ( geneUpList ): 
	    
	    genes = Gene.objects.filter(acronym = data[1])
	    
	    if len(genes) > 0:
		
		gene = genes[0]

		geneUpSummaryObj = GeneExpressionSummaryObj()
		
		geneUpSummaryObj.gene = gene
		
		geneExpressions = GeneExpression.objects.filter ( gene = gene )
		
		for geneExpression in geneExpressions:
		    
		    geneExpressionSectionDataSets = GeneExpressionSectionData.objects.filter(geneExpression = geneExpression)
		    
		    geneUpSummaryDataObj = GeneExpressionSummaryDataObj()
		    geneUpSummaryDataObj.geneExpression = geneExpression
		    for geneExpressionSectionDataSet in geneExpressionSectionDataSets: 
			
			geneUpSummaryDataObj.geneExpressionSectionDataList.append(geneExpressionSectionDataSet)
			geneUpSummaryDataObj.totalExpressionEnergy += geneExpressionSectionDataSet.expressionEnergy
			
		    geneUpSummaryObj.geneExpressionSummaryDataObjList.append(geneUpSummaryDataObj)
		    
		    geneUpSummaryObj.geneExpressionSummaryDataObjList.sort(key= lambda x: x.totalExpressionEnergy, reverse = True) 
			
		geneUpSummaryObjList.append(geneUpSummaryObj)
		
	for geneUpSummaryObj in geneUpSummaryObjList[:10]:
	    
	    print " ****** for gene " + str(geneUpSummaryObj.gene.acronym)  

	    for geneExpressionSummaryDataObj in geneUpSummaryObj.geneExpressionSummaryDataObjList[:10]:
		
		print " ---- for region " + str(geneExpressionSummaryDataObj.geneExpression.brainRegion.name)  + " total energy is " + str(geneExpressionSummaryDataObj.totalExpressionEnergy)  + " data is " + str([x.expressionEnergy for x in geneExpressionSummaryDataObj.geneExpressionSectionDataList])	
		
    except:
	
	traceback.print_exc(file=sys.stdout)

    return 
	    
loadFileData()
		


		
