from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    
    (r'^$', 'rnaseq.views.landing'),

    (r'^rnaseq/$', 'rnaseq.views.landing'),
    (r'^rnaseq/processLanding/$', 'rnaseq.views.processLanding'),  

    (r'^rnaseq/listProjects/$', 'rnaseq.views.listProjects'),  
    (r'^rnaseq/listFiles/$', 'rnaseq.views.listFiles'),  
    (r'^rnaseq/listSubmittedJobs/$', 'rnaseq.views.listSubmittedJobs'),  
    
    (r'^rnaseq/addProject/$', 'rnaseq.views.addProject'),  
    (r'^rnaseq/addDataFile/$', 'rnaseq.views.addDataFile'),  

    (r'^rnaseq/submitAddProject/$', 'rnaseq.views.submitAddProject'),  
    (r'^rnaseq/submitAddDataFile/$', 'rnaseq.views.submitAddDataFile'),  

    (r'^rnaseq/displayFileDetails/$', 'rnaseq.views.displayFileDetails'),  
    (r'^rnaseq/analyzeFileSelect/$', 'rnaseq.views.analyzeFileSelect'),  

    (r'^rnaseq/analyzeFileSelectFactors/$', 'rnaseq.views.analyzeFileSelectFactors'), 

    (r'^rnaseq/analyzeFileShowContrastMatrix/$', 'rnaseq.views.analyzeFileShowContrastMatrix'), 
    
    (r'^rnaseq/analyzeFileSubmit/$', 'rnaseq.views.analyzeFileSubmit'),     
    
    (r'^rnaseq/analyzeFileSelectColumns/$', 'rnaseq.views.analyzeFileSelectColumns'),   
    
    (r'^rnaseq/analyzeProject/$', 'rnaseq.views.analyzeProject'),       

    #(r'^rnaseq/listAnalysisDetails/$', 'rnaseq.views.listAnalysisDetails'),      
    (r'^rnaseq/displayAnalysisDetail/$', 'rnaseq.views.displayAnalysisDetail'),

    (r'^rnaseq/submittedJobDetail/$', 'rnaseq.views.submittedJobDetail'),  
    
    (r'^rnaseq/sampleDetail/$', 'rnaseq.views.sampleDetail'),     

    (r'^rnaseq/downloadDEGData/$', 'rnaseq.views.downloadDEGData'),   

    (r'^rnaseq/downloadData/$', 'rnaseq.views.downloadData'),   

    (r'^rnaseq/downloadImage/$', 'rnaseq.views.downloadImage'),
    
    (r'^rnaseq/listAnalyses/$', 'rnaseq.views.listAnalyses'),   

    (r'^rnaseq/deletePhenotypeFile/$', 'rnaseq.views.deletePhenotypeFile'),   
    
    (r'^rnaseq/deleteProjectFiles/$', 'rnaseq.views.deleteProjectFiles'),   
    
    (r'^rnaseq/deleteProject/$', 'rnaseq.views.deleteProject'),  
    
    (r'^rnaseq/deleteAnalysisDetail/$', 'rnaseq.views.deleteAnalysisDetail'),  
    
    (r'^rnaseq/displayNewProjects/$', 'rnaseq.views.displayNewProjects'),   

    (r'^rnaseq/submitAddNewProject/$', 'rnaseq.views.submitAddNewProject'),   

    (r'^rnaseq/showPlots/$', 'rnaseq.views.showPlots'), 
    
    (r'^rnaseq/scatterPlot/$', 'rnaseq.views.scatterPlot'), 

    (r'^accounts/', include('registration.urls')),
) 

urlpatterns += staticfiles_urlpatterns()

#print str(urlpatterns)
