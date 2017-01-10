from django.db import models
from django.contrib.auth.models import User
    
class Project(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, blank = True, null=True)    
    #startDate = models.DateTimeField(blank = True, null = True )
    #endDate = models.DateTimeField(blank = True, null = True ) 
    description = models.CharField(max_length=512, blank = True, null = True)
    autoLoaded = models.NullBooleanField()
    autoLoadedFromPath = models.CharField(max_length=512, blank = True, null = True)
    autoLoadedDate = models.DateTimeField(blank = True, null = True ) 
    def __str__(self):
        return self.name

class FileType(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    def __str__(self):
        return self.name

class DataFile(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    uploadedBy = models.ForeignKey(User, blank = True, null = True )
    uploadedDate = models.DateTimeField(blank = True, null = True )
    filePath = models.CharField(max_length=512)    
    fileType = models.ForeignKey(FileType, blank = True, null = True )
    project = models.ForeignKey ( Project ) 
    startingColumn = models.IntegerField(blank = True, null = True)
    commaOrTabDelimitedFlag = models.NullBooleanField()
    def __str__(self):
        return self.name
 

class SampleDetail(models.Model):

    dataFile = models.ForeignKey(DataFile)
    
    sampleName = models.CharField(max_length=512)
    numberOfInputReads = models.IntegerField()

    pctUniquelyMappedReads = models.FloatField()
    pctMappedMultipleLoci = models.FloatField()
    pctUnMappedTooManyLoci = models.FloatField()    

    pctUnMappedTooManyMismatches = models.FloatField() 
    pctUnMappedTooShort = models.FloatField() 
    pctUnMappedOther = models.FloatField() 

    qcQualiMapHTMLPath = models.CharField(max_length=512)
    fastQcHTMLPath = models.CharField(max_length=512)

    totalAlignments = models.IntegerField()

    def __unicode__(self):
        return str(self.numberOfInputReads)

class JobStatusCode(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255, null=True)
    def __unicode__(self):
        return self.code

class SubmittedJobType(models.Model):
    name = models.CharField ( max_length=10)  
    description = models.CharField ( max_length=255)   
    def __unicode__(self):
        return str(self.description)     
    
class AdjustMethod(models.Model):
    name = models.CharField(max_length=256)
    description =  models.CharField(max_length=512)
    def __str__(self):
        return self.name
        
class NormalizationMethod(models.Model):
    name = models.CharField ( max_length=10)  
    description = models.CharField ( max_length=255)   
    def __unicode__(self):
        return str(self.description) 

class AnalysisDetail(models.Model):
    
    name = models.CharField ( max_length=255, blank = True, null=True)

    dataFile = models.ForeignKey(DataFile) 
    
    phenotypeFile = models.ForeignKey(DataFile, related_name = "phenotypeFile")     
    
    description = models.CharField ( max_length=255)

    sampleColumnName = models.CharField ( max_length=255)  
    blockColumnName = models.CharField ( max_length=255, blank = True, null=True)       

    logFoldChangeDecideTests = models.FloatField(blank = True, null=True)
    pValueCutOffDecideTests = models.FloatField(blank = True, null=True)
    
    normalizationMethod = models.ForeignKey(NormalizationMethod, blank = True, null=True)

    def __unicode__(self):
        return str(self.dataFile)

class AnalysisResultFile(models.Model):
 
    name = models.CharField ( max_length=128)  
    filePath = models.CharField ( max_length=255)
    analysisDetail = models.ForeignKey(AnalysisDetail) 
    
    resultFileName = models.CharField ( max_length=128)      
    
    def __unicode__(self):
        return str(self.description) 

class AnalysisPlot(models.Model):
 
    name = models.CharField ( max_length=128)  
    plotPath = models.CharField ( max_length=255)

    analysisDetail = models.ForeignKey(AnalysisDetail) 
    
    plotFileName = models.CharField ( max_length=128)  
    
    def __unicode__(self):
        return str(self.description) 
    
class SampleNameXRef(models.Model):
    
    dataFileColumnName = models.CharField ( max_length=255, blank = True, null=True)
    sampleName = models.CharField ( max_length=255, blank = True, null=True)    
    analysisDetail = models.ForeignKey(AnalysisDetail)

    def __unicode__(self):
        return str(self.dataFile)    

class DesignFactor(models.Model):
    name = models.CharField ( max_length=128)  
    description = models.CharField ( max_length=255)   
    baseLineFactorValue = models.CharField ( max_length=255)   
    analysisDetail = models.ForeignKey(AnalysisDetail)
    def __unicode__(self):
        return str(self.description) 
        
class LimmaContrast(models.Model):
    name = models.CharField ( max_length=128)  
    description = models.CharField ( max_length=255) 
    analysisDetail = models.ForeignKey(AnalysisDetail)
    numerator = models.CharField ( max_length=128) 
    denominator = models.CharField ( max_length=128)   
    def __unicode__(self):
        return str(self.description) 
    
class SubmittedJob(models.Model):
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=512, null=True, blank = True)
    submittedBy = models.ForeignKey(User) 
    submittedOn = models.DateTimeField( null=True, blank = True)

    submittedJobType = models.ForeignKey(SubmittedJobType)
    
    jobStatusCode = models.ForeignKey(JobStatusCode)
    analysisDetail = models.ForeignKey(AnalysisDetail, null=True, blank = True)
    downloadDataFileLink = models.CharField(max_length=512, null=True, blank = True)
    completedTime = models.DateTimeField(null=True, blank=True)
    def __unicode__(self):
        return self.name    

class ColumnType(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    def __str__(self):
        return self.name
