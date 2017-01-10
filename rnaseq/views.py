from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import HttpResponse

from rnaseq.models import *
from rnaseq.rnaseqObjs import *
from rnaseq.rnaseqConstants import *

import rpy2.robjects as robjects
from rpy2.robjects import r
from rpy2.robjects.packages import importr

import pandas as pd
from pandas import DataFrame

import openpyxl
import rnaseq.tasks as ts
import seaborn as sns
from seaborn import color_palette, diverging_palette
import matplotlib.pyplot as plt

#from bokeh.embed import components
#from bokeh.plotting import figure, ColumnDataSource
#from bokeh.models import HoverTool, Circle, Panel, Tabs
from bokeh.plotting import *
import bokeh
from bokeh.charts import Scatter, output_file, show
from bokeh.sampledata.autompg import autompg as df
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool

from bokeh.embed import components
from bokeh.models import Range1d

from bokeh.plotting import figure

#########
#from bokeh.models import Circle , HoverTool
#from bokeh.plotting import figure, ColumnDataSource
#########

from collections import OrderedDict

from bokeh.charts import Bar, output_file

import os, sys, traceback

import zipfile
import hashlib
import zlib

import io
import re
import shutil

from django.conf import settings
import numpy
import itertools
import csv
import datetime
import os.path
import rnaseq.task_utils as tsk

from bokeh.charts import Bar, output_file, show
from bokeh.charts.attributes import cat, color
from bokeh.charts.operations import blend

import math
from math import * 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/registration/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    })

#@login_required
def landing(request):
    return render_to_response("rnaseq/landing.html", {

    },  RequestContext(request))

#@login_required
def processLanding(request):
    
    ''' Function process landing page submit
    Input: params.request
    Output: Delegates task to corresponding handler
    '''
    rnaseqHomeButton = request.POST.get("rnaseqHomeButton","0" )

    if rnaseqHomeButton == "0":
        return listProjects( request )
    elif rnaseqHomeButton == "1":
        return listProjects ( request )
    elif rnaseqHomeButton == "2":
        return displayExpressionLevels ( request )
    elif rnaseqHomeButton == "3":
        return brainConnectivity ( request )
    elif rnaseqHomeButton == "4":
        return listAnalysisHeaders ( request )
    elif rnaseqHomeButton == "5":
        return submittedJobs ( request )

@login_required
def analyzeProject(request):

    ''' Function: Analyze project
    Input: params.request
    Output: 
        dataFile,
        analysisDetailObjList,
        phenotypeFileObjList,
    '''

    projectId = request.POST.get("projectId",0 )
    
    print (" project id = " + str(projectId))

    project = Project.objects.get(pk = projectId)

    contrastMatrixFileType = FileType.objects.filter(name = "contrastMatrix")[0]

    dataFile = DataFile.objects.filter ( project = project, fileType = contrastMatrixFileType )[0]

    analysisDetails = AnalysisDetail.objects.filter(dataFile = dataFile)

    phenotypeFileType = FileType.objects.filter(name = "phenotypeFile")[0]

    phenotypeFiles = DataFile.objects.filter(project = dataFile.project, fileType = phenotypeFileType)
    
    phenotypeFileObjList = []
    
    for phenotypeFile in phenotypeFiles:
        
        phenotypeFileObj = PhenotypeFileObj()
        
        phenotypeFileObj.phenotypeFile = phenotypeFile

        analysisDetails = AnalysisDetail.objects.filter ( phenotypeFile = phenotypeFile )
        
        if len(analysisDetails ) > 0:

            phenotypeFileObj.noDeleteFlag = True
            
        phenotypeFileObjList.append(phenotypeFileObj)    

    analysisDetailObjList = []

    for analysisDetail in analysisDetails:

        analysisDetailObj = AnalysisDetailObj()

        analysisDetailObj.analysisDetail = analysisDetail

        submittedJob = SubmittedJob.objects.filter(analysisDetail = analysisDetail)[0]

        analysisDetailObj.dateAnalyzed = submittedJob.completedTime

        analysisDetailObjList.append(analysisDetailObj)

    return render_to_response('rnaseq/analyzeFileSelect.html', {

        "dataFile":dataFile,
        "analysisDetailObjList":analysisDetailObjList,
        "phenotypeFileObjList":phenotypeFileObjList,

    },  RequestContext(request))

@login_required
def analyzeFileSelect(request):
    
    '''Function: Show the screen prompting the user to  upload Phenotype File. 
    Input: request
    Output: List of phenotype files, past analyses'''
    
    try:

        dataFileId = request.POST.get("dataFileId",0 )
    
        dataFile = DataFile.objects.get(pk = dataFileId)
    
        analysisDetails = AnalysisDetail.objects.filter(dataFile = dataFile)
    
        phenotypeFileType = FileType.objects.filter(name = "phenotypeFile")[0]
    
        phenotypeFiles = DataFile.objects.filter(project = dataFile.project, fileType = phenotypeFileType)
        
        phenotypeFileObjList = []
        
        for phenotypeFile in phenotypeFiles:
            
            phenotypeFileObj = PhenotypeFileObj()
            
            phenotypeFileObj.phenotypeFile = phenotypeFile
    
            analysisDetails = AnalysisDetail.objects.filter ( phenotypeFile = phenotypeFile )
            
            if len(analysisDetails ) > 0:
    
                phenotypeFileObj.noDeleteFlag = True
                
            phenotypeFileObjList.append(phenotypeFileObj)
    
        analysisDetailObjList = []
    
        for analysisDetail in analysisDetails:
    
            analysisDetailObj = AnalysisDetailObj()
    
            analysisDetailObj.analysisDetail = analysisDetail
    
            submittedJob = SubmittedJob.objects.filter(analysisDetail = analysisDetail)[0]
    
            analysisDetailObj.dateAnalyzed = submittedJob.completedTime
    
            analysisDetailObjList.append(analysisDetailObj)
        
    except:
        
        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/analyzeFileSelect.html', {

        "dataFile":dataFile,
        "analysisDetailObjList":analysisDetailObjList,
        "phenotypeFileObjList":phenotypeFileObjList,

    },  RequestContext(request))

@login_required
def showPlots(request):
    
    '''Function: Show the different plots like MDS plots, MA plots, prior
    to submitting analysis. 
    Input: request
    Output:
        "plotObjList":plotObjList,

        "datafile":dataFile,
        "designMatrix":designMatrix,

        "matrixColumns":matrixColumns,
        
        "designFactorObjList":designFactorObjList,

        "contrasts":contrasts,
        "contrastMatrix":contrastMatrix,
        "contrastMatrixColumns":contrastMatrixColumns,
        "phenotypeFile":phenotypeFile,
        "phenotypeColumns":phenotypeColumns,
        "columnTypeIds":columnTypeIds,
        "contrastMatrixRowObjList":contrastMatrixRowObjList,
        "analysisDetailName": analysisDetailName,
        "baselines":baselines,

        "analysisDetails":analysisDetails,

        "matrixColumnMatchObjList":matrixColumnMatchObjList,
        '''    

    try:

        dataFileId = request.POST.get("dataFileId",0)

        dataFile = DataFile.objects.get(pk = dataFileId)
        
        analysisDetails = AnalysisDetail.objects.filter ( dataFile = dataFile)

        phenotypeFileId = request.POST.get("phenotypeFileId",0)
        
        phenotypeFile = DataFile.objects.get(pk = phenotypeFileId)

        phenotypeFileName = phenotypeFile.name

        phenotypeColumns = request.POST.getlist("phenotypeColumn")

        columnTypeIds = request.POST.getlist("columnTypeId")

        singleFirstContrasts = request.POST.getlist("singleFirstContrast")
        singleSecondContrasts = request.POST.getlist("singleSecondContrast")
        
        allSingleContrasts = [a + "-" + b for (a,b) in zip(singleFirstContrasts, singleSecondContrasts)]

        doubleFirstContrasts = request.POST.getlist("doubleFirstContrast")
        doubleSecondContrasts = request.POST.getlist("doubleSecondContrast")

        allDoubleContrasts = ["(" + x + ")-(" + y + ")"for x,y in zip(doubleFirstContrasts, doubleSecondContrasts)]

        singleContrasts = request.POST.getlist("singleContrastString")
        doubleContrasts = request.POST.getlist("doubleContrastString")

        print ( " single contrasts = " + str(singleContrasts) )
        print ( " double contrasts = " + str(doubleContrasts) )

        singleFirstContrasts = [x for (x,y) in zip(singleFirstContrasts, allSingleContrasts) if y in singleContrasts ]
        singleSecondContrasts = [x for (x,y) in zip(singleSecondContrasts, allSingleContrasts) if y in singleContrasts ]
       
        doubleFirstContrasts = [x for (x,y) in zip(doubleFirstContrasts, allDoubleContrasts) if y in doubleContrasts ]
        doubleSecondContrasts = [x for (x,y) in zip(doubleSecondContrasts, allDoubleContrasts) if y in doubleContrasts ]

        contrasts = singleContrasts + doubleContrasts
        
        #print (" ***** contrasts = " + str(contrasts) )

        #print (" ***** singleFirstContrasts = " + str(singleFirstContrasts) )
        #print (" ***** singleSecondContrasts = " + str(singleSecondContrasts) )

        #print (" ***** doubleFirstContrasts = " + str(doubleFirstContrasts) )
        #print (" ***** doubleSecondContrasts = " + str(doubleSecondContrasts) )

        baselines = request.POST.getlist("baseline")

        normalizationMethod = request.POST.get("normalizationMethod",0)

        columnTypeIds = [int(x) for x in columnTypeIds  if x != '' ]

        phenotypeColumnObjList = []

        samples = []

        animals = []

        plotObjList = []

        sampleColumn = ''
        
        analysisDetailName = "Analysis_for_" + str(dataFile.name) + "_on_" + str(datetime.datetime.strftime(datetime.datetime.now(), "%d-%b-%Y-%H_%M_%S"))

        #print " column type ids = " + str(columnTypeIds)

        for index, columnTypeId in enumerate ( columnTypeIds ):

            if phenotypeColumns [index] != '':

                columnType = ColumnType.objects.get(pk = int(columnTypeId))

                if columnType.name == "factor":

                    phenotypeColumnObj = PhenotypeColumnObj()

                    phenotypeColumnObj.colName = phenotypeColumns [index]
                    phenotypeColumnObj.columnType = columnType

                    phenotypeColumnObjList.append(phenotypeColumnObj)

                elif columnType.name == "sample":

                    sampleColumn = phenotypeColumns [index]

        filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(dataFile.project.id)

        phenotypeFileDf = pd.DataFrame.from_csv(filePath + "/" + str(phenotypeFileName), index_col=False)

        factorSetList = []

        listPlotFactors = []

        listPlotFactorNames = []

        sampleColumnName = ''

        blockColumn = ''

        factorColumns = []

        factorColumnValues = []
        
        factorNum = 0         
        
        designFactorObjList = []
        
        plotObj = PlotObj()
        
        plotObj.plotType = "MA"

        plotObj.plotLabel = ""

        plotObj.plotPath = "plots/plotMA" + "_Project_" + str(dataFile.project.id) + "_user_" + str(request.user)

        plotObj.plotName = "plotMA" 
        
        plotObjList.append(plotObj)          
    
        for phenotypeColumnIndex, phenotypeColumnObj in enumerate ( phenotypeColumnObjList ):
    
            designFactorObj = DesignFactorObj()
            
            designFactorObj.designFactorName = phenotypeColumnObj.colName
            
            columnValueList = phenotypeFileDf [phenotypeColumnObj.colName].tolist()
    
            #columnValueList = list(columnValues)
            
            designFactorObj.designFactorName = phenotypeColumnObj.colName
            
            designFactorObj.designFactorBaseline = baselines[phenotypeColumnIndex]
            designFactorObj.designFactorValues = ",".join(list(set(columnValueList)))  
            
            designFactorObjList.append(designFactorObj)        

            factorColumnValues.append(columnValueList)

            if phenotypeColumnObj.columnType.name == "factor":

                columnValueList = [x.replace(" ","_").replace("(","").replace(")","") for x in columnValueList]

                factorSetList.append(columnValueList)

                listPlotFactors.append(columnValueList)

                listPlotFactorNames.append(phenotypeColumnObj.colName)

                factorColumns.append(phenotypeColumnObj.colName)

                #plotMDSPathList.append("plotMDS_" + phenotypeColumnObj.colName)
                
                plotObj = PlotObj()
                
                plotObj.plotType = "MDS"

                plotObj.plotLabel = phenotypeColumnObj.colName

                plotObj.plotName = "plotMDS_" + phenotypeColumnObj.colName 

                plotObj.plotPath = "plots/plotMDS_" + phenotypeColumnObj.colName + "_Project_" + str(dataFile.project.id) + "_user_" + str(request.user)
        
                plotFactorValues = set(phenotypeFileDf[phenotypeColumnObj.colName].tolist())
    
                redColorFactorValue = baselines[factorNum]            
    
                plotObj.redColorFactorValue = redColorFactorValue                

                blueColorFactorValue = ''
                
                #print (" baselines = " +  str(baselines))
                
                #print (" list(plotFactorValues) " + str(list(plotFactorValues)))
                
                #print (" baselines[factorNum] " + str(baselines[factorNum]))
                
                if len(list(plotFactorValues)) > 1:
                    
                    plotFactorValuesList = list(plotFactorValues)
                    
                    plotFactorValuesListContrast = [x for x in plotFactorValuesList if x != baselines[factorNum]]

                    #print (" plotFactorValuesListContrast = " +  str(plotFactorValuesListContrast))
                    
                    blueColorFactorValue = plotFactorValuesListContrast[0]            
    
                plotObj.blueColorFactorValue = blueColorFactorValue                
                
                plotObjList.append(plotObj)
                
                factorNum = factorNum + 1

            elif phenotypeColumnObj.columnType.name == "sample" and len(samples) == 0:

                samples = columnValueList

                sampleColumnName = phenotypeColumnObj.columnType.name

            elif phenotypeColumnObj.columnType.name == "block" and len(animals) == 0:

                animals = columnValueList

                blockColumnName = phenotypeColumnObj.columnType.name

        factors = []

        #print " factor set list = " + str(factorSetList)

        factors = [".".join(x) for x in zip (*factorSetList)]

        factorColumnValuesMap = {}

        factorSetMap = {}

        for factorIndex, factorColumn in enumerate(factorColumns):

            factorColumnValuesMap[factorColumn] = robjects.StrVector(factorColumnValues[factorIndex])
            
            uniqueFactorColumnValues = list(set(factorColumnValues[factorIndex]))
            
            #print ( " unique values = " + str(uniqueFactorColumnValues))
            
            #print ( " $$$$$ base line value = " + str(baselines[factorIndex]) )

            #print ( " $$$$$333 index = " + str(uniqueFactorColumnValues.index(baselines[factorIndex]) ))

            baselineIndex = uniqueFactorColumnValues.index(baselines[factorIndex])
            
            if baselineIndex != -1 and baselineIndex == 0 and len(uniqueFactorColumnValues) > 0:
                
                uniqueFactorColumnValues[0] , uniqueFactorColumnValues[1] = uniqueFactorColumnValues[1] , uniqueFactorColumnValues[0] 

            #print ( " unique values after = " + str(uniqueFactorColumnValues))

            #factorSetMap[factorColumn] = robjects.StrVector(list(set(factorColumnValues[factorIndex])))           
            
            factorSetMap[factorColumn] =  uniqueFactorColumnValues

        DESIGN_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/make_design_matrix.R'); design_matrix")

        designMatrixR = numpy.array(DESIGN_FN( robjects.StrVector(factors)))

        #print " designMatrix = " + str(designMatrixR)

        LEVELS_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/find_levels.R'); find_levels")

        matrixColumns = numpy.array(LEVELS_FN( robjects.StrVector(factors)))

        #print " matrix columns = " + str(matrixColumns)

        designMatrix = []

        for row in designMatrixR:

            row = [int(x) for x in numpy.array(row)]

            designMatrix.append(numpy.array(row))

        CONTRASTS_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/make_contrasts.R'); contrasts_matrix")

        #print " contrastMatrix = " + str(contrasts)

        contrastMatrixR = numpy.array(CONTRASTS_FN( robjects.StrVector(factors), robjects.StrVector(contrasts)))

        #print " contrastMatrix = " + str(contrastMatrixR)

        contrastMatrix = []

        #for row in contrastMatrixR:

            #row = [int(x) for x in numpy.array(row)]

            #contrastMatrix.append(numpy.array(row))

            #print " adding row " + str(row)

        contrastMatrixRowObjList = []

        for rowIndex, row in enumerate ( contrastMatrixR ) :

            row = [int(x) for x in numpy.array(row)]

            contrastMatrix.append(numpy.array(row))

            #print " adding row " + str(row)

            contrastMatrixRowObj = ContrastMatrixRowObj()

            contrastMatrixRowObj.contrastLevel = matrixColumns [rowIndex]

            contrastMatrixRowObj.contrastMatrixRow = numpy.array(row)

            contrastMatrixRowObjList.append(contrastMatrixRowObj)

        #designMatrixFilePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(dataFile.project.id)
        #contrastMatrixFilePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(dataFile.project.id)

        contrastMatrixColumns = contrasts

        matrixColumnMatchObjList = []

        sampleNames = phenotypeFileDf [sampleColumn].tolist()

        numSamples = range(len(sampleNames))

        for sampleIndex, sampleName in enumerate(sampleNames):

            matrixColumnMatchObj = MatrixColumnMatchObj()

            sampleNameValue = request.POST.get("sampleName-" + str(sampleIndex),"" )

            #print " sample name value = " + str(sampleNameValue) + " for : sampleName-" + str(sampleIndex)

            matchColumnValue = request.POST.get("dataMatrixColumn-" + str(sampleIndex),"" )

            #print " match column value = " + str(matchColumnValue) + " for : sampleName-" + str(sampleIndex)

            matrixColumnMatchObj.selectedSampleName = sampleNameValue
            matrixColumnMatchObj.selectedMatrixColumn = matchColumnValue

            matrixColumnMatchObjList.append(matrixColumnMatchObj)

        sampleXrefList = []

        #print " ****** sample column = " + str(sampleColumn)

        sampleNames = phenotypeFileDf [sampleColumn].tolist()

        numSamples = range(len(sampleNames))

        for sampleIndex, sampleName in enumerate(sampleNames):

            matchColumnValue = request.POST.get("dataMatrixColumn-" + str(sampleIndex),"" )

            #print " match column value = " + str(matchColumnValue)     + " for : sampleName-" + str(sampleIndex)

            sampleXrefList.append(matchColumnValue)

        basePlotPath = settings.IMAGE_OUTPUT_FOLDER + "/plots"

        #basePlotProjectPath = settings.IMAGE_OUTPUT_FOLDER + "/plots/Project_" + str(dataFile.project.id)
        
        filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(dataFile.project.id)
        
        print ( " ***** basePlotPath = " + str(basePlotPath) )

        print ( " ***** filePath = " + str(filePath) )
        
        if not os.path.isdir(filePath):
            
            os.mkdir(filePath)
            
        #if not os.path.isdir(basePlotProjectPath):
            
            #os.mkdir(basePlotProjectPath)

        if not os.path.isdir(basePlotPath):
            
            os.mkdir(basePlotPath)

        countsMatrixFilePath = filePath + "/" + str(dataFile.name) +".csv"

        #print (" matrix file path = " + str(countsMatrixFilePath) )
        #print (" base plot path = " + str(basePlotPath) )
        #print (" factors = " + str(factors) )
        #print (" factorColumns = " + str(factorColumns) )
        #print (" factorColumnValuesMap = " + str(factorColumnValuesMap) )
        #print (" baselines = " + str(baselines) )
        #print (" sampleXRefList = " + str(sampleXrefList) )
        #print (" sampleNames = " + str(sampleNames) )

        #print (" factorSetMap = " + str(factorSetMap) )
        
        PLOT_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/create_plots.R'); createPlots")
        
        startingColumn = dataFile.startingColumn
        
        if startingColumn == 0:
            
            startingColumn = DEFAULT_STARTING_COLUMN

        PLOT_FN(countsMatrixFilePath, basePlotPath, robjects.StrVector(factors), robjects.StrVector(factorColumns), robjects.ListVector(factorColumnValuesMap), robjects.StrVector(baselines), robjects.StrVector(sampleXrefList), robjects.StrVector(sampleNames), robjects.ListVector(factorSetMap), str(dataFile.project.id), str(request.user), str(startingColumn), dataFile.commaOrTabDelimitedFlag )
         
        #PLOT_FN(countsMatrixFilePath, basePlotPath, robjects.StrVector(factors), robjects.StrVector(factorColumns), robjects.ListVector(factorColumnValuesMap), robjects.StrVector(factorSetList), robjects.StrVector(sampleXrefList), robjects.StrVector(sampleNames))	        

        #plotMDSPath = "plotMDS"

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/showPlots.html', {

        "plotObjList":plotObjList,

        "datafile":dataFile,
        "designMatrix":designMatrix,

        "matrixColumns":matrixColumns,
        
        "designFactorObjList":designFactorObjList,

        "contrasts":contrasts,
        "contrastMatrix":contrastMatrix,
        "contrastMatrixColumns":contrastMatrixColumns,
        "phenotypeFile":phenotypeFile,
        "phenotypeColumns":phenotypeColumns,
        "columnTypeIds":columnTypeIds,
        "contrastMatrixRowObjList":contrastMatrixRowObjList,
        "analysisDetailName": analysisDetailName,
        "baselines":baselines,

        "analysisDetails":analysisDetails,

        "singleFirstContrasts" : singleFirstContrasts,
        "singleSecondContrasts" : singleSecondContrasts,
       
        "doubleFirstContrasts" : doubleFirstContrasts,
        "doubleSecondContrasts" : doubleSecondContrasts, 

        "matrixColumnMatchObjList":matrixColumnMatchObjList,

    },  RequestContext(request))

