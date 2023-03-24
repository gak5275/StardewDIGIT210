# ####################################################
# PIP INSTALLS TO MAKE FOR NLTK LDA TOPIC MODELING
# pip install gensim
# pip install pyldavis
# pip install nltk
# pip install ipython
# pip install saxonche
# ####################################################
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
import gensim.corpora as corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models
from gensim.models import Phrases
from saxonche import PySaxonProcessor
import os


# Stopwords
stop_words = stopwords.words('english')

newStopWords = []
stop_words.extend(newStopWords)

workingDir = os.getcwd()
parentDir = workingDir.removesuffix('python')
stardewPath = os.path.join(parentDir, 'xmlfiles')
print('WORKING DIRECTORY:', workingDir)
print('FILEPATH:', stardewPath)


# Clean the Documents:
def clean_doc(doc):
    print("RUNNING CLEANDOC")
    print(doc)
    with PySaxonProcessor(license=False) as proc:
        xml = open(doc, encoding='utf-8').read()

        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=xml)
        xp.set_context(xdm_item=node)

        text = xp.evaluate('//dialogue ! text()')
        dialogue = text.__str__()
    no_punct = ''
    for c in dialogue:
        if c not in string.punctuation:
            no_punct = no_punct + c

    words = no_punct.lower().split()

    final_words = []
    for word in words:
        if word not in stop_words:
            final_words.append(word)

    return final_words


# Finding the Files
allDocs = []
print('THIS IS OS.LISTDIR LIST:', os.listdir(stardewPath))

fileList = os.listdir(stardewPath)
for file in fileList:
    f = f"{stardewPath}\{file}"
    if file.endswith(".xml"):
        print("This is a File:", f)
        filepath = f"{stardewPath}/{file}"
        allDocs.append(filepath)
        clean_doc(filepath)
    elif os.path.isdir(f):
        print('This is a Folder:', f)
        newFiles = [file + '\\' + x for x in os.listdir(f)]
        fileList.extend(newFiles)


# Preparing Corpus
cleaned_docs = [clean_doc(doc) for doc in allDocs]
bigram = Phrases(cleaned_docs, min_count=20)
for idx in range(len(cleaned_docs)):
    for token in bigram[cleaned_docs[idx]]:
        if '_' in token:
            cleaned_docs[idx].append(token)

id2word = corpora.Dictionary(cleaned_docs)
corpus = [id2word.doc2bow(cleaned_doc) for cleaned_doc in cleaned_docs]

lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=30)
topics = lda_model.get_document_topics(corpus)
print("Number of topics:", len(topics))
sorted_topics = sorted(topics[1], key=lambda x: x[1], reverse=True)


# Create the Visualization
vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word, mds="mmds", R=30)
pyLDAvis.save_html(vis, 'topicModel_Visualization.html')
print("Visual Outputted")