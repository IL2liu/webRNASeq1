import os, sys, traceback
import pandas as pd

import seaborn as sns
from seaborn import color_palette, diverging_palette
import matplotlib.pyplot as plt

from bokeh.plotting import *
import bokeh
from bokeh.charts import Scatter, output_file, show
from bokeh.sampledata.autompg import autompg as df
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool

from bokeh.embed import components
from bokeh.models import Range1d

def clusterMap():

    try:

        df = pd.DataFrame.from_csv("clusterMapDf.csv")

        ax = sns.clustermap(df, z_score = 1)

        sns.plt.setp(ax.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        sns.plt.setp(ax.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)

        sns.plt.title('Cluster map ' )

        sns.plt.show()
        
        #plotName = "clusterMap.png"
        #plotPath = settings.IMAGE_OUTPUT_FOLDER + "/" + plotName

        #contrastObjObj.clusterMapName = plotName

        #if os.path.isfile(plotPath):
            #os.remove(plotPath)

        #sns.plt.savefig(plotPath)

        #fig = plt.figure(figsize=(16, 16), dpi = 1200)

        #size = fig.get_size_inches()*fig.dpi # size in pixels

        #dpi = fig.get_dpi()

    except:

        traceback.print_exc(file=sys.stdout)

    return

clusterMap()