@login_required
def analyzeFileSubmit(request):
    
    '''Function: Submit analysis to Celery message queue. 
    Input: request
    Output:
        "plotObjList":plotObjList,

        "datafile":dataFile,
        "designMatrix":designMatrix,

        "matrixColumns":matrixColumns,
        
        "designFactorObjList":designFactorObjList,

        "contrasts":contrasts,
        "contrastMatrix":contrastMatrix,
        "contrastMatrixColumns":contrastMatrixColumns,
        "phenotypeFile":phenotypeFile,
        "phenotypeColumns":phenotypeColumns,
        "columnTypeIds":columnTypeIds,
        "contrastMatrixRowObjList":contrastMatrixRowObjList,
        "analysisDetailName": analysisDetailName,
        "baselines":baselines,

        "analysisDetails":analysisDetails,

        "matrixColumnMatchObjList":matrixColumnMatchObjList,
        '''      
    

    dataFileId = request.POST.get("dataFileId",0)

    dataFile = DataFile.objects.get(pk = dataFileId)
    
    phenotypeFileId = request.POST.get("phenotypeFileId",0)
    
    phenotypeFile = DataFile.objects.get(pk = phenotypeFileId)
    
    phenotypeFileName = phenotypeFile.name    

    phenotypeColumns = request.POST.getlist("phenotypeColumn")

    columnTypeIds = request.POST.getlist("columnTypeId")
    
    baseline =  request.POST.getlist("baseline")

    contrasts = request.POST.getlist("contrastString")

    normalizationMethod = request.POST.getlist("normalizationMethod")

    decidetestsPValue = request.POST.getlist("decidetestsPValue")

    decidetestsLFC = request.POST.getlist("decidetestsLFC")
    
    analysisDetailName = request.POST.get("analysisDetailName","")
    
    singleFirstContrasts = request.POST.getlist("singleFirstContrast")
    singleSecondContrasts = request.POST.getlist("singleSecondContrast")

    doubleFirstContrasts = request.POST.getlist("doubleFirstContrast")
    doubleSecondContrasts = request.POST.getlist("doubleSecondContrast") 
    
    allContrastStrings = singleFirstContrasts + singleSecondContrasts + doubleFirstContrasts + doubleSecondContrasts

    print ( " ******** singleFirstContrasts ********* " + str(singleFirstContrasts) ) 
    print ( " ******** singleSecondContrasts ********* " + str(singleSecondContrasts) ) 

    print ( " ******** doubleFirstContrasts ********* " + str(doubleFirstContrasts) ) 
    print ( " ******** doubleSecondContrasts ********* " + str(doubleSecondContrasts) )     

    print ( " ******** allContrastStrings ********* " + str(allContrastStrings) ) 

    columnTypeIds = [int(x) for x in columnTypeIds  if x != '' ]

    #print "phenotypeColumns = " + str(phenotypeColumns)

    #print "columnTypeIds = " + str(columnTypeIds)

    phenotypeColumnObjList = []

    samples = []

    animals = []

    plotMDSPathList = []

    sampleColumn = ''

    #print " column type ids = " + str(columnTypeIds)

    for index, columnTypeId in enumerate ( columnTypeIds ):

        if phenotypeColumns [index] != '':

            columnType = ColumnType.objects.get(pk = int(columnTypeId))

            if columnType.name == "factor":

                phenotypeColumnObj = PhenotypeColumnObj()

                phenotypeColumnObj.colName = phenotypeColumns [index]
                phenotypeColumnObj.columnType = columnType

                phenotypeColumnObjList.append(phenotypeColumnObj)

            elif columnType.name == "sample":

                sampleColumn = phenotypeColumns [index]
                
            elif columnType.name == "block":

                blockColumnName = phenotypeColumns [index]                

    filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(dataFile.project.id)

    phenotypeFileDf = pd.DataFrame.from_csv(filePath + "/" + str(phenotypeFileName), index_col=False)

    factorSetList = []

    listPlotFactors = []

    listPlotFactorNames = []

    sampleColumnName = ''

    blockColumnName = ''

    factorColumns = []

    factorColumnValues = []

    for phenotypeColumnObj in phenotypeColumnObjList:

        #print " file is = " + str(phenotypeFile)

        #print " column is " + str (phenotypeColumnObj.colName) + " col name = " + str(phenotypeColumnObj.colName) + " column type name " + str(columnType.name)

        #print " samples are " + str(phenotypeFile [phenotypeColumnObj.colName])

        columnValues = phenotypeFileDf [phenotypeColumnObj.colName].tolist()

        columnValueList = list(columnValues)

        factorColumnValues.append(columnValueList)

        if phenotypeColumnObj.columnType.name == "factor":

            columnValueList = [x.replace(" ","_").replace("(","").replace(")","") for x in columnValueList]

            factorSetList.append(columnValueList)

            listPlotFactors.append(columnValueList)

            listPlotFactorNames.append(phenotypeColumnObj.colName)

            factorColumns.append(phenotypeColumnObj.colName)

            plotMDSPathList.append("plotMDS_" + phenotypeColumnObj.colName)

        elif phenotypeColumnObj.columnType.name == "sample" and len(samples) == 0:

            samples = columnValueList

            sampleColumnName = phenotypeColumnObj.columnType.name

        elif phenotypeColumnObj.columnType.name == "block" and len(animals) == 0:

            animals = columnValueList

            blockColumnName = phenotypeColumnObj.columnType.name

    factors = []

    #print " factor set list = " + str(factorSetList)

    factors = [".".join(x) for x in zip (*factorSetList)]
    
    factorSetList = [list(set(x)) for x in factorSetList]

    factorSetList = [x[0] for x in factorSetList]

    factorColumnValuesMap = {}
    
    factorSetMap = {}

    for factorIndex, factorColumn in enumerate(factorColumns):

        factorColumnValuesMap[factorColumn] = robjects.StrVector(factorColumnValues[factorIndex])
        
        factorSetMap[factorColumn] = robjects.StrVector(list(set(factorColumnValues[factorIndex])))         
        
        uniqueFactorColumnValues = list(set(factorColumnValues[factorIndex]))
        
        baselineIndex = uniqueFactorColumnValues.index(baseline[factorIndex])
        
        if baselineIndex != -1 and baselineIndex == 0 and len(uniqueFactorColumnValues) > 0:
            
            uniqueFactorColumnValues[0] , uniqueFactorColumnValues[1] = uniqueFactorColumnValues[1] , uniqueFactorColumnValues[0] 

        factorSetMap[factorColumn] =  uniqueFactorColumnValues        

    DESIGN_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/make_design_matrix.R'); design_matrix")

    designMatrixR = numpy.array(DESIGN_FN( robjects.StrVector(factors) ))

    #print " designMatrix = " + str(designMatrixR)

    LEVELS_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/find_levels.R'); find_levels")

    matrixColumns = numpy.array(LEVELS_FN( robjects.StrVector(factors)  ))

    #print " matrix columns = " + str(matrixColumns)

    designMatrix = []

    for row in designMatrixR:

        row = [int(x) for x in numpy.array(row)]

        designMatrix.append(numpy.array(row))

    CONTRASTS_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/make_contrasts.R'); contrasts_matrix")

    #print " contrastMatrix = " + str(contrasts)

    contrastMatrixR = numpy.array(CONTRASTS_FN( robjects.StrVector(factors),  robjects.StrVector(contrasts)))

    #print " contrastMatrix = " + str(contrastMatrixR)

    contrastMatrix = []

    for row in contrastMatrixR:

        row = [int(x) for x in numpy.array(row)]

        contrastMatrix.append(numpy.array(row))

        #print " adding row " + str(row)

    sampleXrefList = []

    sampleNames = phenotypeFileDf [sampleColumn].tolist()

    numSamples = range(len(sampleNames))

    #basePath = settings.PROJECT_BASE_FOLDER

    basePlotPath = settings.IMAGE_OUTPUT_FOLDER + "/plots"

    #filePath = settings.DATA_OUTPUT_FOLDER # + "/webRNASeq/" + str(datafile.filePath)

    countsMatrixFilePath = filePath + "/" + str(dataFile.name) +".csv"

    analysisDetail = AnalysisDetail(name = analysisDetailName, dataFile = dataFile, phenotypeFile = phenotypeFile, sampleColumnName = sampleColumn, blockColumnName = blockColumnName)
    analysisDetail.save()

    for sampleIndex, sampleName in enumerate(sampleNames):

        matchColumnValue = request.POST.get("dataMatrixColumn-" + str(sampleIndex),"" )

        #print " match column value = " + str(matchColumnValue) + " for : sampleName-" + str(sampleIndex)

        sampleXrefList.append(matchColumnValue)
        
        sampleNameXRef = SampleNameXRef  ( dataFileColumnName = matchColumnValue, sampleName = sampleName, analysisDetail = analysisDetail ) 
        
        sampleNameXRef.save()        

    for factorIndex, factorColumn in enumerate(factorColumns):

        designFactor = DesignFactor(name = factorColumn, description = factorColumn, analysisDetail = analysisDetail, baseLineFactorValue = baseline[factorIndex])
        designFactor.save()
        
    numeratorContrasts = singleFirstContrasts + doubleFirstContrasts
    denominatorContrasts = singleSecondContrasts + doubleSecondContrasts

    for index, contrast in enumerate(contrasts):

        limmaContrast = LimmaContrast(analysisDetail = analysisDetail, name = contrast, description = contrast, numerator = numeratorContrasts[index], denominator = denominatorContrasts[index] )
        limmaContrast.save()

    queueJobStatusCode = JobStatusCode.objects.all().filter(code="QUEUE")[0]
    analysisJobType  = SubmittedJobType.objects.all().filter(name="Analysis")[0]

    submittedJob = SubmittedJob (name = " Limma analysis " + str(analysisDetail.id ), description = " Limma analysis " + str(analysisDetail.id ), submittedBy = request.user, submittedOn= datetime.datetime.now(), jobStatusCode = queueJobStatusCode, analysisDetail = analysisDetail, submittedJobType = analysisJobType)

    submittedJob.save()

    outputPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(dataFile.project.id) + "/Analysis_" + str(analysisDetail.id)

    #print " output path = " + str(outputPath)
    #print " file path = " + str(countsMatrixFilePath)
    #print " base plot path = " + str(basePlotPath)
    #print " listPlotFactorNames = " + str(listPlotFactorNames)

    #print " samples = " + str(samples)
    #print " factors = " + str(factors)
    #print " animals = " + str(animals)
    #print " listPlotFactors = " + str(listPlotFactors)
    #print " contrasts = " + str(contrasts)
    #print " decidetestsPValue = " + str(decidetestsPValue)
    #print " decidetestsLFC = " + str(decidetestsLFC)

    if not os.path.isdir(outputPath):
        os.mkdir(outputPath)

    designMatrixFilePath = outputPath + "/designMatrix.csv"
    contrastMatrixFilePath = outputPath + "/contrastMatrix.csv"

    designMatrixDf = pd.DataFrame(designMatrix, columns = matrixColumns)
    designMatrixDf.to_csv(designMatrixFilePath, index = False)

    contrastMatrixDf = pd.DataFrame(contrastMatrix, columns = contrasts)
    contrastMatrixDf["Levels"] = matrixColumns
    contrastMatrixDf.to_csv(contrastMatrixFilePath, index = "Levels")
    
    # save plots 
    
    plotFactorName = "plotMA" + "_Project_" + str(dataFile.project.id) + "_user_" + str(request.user) + "_Analysis_" + str(analysisDetail.id)

    analysisPlot = AnalysisPlot(analysisDetail = analysisDetail, name = "PlotMA", plotPath = settings.IMAGE_OUTPUT_FOLDER + "/plots/" + plotFactorName, plotFileName = plotFactorName)
    
    analysisPlot.save()

    for factorColumn in factorColumns:
        plotFactorName = "plotMDS_" + factorColumn + "_Project_" + str(dataFile.project.id) + "_user_" + str(request.user) + "_Analysis_" + str(analysisDetail.id)
        
        analysisPlot = AnalysisPlot(analysisDetail = analysisDetail, name = "PlotMDS_" + str(factorColumn), plotPath = settings.IMAGE_OUTPUT_FOLDER + "/plots/" + plotFactorName, plotFileName = plotFactorName)
        
        analysisPlot.save()

    for contrast in contrasts:

        analysisResultFile = AnalysisResultFile(analysisDetail = analysisDetail, name = "Result " + str(contrast), filePath = outputPath + "/" + contrast, resultFileName = contrast)
        analysisResultFile.save()
        
    #plotFactorName = "plotScatter" + "_Project_" + str(dataFile.project.id) + "_user_" + str(request.user) + "_Analysis_" + str(analysisDetail.id)

    #analysisPlot = AnalysisPlot(analysisDetail = analysisDetail, name = "PlotScatter", plotPath = settings.IMAGE_OUTPUT_FOLDER + "/plots/" + plotFactorName, plotFileName = plotFactorName)
    
    #analysisPlot.save()        

    #print ( (factorColumnValuesMap))

    startingColumn = dataFile.startingColumn
    
    if startingColumn == 0:
        
        startingColumn = DEFAULT_STARTING_COLUMN
    
    allContrasts = contrasts + allContrastStrings 
    
    print ( " %%%%%%%%%%% $$$$$$$$$ allContrasts $$$$$$$$$$ %%%%%%%%%%%% " + str(allContrasts) ) 

    ts.submitLimma.delay(countsMatrixFilePath, basePlotPath, outputPath, factors, factorColumns, factorColumnValuesMap, factorSetList, sampleXrefList, sampleNames, animals, contrasts, factorSetMap, submittedJob, dataFile.project.id, str(request.user) , analysisDetail.id, str(startingColumn) , dataFile.commaOrTabDelimitedFlag, allContrasts)

    #tsk.callLimmaTask(countsMatrixFilePath, basePlotPath, outputPath, factors, factorColumns, factorColumnValuesMap, factorSetList, sampleXrefList, sampleNames, animals, contrasts, submittedJob)

    #print " phenotype columns = " + str(phenotypeColumns)

    completedFlag = True

    if not submittedJob.completedTime:

        completedFlag = False

    #print " ---- completed flag !!!!!!! = " + str(completedFlag)

    return render_to_response('rnaseq/displaySubmittedJob.html', {
        "submittedJob":submittedJob,
        "completedFlag":completedFlag,
    },  RequestContext(request))

