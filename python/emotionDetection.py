import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import pandas as pd
from matplotlib.ticker import MaxNLocator

# Load data
df1 = pd.read_csv('..\csv\MainYAML.csv', encoding='utf8')
df2 = pd.read_csv('..\csv\MajorYAML.csv', encoding='utf8')
df = pd.concat([df1, df2])
lemmatizer = WordNetLemmatizer()
def preprocess_text(text):
    words = [lemmatizer.lemmatize(word) for word in text.split()]
    # Remove stop words
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    # Join words back into a string
    return ' '.join(words)

preprocess_text = df['dialogue'].apply(preprocess_text)
preprocess_text = ' '.join(preprocess_text)
preprocess_text = preprocess_text.translate(str.maketrans('','',string.punctuation))
tokens = word_tokenize(preprocess_text)

clean = []
for token in tokens:
    if token not in stopwords.words('english'):
        clean.append(token)

emotions = []
with open('emotion.txt','r') as file:
    for i in file:
        text = i.strip().replace(' ','').replace(',','').replace('\'','')
        word, emotion = text.split(':')
        if word in clean:
            emotions.append(emotion)

emotions_counter = Counter(emotions)


# sort the data
x = list(emotions_counter.keys())
y = list(emotions_counter.values())

data = pd.DataFrame({'emotion': x,'number': y})
data_sorted = data.sort_values('number', ascending = False)

plot, ax= plt.subplots(figsize=(9,6))
ax.set_xticks(range(len(x)))
ax.set_xticklabels(x, rotation=25, fontsize=7, ha='right')
sns.barplot(x='emotion', y='number', data=data_sorted,
            order=data_sorted.emotion, ax=ax)
plt.title("Emotion Detection")

# plt.show()

# Save the bar plot as a PNG image
plt.savefig("../dataviz/emotionDetection.png", dpi=300)