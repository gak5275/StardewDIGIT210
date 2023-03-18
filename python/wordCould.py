# method from: https://github.com/bryan-md/wordcloud/blob/main/wordcloud.ipynb
import spacy
import pandas as pd
import numpy as np
from collections import Counter
from wordcloud import WordCloud
from spacy.lang.en.stop_words import STOP_WORDS
import matplotlib.pyplot as plt

def generate_wordcloud(word_freq):
    # a list of non-string values to exclude
    exclude_list = [None, [], {}, set()]
    full_dict = {}
    for key in word_freq:
        if isinstance(key, str):
            if key not in exclude_list:
                full_dict[key] = word_freq[key]
    wordcloud = WordCloud(background_color='white',
                          max_words=150,
                          height=600,
                          width=1200).generate_from_frequencies(full_dict)
    return wordcloud

# main
# load spacy
nlp = spacy.load("en_core_web_sm")
# load data
df1 = pd.read_csv('..\csv\MainYAML.csv', encoding='utf8')
df2 = pd.read_csv('..\csv\MajorYAML.csv', encoding='utf8')
df = pd.concat([df1,df2], ignore_index=True)

# spacy lemmatization
def lemmatize_text(text):
    doc = nlp(text)
    lemmatized_tokens = ' '.join([token.lemma_ for token in doc])
    return lemmatized_tokens

text = df['dialogue'].apply(lemmatize_text)
text = ' '.join(text)

# update stopwords
extra_stopwords={'think','don\'t', 'going', 'know', 'feel', 'you\'re', 'i\'ve',
                 'isn\'t', 'i\'ll', 'feel', 'want', 'maybe', 'need', 'sure',
                 'guess', 'little', 'live', 'look', 'thing', 'start', 'smell',
                 'today', 'tomorrow', 'right', 'year', 'tell', 'sound', 'ei\'m',
                 'people', 'come', 'remember', 'change', 'sorry', 'place', 'sigh',
                 'close', 'long', 'hear', 'understand', 'tonight'
                 }
STOP_WORDS.update(extra_stopwords)

# create the WordCloud object
wordcloud = WordCloud(stopwords = STOP_WORDS, background_color='white',
                      collocations=True,
                      min_word_length=4,
                      max_words=150,
                      collocation_threshold=10).generate(text)
# count the frequency of words in the WordCloud
text1_dict = Counter(wordcloud.process_text(text))
# Count the frequency of words in the original dialogue column
text2_dict = Counter(df.loc[:4000]['dialogue'].str.lower().str.split(expand=True).stack().value_counts())

# find the most common word frequency from the first dictionary
# and divide by the most common word frequency in the second dictionary
multiplier = text1_dict.most_common(1)[0][1] / text2_dict.most_common(1)[0][1]

# multiply the value in dictionary 2, by the mutiplier above to make
# the top value equal to the first dictionary. Use subsequently smaller values of the multiplier
text2_dict = {k: int(k[1] * v) for k, v in zip(text2_dict.items(), np.linspace(multiplier, 1, 4000))}

# combine the two dictionaries
full_dict = Counter(text1_dict) + Counter(text2_dict)

# create the WordCloud image
wordcloud = generate_wordcloud(full_dict)
# display the WordCloud image
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud, interpolation='bilInear')
plt.axis('off')
plt.show()

# save the word cloud as a PNG image
plt.savefig("wordcloud.png", dpi=300)