@login_required
def analyzeFileSelectColumns(request):

    dataFileId = request.POST.get("dataFileId",0 )

    phenotypeFileName = request.POST.get("phenotypeFileName","" )

    dataFile = DataFile.objects.get(pk = dataFileId)

    phenotypeFile = ''

    phenotypeColumnObjList = []

    phenotypeDataList = []

    columnTypes = ColumnType.objects.all()
    
    factorColumnType = ColumnType.objects.filter(name = "factor")[0]

    phenotypeRowValuesList = []
    phenotypeColumns = []
    
    phenotypeLines = []

    phenotypeFileId = 0

    try:

        phenotypeFileId = int(request.POST.get("phenotypeFileId","0" ) )

    except:
        pass

    if phenotypeFileId != 0 :

        phenotypeFile = DataFile.objects.get(pk = phenotypeFileId)

        phenotypeLines = open(settings.DATA_OUTPUT_FOLDER + "/Project_" + str(dataFile.project.id) + "/" + phenotypeFile.name, "r")

        phenotypeFileName = phenotypeFile.name

    else:

        phenotypeFile = request.FILES['datafilePath']

        if phenotypeFileName == '':

            phenotypeFileName = request.FILES['datafilePath'].name

        phenotypeData = phenotypeFile.read().decode()

        phenotypeLines = phenotypeData.split("\r")

    for index, phenotype in enumerate ( phenotypeLines ) :
        if index == 0:

            phenotypeColumns = phenotype.replace("\t","").replace("\n","").split(",")

            #print " columns = " + str(phenotypeColumns)

            for phenotypeColumn in phenotypeColumns:

                phenotypeColumnObj = PhenotypeColumnObj()

                phenotypeColumnObj.colName = phenotypeColumn

                phenotypeColumnObjList.append (phenotypeColumnObj)

            continue

        phenotypeRowValues = phenotype.replace("\t","").replace("\n","").split(",")

        phenotypeRowValuesList.append(phenotypeRowValues)

        phenotypeObjList = []

        for phenotypeRowValue in phenotypeRowValues :

            phenotypeObj = PhenotypeObj()

            phenotypeObj.colName = phenotypeRowValue

            phenotypeObjList.append (phenotypeObj)

        phenotypeDataList.append(phenotypeObjList)

    print ( " phenotypeRowValuesList shape = " + str(phenotypeRowValuesList)  )
    print ( " phenotypeColumns = " + str(len ( phenotypeColumns ) ) )
    
    df = pd.DataFrame(phenotypeRowValuesList, columns = phenotypeColumns)

    phenotypeColumnMap = {}

    for dfColumn in df.columns :
        
        phenotypeColumnMap [dfColumn] = list(set(df [dfColumn].tolist()))

    filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(dataFile.project.id)

    if phenotypeFileId == 0 :

        if not os.path.isdir( filePath ):
            os.mkdir(filePath)

        df.to_csv(filePath + "/" + str(phenotypeFileName), index = False )

        phenotypeFileType = FileType.objects.filter(name = "phenotypeFile")[0]

        phenotypeFile = DataFile ( name = phenotypeFileName , description = "Phenotype File", project = dataFile.project, filePath = filePath, fileType = phenotypeFileType)
        phenotypeFile.save()

    phenotypeFileDf = pd.DataFrame.from_csv(filePath + "/" + str(phenotypeFileName), index_col=False)             

    phenotypeFileObj = PhenotypeFileObj()

    phenotypeFileObj.fileColumns = phenotypeFileDf.columns

    phenotypeFileObj.fileRows = phenotypeFileDf.values.tolist()

    print (" map *** = " + str(phenotypeColumnMap))

    return render_to_response('rnaseq/analyzeFileSelectColumns.html', {

        "dataFile":dataFile,
        "columnTypes":columnTypes,
        "factorColumnType":factorColumnType,
        "phenotypeColumnObjList":phenotypeColumnObjList,
        "phenotypeDataList":phenotypeDataList,
        "phenotypeFile":phenotypeFile,
        "phenotypeColumnMap":phenotypeColumnMap,
        "phenotypeFileObj":phenotypeFileObj,
    },  RequestContext(request))

def fetchAnalysisParameters(request):

    robjects.r('library(Biobase)')
    robjects.r('library(statmod)')
    robjects.r('library(affy)')
    robjects.r('library(edgeR)')
    robjects.r('require(limma)')

    dataFileId = request.POST.get("dataFileId",0)

    phenotypeFilePath = request.POST.get("phenotypeFilePath","")

    phenotypeColumns = request.POST.getlist("phenotypeColumn")

    columnTypeIds = request.POST.getlist("columnTypeId")

    columnTypeIds = [int(x) for x in columnTypeIds  if x != '' ]

    #print "phenotypeColumns = " + str(phenotypeColumns)

    #print "columnTypeIds = " + str(columnTypeIds)

    phenotypeColumnObjList = []

    for index, columnTypeId in enumerate ( columnTypeIds ):

        #print " id = " + str(columnTypeId)

        if phenotypeColumns [index] != '':

            #print " for phenotypeColumns [index] = " + str(phenotypeColumns [index]) + " column type id = " + str(columnTypeId)

            columnType = ColumnType.objects.get(pk = int(columnTypeId))

            if columnType.name == "factor":

                phenotypeColumnObj = PhenotypeColumnObj()

                phenotypeColumnObj.colName = phenotypeColumns [index]
                phenotypeColumnObj.columnType = columnType

                phenotypeColumnObjList.append(phenotypeColumnObj)

    dataFile = DataFile.objects.get(pk = dataFileId)

    phenotypeFile = pd.DataFrame.from_csv(phenotypeFilePath)

    #print " columns = " + str(phenotypeFile.columns)

    factorSetList = []

    for phenotypeColumnObj in phenotypeColumnObjList:

        columnValues = phenotypeFile [phenotypeColumnObj.colName].tolist()

        columnValueList = list(columnValues)

        factorSetList.append(columnValueList)

    combinationStringList = [".".join(x) for x in zip (*factorSetList)]

    #print ":::: " + str(combinationStringList)

    rfactorList = robjects.StrVector(combinationStringList)

    robjects.globalenv["f"] = rfactorList

    #combinationStringList = [".".join(x) for x in combinationStringList]

    #print " combinationStringList *** " + str(combinationStringList)

    robjects.r('design.limma <-model.matrix(~0+f)')

    designMatrixR = numpy.array(robjects.globalenv["design.limma"])

    designMatrix = []

    for row in designMatrixR:

        designMatrix.append(numpy.array(row))

        #print " row = " +str(row[1])

    #print str(numpy.array(designMatrix))

    robjects.r('colnames(design.limma)<-levels(f)')

    robjects.r('columnNames <- levels(f)')

    matrixColumns = numpy.array(robjects.globalenv["columnNames"])

    matrixColumns = list(set(combinationStringList))

    #print "constrast = " + str(list(set(combinationStringList)))

    combinationStringList =  list(set(combinationStringList))

    contrasts = []

    contrastTuples = list(itertools.combinations(combinationStringList,2))

    contrasts = ["-".join(x) for x in contrastTuples]

    return contrasts

@login_required
def analyzeFileSelectFactors(request):
    
    try:

        dataFileId = request.POST.get("dataFileId",0)
    
        phenotypeFileId = request.POST.get("phenotypeFileId",0)
        
        phenotypeFile = DataFile.objects.get(pk = phenotypeFileId)
        
        phenotypeFileName = phenotypeFile.name
    
        phenotypeColumns = request.POST.getlist("phenotypeColumn")
        
        baselines = request.POST.getlist("baseline")
        
        print (" --- before baselines -- " + str(baselines))
        
        baselines = [x for x in baselines if x]
        
        print (" --- after baselines -- " + str(baselines))
    
        columnTypeIds = request.POST.getlist("columnTypeId")
    
        columnTypeIds = [int(x) for x in columnTypeIds  if x != '' ]
    
        phenotypeColumnObjList = []
    
        sampleColumn = ''
    
        for index, columnTypeId in enumerate ( columnTypeIds ):
    
            #print " id = " + str(columnTypeId)
    
            if phenotypeColumns [index] != '':
    
                #print " for phenotypeColumns [index] = " + str(phenotypeColumns [index]) + " column type id = " + str(columnTypeId)
    
                columnType = ColumnType.objects.get(pk = int(columnTypeId))
                
                print ( " column type = " + str(columnType) )                 
    
                if columnType.name == "factor":
    
                    phenotypeColumnObj = PhenotypeColumnObj()
    
                    phenotypeColumnObj.colName = phenotypeColumns [index]
                    phenotypeColumnObj.columnType = columnType
    
                    phenotypeColumnObjList.append(phenotypeColumnObj)
    
                elif columnType.name == "sample":
    
                    sampleColumn = phenotypeColumns [index]
                    
                    print ( " &&&& in sample column &&&& = " + str(sampleColumn) ) 
    
        print ( " &&&& AAAFFFTTTERRR in sample column &&&& = " + str(sampleColumn) ) 

        dataFile = DataFile.objects.get(pk = dataFileId)
    
        filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(dataFile.project.id)
    
        #print " path = " + str(phenotypeFileName)
    
        phenotypeFileDf = pd.DataFrame.from_csv(filePath + "/" + str(phenotypeFileName), index_col = False)
    
        factorSetList = []
        
        designFactorObjList = []
    
        for phenotypeColumnIndex, phenotypeColumnObj in enumerate ( phenotypeColumnObjList ):
    
            designFactorObj = DesignFactorObj()
            
            designFactorObj.designFactorName = phenotypeColumnObj.colName
            
            columnValueList = phenotypeFileDf [phenotypeColumnObj.colName].tolist()
    
            #columnValueList = list(columnValues)
            
            designFactorObj.designFactorName = phenotypeColumnObj.colName
            
            designFactorObj.designFactorBaseline = baselines[phenotypeColumnIndex]
            designFactorObj.designFactorValues = ",".join(list(set(columnValueList)))  
            
            designFactorObjList.append(designFactorObj)
    
            columnValueList = [x.replace(" ","_").replace("(","").replace(")","") for x in columnValueList]
    
            factorSetList.append(columnValueList)
    
        factors = [".".join(x) for x in zip (*factorSetList)]
    
        print (" factors 1111 = " + str(factorSetList) )
    
        DESIGN_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/make_design_matrix.R'); design_matrix")
    
        designMatrixR = numpy.array(DESIGN_FN( robjects.StrVector(factors)))
    
        #print " designMatrix = " + str(designMatrixR)
    
        LEVELS_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/find_levels.R'); find_levels")
    
        matrixColumns = numpy.array(LEVELS_FN( robjects.StrVector(factors)))
    
        #print " matrix columns = " + str(matrixColumns)
    
        designMatrix = []
    
        for row in designMatrixR:
    
            #row = numpy.array(row)
    
            row = [int(x) for x in numpy.array(row)]
    
            designMatrix.append(numpy.array(row))
    
        factors =  list(set(factors))
        
        print  ( " factors are " + str(factors) ) 
        
        contrasts = []
    
        contrastTuples = list(itertools.permutations(factors,2))    
        
        contrastsFinal = []
        
        foldChangeConstrasts = []
        
        singleFirstContrasts = []
        singleSecondContrasts = []          
        
        for contrast in contrastTuples:
            
            #contrastParts = contrastTuples[1].split("-")
            
            contrast1 = contrast[0]
            contrast2 = contrast[1]
            
            print (" for contrast " + str(contrast1) + " : " + str(contrast2))
            
            if contrast1.find(".") != -1 and contrast2.find(".") != -1 :
            
                contrast1Factors = contrast1.split(".")
                contrast2Factors = contrast2.split(".")
                
                contrast1FactorFirst = contrast1Factors[0]
                contrast1FactorSecond = contrast1Factors[1]
                
                contrast2FactorFirst = contrast2Factors[0]
                contrast2FactorSecond = contrast2Factors[1]
        
                print (" first contrast " + str(contrast1FactorFirst) + " : " + str(contrast2FactorFirst))
                print (" second contrast " + str(contrast1FactorSecond) + " : " + str(contrast2FactorSecond))
    
                if contrast2FactorSecond in baselines and contrast1FactorSecond not in baselines:   
                    
                    if contrast1FactorFirst == contrast2FactorFirst:
                       
                        contrastsFinal.append(contrast)
                        
                        foldChangeConstrasts.append(contrast)
    
                elif contrast2FactorSecond not in baselines and contrast1FactorSecond not in baselines:             
                       
                    if contrast1FactorFirst != contrast2FactorFirst and contrast2FactorFirst in baselines:
                       
                        contrastsFinal.append(contrast)
                   
                singleFirstContrasts = [x[0] for x in contrastsFinal]
                singleSecondContrasts = [x[1] for x in contrastsFinal]                        

            else:

                contrastsFinal.append([contrast1, contrast2])

                singleFirstContrasts.append(contrast1)
                singleSecondContrasts.append(contrast2)
    
        print ( " ***** contrasts %%%%% " + str(contrastsFinal) )
        
        #singleFirstContrasts = [x[0] for x in contrastsFinal]
        #singleSecondContrasts = [x[1] for x in contrastsFinal]
    
        contrasts = ["-".join(x) for x in contrastsFinal]
    
        print ( " ***** contrasts 33333 " + str(contrasts) )
        
        singleContrasts = list(zip(contrasts, singleFirstContrasts, singleSecondContrasts))
        
        foldChangeConstrasts = ["-".join(x) for x in foldChangeConstrasts]
    
        otherContrasts = list(itertools.permutations(foldChangeConstrasts,2))
        
        doubleFirstContrasts = [x for (x,y) in otherContrasts]
        doubleSecondContrasts = [y for (x,y) in otherContrasts]
    
        otherContrasts = ["(" + x + ")-(" + y + ")" for (x,y) in otherContrasts]

        doubleContrasts = list(zip(otherContrasts, doubleFirstContrasts, doubleSecondContrasts) )

        sampleNames = phenotypeFileDf [sampleColumn].tolist()

        print ( " sampleColumn ********** = " + str(sampleColumn ) + " sampleNames = " + str(sampleNames ) ) 
    
        numSamples = range(len(sampleNames))
    
        filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(dataFile.project.id)
    
        print (" in comma " + filePath + "/" + str(dataFile.name) + ".csv flag = " + str(dataFile.commaOrTabDelimitedFlag) )
    
        if dataFile.commaOrTabDelimitedFlag:
    
            contrastMatrixFileDf = pd.DataFrame.from_csv(filePath + "/" + str(dataFile.name) + ".csv")
            
            print (" in comma ")
    
        else:
            
            contrastMatrixFileDf = pd.DataFrame.from_csv(filePath + "/" + str(dataFile.name) + ".csv", sep="\t")
            
            print (" NOT in comma " + str(contrastMatrixFileDf.columns))
            
        startingColumn = dataFile.startingColumn
            
        if startingColumn == 0:
            
            startingColumn = DEFAULT_STARTING_COLUMN
            
        dataMatrixColumns = contrastMatrixFileDf.columns[startingColumn -1:]
        
        print ("dataMatrixColumns = " + str(dataMatrixColumns))
    
        matrixColumnMatchObjList = []
    
        print (" data matrix columns = " + str(dataMatrixColumns))

        print (" sampleNames = " + str(sampleNames))
    
        for sampleName in sampleNames:
    
            matrixColumnMatchObj = MatrixColumnMatchObj()
    
            matrixColumnMatchObj.sampleNames = sampleNames
            matrixColumnMatchObj.dataMatrixColumns = dataMatrixColumns
    
            matrixColumnMatchObj.selectedSampleName = sampleName
    
            #print " sample name = " + str(sampleName)
    
            matchColumns = [x for x in dataMatrixColumns if sampleName in x]
    
            if len(matchColumns) > 0:
    
                matchColumn = matchColumns[0]
    
                matrixColumnMatchObj.selectedMatrixColumn = matchColumn
    
            matrixColumnMatchObjList.append(matrixColumnMatchObj)
            
        #print (" ***************** singleContrasts " + str ( [(x,y,z) for (x,y,z) in singleContrasts]  ) )
        #print (" ***************** doubleContrasts " + str([(x,y,z) for (x,y,z) in doubleContrasts]) )
    
    except:
        
        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/analyzeFileSelectFactors.html', {

        "dataFile":dataFile,
        "designMatrix":designMatrix,
        "matrixColumns":matrixColumns,
        
        "baselines":baselines,
        "designFactorObjList":designFactorObjList,
        "phenotypeFile":phenotypeFile,
        "phenotypeColumns":phenotypeColumns,
        "columnTypeIds":columnTypeIds,

        "singleContrasts":singleContrasts,        
        "doubleContrasts":doubleContrasts,

        "matrixColumnMatchObjList":matrixColumnMatchObjList,

    },  RequestContext(request))

