#!/usr/bin/env python

from rpy2 import robjects

DESIGN_FN = robjects.r("source('make_design_matrix.R'); design_matrix")

s = ['Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel']

matrix = DESIGN_FN(s)

print matrix
