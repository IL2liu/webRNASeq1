#!/usr/bin/env python

from rpy2 import robjects

CONTRAST_2_FN = robjects.r("source('make_contrast_matrix_2.R'); contrast_matrix")

groups = ['Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'Placebo', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel', 'lowgel']

conditions = ['baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel', 'postgel']

factorColumnValuesMap["groups"] = robjects.StrVector(groups)

factorColumnValuesMap["conditions"] = robjects.StrVector(conditions)

robjects.ListVector(factorColumnValuesMap)


matrix = DESIGN_FN(robjects.StrVector(s))

print matrix
