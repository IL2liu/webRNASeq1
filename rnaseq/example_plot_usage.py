#!/usr/bin/env python

from rpy2 import robjects

factors = ['Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel']

samples = ['DV13-BL', 'EL86-BL', 'HA05-BL', 'FF66-BL', 'DH91-BL', 'DV13-PG', 'EL86-PG', 'GI57-PG', 'HA05-PG', 'FF66-PG', 'DH91-PG', 'HI81-PG', 'HH91-BL', 'GC05-BL', 'HH78-BL', 'EJ42-BL', 'FH29-BL', 'FC50-BL', 'GK45-BL', 'FV47-BL', 'HH91-PG', 'GC05-PG', 'HH78-PG', 'EJ42-PG', 'FH29-PG', 'FC50-PG', 'GK45-PG', 'FV47-PG', 'IC87-PG', 'GB85-PG']

filePath = "/Users/mitras/self/teleshova/counts.matrix"

plotPath = '/Users/mitras/projects/webRNASeq/static/img'

PLOT_FN = robjects.r("source('" + settings.PROJECT_BASE_FOLDER + "/create_plots.R'); createPlots")

PLOT_FN(filePath, plotPath, robjects.StrVector(factors), robjects.StrVector(samples))	

plotMAPath = basePlotPath, "/plotMA.png"

plotMDSPath = basePlotPath, "/plotMDS.png"
