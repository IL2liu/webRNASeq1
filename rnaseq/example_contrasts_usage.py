#!/usr/bin/env python

from rpy2 import robjects

MAT_FN = robjects.r("source('contrasts_matrix.R'); contrasts_matrix")

contrasts = [
    'lowgel.postgel-lowgel.baseline',
    'Placebo.postgel-Placebo.baseline',
    '(lowgel.postgel-lowgel.baseline)-(Placebo.postgel-Placebo.baseline)',
    'lowgel.baseline-Placebo.baseline',
    'lowgel.postgel-Placebo.postgel',
]

matrix = MAT_FN('./counts.matrix.xls', './Teleshova.meta.txt', contrasts)

print matrix