@login_required
def analyzeFileShowContrastMatrix(request):

    try:

        datafileId = request.POST.get("dataFileId",0 )

        datafile = DataFile.objects.get(pk = datafileId)

        phenotypeFileName = request.POST.get("phenotypeFileName","")

        phenotypeColumns = request.POST.getlist("phenotypeColumn" )
        columnTypeIds = request.POST.getlist("columnTypeId" )

        #print " phenotypeColumns = ***** = " + str(phenotypeColumns)

        columnTypeIds = request.POST.getlist("columnTypeId")

        contrasts = request.POST.getlist("contrastString")

        baseline = request.POST.getlist("baseline")

        #print " contrastStrings = " + str(contrasts)

        #decidetestsLFC = DECIDE_TESTS_LFC

        #decidetestsPValue = DECIDE_TESTS_PVALUE

        columnTypeIds = [int(x) for x in columnTypeIds  if x != '' ]

        phenotypeColumnObjList = []

        sampleColumn = ''

        for index, columnTypeId in enumerate ( columnTypeIds ):

            if phenotypeColumns [index] != '':

                columnType = ColumnType.objects.get(pk = int(columnTypeId))

                if columnType.name == "factor":

                    phenotypeColumnObj = PhenotypeColumnObj()

                    phenotypeColumnObj.colName = phenotypeColumns [index]
                    phenotypeColumnObj.columnType = columnType

                    phenotypeColumnObjList.append(phenotypeColumnObj)

                elif columnType.name == "sample":

                    sampleColumn = phenotypeColumns [index]

        filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(datafile.project.id)

        phenotypeFile = pd.DataFrame.from_csv(filePath + "/" + str(phenotypeFileName), index_col = None)

        #print str(phenotypeFile)

        factorSetList = []

        listPlotFactors = []

        for phenotypeColumnObj in phenotypeColumnObjList:

            #print " column is " + str (phenotypeColumnObj.colName) + " col name = " + str(phenotypeColumnObj.colName) + " column type name " + str(columnType.name)

            columnValues = phenotypeFile [phenotypeColumnObj.colName].tolist()

            columnValueList = list(columnValues)

            if phenotypeColumnObj.columnType.name == "factor":

                columnValueList = [x.replace(" ","_").replace("(","").replace(")","") for x in columnValueList]

                factorSetList.append(columnValueList)

        factors = [".".join(x) for x in zip (*factorSetList)]

        #print " factors = " + str(factors)

        DESIGN_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/make_design_matrix.R'); design_matrix")

        designMatrixR = numpy.array(DESIGN_FN( robjects.StrVector(factors), baseline))

        #print " designMatrix = " + str(designMatrixR)

        LEVELS_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/find_levels.R'); find_levels")

        matrixColumns = numpy.array(LEVELS_FN( robjects.StrVector(factors), baseline))

        #print " matrix columns = " + str(matrixColumns)

        designMatrix = []

        for row in designMatrixR:

            row = [int(x) for x in numpy.array(row)]

            designMatrix.append(numpy.array(row))

        CONTRASTS_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/make_contrasts.R'); contrasts_matrix")

        #print " contrastMatrix = " + str(contrasts)

        contrastMatrixR = numpy.array(CONTRASTS_FN( robjects.StrVector(factors), baseline, robjects.StrVector(contrasts)))

        #print " contrastMatrix = " + str(contrastMatrixR)

        contrastMatrix = []

        contrastMatrixRowObjList = []

        for rowIndex, row in enumerate ( contrastMatrixR ) :

            row = [int(x) for x in numpy.array(row)]

            contrastMatrix.append(numpy.array(row))

            #print " adding row " + str(row)

            contrastMatrixRowObj = ContrastMatrixRowObj()

            contrastMatrixRowObj.contrastLevel = matrixColumns [rowIndex]

            contrastMatrixRowObj.contrastMatrixRow = numpy.array(row)

            contrastMatrixRowObjList.append(contrastMatrixRowObj)
            #self.contrastLevel = ''
            #self.contrastMatrixRow = []

        contrastMatrixColumns = contrasts

        matrixColumnMatchObjList = []

        sampleNames = phenotypeFile [sampleColumn].tolist()

        numSamples = range(len(sampleNames))

        for sampleIndex, sampleName in enumerate(sampleNames):

            matrixColumnMatchObj = MatrixColumnMatchObj()

            sampleNameValue = request.POST.get("sampleName-" + str(sampleIndex),"" )

            #print " sample name value = " + str(sampleNameValue) + " for : sampleName-" + str(sampleIndex)

            matchColumnValue = request.POST.get("dataMatrixColumn-" + str(sampleIndex),"" )

            #print " match column value = " + str(matchColumnValue) + " for : sampleName-" + str(sampleIndex)

            matrixColumnMatchObj.selectedSampleName = sampleNameValue
            matrixColumnMatchObj.selectedMatrixColumn = matchColumnValue

            matrixColumnMatchObjList.append(matrixColumnMatchObj)

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/analyzeFileShowContrastMatrix.html', {

        "datafile":datafile,
        "designMatrix":designMatrix,

        "matrixColumns":matrixColumns,
        
        "baseline":baseline,        

        "contrasts":contrasts,
        "contrastMatrix":contrastMatrix,
        "contrastMatrixColumns":contrastMatrixColumns,
        "phenotypeFileName":phenotypeFileName,
        "phenotypeColumns":phenotypeColumns,
        "columnTypeIds":columnTypeIds,

        "contrastMatrixRowObjList":contrastMatrixRowObjList,

        "matrixColumnMatchObjList":matrixColumnMatchObjList,

    },  RequestContext(request))

@login_required
def scatterPlotSubmit(request):

    #print " IN SCATTER !!!!!!!! "

    try:

        analysisResultFilterObj = getAnalysisResultFilterObj(request)

        analysisDetailId = request.POST.get("analysisDetailId",0 )
        analysisDetail = AnalysisDetail.objects.get ( pk = analysisDetailId )
        combinationString = analysisDetail.combinationString

        genesUp = []
        genesDown = []

        genesUp = request.POST.getlist("geneUp")
        genesDown = request.POST.getlist("geneDown")

        #print " genes up are " + str ( genesUp )
        #print " genes down are " + str ( genesDown )

        dataFile = open( settings.PROJECT_BASE_FOLDER + "/webBrainrnaseq/expdata_filtered_final_" + combinationString + ".csv" ,  "r" )

        index = 0

        geneExpressionScatterObjList = []

        upMarkedGeneExpressionScatterObjList = []

        downMarkedGeneExpressionScatterObjList = []

        for index, line in enumerate ( dataFile ):

            if index == 0:
                continue

            if analysisResultFilterObj.numRecordsToDisplay != 0 and index > analysisResultFilterObj.numRecordsToDisplay + 1:
                break

            line = line.replace("\"","").replace("\r","").replace("\n","")

            data = line.split(",")

            if data[0] == '':
                break

            CPU_IN_values = [data[0], data[2], data[4]]
            CPU_IP_values = [data[1], data[3], data[5]]

            NAC_IN_values = [data[6], data[8], data[10]]
            NAC_IP_values = [data[7], data[9], data[11]]

            CPU_IN_values = [float(x) for x in CPU_IN_values]
            CPU_IP_values = [float(x) for x in CPU_IP_values]

            NAC_IN_values = [float(x) for x in NAC_IN_values]
            NAC_IP_values = [float(x) for x in NAC_IP_values]

            CPU_IN_value = numpy.mean(CPU_IN_values)
            CPU_IP_value = numpy.mean(CPU_IP_values)

            NAC_IN_value = numpy.mean(NAC_IN_values)
            NAC_IP_value = numpy.mean(NAC_IP_values)

            if combinationString == "NAC_IP_vs_NAC_IN":

                foldChangeValue1 = NAC_IP_value
                foldChangeValue2 = NAC_IN_value

            elif combinationString == "CPU_IP_vs_NAC_IP":

                foldChangeValue1 = CPU_IP_value
                foldChangeValue2 = NAC_IP_value

            elif combinationString == "CPU_IP_vs_CPU_IN":

                foldChangeValue1 = CPU_IP_value
                foldChangeValue2 = CPU_IN_value

            #print " compare " + str(abs(log(float(foldChangeValue1)/float(foldChangeValue2))) ) + " and " + str( analysisResultFilterObj.foldChangeCutOff )

            #print " compare " + str(float(foldChangeValue1)/float(foldChangeValue2)) + " and " + str( analysisResultFilterObj.foldChangeCutOff )

            if analysisResultFilterObj.foldChangeCutOff != 0 and abs(log(float(foldChangeValue1)/float(foldChangeValue2))) < analysisResultFilterObj.foldChangeCutOff:
                continue

            geneExpressionScatterObj = GeneExpressionScatterObj()

            geneExpressionScatterObj.gene = data[12]

            geneExpressionScatterObj.log2FoldChangeAvg1 = log(foldChangeValue1)
            geneExpressionScatterObj.log2FoldChangeAvg2 = log(foldChangeValue2)

            geneExpressionScatterObjList.append (geneExpressionScatterObj)

            arrowSize = 1

            ax = 60
            ay = -90

            if geneExpressionScatterObj.gene in genesUp:

                #print " IN UP fold change value 1 = " + str (foldChangeValue1) + " 2 = " + str(foldChangeValue2) + " gene " + str(data[12])

                geneExpressionScatterObj.arrowSize = arrowSize

                geneExpressionScatterObj.ax = ax
                geneExpressionScatterObj.ay = ay

                arrowSize = arrowSize + .2
                ax = ax + 1
                ay = ay - 1

                upMarkedGeneExpressionScatterObjList.append (geneExpressionScatterObj)

            if geneExpressionScatterObj.gene in genesDown:

                #print " IN DOWN fold change value 1 = " + str (foldChangeValue1) + " 2 = " + str(foldChangeValue2) + " gene " + str(data[12])

                geneExpressionScatterObj.arrowSize = arrowSize

                geneExpressionScatterObj.ax = ax
                geneExpressionScatterObj.ay = ay

                arrowSize = arrowSize + .2
                ax = ax - 1
                ay = ay + 1

                downMarkedGeneExpressionScatterObjList.append (geneExpressionScatterObj)

        #print " geneExpressionScatterObjList " + str ([(x.gene, x.log2FoldChangeAvg1, x.log2FoldChangeAvg2 ) for x in geneExpressionScatterObjList] )
    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/scatterplotSubmit.html', {
        'geneExpressionScatterObjList':geneExpressionScatterObjList,
        'upMarkedGeneExpressionScatterObjList':upMarkedGeneExpressionScatterObjList,
        'downMarkedGeneExpressionScatterObjList':downMarkedGeneExpressionScatterObjList,
        'analysisResultFilterObj':analysisResultFilterObj,
    },  RequestContext(request))

@login_required
def correlationPlotSubmit(request):

    #print " IN SCATTER !!!!!!!! "

    try:

        combinationString = request.POST.get("combinationString",0 )

        geneExpressionScatterObjList = []

        upMarkedGeneExpressionScatterObjList = []

        downMarkedGeneExpressionScatterObjList = []

        for index, line in enumerate ( dataFile ):

            if index == 0:
                continue

            #if index >1300:
                #break

            line = line.replace("\"","").replace("\r","").replace("\n","")

            data = line.split(",")

            if data[0] == '':
                break

            CPU_IN_values = [data[0], data[2], data[4]]
            CPU_IP_values = [data[1], data[3], data[5]]

            NAC_IN_values = [data[6], data[8], data[10]]
            NAC_IP_values = [data[7], data[9], data[11]]

            CPU_IN_values = [float(x) for x in CPU_IN_values]
            CPU_IP_values = [float(x) for x in CPU_IP_values]

            NAC_IN_values = [float(x) for x in NAC_IN_values]
            NAC_IP_values = [float(x) for x in NAC_IP_values]

            CPU_IN_value = numpy.mean(CPU_IN_values)
            CPU_IP_value = numpy.mean(CPU_IP_values)

            NAC_IN_value = numpy.mean(NAC_IN_values)
            NAC_IP_value = numpy.mean(NAC_IP_values)

            if combinationString == "NAC_IP_vs_NAC_IN":

                foldChangeValue1 = NAC_IP_value
                foldChangeValue2 = NAC_IN_value

            elif combinationString == "CPU_IP_vs_NAC_IP":

                foldChangeValue1 = CPU_IP_value
                foldChangeValue2 = NAC_IP_value

            elif combinationString == "CPU_IP_vs_CPU_IN":

                foldChangeValue1 = CPU_IP_value
                foldChangeValue2 = CPU_IN_value

            geneExpressionScatterObj = GeneExpressionScatterObj()

            geneExpressionScatterObj.gene = data[12]

            geneExpressionScatterObj.log2FoldChangeAvg1 = log(foldChangeValue1)
            geneExpressionScatterObj.log2FoldChangeAvg2 = log(foldChangeValue2)

            geneExpressionScatterObjList.append (geneExpressionScatterObj)

            arrowSize = 1

            ax = 60
            ay = -90

            if geneExpressionScatterObj.gene in genesUp:

                #print " IN UP fold change value 1 = " + str (foldChangeValue1) + " 2 = " + str(foldChangeValue2) + " gene " + str(data[12])

                geneExpressionScatterObj.arrowSize = arrowSize

                geneExpressionScatterObj.ax = ax
                geneExpressionScatterObj.ay = ay

                arrowSize = arrowSize + .2
                ax = ax + 1
                ay = ay - 1

                upMarkedGeneExpressionScatterObjList.append (geneExpressionScatterObj)

            if geneExpressionScatterObj.gene in genesDown:

                #print " IN DOWN fold change value 1 = " + str (foldChangeValue1) + " 2 = " + str(foldChangeValue2) + " gene " + str(data[12])

                geneExpressionScatterObj.arrowSize = arrowSize

                geneExpressionScatterObj.ax = ax
                geneExpressionScatterObj.ay = ay

                arrowSize = arrowSize + .2
                ax = ax - 1
                ay = ay + 1

                downMarkedGeneExpressionScatterObjList.append (geneExpressionScatterObj)

        #print " geneExpressionScatterObjList " + str ([(x.gene, x.log2FoldChangeAvg1, x.log2FoldChangeAvg2 ) for x in geneExpressionScatterObjList] )
    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/scatterplotSubmit.html', {
        'geneExpressionScatterObjList':geneExpressionScatterObjList,
        'upMarkedGeneExpressionScatterObjList':upMarkedGeneExpressionScatterObjList,
        'downMarkedGeneExpressionScatterObjList':downMarkedGeneExpressionScatterObjList,
    },  RequestContext(request))

@login_required
def brainConnectivity(request):

    try:

        #print " in connectivity "

        cpuBrainRegion = BrainRegion.objects.filter ( name = 'CPU')
        nacBrainRegion = BrainRegion.objects.filter ( name = 'NAC')

        connectivityMatrix = []

        connectivityValueObjList = []

        projectionRegions = ['CPU-R','NAC-R','CPU-L','NAC-L']

        targetRegions = []

        workbook = openpyxl.load_workbook(filename = "connectivity_final_xls.xlsx" ,  use_iterators = True)

        worksheets = workbook.get_sheet_names()

        index = 0

        for worksheet in workbook :

            for data in worksheet.iter_rows():

                if index == 0:
                    index = index + 1
                    continue

                #if index >15:
                    #break

                if data[0].value == None:
                    break

                dataValue = [x.value for x in data[1:5]]

                regionName = data[0].value

                brainRegionList = BrainRegion.objects.filter (name = regionName )

                brainRegionDescription = regionName

                brainRegion = ''

                if len ( brainRegionList ) > 0 :

                    brainRegionDescription = brainRegionList[0].description

                    brainRegion = brainRegionList[0]

                connectivityValueObj = ConnectivityValueObj()

                connectivityValueObj.targetBrainRegion = brainRegion

                connectivityList = []

                #print " ********* data line = " + str ( index ) + " value " + str (dataValue)

                try:

                    connectivityList = [round(math.log(float(x)),8) for x in dataValue]

                except:
                    pass

                #print " after data = " + str (connectivityList)

                if len (connectivityList)> 0:

                    connectivityMatrix.append (connectivityList)

                    connectivityValueObj.connectivityListFull = connectivityList

                    connectivityValueObjList.append (connectivityValueObj)

                    targetRegions.append ( brainRegionDescription  + "-" + str(index))

                index = index + 1

        connectivityMatrix = array (connectivityMatrix)
        connectivityMatrix = connectivityMatrix.transpose()

        #print " shape " + str (connectivityMatrix.shape)
        #print " connectivityMatrix = " + str (connectivityMatrix)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/brainConnectivity.html', {
        "connectivityMatrix":connectivityMatrix,
        "connectivityValueObjList":connectivityValueObjList,
        "targetRegions":targetRegions,
        "projectionRegions":projectionRegions,
    },  RequestContext(request))

