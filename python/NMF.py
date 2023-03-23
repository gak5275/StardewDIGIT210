from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from nltk.stem import WordNetLemmatizer
import pandas as pd
import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Load data
df1 = pd.read_csv('..\csv\MainYAML.csv', encoding='utf8')
df2 = pd.read_csv('..\csv\MajorYAML.csv', encoding='utf8')
df = pd.concat([df1,df2])

# Preprocess data
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = [lemmatizer.lemmatize(word) for word in text.split()]
    # Remove stop words
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words and len(word) > 3]
    # Join words back into a string
    return ' '.join(words)

preprocess_text = df['dialogue'].apply(preprocess_text)

vectorizer = TfidfVectorizer(max_features=1000, max_df=0.5, min_df=3, stop_words='english')
X = vectorizer.fit_transform(preprocess_text)

# Train NMF model
num_topics = 10
nmf_model = NMF(n_components=num_topics, random_state=42)
nmf_model.fit(X)

# Print top words for each topic
feature_names = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(nmf_model.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]))
