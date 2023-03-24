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


stop_words = stopwords.words('english')

newStopWords = ["said", "one", "go", "went", "came", "like", "one"]
stop_words.extend(newStopWords)

workingDir = os.getcwd()
print('THIS IS WORKING DIRECTORY', workingDir)
parentDir = workingDir.removesuffix('python')
stardewPath = os.path.join(parentDir, 'xmlfiles')
print('THIS IS THE FILEPATH FOR ALL FILES', stardewPath)

# cleaning documents:
def clean_doc(doc):
    print("RUNNING CLEANDOC")
    print("THIS IS THE DOC: ", doc)
    with PySaxonProcessor(license=False) as proc:
        xml = open(doc, encoding='utf-8').read()

        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=xml)
        xp.set_context(xdm_item=node)

        text = xp.evaluate('//dialogue ! text()')
        dialogue = text.__str__()
    #print("THIS IS THE DIALOGUE", dialogue)
    print("Class of dialogue", type(dialogue))
    no_punct = ''
    for c in dialogue:
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

# ebb: This controls our file handling as a for loop over the directory:
allDocs = []
#print('THIS IS ALL DOCS', allDocs)
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
#print(allDocs)

# PREPARING THE CORPUS FOR TOPIC MODELING ########################
cleaned_docs = [clean_doc(doc) for doc in allDocs]
# Add bigrams and trigrams to docs (only ones that appear 20 times or more).
#print(cleaned_docs)
bigram = Phrases(cleaned_docs, min_count=20)
for idx in range(len(cleaned_docs)):
    for token in bigram[cleaned_docs[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            cleaned_docs[idx].append(token)

#print(cleaned_docs)

# ebb: We used this code to help us locate buggy text files. It will stop on files that can't be processed due to weird non-Unicode characters.
# cleaned_docs = []
# for doc in allDocs:
#     print("This doc is going to the cleaners: " + f"{doc=}")
#     clean_doc(doc)

id2word = corpora.Dictionary(cleaned_docs)

# print(id2word[260])
corpus = [id2word.doc2bow(cleaned_doc) for cleaned_doc in cleaned_docs]
#print("THIS IS THE CORPUS", corpus)


lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=30)
# Suggestion: Try 10 - 50 topics and vary in 5s
topics = lda_model.get_document_topics(corpus)
print("Number of topics:", len(topics))
sorted_topics = sorted(topics[1], key=lambda x: x[1], reverse=True)

# ebb: So, let's see what's in a topic:
for topic in topics[1][:10]:
    #print(f"{topic=}")
    # if topic[1] > .5:
    # This asks for up to 10 topics in document 209. It'll be fine if 10 topic clusters aren't really available there.
    terms = lda_model.get_topic_terms(topic[0], 15)
    # topic[0] is not the same as topics. (topics are documents). topic is an actual topic.
    # topic[0] is probably the heaviest weighted "top" topic.
    for num in terms:
        num = num[0]
        #print(num, id2word[num])
    #print()

# ###### VISUALIZING THE TOPIC MODELS ####################
# ebb: We're using the pyLDAvis (python LDA topic modeling vis) library to output an HTML file
# that shows an interactive visualization. It will output an HTML file in your working directory.
# You want to go and open that file in a web browser to view the model and adjust it.
# HOW TO READ THE LDA Visualization:
# See https://we1s.ucsb.edu/research/we1s-tools-and-software/topic-model-observatory/tmo-guide/tmo-guide-pyldavis/
# As you inspect the visualization, you should come back to this script and
# experiment with adding stop words and adjusting the number of topics to model.
vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word, mds="mmds", R=30)
pyLDAvis.save_html(vis, 'topicModel_Visualization.html')