@login_required
def uploadFile(request):

    dataFiles = DataFile.objects.all()

    return render_to_response('rnaseq/listProjects.html', {
        "dataFiles":dataFiles,
    },  RequestContext(request))

@login_required
def listFiles(request):

    projectId = request.POST.get("projectId",0 )

    #print " project = " + str(projectId)

    project = Project.objects.get(pk = projectId)

    contrastMatrixFileType = FileType.objects.filter(name = "contrastMatrix")[0]

    dataFiles = DataFile.objects.filter ( project = project, fileType = contrastMatrixFileType )

    return render_to_response('rnaseq/listFiles.html', {
        "dataFiles":dataFiles,
        "project":project,
    },  RequestContext(request))

@login_required
def submittedJobs(request):

    submittedJobs = []

    if request.user.is_superuser:
        submittedJobs = SubmittedJob.objects.all()
    else:
        submittedJobs = SubmittedJob.objects.filter(submittedBy = request.user)    
    
    submittedJobObjList = []
    
    for submittedJob in submittedJobs:
        
        submittedJobObj = SubmittedJobObj()
        
        submittedJobObj.submittedJob = submittedJob
        
        completedFlag = True

        #print " ---- completed flag = " + str(completedFlag)

        if not submittedJob.completedTime:

            completedFlag = False  
            
        submittedJobObj.completedFlag = completedFlag
        
        submittedJobObjList.append(submittedJobObj)
        
        print (submittedJobObjList)

    return render_to_response('rnaseq/submittedJobs.html', {
        "submittedJobObjList":submittedJobObjList,
    },  RequestContext(request))

@login_required
def listProjects(request):

    projectObjList = []

    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(user = request.user)

    contrastMatrixFileType = FileType.objects.filter(name = "contrastMatrix")[0]

    for project in projects:

        projectObj = ProjectObj()
        
        projectObj.project = project
    
        dataFiles = DataFile.objects.filter ( project = project, fileType = contrastMatrixFileType )        
        
        projectObj.numContrastMatrixFiles = len(dataFiles)
        
        projectObjList.append(projectObj)
    
    return render_to_response('rnaseq/listProjects.html', {
        "projectObjList":projectObjList,
    }, RequestContext(request))

@login_required
def listSubmittedJobs(request):

    submittedJobs = []

    if request.user.is_superuser:
        submittedJobs = SubmittedJob.objects.all()
    else:
        submittedJobs = SubmittedJob.objects.filter(submittedBy = request.user)      

    submittedJobObjList = []
    
    for submittedJob in submittedJobs:
        
        submittedJobObj = SubmittedJobObj()
        
        submittedJobObj.submittedJob = submittedJob
        
        completedFlag = True

        #print " ---- completed flag = " + str(completedFlag)

        if not submittedJob.completedTime:

            completedFlag = False  
            
        submittedJobObj.completedFlag = completedFlag
        
        submittedJobObjList.append(submittedJobObj)
        
        #print (submittedJobObjList)    

    return render_to_response('rnaseq/submittedJobs.html', {
        "submittedJobObjList":submittedJobObjList,
    }, RequestContext(request))

@login_required
def listAnalysisHeaders(request):

    analysisHeaders = AnalysisHeader.objects.all()

    return render_to_response('rnaseq/listAnalysisHeaders.html', {
        "analysisHeaders":analysisHeaders,
    },  RequestContext(request))

#@login_required
#def listAnalysisDetails(request):

    ##analysisHeaderId = request.POST.get("analysisHeaderId",0 )

    ##analysisHeader = AnalysisHeader.objects.get(pk = analysisHeaderId)

    ##analysisDetails = AnalysisDetail.objects.filter(analysisHeader = analysisHeader)

    #return render_to_response('rnaseq/listAnalysisDetails.html', {
        ##"analysisDetails":analysisDetails,
    #},  RequestContext(request))

@login_required
def displayFileDetails(request):

    try:

        dataFileId = request.POST.get("dataFileId",0 )

        dataFile = DataFile.objects.get ( pk = dataFileId)

        sampleDetailList = SampleDetail.objects.filter (dataFile = dataFile)

        sampleData = []

        for sampleDetail in sampleDetailList:
            
            sampleData.append([sampleDetail.sampleName, sampleDetail.numberOfInputReads, sampleDetail.sampleName + " (" + str(sampleDetail.numberOfInputReads) + " reads)",sampleDetail.pctUniquelyMappedReads,sampleDetail. pctMappedMultipleLoci,sampleDetail.pctUnMappedTooManyLoci,sampleDetail.pctUnMappedTooManyMismatches,sampleDetail.pctUnMappedTooShort,sampleDetail.pctUnMappedOther])
            
        sampleDf = pd.DataFrame(sampleData, columns = ["sampleName","numberOfInputReads", "sampleNameDesc", "pctUniquelyMappedReads", "pctMappedMultipleLoci","pctUnMappedTooManyLoci", "pctUnMappedTooManyMismatches","pctUnMappedTooShort","pctUnMappedOther"], index = None)         
            
        print (sampleDf)
        
        barplot = Bar(sampleDf,
                  values=blend("pctUniquelyMappedReads", "pctMappedMultipleLoci","pctUnMappedTooManyLoci", "pctUnMappedTooManyMismatches","pctUnMappedTooShort","pctUnMappedOther", name='percentages', labels_name='percentage'),
                  label=cat(columns='sampleNameDesc', sort=False),
                  stack=cat(columns='percentage', sort=False),
                  color=color(columns='percentage', palette=['SaddleBrown', 'red', 'Goldenrod','Silver','blue','green','yellow'],
                              sort=False),
                  legend='bottom_right',
                  title="Percentages",
                  tooltips=[('percentage', '@percentage'), ('sample', '@sampleNameDesc'), ])
        
        
        
        plotPath = settings.IMAGE_OUTPUT_FOLDER + "/sampleDetail.png"
        
        barPlotScript, barPlotDiv = components(barplot)
        
        plt.savefig(plotPath)     
        
        #barplot.plt.savefig(settings.IMAGE_OUTPUT_FOLDER + "/sampleDetail.png")   

    except:
        traceback.print_exc(file=sys.stdout)
        messages.add_message(request, messages.ERROR, 'Error occurred while fetching details for data file id' + str(dataFileId) )

    return render_to_response('rnaseq/displayFileDetails.html', {
        "dataFile":dataFile,
        #"geneObjList":geneObjList,
        "sampleDetailList":sampleDetailList,
        "barPlotScript": barPlotScript,
        "barPlotDiv": barPlotDiv,
    },  RequestContext(request))

@login_required
def fetchAnalysisParameterObj(request):

    combinationObjList = []

    try:

        #comparisonMethodDifference = ComparisonMethod.objects.filter (name = "Difference")[0]
        #comparisonMethodFoldChange = ComparisonMethod.objects.filter (name = "Fold Change")[0]

        for combinationNum in range ( NUM_COMPARISONS):

            combinationObj = CombinationObj()

            combinationObj.combinationNum = combinationNum

            combinationObj.combination1String = request.POST.get("combination1String-" + str(combinationNum),False )
            combinationObj.combination2String = request.POST.get("combination2String-" + str(combinationNum),False )

            if not combinationObj.combination1String or not combinationObj.combination2String:
                continue

            combinationString = combinationObj.combination1String + "_vs_" + combinationObj.combination2String
            combinationObj.combinationString = combinationString

            combinationObj.comparisonMethod = comparisonMethodDifference
            if combinationObj.combination1String.find("-") != -1 and combinationObj.combination2String.find("-") != -1:
                combinationObj.comparisonMethod = comparisonMethodFoldChange

            foldChangeCutOff = 0

            try:
                foldChangeCutOff = request.POST.get("foldChangeCutOff-" + str(combinationNum),0 )
                foldChangeCutOff = float (foldChangeCutOff)
            except:
                foldChangeCutOff = 0
                pass

            pValueCutOff = 0

            try:
                pValueCutOff = request.POST.get("pValueCutOff-" + str(combinationNum),0 )
                pValueCutOff = float (pValueCutOff)
            except:
                pValueCutOff = 0
                pass

            testStatGreaterThanZero = False

            try:
                testStatGreaterThanZeroString = request.POST.get("testStatGreaterThanZero-" + str(combinationNum),0 )

                if testStatGreaterThanZeroString == "1":
                    testStatGreaterThanZero = True
            except:
                testStatGreaterThanZero = False
                pass

            combinationObj.foldChangeCutOff = foldChangeCutOff
            combinationObj.pValueCutOff = pValueCutOff

            topTableAdjustMethod = AdjustMethod.objects.filter ( name = 'BH')[0]

            try:
                topTableAdjustMethodId = request.POST.get("topTableAdjustMethodId-" + str(combinationNum),False )
                topTableAdjustMethodId = float (topTableAdjustMethodId)
                topTableAdjustMethod = AdjustMethod.objects.get ( pk = topTableAdjustMethodId)
            except:
                pass

            combinationObj.topTableAdjustMethod = topTableAdjustMethod

            #print " adding parameter combination num " + str (combinationNum) + " obj 1 = " + str (combinationObj.combination1String) + " 2 = " + str (combinationObj.combination2String)
            #print " fold change " + str ( foldChangeCutOff ) +  " p value = " + str (pValueCutOff) + " top table adjust method " + str(combinationObj.topTableAdjustMethod)  + " testStatGreaterThanZero " + str (testStatGreaterThanZero)

            combinationObjList.append ( combinationObj )

    except:
        traceback.print_exc(file=sys.stdout)

    return combinationObjList

@login_required
def sampleDetail(request):

    try:

        sampleDetailId = request.POST.get("sampleDetailId",0 )

        #print " sample detail id = " + str(sampleDetailId)

        sampleDetail = SampleDetail.objects.get ( pk = sampleDetailId)

        #shutil.copy(sampleDetail.qcQualiMapHTMLPath, "/Users/mitras/projects/webRNASeq/templates/rnaseq/.")
        #shutil.copy(sampleDetail.fastQcHTMLPath, "/Users/mitras/projects/webRNASeq/templates/rnaseq/.")

    except:
        traceback.print_exc(file=sys.stdout)
        messages.add_message(request, messages.ERROR, 'Error occurred while fetching details for sample detail id' + str(sampleDetailId) )

    return render_to_response('rnaseq/sampleDetail.html', {

        "sampleDetail" : sampleDetail,

    },  RequestContext(request))

@login_required
def addProject(request):

    try:

        projects = Project.objects.filter ( user = request.user)

    except:
        traceback.print_exc(file=sys.stdout)
        messages.add_message(request, messages.ERROR, 'Error occurred while fetching details for sample detail id' + str(sampleDetailId) )

    return render_to_response('rnaseq/addProject.html', {
        
        "projects" : projects , 

    },  RequestContext(request))

@login_required
def addDataFile(request):

    try:

        projectId = request.POST.get("projectId",0 )

        project = Project.objects.get(pk = projectId)
        
        startingColumn = DEFAULT_STARTING_COLUMN
        
        print (" starting = " + str(startingColumn) )

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/addDataFile.html', {

        "sampleDetail" : sampleDetail,
        "project" : project,
        "startingColumn":startingColumn,

    },  RequestContext(request))

@login_required
def submitAddProject(request):

    messages = []

    try:

        projectName = request.POST.get("projectName","" )
        projectDescription = request.POST.get("projectDescription","" )
        #startDate = request.POST.get("startDate","" )
        #endDate = request.POST.get("endDate","" )
        
        #startDateTime = datetime.datetime.now()
        #if startDate != '':
            #startDateTime = datetime.datetime.strptime(startDate, "%m/%d/%Y")

        #endDateTime = None
        #if endDate != '':
            #endDateTime = datetime.datetime.strptime(endDate, "%m/%d/%Y")

        #project = Project ( name = projectName, user = request.user, description = projectDescription, startDate = startDateTime, endDate = endDateTime )

        project = Project ( name = projectName, user = request.user, description = projectDescription )
        project.save()

        contrastMatrixFileType = FileType.objects.filter(name = "ContrastMatrix")[0]
        dataFiles = DataFile.objects.filter ( project = project, fileType = contrastMatrixFileType )

    except:
        traceback.print_exc(file=sys.stdout)
        messages.add_message(request, messages.ERROR, 'Error occurred while adding project' + str(sampleDetailId) )

    return render_to_response('rnaseq/listFiles.html', {
            "dataFiles":dataFiles,
            "project":project,
        },  RequestContext(request))

@login_required
def submitAddDataFile(request):

    project = ""

    try:

        projectId = request.POST.get("projectId",0 )

        project = Project.objects.get (pk = projectId)

        contrastFileType = FileType.objects.filter(name = "contrastMatrix")[0]
        qcZipFileType = FileType.objects.filter(name = "qcZipFile")[0]

        filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(projectId)

        if not os.path.isdir( filePath ):
            os.mkdir(filePath)

        dataFileName = request.POST.get("dataFileName","" )
        dataFileDescription = request.POST.get("dataFileDescription","" )
        
        startingColumn = request.POST.get("startingColumn",0 )
        
        if startingColumn == 0:
            
            startingColumn == DEFAULT_STARTING_COLUMN
        
        commaOrTabDelimitedFlag = False
        
        commaOrTabDelimited = request.POST.get("commaOrTabDelimited","0" ) 
        
        if commaOrTabDelimited == "1":
            
            commaOrTabDelimitedFlag= True
        
        # counts matrix
        dataFile = request.FILES["countsMatrix"]

        #print " ***** before read counts matrix "
        
#, dialect=csv.excel_tab        

        data = [row for row in csv.reader(dataFile.read().decode().split("\n"), dialect=csv.excel_tab)]

        dataList = []

        outputFile = open(filePath + "/" + str(dataFileName) +".csv", "w")

        for i, line in enumerate(data):

            if len(line) > 0:

                outputFile.write(",".join(line))
                outputFile.write("\n")

                #dataList.append(line[0].split("\t"))

        ##r = pe.get_records(file_type="xlsx", file_content=content)
        #print " ***** !!!!!! after read counts matrix "

        #df = pd.DataFrame(dataList)
        #df.to_csv(filePath + "/" + str(dataFileName) +".csv" , index = False, sep=',', header=None, quoting=csv.QUOTE_NONNUMERIC )

        contrastDataFile = DataFile ( name = dataFileName , description = dataFileDescription, project = project, filePath = filePath, fileType = contrastFileType, startingColumn = startingColumn, commaOrTabDelimitedFlag = commaOrTabDelimitedFlag)
        
        contrastDataFile.save()

        # load qc files if available
        
        try:

            # zip file
            qcFileZip = request.FILES["qcFilesZip"]
    
            #if qcFileZip.file is not None and zipfile.is_zipfile(qcFileZip.file):
    
            zfile = zipfile.ZipFile(qcFileZip)
    
            zfile.extractall(filePath )
            zfile.close()
    
            dataFile = DataFile ( name = qcFileZip , description = qcFileZip, project = project, filePath = filePath, fileType = qcZipFileType)
            dataFile.save()
    
            df = pd.DataFrame.from_csv(filePath + "/summary.csv")
    
            for index, datarow in df.iterrows():
    
                sampleNameString = str(index)
    
                numberOfInputReads = datarow["Number of input reads"]
                pctUniquelyMappedReads = datarow['Uniquely mapped reads %'].replace("%","")
                pctMappedMultipleLoci = datarow['% of reads mapped to multiple loci'].replace("%","")
    
                pctUnMappedTooManyLoci = datarow['% of reads mapped to too many loci'].replace("%","")
    
                pctUnMappedTooManyMismatches = datarow['% of reads unmapped: too many mismatches'].replace("%","")
                pctUnMappedTooShort = datarow['% of reads unmapped: too short'].replace("%","")
                pctUnMappedOther = datarow['% of reads unmapped: other'].replace("%","")
    
                totalAlignments = datarow['total alignments']
    
                sampleName = sampleNameString[:sampleNameString.find("_Log.final.out")]
    
                qcQualiMapHTMLPath = filePath + "/qc/" + sampleName + "_qualimap/qualimapReport.html"
                fastQcHTMLPath = filePath + "/qc/" + sampleName + "_fastqc/" + sampleName + "_fastqc.html"
    
                sampleDetail = SampleDetail ( sampleName = sampleName, dataFile = contrastDataFile, numberOfInputReads = numberOfInputReads, pctUniquelyMappedReads = pctUniquelyMappedReads, pctMappedMultipleLoci = pctMappedMultipleLoci, pctUnMappedTooManyLoci = pctUnMappedTooManyLoci, pctUnMappedTooManyMismatches = pctUnMappedTooManyMismatches ,  pctUnMappedTooShort = pctUnMappedTooShort  ,  pctUnMappedOther = pctUnMappedOther, totalAlignments = totalAlignments, qcQualiMapHTMLPath = qcQualiMapHTMLPath, fastQcHTMLPath= fastQcHTMLPath )
    
                sampleDetail.save()
                
        except:
            pass
            #traceback.print_exc(file=sys.stdout)
            #messages.add_message(request, messages.ERROR, 'Error occurred while fetching details for data file id' + str(dataFileId) )                

    #except:
        #traceback.print_exc(file=sys.stdout)
        ##messages.add_message(request, messages.ERROR, 'Error occurred while fetching details for sample detail id' + str(sampleDetailId) )

    #return render_to_response('rnaseq/submitAddDataFile.html', {
        #"project":project,
    #},  RequestContext(request))

        #sampleDetailList = SampleDetail.objects.filter (dataFile = dataFile)

        contrastMatrixFileType = FileType.objects.filter(name = "ContrastMatrix")[0]

        dataFiles = DataFile.objects.filter ( project = project, fileType = contrastMatrixFileType )

    except:
        traceback.print_exc(file=sys.stdout)
        messages.add_message(request, messages.ERROR, 'Error occurred while fetching details for data file id' + str(dataFileId) )

    return render_to_response('rnaseq/listFiles.html', {
        "project":project,
        "dataFiles":dataFiles,
    },  RequestContext(request))

