from rnaseq.models import *
import os, sys, traceback
import pandas as pd

#QC_FILE_BASE_PATH = "/static/qc/"

jobStatusCode = JobStatusCode(code= "QUEUE", description = "In Queue")
jobStatusCode.save()

jobStatusCode = JobStatusCode(code= "START", description = "Started")
jobStatusCode.save()

jobStatusCode = JobStatusCode(code= "END", description = "Ended")
jobStatusCode.save()

jobStatusCode = JobStatusCode(code= "TERM", description = "Terminated")
jobStatusCode.save()

submittedJobType = SubmittedJobType(name = "Download", description = "Create download Zip File")
submittedJobType.save()

submittedJobType = SubmittedJobType(name = "Upload", description = "Upload files")
submittedJobType.save()

submittedJobType = SubmittedJobType(name = "Analysis", description = "Analysis of data using Limma")
submittedJobType.save()

dataFileType = FileType(name = "contrastMatrix", description = "ContrastMatrix")
dataFileType.save()

dataFileType = FileType(name = "qcZipFile", description = "Zip of QC files")
dataFileType.save()

dataFileType = FileType(name = "phenotypeFile", description = "Phenotype File")
dataFileType.save()

#project = Project ( name = "Teleshova RNA Seq Analysis", description = "Teleshova RNA Seq Analysis Pipeline Project")
#project.save()

#dataFile = DataFile (name = "HIV data", description = "HIV data", filePath = "data_csv.csv", phenotypeDataFile = phenotypeDataFile, project = project )
#dataFile.save()

#project = Project ( name = "Test RNA Seq project", description = "Test RNA Seq project")
#project.save()

#dataFile = DataFile (name = "Test RNA Seq data", description = "Test RNA Seq data", filePath = "data_csv.csv", project = project )
#dataFile.save()

columnType = ColumnType ( name = "factor" , description = "factor") 
columnType.save()

columnType = ColumnType ( name = "block" , description = "block") 
columnType.save()

columnType = ColumnType ( name = "sample" , description = "sample") 
columnType.save()

#dataFile = DataFile.objects.get ( pk = 2) 

#df = pd.DataFrame.from_csv("/Users/mitras/self/limma/final/summary.csv")

#for index, datarow in df.iterrows():
    
    #sampleNameString = str(index)
    
    #numberOfInputReads = datarow["Number of input reads"]
    #pctUniquelyMappedReads = datarow['Uniquely mapped reads %'].replace("%","")
    #pctUniquelyMappedMultipleLoci = datarow['% of reads mapped to multiple loci'].replace("%","")

    #pctUniquelyMappedTooManyLoci = datarow['% of reads mapped to too many loci'].replace("%","")
    
    #pctUniquelyMappedTooManyMismatches = datarow['% of reads unmapped: too many mismatches'].replace("%","")
    #pctUniquelyMappedTooShort = datarow['% of reads unmapped: too short'].replace("%","")
    
    #totalAlignments = datarow['total alignments']
    
    #sampleName = sampleNameString[:sampleNameString.find("_Log.final.out")]
    
    #qcQualiMapHTMLPath = QC_FILE_BASE_PATH + sampleName + "_qualimap/qualimapReport.html"
    #fastQcHTMLPath = QC_FILE_BASE_PATH + sampleName + "_fastqc/" + sampleName + "_fastqc.html"
    
    #sampleDetail = SampleDetail ( sampleName = sampleName, dataFile = dataFile, numberOfInputReads = numberOfInputReads, pctUniquelyMappedReads = pctUniquelyMappedReads, pctUniquelyMappedMultipleLoci = pctUniquelyMappedMultipleLoci, pctUniquelyMappedTooManyLoci = pctUniquelyMappedTooManyLoci, pctUniquelyMappedTooManyMismatches = pctUniquelyMappedTooManyMismatches ,  pctUniquelyMappedTooShort = pctUniquelyMappedTooShort, totalAlignments = totalAlignments, qcQualiMapHTMLPath = qcQualiMapHTMLPath, fastQcHTMLPath= fastQcHTMLPath )
    
    #sampleDetail.save()    