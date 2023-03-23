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
