# method from: https://github.com/priya-dwivedi/Deep-Learning/blob/master/topic_modeling/LDA_Newsgroup.ipynb
import spacy
import pandas as pd
import gensim
import nltk
from nltk.stem import SnowballStemmer

nlp = spacy.load("en_core_web_sm")
nltk.download('wordnet')
stemmer = SnowballStemmer('english')
# load data
df1 = pd.read_csv('..\csv\MainYAML.csv', encoding='utf8')
df2 = pd.read_csv('..\csv\MajorYAML.csv', encoding='utf8')

allDocs = [df1, df2]

def clean_doc(doc):
    # lemmatization
    dialogue = doc["dialogue"].to_string()
    lemmatized_tokens = []
    doc = nlp(dialogue)
    for token in doc:
        if token.is_alpha:
            lemmatized_tokens.append(token.lemma_)
    lemmatized_tokens = ' '.join(lemmatized_tokens)
    # tokenization
    tokens = []
    for token in gensim.utils.simple_preprocess(lemmatized_tokens):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            tokens.append(token)
    return tokens

clean_docs = [clean_doc(doc) for doc in allDocs]

# generate bag of words
dict = gensim.corpora.Dictionary(clean_docs)
corpus = [dict.doc2bow(tokens) for tokens in clean_docs]
bow_doc_x = corpus[1]
for i in range(len(bow_doc_x)):
    print("Word {} (\"{}\") appears {} time.".format(bow_doc_x[i][0],
                                                     dict[bow_doc_x[i][0]],
                                                     bow_doc_x[i][1]))

# LDA
lda_model = gensim.models.LdaModel(corpus,
                                   num_topics = 5,
                                   id2word = dict,
                                   passes = 10)

for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic ))
    print("\n")

'''

Topic: 0 
Words: 0.002*"like" + 0.002*"good" + 0.001*"think" + 0.001*"today" + 0.001*"feel" + 0.001*"look" + 0.001*"know" + 0.001*"guess" + 0.001*"time" + 0.001*"want"


Topic: 1 
Words: 0.025*"like" + 0.016*"good" + 0.015*"think" + 0.014*"know" + 0.014*"look" + 0.013*"feel" + 0.012*"today" + 0.011*"want" + 0.010*"time" + 0.009*"guess"


Topic: 2 
Words: 0.001*"like" + 0.001*"think" + 0.001*"know" + 0.001*"good" + 0.001*"look" + 0.001*"today" + 0.001*"maybe" + 0.001*"time" + 0.001*"want" + 0.001*"feel"


Topic: 3 
Words: 0.001*"like" + 0.001*"think" + 0.001*"know" + 0.001*"look" + 0.001*"feel" + 0.001*"good" + 0.001*"want" + 0.001*"today" + 0.001*"time" + 0.001*"guess"


Topic: 4 
Words: 0.001*"like" + 0.001*"good" + 0.001*"know" + 0.001*"feel" + 0.001*"look" + 0.001*"think" + 0.001*"tell" + 0.001*"want" + 0.001*"little" + 0.001*"need"

'''