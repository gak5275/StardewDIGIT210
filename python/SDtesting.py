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
from gensim.models import Phrases
import os
import re
import saxonche

workingDir = os.getcwd()
parentDir = re.sub('python', '', workingDir)
stardewPath = os.path.join(parentDir, 'StardewText')


# cleaning documents:
def clean_doc(doc):
    print("RUNNING CLEANDOC")
    print("THIS IS THE DOC INSIDE OF CLEAN_DOC", doc)
    text = open(doc).read()
    no_punct = ''
    dialogue = doc.evaluate_single('(?<=(<dialogue>))(.+)(?=(</dialogue>))')
    print("THIS IS THE DIALOGUE:", dialogue)
    for c in text:
        if c not in string.punctuation:
            no_punct = no_punct + c
    # with list comprehension
    # no_punct = ''.join([c for c in doc if c not in string.punctuation])

    words = no_punct.lower().split()

    final_words = []
    for word in words:
        if word not in stop_words:
            final_words.append(word)

    return final_words


#ws: return all files nested infinitely in folders

#define function findfiles
    #make a variable PATHLIST with the list with the filepaths from StardewText
    #make a variable editing the above with the list of all full paths
    #for each filepath in the list:
        #variable ext = the filepath + the name of it's appropriate file/folder
        #if ext ends with txt or yaml
            #add the small path to filepath
        #else, if the full path is a folder
            #variable = list of filepaths for each thing in folder
            #add list of filepaths to PATHLIST

allDocs = []
def findfiles():
    print("RUNNING FINDFILES")
    pathList = os.listdir(stardewPath)
    for path in pathList:
        #print('THIS IS PATHLIST: \n ------------', pathList)
        ext = f"{stardewPath}\{path}"
        #print(ext, path.endswith(".xml"), os.path.isdir(ext))
        if path.endswith(".xml"):
            filepath = f"{stardewPath}\\{path}/"
            print('THIS IS THE FILEPATH:', filepath)
            allDocs.append(filepath)
            print("THIS IS THE ALL DOCS:", allDocs)
            clean_doc(filepath)
        elif os.path.isdir(ext):
            #print('This is a Folder:', ext)
            #print("This is the stuff I want to add to PathList:", os.listdir(ext))
            newPaths = [path + '\\' + x for x in os.listdir(ext)]
            #print("NEWPATHS:", newPaths)
            pathList.extend(newPaths)

    print(allDocs)


# cleaned_docs = []
cleaned_docs = [clean_doc(doc) for doc in allDocs]
#cleaned_docs = []
#for doc in allDocs:
#    print("This doc is going to the cleaners: " + f"{doc=}")
#    cleaned = clean_doc(doc)
#    cleaned_docs.append(cleaned)
#id2word = corpora.Dictionary(cleaned_docs)

bigram = Phrases(cleaned_docs, min_count=20)
for idx in range(len(cleaned_docs)):
    for token in bigram[cleaned_docs[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            cleaned_docs[idx].append(token)

id2word = corpora.Dictionary(cleaned_docs)

corpus = [id2word.doc2bow(cleaned_doc) for cleaned_doc in cleaned_docs]
print("THIS IS THE CORPUS", corpus)

lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=30)

topics = lda_model.get_document_topics(corpus)
sorted_topics = sorted(topics[208], key=lambda x: x[1], reverse=True)

for topic in topics[208][:10]:
    #print(f"{topic=}")
    terms = lda_model.get_topic_terms(topic[0], 15)
    for num in terms:
        num = num[0]
        #print(num, id2word[num])
    #print()

#vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word, mds="mmds", R=30)
#pyLDAvis.save_html(vis, 'topicModel_Visualization.html')