def getAnalysisResultFilterObj(request):

    analysisResultFilterObj = AnalysisResultFilterObj()

    try:

        try:
            analysisResultFilterObj.numRecordsToDisplay = int(request.POST.get("numRecordsToDisplay",0 ))
        except:
            pass
        try:
            analysisResultFilterObj.topTableFoldChangeCutOff = float(request.POST.get("topTableFoldChangeCutOff",0 ))
        except:
            pass
        try:
            analysisResultFilterObj.foldChangeCutOff = float(request.POST.get("foldChangeCutOff",0 ))
        except:
            pass

        #print " num records = " + str (analysisResultFilterObj.numRecordsToDisplay)

        if analysisResultFilterObj.numRecordsToDisplay == 0 and analysisResultFilterObj.topTableFoldChangeCutOff == 0 and analysisResultFilterObj.foldChangeCutOff == 0:

            #print " default num records = " + str (DEFAULT_NUM_RECORDS_TO_DISPLAY)

            analysisResultFilterObj.numRecordsToDisplay = DEFAULT_NUM_RECORDS_TO_DISPLAY

    except:

        traceback.print_exc(file=sys.stdout)

    return analysisResultFilterObj

@login_required
def downloadDEGData(request):

    analysisDetailId = request.POST.get("analysisDetailId",0)
    
    analysisDetail = AnalysisDetail.objects.get ( pk = analysisDetailId ) 

    upDownFlag = request.POST.get("upDownFlag","0")
    contrastNum = request.POST.get("contrastNum",0)

    response = HttpResponse(content_type='text/csv')

    try:

        analysisDetail = AnalysisDetail.objects.get(pk = analysisDetailId)

        filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/Analysis_" + str(analysisDetail.id)

        analysisPlots = AnalysisPlot.objects.filter(analysisDetail = analysisDetail)

        analysisResultFiles = AnalysisResultFile.objects.filter(analysisDetail = analysisDetail)

        designFactors = DesignFactor.objects.filter(analysisDetail = analysisDetail)
        limmaContrasts = LimmaContrast.objects.filter(analysisDetail = analysisDetail)

        contrastObjList = []

        analysisDetailObj = AnalysisDetailObj()

        analysisDetailObj.analysisDetail = analysisDetail

        analysisDetailObj.designFactors = designFactors
        analysisDetailObj.limmaContrasts = limmaContrasts

        upDownFlagName = ""

        logFCValue = ""
        cutOffPValue = ""

        #print " upDownFlag = " + str(upDownFlag)

        for analysisIndex, analysisResultFile in enumerate(analysisResultFiles):

            #print " analysisIndex = " + str(analysisIndex) + " contrastIndex = " + str(contrastNum)

            if analysisIndex == int(contrastNum):

                topTableDataFrame = pd.DataFrame.from_csv(analysisResultFile.filePath + ".csv")
                
                if upDownFlag == "0":

                    upDownFlagName = "Up"

                    cutOffUpLogFC = float(request.POST.get("cutOffUpLogFC-"+str(analysisIndex),0 ))
                    cutOffUpPValue = float(request.POST.get("cutOffUpPValue-"+str(analysisIndex),0 ))

                    logFCValue = cutOffUpLogFC
                    cutOffPValue = cutOffUpPValue

                    topTableDataFrame = topTableDataFrame[topTableDataFrame['logFC'] > cutOffUpLogFC]
                    
                    if cutOffUpPValue != 0:

                        topTableDataFrame = topTableDataFrame[topTableDataFrame['adj.P.Val'] < cutOffUpPValue]

                elif upDownFlag == "1":

                    upDownFlagName = "Down"

                    cutOffDownLogFC = float(request.POST.get("cutOffDownLogFC-"+str(analysisIndex),0 ))
                    cutOffDownPValue = float(request.POST.get("cutOffDownPValue-"+str(analysisIndex),0 ))

                    logFCValue = cutOffDownLogFC
                    cutOffPValue = cutOffDownPValue

                    topTableDataFrame = topTableDataFrame[topTableDataFrame['logFC'] < cutOffDownLogFC]
                    
                    if cutOffDownPValue != 0:
                        
                        topTableDataFrame = topTableDataFrame[topTableDataFrame['adj.P.Val'] < cutOffDownPValue]
                    
                print (topTableDataFrame)
                    
                #downloadFilePath = "Project_" + str(analysisDetail.dataFile.project.name) + "_user_" + str(request.user) +                    

                fileName =  "Analysis_" + str(analysisDetail.name) + "_DownloadDEGData_" + upDownFlagName + "_logFC_" + str(logFCValue) + "_adj_p_val_" + str(cutOffPValue) + ".csv"
                
                print (fileName)

                response['Content-Disposition'] = 'attachment; filename=%s'%fileName

                writer = csv.writer(response,delimiter=",")

                writer.writerow(["genes,logFC,AveExpr,t,P.Value,adj.P.Val,B"])

                for index, row in topTableDataFrame.iterrows():

                    writer.writerow([row["genes"],row["logFC"],row["AveExpr"],row["t"],row["P.Value"],row["adj.P.Val"],row["B"]])

                break

    except:

        traceback.print_exc(file=sys.stdout)

    return response

@login_required
def displayAnalysisDetail(request):

    try:

        analysisDetailId = request.POST.get("analysisDetailId",0 )

        defaultCutOffPValue = 0
        defaultCutOffLogFC = 1.5

        analysisDetail = AnalysisDetail.objects.get(pk = analysisDetailId)
        
        phenotypeFileType = FileType.objects.filter(name = "phenotypeFile")[0]
        
        phenotypeFile = DataFile.objects.filter(project = analysisDetail.dataFile.project, fileType = phenotypeFileType)[0]
        
        phenotypeFileName = phenotypeFile.name
        
        filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id)
    
        phenotypeFileDf = pd.DataFrame.from_csv(filePath + "/" + str(phenotypeFileName), index_col=False)             

        phenotypeFileObj = PhenotypeFileObj()

        phenotypeFileObj.fileColumns = phenotypeFileDf.columns

        phenotypeFileObj.fileRows = phenotypeFileDf.values.tolist()

        analysisPlots = AnalysisPlot.objects.filter(analysisDetail = analysisDetail)
        
        plotObjList = []
        
        for analysisPlot in analysisPlots:
        
            plotObj = PlotObj()
        
            #plotObj.plotType = "MDS"

            plotObj.plotLabel = analysisPlot.plotFileName
            
            plotObj.plotName = analysisPlot.name

            plotObj.plotPath = "plotMDS_" + analysisPlot.plotPath
        
            plotObjList.append(plotObj)   
        
        analysisResultFiles = AnalysisResultFile.objects.filter(analysisDetail = analysisDetail)

        designFactors = DesignFactor.objects.filter(analysisDetail = analysisDetail)
        limmaContrasts = LimmaContrast.objects.filter(analysisDetail = analysisDetail)

        contrastObjList = []

        analysisDetailObj = AnalysisDetailObj()

        analysisDetailObj.analysisDetail = analysisDetail

        analysisDetailObj.limmaContrasts = limmaContrasts
        
        outputPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/Analysis_" + str(analysisDetail.id)
        
        #fitDataOutputPath = paste(outputPath, "/fitCoefficients", "_Project_", projectId, "_Analysis_", analysisDetailId, ".csv", sep="")
  
        fitCoefficientsDf = pd.DataFrame.from_csv (outputPath + "/fitCoefficients.csv", index_col = None)

        normalizedCountsDf = pd.DataFrame.from_csv (outputPath + "/NormalizedData.csv", index_col = None)
       
        designFactorObjList = []
        
        print (" design factor " + str(designFactors) + " head = " + str(phenotypeFileDf.columns))
        
        for designFactor in designFactors:
            
            designFactorObj = DesignFactorObj()
            
            designFactorObj.designFactor = designFactor

            print (" design factor " + str(designFactor.name) )
            
            designFactorValues = set(phenotypeFileDf[designFactor.name].tolist())
            
            designFactorObj.designFactorValues = ",".join(list(designFactorValues))

            designFactorObj.designFactorBaseline = designFactor.baseLineFactorValue
            
            designFactorObjList.append(designFactorObj)

        analysisDetailObj.designFactorObjList = designFactorObjList     

        designMatrixFilePath = outputPath + "/designMatrix.csv"
        contrastMatrixFilePath = outputPath + "/contrastMatrix.csv"

        designMatrixDf = pd.DataFrame.from_csv(designMatrixFilePath, index_col = None)
        matrixColumns = designMatrixDf.columns
        designMatrix = designMatrixDf.as_matrix()

        contrastMatrixDf = pd.DataFrame.from_csv(contrastMatrixFilePath, index_col = 0)
        contrastMatrixColumns = contrastMatrixDf.columns
        contrastMatrix = contrastMatrixDf.as_matrix()

        contrastMatrixRowObjList = []

        for rowIndex, row in enumerate ( contrastMatrix ) :

            contrastMatrixRowObj = ContrastMatrixRowObj()

            contrastMatrixRowObj.contrastLevel = matrixColumns [rowIndex]

            contrastMatrixRowObj.contrastMatrixRow = numpy.array(row)

            contrastMatrixRowObjList.append(contrastMatrixRowObj)

        for analysisIndex, analysisResultFile in enumerate(analysisResultFiles):

            cutOffUpLogFC = float(request.POST.get("cutOffUpLogFC-"+str(analysisIndex),0 ))
            cutOffDownLogFC = float(request.POST.get("cutOffDownLogFC-"+str(analysisIndex),0 ))

            cutOffUpPValue = float(request.POST.get("cutOffUpPValue-"+str(analysisIndex),0 ))
            cutOffDownPValue = float(request.POST.get("cutOffDownPValue-"+str(analysisIndex),0 ))

            if cutOffUpLogFC == 0:
                cutOffUpLogFC = defaultCutOffLogFC

            if cutOffDownLogFC == 0:
                cutOffDownLogFC = -defaultCutOffLogFC

            if cutOffUpPValue == 0:
                cutOffUpPValue = defaultCutOffPValue

            if cutOffDownPValue == 0:
                cutOffDownPValue = defaultCutOffPValue
                
            customGeneListFlag = request.POST.get("customGeneListFlag","0" )
            
            customGeneList = []
    
            if customGeneListFlag == "1":       
                
                print ( " analysis index = " + str(analysisIndex))
    
                customGeneListFile = request.FILES['customGeneListFile-'+str(analysisIndex)]
            
                geneListData = customGeneListFile.read().decode()
    
                geneListDataLines = geneListData.split("\r")
    
                for index, geneListDataLine in enumerate ( geneListDataLines ) :
                    
                    geneListDataLineValues = geneListDataLine.replace("\t","").replace("\n","").split(",")
                    
                    customGeneList.append(geneListDataLineValues[0])                

            contrastObj = ContrastObj()

            contrastObj.contrast = analysisResultFile.resultFileName

            contrastObj.cutOffUpPValue = cutOffUpPValue
            contrastObj.cutOffDownPValue = cutOffDownPValue

            contrastObj.cutOffUpLogFC = cutOffUpLogFC
            contrastObj.cutOffDownLogFC = cutOffDownLogFC

            #print " cut off up fc " + str(cutOffUpLogFC)
            #print " cut off down fc " + str(cutOffDownLogFC)

            #print " cut off up p value " + str(cutOffUpPValue)
            #print " cut off down p value " + str(cutOffDownPValue)

            topTableDataFrame = pd.DataFrame.from_csv(analysisResultFile.filePath + ".csv", index_col = None)

            #topTableDataFrame = pd.merge(topTableDataFrame, fitCoefficientsDf, how="inner", on = "genes")

            #topTableDataFrame.to_csv("outTopTableDf_merged.csv", index = None)

            topTableUpDataFrame = topTableDataFrame[topTableDataFrame['logFC'] > cutOffUpLogFC]
            #print " for up filter after FC " + str(topTableUpDataFrame.count())
            if cutOffUpPValue != 0:
                topTableUpDataFrame = topTableUpDataFrame[topTableUpDataFrame['P.Value'] < cutOffUpPValue]
            #print " for up filter after adj p val " + str(topTableUpDataFrame.count())

            topTableDownDataFrame = topTableDataFrame[topTableDataFrame['logFC'] < cutOffDownLogFC]

            #print " for down filter after FC " + str(topTableDownDataFrame.head())
            if cutOffDownPValue != 0:
                topTableDownDataFrame = topTableDownDataFrame[topTableDownDataFrame['P.Value'] < cutOffDownPValue]
            #print " for up filter after adj p val " + str(topTableDownDataFrame.count())

            geneUpList = list(topTableUpDataFrame.sort('logFC',ascending = False).values)
            geneDownList = list(topTableDownDataFrame.sort('logFC',ascending = False).values)

            #print " num gene up for contrast " + str(analysisResultFile.resultFileName) + " is " + str(len(geneUpList))
            #print " num gene down for contrast " + str(analysisResultFile.resultFileName) + " is " + str(len(geneDownList))

            for geneIndex, data in enumerate ( geneUpList ):

                geneUpObj = GeneInfoObj()

                if geneIndex > DEFAULT_MAX_LIST_DISPLAY:

                    break

                #print " gene id = " + str(data[0])
                geneUpObj.geneId = data[1]
                
                #try:
                    #geneUpObj.entrezGeneNumber = int(re.findall(r'\d+', data[0])[0])   
                #except:
                    #pass

                #geneUpObj.geneName = data[1]

                geneUpObj.logFC = data[2]
                geneUpObj.aveExpr = data[3]
                geneUpObj.tValue = data[4]
                geneUpObj.pValue = data[5]
                geneUpObj.adjustedPValue = data[6]
                geneUpObj.BValue = data[7]

                contrastObj.geneUpObjList.append(geneUpObj)

            for geneIndex, data in enumerate ( geneDownList ):

                if geneIndex > DEFAULT_MAX_LIST_DISPLAY:

                    break

                geneDownObj = GeneInfoObj()
                geneDownObj.geneId = data[0]

                #try:
                    #print ( " for down = " + str(re.findall(r'\d+', data[0])[0]) ) 
                    #geneDownObj.entrezGeneNumber = int(re.findall(r'\d+', data[0])[0])   
                #except:
                    #print ( " error in entrez " ) 
                    #pass

                #geneDownObj.geneName = data[0]

                geneDownObj.logFC = data[2]
                geneDownObj.aveExpr = data[3]
                geneDownObj.tValue = data[4]
                geneDownObj.pValue = data[5]
                geneDownObj.adjustedPValue = data[6]
                geneDownObj.BValue = data[7]

                contrastObj.geneDownObjList.append(geneDownObj)
                
            contrastObj.geneDownObjList.sort(key=lambda x: x.adjustedPValue) 

            for geneIndex, geneObj in enumerate ( contrastObj.geneDownObjList ):                
                
                contrastObj.geneDownObjList[geneIndex].geneRank = geneIndex + 1 

                #print (" setting index " + str(contrastObj.geneUpObjList[geneIndex].geneName) + " index " + str(geneIndex) + " p val "+ str(contrastObj.geneUpObjList[geneIndex].adjustedPValue))

            contrastObj.geneUpObjList.sort(key=lambda x: x.adjustedPValue) 

            for geneIndex, geneObj in enumerate ( contrastObj.geneUpObjList ):                
                
                contrastObj.geneUpObjList[geneIndex].geneRank = geneIndex + 1    
                
            contrastObj = scatterPlot(contrastObj, analysisDetail, normalizedCountsDf, phenotypeFileDf, topTableDataFrame)

            contrastObj = clusterMap(contrastObj, analysisDetail, normalizedCountsDf, phenotypeFileDf, topTableDataFrame, customGeneList)

            contrastObjList.append(contrastObj)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/analyzeFileResults.html', {
        "analysisDetail":analysisDetail,
        "analysisDetailObj":analysisDetailObj,
        "analysisPlots":analysisPlots,
        "analysisResultFiles":analysisResultFiles,
        #"limmaContrast":limmaContrast,
        "contrastObjList":contrastObjList,
        "contrastMatrixRowObjList":contrastMatrixRowObjList,
        "matrixColumns": matrixColumns,

        "designMatrix" : designMatrix,
        
        "plotObjList":plotObjList,

        "contrastMatrixColumns": contrastMatrixColumns,
        "contrastMatrix": contrastMatrix,
        
        "phenotypeFileObj":phenotypeFileObj,

    },  RequestContext(request))

@login_required
def submittedJobDetail(request):

    try:
        submittedJobId = request.POST.get("submittedJobId",0 )

        submittedJob = SubmittedJob.objects.get(pk = submittedJobId)

        completedFlag = True

        #print " ---- completed flag = " + str(completedFlag)

        if not submittedJob.completedTime:

            completedFlag = False

        #print " completed flag = " + str(completedFlag)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/displaySubmittedJob.html', {
        "submittedJob":submittedJob,
        "completedFlag":completedFlag,
    },  RequestContext(request))

