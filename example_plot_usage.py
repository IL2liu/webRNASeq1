#!/usr/bin/env python

from rpy2 import robjects
from collections import OrderedDict

countsMatrixFilePath = "/Users/mitras/self/teleshova/counts.matrix"

basePlotPath = "/Users/mitras/projects/webRNASeq/static/img"

factors = ['baseline.Placebo', 'baseline.Placebo', 'baseline.Placebo', 'baseline.Placebo', 'baseline.Placebo', 'postgel.Placebo', 'postgel.Placebo', 'postgel.Placebo', 'postgel.Placebo', 'postgel.Placebo', 'postgel.Placebo', 'postgel.Placebo', 'baseline.lowgel', 'baseline.lowgel', 'baseline.lowgel', 'baseline.lowgel', 'baseline.lowgel', 'baseline.lowgel', 'baseline.lowgel', 'baseline.lowgel', 'postgel.lowgel', 'postgel.lowgel', 'postgel.lowgel', 'postgel.lowgel', 'postgel.lowgel', 'postgel.lowgel', 'postgel.lowgel', 'postgel.lowgel', 'postgel.lowgel', 'postgel.lowgel']

factorColumns = ['Condition', 'Group']
 
factorColumnValues = [['baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel'], ['Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel']]

factorColumnValuesMap = {}

for index, factorColumn in enumerate ( factorColumns ):
    
    factorColumnValuesMap[factorColumn] = robjects.StrVector(factorColumnValues[index])

#factorColumnValuesMap = {

    #'Group': robjects.StrVector(['Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel']), 
    
    #'Condition': robjects.StrVector(['baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel'])}

factorSetList = ['baseline', 'Placebo']

sampleXrefList = [u'DV13-BL_S1_R1_001.bam', u'EL86-BL_S3_R1_001.bam', u'HA05-BL_S6_R1_001.bam', u'FF66-BL_S4_R1_001.bam', u'DH91-BL_S5_R1_001.bam', u'DV13-PG_S3_R1_001.bam', u'EL86-PG_S2_R1_001.bam', u'GI57-PG_S9_R1_001.bam', u'HA05-PG_S7_R1_001.bam', u'FF66-PG_S1_R1_001.bam', u'DH91-PG_S14_R1_001.bam', u'HI81-PG_S5_R1_001.bam', u'HH91-BL_S2_R1_001.bam', u'GC05-BL_S7_R1_001.bam', u'HH78-BL_S8_R1_001.bam', u'EJ42-BL_S9_R1_001.bam', u'FH29-BL_S10_R1_001.bam', u'FC50-BL_S11_R1_001.bam', u'GK45-BL_S12_R1_001.bam', u'FV47-BL_S13_R1_001.bam', u'HH91-PG_S14_R1_001.bam', u'GC05-PG_S13_R1_001.bam', u'HH78-PG_S10_R1_001.bam', u'EJ42-PG_S15_R1_001.bam', u'FH29-PG_S4_R1_001.bam', u'FC50-PG_S6_R1_001.bam', u'GK45-PG_S12_R1_001.bam', u'FV47-PG_S15_R1_001.bam', u'IC87-PG_S11_R1_001.bam', u'GB85-PG_S8_R1_001.bam']

sampleNames = ['DV13-BL', 'EL86-BL', 'HA05-BL', 'FF66-BL', 'DH91-BL', 'DV13-PG', 'EL86-PG', 'GI57-PG', 'HA05-PG', 'FF66-PG', 'DH91-PG', 'HI81-PG', 'HH91-BL', 'GC05-BL', 'HH78-BL', 'EJ42-BL', 'FH29-BL', 'FC50-BL', 'GK45-BL', 'FV47-BL', 'HH91-PG', 'GC05-PG', 'HH78-PG', 'EJ42-PG', 'FH29-PG', 'FC50-PG', 'GK45-PG', 'FV47-PG', 'IC87-PG', 'GB85-PG']

plotPath = '/Users/mitras/projects/webRNASeq/static/img'

PLOT_FN = robjects.r("source('create_plots.R'); createPlots")

print str(factorColumnValuesMap)

PLOT_FN(countsMatrixFilePath, basePlotPath, robjects.StrVector(factors), robjects.StrVector(factorColumns), robjects.ListVector(factorColumnValuesMap), robjects.StrVector(factorSetList), robjects.StrVector(sampleXrefList), robjects.StrVector(sampleNames))	

plotMAPath = basePlotPath, "/plotMA.png"

plotMDSPath = basePlotPath, "/plotMDS.png"
