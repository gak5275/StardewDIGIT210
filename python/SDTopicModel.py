# ####################################################
# This is the intro to topic modeling code that has been modified for our purposes.
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

# ############ STOP WORDS AND PUNCTUATION CUSTOMIZED HERE ###################
stop_words = stopwords.words('english')
print(f"{stop_words=}")
print(f"{string.punctuation=}")

# ADDING WORDS TO THE STOP WORD LIST
# stop_words = stop_words.append("said", "would", "one", "could", "even", "like", "get", "got", "really", "also")
#OR
#newStopWords = ["would", "one", "could", "even", "like", "get", "got", "really", "also", "called", "didn't", "didnt", "still", "i'm", "im", "well", "us", "many", "much"]
#stop_words.extend(newStopWords)
#print("UPDATED: " + f"{stop_words=}")
# ##################################################################

# Set up to read our file directory ###
#Variable with current dir
workingDir = os.getcwd()
#Edit current string by lopping off the end with '/python'
parentDir = re.sub('python', '', workingDir)
#Add the directory ending that we want to get all files from
stardewPath = os.path.join(parentDir, 'StardewText')
#print('StardewText Path:', stardewPath)

# cleaning documents:
def clean_doc(doc):
    text = open(doc, encoding='utf-8').read()
    no_punct = ''
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

    # with list comprehension
    # final_words = [word for word in words if word not in stop_words]
    return final_words

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
        #print(ext, path.endswith(".txt"), os.path.isdir(ext))
        if path.endswith(".txt")):
            print('This is a File:', path)
            filepath = f"{stardewPath}\\{path}\\"
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

# PREPARING THE CORPUS FOR TOPIC MODELING ########################
cleaned_docs = [clean_doc(doc) for doc in allDocs]
id2word = corpora.Dictionary(cleaned_docs)

# print(id2word[260])
corpus = [id2word.doc2bow(cleaned_doc) for cleaned_doc in cleaned_docs]
# print(corpus)

# Show the words and numbers in just the first document:
# for num in corpus[0]:
#     num = num[0]
#     print(f"{num}\t{id2word[num]}")

# TOPIC MODELING with LDA ########################
# ebb: Here in the next line, we set the parameters for LDA topic modeling.
# This is sometimes compared to rolling dice, because we start the process by
# predicting the number of topics we expect to see in the results.
# You can take this backwards and forwards and see how it affects the distribution and
# assignment of topics in the corpus. The num_topics is the parameter you keep adjusting.
# In this assignment I'd like you to:
#   * Try a few different num_topics and notice how that changes
# your results. Find a number you think works well for showing topics in this corpus.
#   * Also, I'd like you to experiment with adjusting the stop_words list (above) when you see a lot
# of the same words repeating across topics.
lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=15)
# Suggestion: Try 10 - 50 topics and vary in 5s
topics = lda_model.get_document_topics(corpus)
print(f"{len(topics)=}")
# ebb: len(topics) appears to be the number of documents. There are
# 209 documents in the Grimm collection.
print(f"{topics[58]=}")
# topics[208] represents the topics in document 209. Remember why?
# Notice our format string: called "f-printing":
# This comes out:
# topics[208]=[(20, 0.11845379), (66, 0.015097282), (74, 0.118847124), (76, 0.31761664), (82, 0.42932528)]
# Topics is a dictionary with the keys as the document numbers and values are the
# list of topics for that document. The values are tuples: (Topic number, weight of topic).
# HEY, don't we want to sort these by weight?
sorted_topics = sorted(topics[58], key=lambda x: x[1], reverse=True)
# This says, sort the topics, and the sort key is x, and then you'll get the second member
print(f"{sorted_topics=}")
# ebb: Notice, every time we run this, we get a different random assortment of topics present in the document we chose.
# Our returns here are a sign of the randomization built into LDA topic modeling!

# ebb: So, let's see what's in a topic:
for topic in topics[58][:10]:
    # This asks for up to 10 topics in document 209. It'll be fine if 10 topic clusters aren't really available there.
    terms = lda_model.get_topic_terms(topic[0], 20)
    # topic[0] is not the same as topics. (topics are documents). topic is an actual topic.
    # topic[0] is probably the heaviest weighted "top" topic.
    print(topic)
    for num in terms:
         num = num[0]
         print(num, id2word[num])
    print()

# ###### VISUALIZING THE TOPIC MODELS ####################
# ebb: We're using the pyLDAvis (python LDA topic modeling vis) library to output an HTML file
# that shows an interactive visualization. It will output an HTML file in your working directory.
# You want to go and open that file in a web browser to view the model and adjust it.
# Then come back to this script and experiment with adding stop words and adjusting the number of
# topics to model.
vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word, mds="mmds", R=50)
pyLDAvis.save_html(vis, 'topicModel_Visualization.html')




