#from rnaseq.rjoel import *
from rnaseq.settings import STATIC_DOC_ROOT
import os, sys, traceback
import csv
import urllib
import shutil
import rpy2.robjects as robjects 
from rpy2.robjects import r
from rpy2.robjects.packages import importr 

import math
import pandas as pd
import urllib2
import itertools
from itertools import *
import numpy

_ROC_FN = _robjects.r('''
    function(inLabels, inComparisonStrings) {
        robjects.r('require(biomaRt)')
        robjects.r('require(DESeq2)')
        robjects.r('require(reshape2)')
        robjects.r('require(ggplot2)')
        robjects.r('require(gplots)')
        robjects.r('require(plyr)')
        robjects.r('require(genefilter)')
        robjects.r('require(edgeR)')
        cont.matrix<-makeContrasts(lowgel=lowgel.postgel-lowgel.baseline,Placebo=Placebo.postgel-Placebo.baseline,diff=(lowgel.postgel-lowgel.baseline)-(Placebo.postgel-Placebo.baseline),baseline_diff=lowgel.baseline-Placebo.baseline,postgel_diff=lowgel.postgel-Placebo.postgel,levels=design.limma)
            
        return(cont.matrix)
    }
''')    

results = _ROC_FN(_robjects.IntVector(yobs), _robjects.FloatVector(ypred))
for name, val in results.items():
    if name == 'fpr':
	fpr = list(val)
    
robjects.r('cm<-cbind("lowgel.postgel" = c(1,0,0,0),"lowgel.baseline" = c(1,1,0,0),"Placebo.postgel"= c(1,0,1,0),"Placebo.baseline" = c(1,1,1,1))')	 

robjects.r('cm2<-cbind(combinationString = cm[,"lowgel.postgel"]-cm[,"Placebo.postgel"])')