@login_required
def displaySubmittedJob(request):

    try:
        submittedJobId = request.POST.get("submittedJobId",0 )

        submittedJob = SubmittedJob.objects.get(pk = submittedJobId)

        completedFlag = True

        #print " ---- completed flag = " + str(completedFlag)

        if not submittedJob.completedTime:

            completedFlag = False

        #print " completed flag = " + str(completedFlag)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/submittedJobDetail.html', {
        "submittedJob":submittedJob,
        "completedFlag":completedFlag,
    },  RequestContext(request))

#@login_required
#def downloadNormalizedData(request):


    #response = HttpResponse(content_type='text/csv')
    #response['Content-Disposition'] = 'attachment; filename="NormalizedData.csv"'

    #try:

        #writer = csv.writer(response,delimiter=",")

        #analysisDetailId = request.POST.get("analysisDetailId",0)

        #analysisDetail = AnalysisDetail.objects.get(pk = analysisDetailId)

        #filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/Analysis_" + str(analysisDetail.id)

        #inFile = open(filePath + "/NormalizedData.csv", "r")

        #for line in inFile:

            #writer.writerow([line])

    #except:

        #traceback.print_exc(file=sys.stdout)

    #return response

@login_required
def listAnalyses(request):

    analysisDetailObjList = []

    try:

        analysisDetails = AnalysisDetail.objects.all()

        for analysisDetail in analysisDetails:

            analysisDetailObj = AnalysisDetailObj()

            analysisDetailObj.analysisDetail = analysisDetail

            submittedJob = SubmittedJob.objects.filter(analysisDetail = analysisDetail)[0]

            analysisDetailObj.completedTime = submittedJob.completedTime

            analysisDetailObjList.append(analysisDetailObj)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/listAnalyses.html', {
        "analysisDetailObjList":analysisDetailObjList,
    },  RequestContext(request))

@login_required
def deletePhenotypeFile(request):

    try:

        dataFileId = request.POST.get("dataFileId",0)

        dataFile = DataFile.objects.get(pk = dataFileId)

        phenotypeFileId = request.POST.get("phenotypeFileId",0)

        phenotypeFile = DataFile.objects.get(pk = phenotypeFileId)

        os.remove(phenotypeFile.filePath + "/" + phenotypeFile.name)

        phenotypeFile.delete()

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/confirmDeletePhenotypeFile.html', {

        "dataFile":dataFile,

    },  RequestContext(request))

@login_required
def deleteAnalysisDetail(request):

    try:

        analysisDetailId = request.POST.get("analysisDetailId",0)

        analysisDetail = AnalysisDetail.objects.get(pk = analysisDetailId)

        dataFile = analysisDetail.dataFile

        shutil.rmtree(settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/Analysis_" + str(analysisDetail.id))

        analysisDetail.delete()

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/confirmDeleteAnalysisDetail.html', {
        "dataFile":dataFile,
    },  RequestContext(request))

@login_required
def deleteProjectFiles(request):

    try:

        dataFileId = request.POST.get("dataFileId",0)

        dataFile = DataFile.objects.get(pk = dataFileId)

        project = dataFile.project

        try:

            qcZipFileType = FileType.objects.filter(name = "qcZipFile")[0]
            qcZipFile = DataFile.objects.filter(project = project, fileType = qcZipFileType)[0]

            shutil.rmtree(dataFile.filePath + "/qc")
            os.remove(dataFile.filePath + "/alignment_summary.csv")
            os.remove(dataFile.filePath + "/summary.csv")

        except: 
            
            pass

        os.remove(dataFile.filePath + "/" + dataFile.name + ".csv")

        analysisDetails = AnalysisDetail.objects.filter( dataFile = dataFile )

        for analysisDetail in analysisDetails :

            shutil.rmtree(dataFile.filePath + "/Project_" + str(project.id) + "/Analysis_" + str(analysis.id))

            analysisDetail.delete()

        SampleDetail.objects.filter(dataFile = dataFile).delete()

        dataFile.delete()
        
        try:
            qcZipFile.delete()
        except:
            pass
        
    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/confirmDeleteFiles.html', {
        "project":project,
    },  RequestContext(request))

@login_required
def downloadData(request):

    analysisDetailId = request.POST.get("analysisDetailId","0")

    analysisDetail = AnalysisDetail.objects.get ( pk = analysisDetailId)

    downloadAllData = request.POST.get("downloadAllData","1")

    downloadPhenotypeFile = request.POST.get("downloadPhenotypeFile","0")

    downloadTopTableResults = request.POST.get("downloadTopTableResults","0")

    downloadDesignMatrix = request.POST.get("downloadDesignMatrix","0")

    downloadQCData = request.POST.get("downloadQCData","0")

    downloadContrastMatrix = request.POST.get("downloadContrastMatrix","0")

    downloadCountsMatrix = request.POST.get("downloadCountsMatrix","0")

    downloadNormalizedData = request.POST.get("downloadNormalizedData","0")

    downloadPlots = request.POST.get("downloadPlots","0")

    if downloadAllData:
        
        downloadPhenotypeFile = "1"
    
        downloadTopTableResults = "1"
    
        downloadDesignMatrix = "1"
    
        downloadQCData = "1"
    
        downloadContrastMatrix = "1"
    
        downloadCountsMatrix = "1"
    
        downloadNormalizedData = "1"        
    
        downloadPlots = "1"        

    contrastMatrixFileType = FileType.objects.filter(name = "contrastMatrix")[0]

    contrastMatrixFile = DataFile.objects.filter ( project = analysisDetail.dataFile.project, fileType = contrastMatrixFileType )[0]

    qcZipFileType = FileType.objects.filter(name = "qcZipFile")[0]

    qcZipFile = DataFile.objects.filter ( project = analysisDetail.dataFile.project, fileType = qcZipFileType )[0]

    phenotypeFileType = FileType.objects.filter(name = "phenotypeFile")[0]

    phenotypeFile = DataFile.objects.filter ( project = analysisDetail.dataFile.project, fileType = phenotypeFileType)[0]

    analysisDetailDownloadFlag = False
    
    dataFilePath = ''

    try:

        analysisDetail = AnalysisDetail.objects.get(pk = analysisDetailId)

        filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/Analysis_" + str(analysisDetail.id)

        # Open BytesIO to grab in-memory ZIP contents
        s = io.BytesIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")
        
        downloadFilePath = settings.DOWNLOAD_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.name) + "_" + str(request.user)
        
        if os.path.isdir(downloadFilePath ):
            
            shutil.rmtree(downloadFilePath)
            
        os.mkdir (downloadFilePath )

        print ( str(downloadCountsMatrix) + " - " + str(downloadPhenotypeFile) + " - " + str(downloadQCData) )
        
        if downloadCountsMatrix == "1" or downloadPhenotypeFile == "1" or downloadQCData == "1":
            
            dataFileDownloadFlag = True
            
            dataFilePath = downloadFilePath + "/" + contrastMatrixFile.name

            os.mkdir (dataFilePath)

        if downloadDesignMatrix =="1" or downloadContrastMatrix == "1" or downloadNormalizedData == "1" or downloadTopTableResults == "1":
            
            analysisDetailDownloadFlag = True
            
            analysisFilePath = downloadFilePath + "/" + analysisDetail.name

            os.mkdir (analysisFilePath)

        if downloadCountsMatrix == "1":

            fromPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/" + contrastMatrixFile.name + ".csv"
            
            #toPath = settings.DOWNLOAD_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.name) + "_" + str(request.user) + "/" + contrastMatrixFile.name + ".csv"
            
            toPath = dataFilePath + "/" + contrastMatrixFile.name + ".csv"
            
            print ( " from = " + str(fromPath) + " to " + str(toPath ))

            shutil.copy (fromPath, toPath)
            
            zf.write(toPath)

        if downloadPhenotypeFile == "1":

            fromPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/" + phenotypeFile.name 
            
            toPath = dataFilePath + "/" + phenotypeFile.name 

            shutil.copy (fromPath, toPath)
            
            zf.write(toPath)
            
            #zf.write(settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/" + phenotypeFile.name)

        if downloadQCData== "1":

            fromPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/" + "alignment_summary.csv"
            toPath = dataFilePath + "/" + "alignment_summary.csv"
            shutil.copy (fromPath, toPath)
            zf.write(toPath)
            
            fromPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/" + "summary.csv"
            toPath = dataFilePath + "/" + "summary.csv"
            shutil.copy (fromPath, toPath)            
            zf.write(toPath)

            fromPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/qc"
            toPath = dataFilePath + "/qc"
            shutil.copytree (fromPath, toPath)            

            # Adding files from directory 'qc'
            for root, dirs, files in os.walk(toPath):
                for f in files:
                    #print " zipping file " + str(f)
                    zf.write(os.path.join(root, f))
                    
        if downloadDesignMatrix:

            fromPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) + "/Analysis_" + str(analysisDetail.id) + "/designMatrix.csv"
            
            toPath = analysisFilePath  + "/designMatrix.csv"
            shutil.copy (fromPath, toPath)
            
            zf.write(toPath)            

        if downloadContrastMatrix:

            fromPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) +  "/Analysis_" + str(analysisDetail.id) + "/contrastMatrix.csv"
            
            toPath = analysisFilePath  + "/contrastMatrix.csv"

            shutil.copy (fromPath, toPath)
            
            zf.write(toPath)    
 
        if downloadTopTableResults:
            
            limmaContrasts = LimmaContrast.objects.filter ( analysisDetail = analysisDetail ) 
            
            for limmaContrast in limmaContrasts:

                fromPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(analysisDetail.dataFile.project.id) +  "/Analysis_" + str(analysisDetail.id) + "/" + limmaContrast.name + ".csv"
                
                toPath = analysisFilePath  + "/" + limmaContrast.name + ".csv"
    
                shutil.copy (fromPath, toPath)
                
                zf.write(toPath) 

        zf.close()

        zip_filename = "Project_" + str(analysisDetail.dataFile.project.name) + "_" + str(request.user) + "_Analysis_" + analysisDetail.name + ".zip"

        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    except:

        traceback.print_exc(file=sys.stdout)

    return resp

@login_required
def downloadImage (request):

    analysisDetailId = request.POST.get("analysisDetailId","0")

    analysisDetail = AnalysisDetail.objects.get ( pk = analysisDetailId)

    imageType = request.POST.get("imageType","")

    imageLabel = request.POST.get("imageType","")

    try:

        if imageType == "plotMDS":

             imageFilePath = settings.IMAGE_OUTPUT_FOLDER + "/" + str(imageType) + "_" + str(imageLabel) + ".png"
           
        elif imageType == "plotMA":

             imageFilePath = settings.IMAGE_OUTPUT_FOLDER + "/" + str(imageType) + ".png"

        # Open StringIO to grab in-memory ZIP contents
        s = io.BytesIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        zf.close()

        zip_filename = str(imageType) + "_" + str(imageLabel) + ".png"

        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(s.getvalue(), content_type = "image/png")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    except:

        traceback.print_exc(file=sys.stdout)

    return resp

@login_required
def deleteProject(request):

    try:

        projectId = request.POST.get("projectId",0)

        project = Project.objects.get(pk = projectId)
        
        projectPath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(project.id)
        
        if os.path.isdir(projectPath):
        
            shutil.rmtree(projectPath)        

        dataFiles = DataFile.objects.filter (project = project)
        
        for dataFile in dataFiles:

            analysisDetails = AnalysisDetail.objects.filter( dataFile = dataFile )

            for analysisDetail in analysisDetails :

                analysisDetail.delete()

            SampleDetail.objects.filter(dataFile = dataFile).delete()

            dataFile.delete()
            
        project.delete()

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/confirmDeleteProject.html', {
    },  RequestContext(request))

@login_required
def checkNewProject(request):

    try:

        listFiles = os.listdir (settings.INPUT_DATA_FOLDER)

        newDataFiles = []
        
        for listFile in listFiles:
            
            if listFile.endswith(".zip"):
                
                projects = Project.objects.filter(autoloadedFromFile = listFile)
                
                if len(projects) == 0:
                    
                    newDataFiles.add(listFile)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/displayNewFiles.html', {
    },  RequestContext(request))

@login_required
def displayNewProjects(request):

    try:

        listFiles = os.listdir (settings.INPUT_DATA_FOLDER)

        newProjectObjList = []
        
        users = User.objects.all()
        
        for listFile in listFiles:
            
            print (" file = " + str(listFile))
            
            if listFile.endswith(".zip"):
                
                newProjectObj = NewProjectObj()
                
                #projects = Project.objects.filter(autoLoadedFromPath = settings.INPUT_DATA_FOLDER + "/" + listFile)
                
                #if len(projects) == 0:

                newProjectObj.projectName = listFile 
                
                newProjectObj.m5ChkSumValueText = "Matches"
                newProjectObj.m5ChkSumValueFlag = True
                
                md5ChkSumValue = hashlib.md5(open(settings.INPUT_DATA_FOLDER + "/" + listFile, 'rb').read()).hexdigest()
    
                md5ChkSumFile = open(settings.INPUT_DATA_FOLDER + "/md5sum_" + listFile + ".txt")
    
                md5ChkSumFlag = True
    
                for line in md5ChkSumFile:
                    
                    data = line.split(" ")
                    
                    print ( " in md5 = " + str(data[0]) + " file md5 = " + str(md5ChkSumValue) )
                    
                    if data[0] != md5ChkSumValue:
                    
                        md5ChkSumFlag = False
                        
                if not md5ChkSumFlag:
                    
                    newProjectObj.m5ChkSumValueText = "Does not Match"
                    newProjectObj.m5ChkSumValueFlag = False
                                        
                newProjectObjList.append(newProjectObj)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/displayNewProjects.html', {

        "users" : users,
        "newProjectObjList": newProjectObjList,
        
    },  RequestContext(request))


@login_required
def submitAddNewProject(request):

    try:
        
        newProjectSelects = request.POST.getlist("newProjectSelect")        
        
        projectNames = request.POST.getlist("projectName")        
        
        newProjects = request.POST.getlist("newProject")   

        #newProjects = projectNames   
        
        print (" projectNames = " + str(projectNames))
        
        print (" new projects = " + str(newProjects))

        userIds = request.POST.getlist("userId")   

        contrastFileType = FileType.objects.filter(name = "contrastMatrix")[0]
        qcZipFileType = FileType.objects.filter(name = "qcZipFile")[0]
        
        for projectIndex, projectName in enumerate(projectNames): 
            
            projectUser = User.objects.get(pk = userIds[projectIndex])
        
            zipFile = zipfile.ZipFile(settings.INPUT_DATA_FOLDER + "/" + newProjects[projectIndex])

            md5ChkSumValue = hashlib.md5(open(settings.INPUT_DATA_FOLDER + "/" + newProjects[projectIndex], 'rb').read()).hexdigest()

            md5ChkSumFile = open(settings.INPUT_DATA_FOLDER + "/md5sum_" + newProjects[projectIndex] + ".txt")

            md5ChkSumFlag = True

            for line in md5ChkSumFile:
                
                data = line.split(" ")
                
                print ( " in md5 = " + str(data[0]) + " file md5 = " + str(md5ChkSumValue) )
                
                if data[0] != md5ChkSumValue:
                
                    md5ChkSumFlag = False
                    
            if not md5ChkSumFlag:
                
                print ("Check sum values do not match.")
                
                continue

            outputDataFolder = settings.OUTPUT_DATA_FOLDER 
    
            print ("before extract " )    
    
            zipFile.extractall(outputDataFolder )

            print ("after extract " )    

            zipFile.close()

            fileName = os.path.splitext(newProjects[projectIndex])[0]
            
            outputProjectFolder = outputDataFolder + "/" + fileName
    
            project = Project(name = projectNames[projectIndex], user = projectUser, startDate = datetime.datetime.now(), autoLoaded = True, autoLoadedFromPath = settings.INPUT_DATA_FOLDER + "/" + projectName, autoLoadedDate = datetime.datetime.now())

            project.save()
    
            filePath = settings.DATA_OUTPUT_FOLDER + "/Project_" + str(project.id)
    
            if not os.path.isdir( filePath ):
                os.mkdir(filePath)
    
                for src_dir, dirs, files in os.walk(outputProjectFolder):
                
                    #print " src_dir = " + str(src_dir)
                    #print " dirs = " + str(dirs)
                    #print " files = " + str(files)
            
                    for file_ in files:
                        src_file = os.path.join(outputProjectFolder, file_)
                        dst_file = os.path.join(filePath, file_)
                        shutil.copy(src_file, dst_file)
            
                    for dir_ in dirs:
                        src_ = os.path.join(src_dir, dir_)
                        dst_ = os.path.join(filePath, dir_)
               
                        #dst_dir = os.path.join(outPath, dir_)
                        shutil.copytree(src_, dst_)
            
                    break
                
                shutil.rmtree(outputProjectFolder)
    
            contrastDataFile = DataFile ( name = "counts.matrix" , description = "Counts Matrix", project = project, filePath = filePath, fileType = contrastFileType)
            contrastDataFile.save()

            qcFileZip = filePath + "/qc" 
    
            dataFile = DataFile ( name = qcFileZip , description = qcFileZip, project = project, filePath = filePath, fileType = qcZipFileType)
            dataFile.save()
    
            df = pd.DataFrame.from_csv(filePath + "/summary.csv")
    
            for index, datarow in df.iterrows():
    
                sampleNameString = str(index)
    
                numberOfInputReads = datarow["Number of input reads"]
                pctUniquelyMappedReads = datarow['Uniquely mapped reads %'].replace("%","")
                pctMappedMultipleLoci = datarow['% of reads mapped to multiple loci'].replace("%","")
    
                pctUnMappedTooManyLoci = datarow['% of reads mapped to too many loci'].replace("%","")
    
                pctUnMappedTooManyMismatches = datarow['% of reads unmapped: too many mismatches'].replace("%","")
                pctUnMappedTooShort = datarow['% of reads unmapped: too short'].replace("%","")
                pctUnMappedOther = datarow['% of reads unmapped: other'].replace("%","")
    
                totalAlignments = datarow['total alignments']
    
                sampleName = sampleNameString[:sampleNameString.find("_Log.final.out")]
    
                qcQualiMapHTMLPath = filePath + "/qc/" + sampleName + "_qualimap/qualimapReport.html"
                fastQcHTMLPath = filePath + "/qc/" + sampleName + "_fastqc/" + sampleName + "_fastqc.html"
    
                sampleDetail = SampleDetail ( sampleName = sampleName, dataFile = contrastDataFile, numberOfInputReads = numberOfInputReads, pctUniquelyMappedReads = pctUniquelyMappedReads, pctMappedMultipleLoci = pctMappedMultipleLoci, pctUnMappedTooManyLoci = pctUnMappedTooManyLoci, pctUnMappedTooManyMismatches = pctUnMappedTooManyMismatches ,  pctUnMappedTooShort = pctUnMappedTooShort  ,  pctUnMappedOther = pctUnMappedOther, totalAlignments = totalAlignments, qcQualiMapHTMLPath = qcQualiMapHTMLPath, fastQcHTMLPath= fastQcHTMLPath )
    
                sampleDetail.save()
    
            contrastMatrixFileType = FileType.objects.filter(name = "ContrastMatrix")[0]
    
            dataFiles = DataFile.objects.filter ( project = project, fileType = contrastMatrixFileType )
            
            os.remove(settings.INPUT_DATA_FOLDER + "/" + newProjects[projectIndex])
            
            os.remove(settings.INPUT_DATA_FOLDER + "/md5sum_" + newProjects[projectIndex] + ".txt")

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('rnaseq/listFiles.html', {
        
        "project":project,
        "dataFiles":dataFiles,

    },  RequestContext(request))

