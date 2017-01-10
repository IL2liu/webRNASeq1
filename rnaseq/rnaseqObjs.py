class ProjectObj(object):
    def __init__(self):

        self.project = ''
        self.numContrastMatrixFiles = 0

    def __unicode__(self):
        return str(self.project.name)

class GeneObj(object):
    def __init__(self):

        self.geneName = ''
        self.chromosome = ''
        self.start = ''
        self.end = ''
        self.strand = ''
        self.length = ''
        self.bamfileValues = []

    def __unicode__(self):
        return str(self.geneName)

class GeneInfoObj(object):
    def __init__(self):

        self.geneId = 0

        self.geneName = ''

        self.logFC = 0
        self.aveExpr = 0
        self.tValue = 0
        self.pValue = 0
        self.adjustedPValue = 0
        self.BValue = 0

        self.logFCInput = 0

    def __unicode__(self):
        return str(self.geneId)

class ContrastObj(object):
    def __init__(self):

        self.contrast = False
        self.contrastId = 0

        self.geneUpObjList = []
        self.geneDownObjList = []

        self.cutOffDownLogFC = 0
        self.cutOffDownPValue = 0

        self.cutOffUpLogFC = 0
        self.cutOffUpPValue = 0
        
        self.scatterPlotPath = ''
        self.scatterPlotName = ''
        
        self.bokehPlotName = ''
        self.bokehPlotScript = ''
        self.bokehPlotDiv = ''
        
        self.bokehHeatMapPlotScript = ''
        self.bokehHeatMapPlotDiv = ''
        self.clusterMapName = ''        

    def __unicode__(self):
        return str(self.contrast)

class ContrastMatrixRowObj(object):
    def __init__(self):

        self.contrastLevel = ''
        self.contrastMatrixRow = []

    def __unicode__(self):
        return str(self.contrastLevel)

class PhenotypeFileObj(object):
    def __init__(self):

        self.phenotypeFile = ''
        self.noDeleteFlag = False
        self.fileColumns = []
        self.fileRows = []

    def __unicode__(self):
        return str(self.phenotypeFile.name)

class PhenotypeObj(object):
    def __init__(self):

        self.colName = ''
        self.factor1 = ''
        self.factor2 = ''
        self.blockGroup = ''

    def __unicode__(self):
        return str(self.colName)

class PhenotypeColumnObj(object):
    def __init__(self):

        self.colName = ''
        self.columnType = ''

    def __unicode__(self):
        return str(self.colName)

class FactorObj(object):
    def __init__(self):

        self.factorId = 0
        self.name = ''
        self.description = ''

    def __unicode__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.__unicode__())

class DesignFactorObj(object):
    def __init__(self):

        self.designFactor = ''
        self.designFactorValues = []
        self.designFactorName = ''
        self.designFactorBaseline = ''

    def __unicode__(self):
        return str(self.designFactor)

    def __hash__(self):
        return hash(self.__unicode__())

class AnalysisDetailObj(object):
    def __init__(self):

        self.analysisDetail = ''
        self.designFactorObjList = []
        self.limmaContrasts = ''
        self.dateAnalyzed = ''

    def __unicode__(self):
        return str(self.analysisDetail.name)

    def __hash__(self):
        return hash(self.__unicode__())

class AnalysisObj(object):
    def __init__(self):

        self.combinationString = ''
        self.pValue = ''

    def __unicode__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.__unicode__())

class CombinationObj(object):

    def __init__(self):

        self.combinationNum = 0

        self.factor1 = ''
        self.factor2 = ''

        self.combinationString = ''
        self.combinationDescription = ''

        self.comparisonType = ''
        self.comparisonMethod = ''

        self.comparisonFromFactor1 = ''
        self.comparisonFromFactor2 = ''

        self.comparisonToFactor1 = ''
        self.comparisonToFactor2 = ''

        self.combination1String = ''
        self.combination2String = ''

        self.foldChangeCutOff = 0
        self.pValueCutOff = 0

        self.testStatGreaterThanZero = False

    def __unicode__(self):
        return str(self.combinationString)

    def __hash__(self):
        return hash(self.__unicode__())

class MatrixColumnMatchObj(object):
    def __init__(self):

        self.selectedSampleName = ''
        self.selectedMatrixColumn = ''

        self.sampleNames = []
        self.dataMatrixColumns = []

    def __unicode__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.__unicode__())

class PlotObj(object):
    def __init__(self):

        self.plotPath = ''
        self.plotType = ''
        self.plotLabel = ''
        self.plotName = ''
        self.redColorFactorValue = ''
        self.blueColorFactorValue = ''
        
    def __unicode__(self):
        return str(self.plotPath)

    def __hash__(self):
        return hash(self.__unicode__())
    
class NewProjectObj(object):
    def __init__(self):

        self.projectName = ''
        self.m5ChkSumValueText = ''
        self.m5ChkSumValueFlag = False
        
    def __unicode__(self):
        return str(self.projectName)

    def __hash__(self):
        return hash(self.__unicode__())
    
class SubmittedJobObj(object):
    def __init__(self):

        self.submittedJob = ''
        self.completedFlag = ''

    def __unicode__(self):
        return str(self.submittedJob.name)
    