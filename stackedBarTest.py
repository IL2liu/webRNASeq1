from bokeh.charts import Bar, output_file, show
from bokeh.charts.attributes import cat, color
from bokeh.charts.operations import blend
from bokeh.charts.utils import df_from_json
from bokeh.sampledata.olympics2014 import data
import pandas as pd
#from rnaseq.models import * 

# utilize utility to make it easy to get json/dict data converted to a dataframe
#df = df_from_json(data)

#print (df.head())

#print (df.columns)

## filter by countries with at least one medal and sort by total medals
#df = df[df['total'] > 0]
#df = df.sort("total", ascending=False)

#bar = Bar(df,
          #values=blend('bronze', 'silver', 'gold', name='medals', labels_name='medal'),
          #label=cat(columns='abbr', sort=False),
          #stack=cat(columns='medal', sort=False),
          #color=color(columns='medal', palette=['SaddleBrown', 'Silver', 'Goldenrod'],
                      #sort=False),
          #legend='top_right',
          #title="Medals per Country, Sorted by Total Medals",
          #tooltips=[('medal', '@medal'), ('country', '@abbr')])


#output_file("stacked_bar.html", title="stacked_bar.py example")

#show(bar)

#dataFile = DataFile.objects.get ( pk = 4 ) 

#sampleDetailList = SampleDetail.objects.filter (dataFile = dataFile)



#sampleDf = pd.DataFrame(columns = ["sampleName","numberOfInputReads","pctUniquelyMappedReads", "pctMappedMultipleLoci","pctUnMappedTooManyLoci", "pctUnMappedTooManyMismatches","pctUnMappedTooShort","pctUnMappedOther"])

#sampleData = []

#for sampleDetail in sampleDetailList:
    
    #sampleDf = sampleDf.append([sampleDetail.sampleName,sampleDetail.numberOfInputReads,sampleDetail.pctUniquelyMappedReads,sampleDetail. pctMappedMultipleLoci,sampleDetail.pctUnMappedTooManyLoci,sampleDetail. pctUnMappedTooManyMismatches,sampleDetail.pctUnMappedTooShort,sampleDetail.pctUnMappedOther])
    
    ###sampleData.append([sampleDetail.sampleName,sampleDetail.numberOfInputReads,sampleDetail.pctUniquelyMappedReads,sampleDetail. pctMappedMultipleLoci,sampleDetail.pctUnMappedTooManyLoci,sampleDetail.pctUnMappedTooShort,sampleDetail.pctUnMappedOther])

#sampleDf = pd.DataFrame(sampleData, columns = ["sampleName","numberOfInputReads","pctUniquelyMappedReads", "pctMappedMultipleLoci","pctUnMappedTooManyLoci", "pctUnMappedTooManyMismatches","pctUnMappedTooShort","pctUnMappedOther"], index = None)             

##sampleDf = pd.DataFrame(sampleData, columns = ["sampleName","numberOfInputReads","pctUniquelyMappedReads", "pctMappedMultipleLoci","pctUnMappedTooManyLoci", "pctUnMappedTooShort","pctUnMappedOther"], index = ["sampleName"])     

##sampleDf = pd.DataFrame(sampleData, columns = ["sampleName","numberOfInputReads","pctUniquelyMappedReads", "pctMappedMultipleLoci","pctUnMappedTooManyLoci", "pctUnMappedTooShort","pctUnMappedOther"])  

sampleDf = pd.DataFrame.from_csv("/Users/mitras/projects/webRNASeq/sampleDetailInfo.csv", index_col = False)

bar = Bar(sampleDf,
          values=blend("pctUniquelyMappedReads", "pctMappedMultipleLoci","pctUnMappedTooManyLoci", "pctUnMappedTooManyMismatches","pctUnMappedTooShort","pctUnMappedOther", name='percentages', labels_name='percentage'),
          label=cat(columns='sampleName', sort=False),
          stack=cat(columns='percentage', sort=False),
          color=color(columns='percentage', palette=['SaddleBrown', 'Silver', 'Goldenrod','red','blue','green','yellow'],
                      sort=False),
          legend='bottom_right',
          title="Percentages",
          tooltips=[('percentage', '@percentage'), ('sample', '@sampleName')])

output_file("stacked_bar.html", title="stacked_bar.py example")

show(bar)

    
#sampleNames = sampleDf["sampleName"].tolist()

#print (sampleNames)

#pctUniquelyMappedReads = sampleDf['pctUniquelyMappedReads'].astype(float).values

#print (pctUniquelyMappedReads)

#pctMappedMultipleLoci = sampleDf['pctMappedMultipleLoci'].astype(float).values
#pctUnMappedTooManyLoci = sampleDf['pctUnMappedTooManyLoci'].astype(float).values
##pctUnMappedTooManyMismatches = sampleDf['pctUnMappedTooManyMismatches'].astype(float).values
#pctUnMappedTooShort = sampleDf['pctUnMappedTooShort'].astype(float).values
#pctUnMappedOther = sampleDf['pctUnMappedOther'].astype(float).values

## build a dict containing the grouped data
##mappedDataDict = OrderedDict(pctUniquelyMappedReads = pctUniquelyMappedReads, pctMappedMultipleLoci = pctMappedMultipleLoci, pctUnMappedTooManyLoci = pctUnMappedTooManyLoci,
                     ##pctUnMappedTooManyMismatches = pctUnMappedTooManyMismatches, pctUnMappedTooShort = pctUnMappedTooShort, pctUnMappedOther = pctUnMappedOther)

#mappedDataDict = OrderedDict(pctUniquelyMappedReads = pctUniquelyMappedReads, pctMappedMultipleLoci = pctMappedMultipleLoci, pctUnMappedTooManyLoci = pctUnMappedTooManyLoci,
                     #pctUnMappedTooShort = pctUnMappedTooShort, pctUnMappedOther = pctUnMappedOther)

#print (mappedDataDict)

#print (sampleNames)

#sampleDf = sampleDf[["pctUniquelyMappedReads", "pctMappedMultipleLoci","pctUnMappedTooManyLoci", "pctUnMappedTooShort","pctUnMappedOther"]]

#barplot = Bar(sampleDf, title="Sample Details", stack="cyl")

#plotPath = settings.IMAGE_OUTPUT_FOLDER + "/sampleDetail.png"

#barPlotScript, barPlotDiv = components(barplot)

#plt.savefig(plotPath)     