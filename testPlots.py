from rnaseq.models import *
from rnaseq.rnaseqObjs import *

from django.conf import settings

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import sys, traceback, os , time
import datetime
from time import mktime

import pandas as pd
from pandas import *

from datetime import datetime
from pandas.tools.plotting import andrews_curves
from pandas.tools.plotting import autocorrelation_plot
from pandas.tools.plotting import radviz

from django.conf import settings

def testPlots():

    try:

        scatterDf = pd.DataFrame()

        analysisDetail = AnalysisDetail.objects.get (pk = 1)
        
        phenotypeFileType = FileType.objects.filter(name = "phenotypeFile")[0]
        
        phenotypeFile = DataFile.objects.filter(project = analysisDetail.dataFile.project, fileType = phenotypeFileType)[0]
        
        phenotypeFileName = phenotypeFile.name
        
        outputPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/Analysis_" + str(analysisDetail.id)
        
        filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id)
    
        phenotypeFileDf = pd.DataFrame.from_csv(filePath + "/" + str(phenotypeFileName), index_col=False)             

        analysisPlots = AnalysisPlot.objects.filter(analysisDetail = analysisDetail)
        
        analysisResultFiles = AnalysisResultFile.objects.filter(analysisDetail = analysisDetail)
        
        analysisResultFile = analysisResultFiles[0]

        designFactors = DesignFactor.objects.filter(analysisDetail = analysisDetail)
        limmaContrasts = LimmaContrast.objects.filter(analysisDetail = analysisDetail)

        normalizedCountsDf = pd.DataFrame.from_csv (outputPath + "/NormalizedData.csv", index_col = None)
        
        topTableDataFrame = pd.DataFrame.from_csv(analysisResultFile.filePath + ".csv", index_col = None)
       
        designFactorObjList = []
        
        print (" design factor " + str(designFactors) + " head = " + str(phenotypeFileDf.columns))

        designFactors = DesignFactor.objects.filter ( analysisDetail = analysisDetail)        

        dataFileColumnNameMap = {}

        for designFactor in designFactors:

            print ( " factr " + str(designFactor.name))

            factorValues = list(set(phenotypeFileDf[designFactor.name].tolist()))

            print ( " factorValues " + str(factorValues))

            for factorValue in factorValues:

                print ( " factorValue " + str(factorValue))

                sampleNames = phenotypeFileDf[phenotypeFileDf[designFactor.name] == factorValue][analysisDetail.sampleColumnName].tolist()

                print ( " sampleNames " + str(sampleNames))

                normalizedCountsDfSel = normalizedCountsDf[sampleNames]

                print ( " for factor " + str(factorValue) + " : " + str(normalizedCountsDfSel.head() ) )

                normalizedCountsDfSel["mean_"+ str(factorValue)] = normalizedCountsDfSel.mean(axis=1)

                #print ( " for normalizedCountsDfSel " + str(normalizedCountsDfSel.columns) + " : " + str(normalizedCountsDfSel.head() ) )

                topTableDataFrame["mean_"+ str(factorValue)] = normalizedCountsDfSel["mean_"+ str(factorValue)]

                sampleNamesTopTable = [x + "_" + factorValue for x in sampleNames]

                topTableDataFrame[sampleNamesTopTable] = normalizedCountsDfSel[sampleNames]
                
        #for analysisResultFile in analysisResultFiles:    

        print (" top table = " + str(topTableDataFrame.head()) )

        cutOffUpPValue = 0.05
        cutOffDownPValue = -0.05

        cutOffUpLogFC = 1.5
        cutOffDownLogFC = -1.5

        topTableUpDataFrame = topTableDataFrame[topTableDataFrame['logFC'] > cutOffUpLogFC]

        if cutOffUpPValue != 0:
            topTableUpDataFrame = topTableUpDataFrame[topTableUpDataFrame['P.Value'] < cutOffUpPValue]

        topTableDownDataFrame = topTableDataFrame[topTableDataFrame['logFC'] < cutOffDownLogFC]

        if cutOffDownPValue != 0:
            topTableDownDataFrame = topTableDownDataFrame[topTableDownDataFrame['P.Value'] < cutOffDownPValue]

        #limmaContrast = LimmaContrast.objects.filter(analysisDetail = analysisDetail, name = contrastObj.contrast)[0]
        nonBaseLineValues = [x for x in factorValues if x != designFactor.baseLineFactorValue]

        numerator = "mean_" + str(nonBaseLineValues[0])
        denominator = "mean_" + str(designFactor.baseLineFactorValue)

        print ( " numerator = " + str(numerator) + " denominator " + str(denominator))

        denominator = denominator.replace("-",".")
        numerator = numerator.replace("-",".")

        topTableDataFrame = topTableDataFrame [  (topTableDataFrame[denominator] !=  0 ) & (topTableDataFrame[numerator] != 0) ]

        topTableDataFrame.to_csv("outTopTableDf_" + analysisResultFile.name + ".csv", index = None)

        xmin, xmax = min(topTableDataFrame[numerator].tolist() )  ,  max ( topTableDataFrame[numerator].tolist() )
        ymin, ymax = min(topTableDataFrame[denominator].tolist() )  ,  max ( topTableDataFrame[denominator].tolist() )

        print ( " ::: topTableDataFrame 111111111 ::: = " + str(topTableDataFrame.head()) )

        significantDf = topTableDataFrame [  (topTableDataFrame["logFC"] >  1.5 ) ]

        #significantDf = topTableDataFrame [  (topTableDataFrame["logFC"] >  1.5 ) & (topTableDataFrame["adj.P.Val"] < 0.05) ]

        print ( " ::: significant ::: = " + str(significantDf.head()) )

        significantDf.to_csv()

        topTableDataFrame["color"] = ["red" if x in significantDf["genes"].tolist() else "blue" for x in topTableDataFrame["genes"].tolist() ]

        topTableDataFrame["marker"] = [3 if x in significantDf["genes"].tolist() else 1 for x in topTableDataFrame["genes"].tolist() ]

        topTableDataFrame.to_csv("finalDF_contrast_" + str(analysisResultFile.name) + ".csv", index = None)

        fig = plt.figure(figsize=(8, 8), dpi = 1200)

        size = fig.get_size_inches()*fig.dpi # size in pixels

        dpi = fig.get_dpi()

        topTableDataFrameBlue = topTableDataFrame [ topTableDataFrame["color"] == "blue" ]

        topTableDataFrameRed = topTableDataFrame [ topTableDataFrame["color"] == "red" ]

        plt.scatter(topTableDataFrameBlue[denominator], topTableDataFrameBlue[numerator],color='#3366ff', label=' ' , s = .85)

        plt.scatter(topTableDataFrameRed[denominator], topTableDataFrameRed[numerator],color='#f04722', label=' ' , s = 20)

        print ( " ::: topTableDataFrameRed ::: = " + str(topTableDataFrameRed.head()) )

        #plt.scatter(topTableDataFrame[denominator], topTableDataFrame[numerator], color= topTableDataFrame["color"], label = 'scatterPlot_p_val < 0.05' , s = .55)

        plt.xlabel(denominator)
        plt.ylabel(numerator)

        plt.title('scatterPlot_' + numerator + '_' + denominator)

        xymin = min(xmin, ymin)
        xymax = max(xmax, ymax)

        plt.xlim(xymin - .5, xymax - xymin-7)
        plt.ylim(xymin - .5, xymax-xymin-7)

        axes = plt.gca()

        plt.plot(axes.get_xlim(), axes.get_ylim(), c = "black")

        plt.plot([axes.get_xlim()[0] + 1.5, axes.get_xlim()[1] +1.5], [axes.get_ylim()[0], axes.get_ylim()[1]], c = "black")
        plt.plot([axes.get_xlim()[0], axes.get_xlim()[1] ], [axes.get_ylim()[0] + 1.5, axes.get_ylim()[1] + 1.5], c = "black")

        axes.spines['top'].set_visible(False)
        axes.spines['right'].set_visible(False)

        axes.spines["top"].set_linewidth(2)
        axes.spines["right"].set_linewidth(2)

        axes.yaxis.set_ticks_position('left')
        axes.xaxis.set_ticks_position('bottom')

        #plotPath = settings.PROJECT_BASE_FOLDER  + '/static/img/plots/scatterPlot_' + numerator + '_' + denominator
        plotName = 'scatterPlot_' + numerator + '_' + denominator

        plt.savefig(plotName + ".png")

    except:

        traceback.print_exc(file=sys.stdout)

    return

testPlots()