# scatter plot
def scatterPlot(contrastObj, analysisDetail, normalizedCountsDf, phenotypeFileDf, topTableDataFrame):

    try:

        scatterDf = pd.DataFrame()
        
        designFactors = DesignFactor.objects.filter ( analysisDetail = analysisDetail)
        
        #sampleNames = phenotypeFileDf[phenotypeFileDf[analysisDetail.sampleColumnName]].tolist()
        
        #contrastMatrixFileType = FileType.objects.filter(name = "contrastMatrix")[0]
    
        #dataFile = DataFile.objects.filter ( project = analysisDetail.dataFile.project, fileType = contrastMatrixFileType )[0]            

        #dataFileDf = pd.DataFrame.from_csv(dataFile.filePath + "/" + dataFile.name + ".csv", index_col = False)
        
        #normalizedCountsDf["genes"] = dataFileDf["Geneid"]

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
                
                normalizedCountsDfSel["genes"] = normalizedCountsDf["genes"]                
                
                print ( " for factor " + str(factorValue) + " : " + str(normalizedCountsDfSel.head() ) )                

                normalizedCountsDfSel["mean_"+ str(factorValue)] = normalizedCountsDfSel.mean(axis=1)                
                
                #print ( " for normalizedCountsDfSel " + str(normalizedCountsDfSel.columns) + " : " + str(normalizedCountsDfSel.head() ) )
                
                #topTableDataFrame["mean_"+ str(factorValue)] = normalizedCountsDfSel["mean_"+ str(factorValue)]
                
                #sampleNamesTopTable = [x + "_" + factorValue for x in sampleNames]
                
                #topTableDataFrame[sampleNamesTopTable] = normalizedCountsDfSel[sampleNames]   
                
                topTableDataFrame = pd.merge(topTableDataFrame, normalizedCountsDfSel, how="inner", on = "genes")   
                
                print (" top table = " + str(topTableDataFrame.head()) )     
                
            #dataFileColumnNames = []
                
            #for sampleName in sampleNames:
                
                #sampleNameXRefs = SampleNameXref.objects.filter(sampleName = sampleName)
                
                #if len(sampleNameXRefs) > 0:
                    
                    #sampleNameXref = sampleNameXRefs[0]
                    
                    #dataFileColumnNames.append( sampleName.dataFileColumnName )
                    
                    #dataFileColumnValues = phenotypeFileDf [ sampleName.dataFileColumnName ].tolist()
                    
                    #dataFileColumnNameMap [sampleName] = dataFileColumnValues

            cutOffUpPValue = contrastObj.cutOffUpPValue
            cutOffDownPValue = contrastObj.cutOffDownPValue 
    
            cutOffUpLogFC = contrastObj.cutOffUpLogFC 
            cutOffDownLogFC = contrastObj.cutOffDownLogFC
    
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
            
            topTableDataFrame[numerator] = pd.to_numeric(topTableDataFrame[numerator], errors='coerce').fillna(0.00001)
            topTableDataFrame[denominator] = pd.to_numeric(topTableDataFrame[denominator], errors='coerce').fillna(0.00001)            
            
            #topTableDataFrame ["data_logFC"] = math.log(  topTableDataFrame[numerator] / topTableDataFrame[denominator]  )           
            
            topTableDataFrame.to_csv("outTopTableDf_final.csv", index = None)
            
            xmin, xmax = min(topTableDataFrame[numerator].tolist() )  ,  max ( topTableDataFrame[numerator].tolist() ) 
            ymin, ymax = min(topTableDataFrame[denominator].tolist() )  ,  max ( topTableDataFrame[denominator].tolist() ) 
    
            print ( " ::: topTableDataFrame 111111111 ::: = " + str(topTableDataFrame.head()) )
          
            #significantDf = topTableDataFrame [  (topTableDataFrame["logFC"] >  1.5 ) ]
    
            #significantDf = topTableDataFrame [ ( (topTableDataFrame["logFC"] >  1.5 ) |  (topTableDataFrame["logFC"] <  -1.5 ) ) & (topTableDataFrame["adj.P.Val"] < 0.05) ]

            significantDf = topTableDataFrame [  (topTableDataFrame["logFC"] >  float(cutOffUpLogFC) ) |  (topTableDataFrame["logFC"] <  float(cutOffDownLogFC) )  ]
     
            print ( " ::: significant ::: = " + str(significantDf.head()) )
            
            significantDf.to_csv()
            
            topTableDataFrame["color"] = ["red" if x in significantDf["genes"].tolist() else "blue" for x in topTableDataFrame["genes"].tolist() ]
    
            topTableDataFrame["marker"] = [3 if x in significantDf["genes"].tolist() else 1 for x in topTableDataFrame["genes"].tolist() ]
    
            topTableDataFrame.to_csv("finalDF_" + str(contrastObj.contrast.replace(".","_")) + ".csv", index = None)
    
            fig = plt.figure(figsize=(16, 16), dpi = 1200)
          
            size = fig.get_size_inches()*fig.dpi # size in pixels
            
            dpi = fig.get_dpi()
                        
            topTableDataFrameBlue = topTableDataFrame [ topTableDataFrame["color"] == "blue" ]        
    
            topTableDataFrameRed = topTableDataFrame [ topTableDataFrame["color"] == "red" ]        
            
            plt.scatter(topTableDataFrameBlue[denominator], topTableDataFrameBlue[numerator],color='#3366ff', label=' ' , s = .85)
                        
            plt.scatter(topTableDataFrameRed[denominator], topTableDataFrameRed[numerator],color='#f04722', label=' ' , s = 15)
            
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
            
            #plt.plot([axes.get_xlim()[0] + log(cutOffUpLogFC,2), axes.get_xlim()[1] + log(cutOffUpLogFC,2)], [axes.get_ylim()[0], axes.get_ylim()[1]], c = "black")       
            #plt.plot([axes.get_xlim()[0], axes.get_xlim()[1] ], [axes.get_ylim()[0] + log(cutOffUpLogFC,2), axes.get_ylim()[1] + log(cutOffUpLogFC,2)], c = "black")     

            plt.plot([axes.get_xlim()[0] + cutOffUpLogFC, axes.get_xlim()[1] + cutOffUpLogFC], [axes.get_ylim()[0], axes.get_ylim()[1]], c = "black")       
            plt.plot([axes.get_xlim()[0], axes.get_xlim()[1] ], [axes.get_ylim()[0] + cutOffUpLogFC, axes.get_ylim()[1] + cutOffUpLogFC], c = "black")     
            
            axes.spines['top'].set_visible(False)
            axes.spines['right'].set_visible(False)
            
            axes.spines["top"].set_linewidth(2)  
            axes.spines["right"].set_linewidth(2)  
            
            axes.yaxis.set_ticks_position('left')
            axes.xaxis.set_ticks_position('bottom')
          
            plotPath = settings.IMAGE_OUTPUT_FOLDER   + '/scatterPlot_' + numerator + '_' + denominator
            plotName = 'scatterPlot_' + numerator + '_' + denominator
        
            plt.savefig(plotPath + ".png")
        
            contrastObj.scatterPlotPath = plotPath
            contrastObj.scatterPlotName = plotName
        
            source = ColumnDataSource(
                    data=dict(
                        y = topTableDataFrame[numerator].tolist(),
                        x = topTableDataFrame[denominator].tolist(),
                        gene=topTableDataFrame["genes"].tolist(),
                        col = topTableDataFrame["color"],
                        marker = topTableDataFrame["marker"],
                        
                    )
                )
            
            #source = ColumnDataSource(
                    #data=dict(
                        #y = significantDf[numerator].tolist(),
                        #x = significantDf[denominator].tolist(),
                        #gene=significantDf["genes"].tolist(),
                        #col = "red",
                        ##marker = significantDf["marker"],
                        
                    #)
                #)

            hover = HoverTool(
                    tooltips=[
                        ("(" + numerator + "," + denominator + ")", "($x, $y)"),
                        ("gene:", "@gene"),
                    ]
                )
            
            p = figure(plot_width=800, plot_height=800, tools=[hover],
                       title="Scatter plot")
            
            p.circle('x', 'y', 'desc', size = 5, color = 'col', source=source)
            
            #p.line()
            
            min_x, max_x = min(topTableDataFrame[denominator].tolist()), max (topTableDataFrame[denominator].tolist())
            min_y, max_y = min(topTableDataFrame[numerator].tolist()), max (topTableDataFrame[numerator].tolist())
            
            print ("min_x = " + str(min_x) + " max_x = " + str(max_x) ) 
            print ("min_y = " + str(min_y) + " max_y = " + str(max_y) ) 
            
            p.line([min_x + cutOffUpLogFC, max_x + cutOffUpLogFC], [min_y, max_y], line_color = "green")       
            p.line([min_x, max_x ], [min_y + cutOffUpLogFC, max_y + cutOffUpLogFC], line_color = "green")     
            
            p.xaxis.axis_label = denominator
            p.yaxis.axis_label = numerator
        
            p.grid.grid_line_color = None    
        
            p.xaxis.minor_tick_line_color = None
            p.yaxis.minor_tick_line_color = None  
            
            xymin = min(xmin, ymin)
            xymax = max(xmax, ymax)
            
            p.set(x_range=Range1d(xymin - .5, xymax - xymin), y_range=Range1d(xymin - .5, xymax-xymin))    
            
            ## bokeh plots
            plot_script = ''
            plot_div = ''     
            plot_script, plot_div = components(p)     
        
            plotName = contrastObj.contrast + " plot"
        
            #contrastObjObj.bokehPlotName = plotName
            contrastObj.bokehPlotScript = plot_script
            contrastObj.bokehPlotDiv = plot_div

    except:

        traceback.print_exc(file=sys.stdout)

    return contrastObj

# clustermap / heatmap 
def clusterMap(contrastObj, analysisDetail, normalizedCountsDf, phenotypeFileDf, topTableDataFrame, customGeneList):

    try:

        scatterDf = pd.DataFrame()
        
        designFactors = DesignFactor.objects.filter ( analysisDetail = analysisDetail)

        dataFileColumnNameMap = {}
        
        cutOffUpPValue = contrastObj.cutOffUpPValue
        cutOffDownPValue = contrastObj.cutOffDownPValue 

        cutOffUpLogFC = contrastObj.cutOffUpLogFC 
        cutOffDownLogFC = contrastObj.cutOffDownLogFC

        #topTableDataFrame = topTableDataFrame[topTableDataFrame['P.Value'] > cutOffUpPValue & topTableDataFrame['logFC'] < cutOffDownLogFC]

        #if cutOffUpPValue != 0:
            #topTableDataFrame = topTableDataFrame[topTableDataFrame['P.Value'] < cutOffUpPValue]

        #if cutOffDownPValue != 0:
            #topTableDataFrame = topTableDataFrame[topTableDataFrame['P.Value'] < cutOffDownPValue]

        if cutOffUpLogFC == 0:
            cutOffUpLogFC = 1.5

        if cutOffDownLogFC == 0:
            cutOffDownLogFC = -1.5
            
        if len(customGeneList) > 0:
            
            topTableDataFrame = topTableDataFrame[topTableDataFrame["genes"].isin(customGeneList)]

        else:
            
            topTableDataFrame = topTableDataFrame[(topTableDataFrame['logFC'] > cutOffUpLogFC) | (topTableDataFrame['logFC'] < cutOffDownLogFC)]        
        
        topTableDataFrame = topTableDataFrame[["genes"]]
            
        topTableDataFrame.set_index(["genes"])
        
        for designFactor in designFactors:
            
            #print ( " factr " + str(designFactor.name))
            
            factorValues = list(set(phenotypeFileDf[designFactor.name].tolist()))

            #print ( " factorValues " + str(factorValues))
            
            for factorValue in factorValues:
                
                #print ( " factorValue " + str(factorValue))                
            
                sampleNames = phenotypeFileDf[phenotypeFileDf[designFactor.name] == factorValue][analysisDetail.sampleColumnName].tolist()
                
                #print ( " sampleNames " + str(sampleNames))                
                
                normalizedCountsDfSel = normalizedCountsDf[sampleNames]
                
                normalizedCountsDfSel["genes"] = normalizedCountsDf["genes"]                
                
                topTableDataFrame = pd.merge(topTableDataFrame, normalizedCountsDfSel, how="inner", on = "genes")   
                
                #print (" top table = " + str(topTableDataFrame.head()) )   
                
        topTableDataFrame.dropna()                

        topTableDataFrame.to_csv("clusterMapDf.csv", index = None)
        
        topTableDataFrame = pd.DataFrame.from_csv("clusterMapDf.csv")            

        #topTableDataFrame.set_index(["genes"])            
     
        ax = sns.clustermap(topTableDataFrame, z_score = 1)
        
        #sns.plt.tight_layout()        

        #ax = sns.heatmap(topTableDataFrame)
        
        sns.plt.setp(ax.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)        
        sns.plt.setp(ax.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)  
        
        sns.plt.title('Cluster map for ' + str(contrastObj.contrast))        
        
        plotName = "clusterMap" 
        plotPath = settings.IMAGE_OUTPUT_FOLDER + "/plots/" + plotName + ".png"
        
        contrastObj.clusterMapName = plotName            
    
        if os.path.isfile(plotPath):
            os.remove(plotPath)        
    
        ax.savefig(plotPath)  

        fig = plt.figure(figsize=(18, 18), dpi = 1200)
      
        size = fig.get_size_inches()*fig.dpi # size in pixels
        
        dpi = fig.get_dpi()

        contrastObj.scatterPlotPath = plotPath
        contrastObj.scatterPlotName = plotName
    
        source = ColumnDataSource(data=topTableDataFrame)
        
        xfield = list({str(x) for x in topTableDataFrame.index.values.tolist()})
        yfield = topTableDataFrame.columns.tolist()
    
        #_WIDTH = 1000  # pixels
        #_HEIGHT = 700  # pixels
        #_PLOT_TOOLS = 'pan,box_zoom,resize,wheel_zoom,save,reset'    
    
        heatmap = figure(
            title='Heatmap for gene expression data',
            x_range =  xfield,
            y_range = yfield,
            plot_width=800,
            plot_height=650,
            tools='pan,box_zoom,resize,wheel_zoom,save,reset',
        )
    
        rect = heatmap.rect(
            x=xfield,
            y=yfield,
            width=1,
            height=1,
            source=source,
            color='color',
            line_color=None,
        )
    
        #tooltips = [
            #(xfield, '@' + xfield),
            #(yfield, '@' + yfield),
            ##(col_field, '@' + col_field),
        #]
    
        #hover = HoverTool(renderers=[rect], tooltips=tooltips)
    
        #heatmap.add_tools(hover)
    
        heatmap.grid.grid_line_color = None
        heatmap.xaxis.visible = None
        heatmap.yaxis.visible = None        

        plotScript, plotDiv = components(heatmap)    
        
        print (" plotScript = " + str(plotScript) )           
        print (" plotDiv = " + str(plotDiv) )           

        contrastObj.bokehHeatMapPlotScript = plotScript
        contrastObj.bokehHeatMapPlotDiv = plotDiv

    except:

        traceback.print_exc(file=sys.stdout)

    return contrastObj