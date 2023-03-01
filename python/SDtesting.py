#######################################################
# PIP INSTALLS TO MAKE FOR NLTK LDA TOPIC MODELING
# pip install gensim
# pip install pyldavis
# pip install nltk
# pip install ipython
# pip install regex
# ####################################################
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
import gensim.corpora as corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models
import os
import re

#Variable with current dir
workingDir = os.getcwd()
#print(workingDir)
#Edit current string by lopping off the end with '/python'
parentDir = re.sub('python', '', workingDir)
#print(parentDir)
#Add the directory ending that we want to get all files from
stardewPath = os.path.join(parentDir, 'StardewText')
print('Stardew Paths', stardewPath)


#ws: return all files nested infinitely in folders

#define function findfiles
    #make a variable PATHLIST with the list with the filepaths from StardewText
    #make a variable editing the above with the list of all full paths
    #for each filepath in the list:
        #variable ext = the filepath + the name of it's appropriate file/folder
        #if ent ends with txt or yaml
            #add the small path to filepath
        #else, if the full path is a folder
            #variable = list of filepaths for each thing in folder
            #add list of filepaths to PATHLIST

allDocs = []
def findfiles():
    pathList = os.listdir(stardewPath)
    for path in pathList:
        #print('THIS IS PATHLIST: \n ------------', pathList)
        ext = f"{stardewPath}\{path}"
        #print(ext, path.endswith(tuple([".yaml", ".txt"])), os.path.isdir(ext))
        if path.endswith(tuple([".yaml", ".txt"])):
            print('This is a File:', path)
            filepath = f"{stardewPath}\\{path}/"
            #print('THIS IS THE FILEPATH:', filepath)
            allDocs.append(filepath)
            #clean_doc(filepath)
        elif os.path.isdir(ext):
            print('This is a Folder:', ext)
            #print("This is the stuff I want to add to PathList:", os.listdir(ext))
            newPaths = [path + '\\' + x for x in os.listdir(ext)]
            #print("NEWPATHS:", newPaths)
            pathList.extend(newPaths)

    print(allDocs)

findfiles()