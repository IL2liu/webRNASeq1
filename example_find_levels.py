#!/usr/bin/env python

from rpy2 import robjects

LEVELS_FN = robjects.r("source('find_levels.R'); find_levels")

s = ['Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.baseline', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'Placebo.postgel', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.baseline', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel', 'lowgel.postgel']

matrix = LEVELS_FN(robjects.StrVector(s))

print matrix
