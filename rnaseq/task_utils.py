import csv
import numpy
from numpy import *
import scipy
import math
from scipy import *
from math import *

import sys, traceback
from rnaseq.models import *

import subprocess, datetime, time
from subprocess import Popen

import re, os

import rpy2.robjects as robjects
from rpy2.robjects import r
from rpy2.robjects.packages import importr

import sys, traceback

import pymongo
from pymongo import MongoClient



from rnaseq.rnaseqObjs import *
from rnaseq.rnaseqConstants import *

#import zipfile
#import datetime

from django.conf import settings


def callLimmaTask(filePath, basePlotPath, outputPath, factors, factorColumns, factorColumnValuesMap, factorColumnValueSet,samples, sampleNames, animals, contrasts, submittedJob):

    contrast = []

    try:

        #print " in task - before calling R !!!! "

        startJobStatusCode = JobStatusCode.objects.all().filter(code="START")[0]
        endJobStatusCode = JobStatusCode.objects.all().filter(code="END")[0]

        submittedJob.jobStatusCode = startJobStatusCode

        submittedJob.save()

        MAT_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/limma_analysis.R'); contrasts_matrix")

        contrast = MAT_FN(filePath, basePlotPath, outputPath, robjects.StrVector(factors), robjects.StrVector(factorColumns),robjects.ListVector(factorColumnValuesMap), robjects.StrVector(factorColumnValueSet),robjects.StrVector(samples), robjects.StrVector(sampleNames), robjects.StrVector(animals), robjects.StrVector(contrasts))

        submittedJob.completedTime = datetime.datetime.now()
        submittedJob.jobStatusCode = endJobStatusCode
        submittedJob.save()

        #print " &&&&&&&& in task - after calling R "

    except:

        traceback.print_exc(file=sys.stdout)

    return