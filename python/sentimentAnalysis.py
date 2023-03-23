import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from scipy.stats import norm
import seaborn as sns
import matplotlib.pyplot as plt

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Create the instance
sia = SentimentIntensityAnalyzer()

# Load data
df1 = pd.read_csv('..\csv\MainYAML.csv', encoding='utf8')
df2 = pd.read_csv('..\csv\MajorYAML.csv', encoding='utf8')
df = pd.concat([df1, df2])

# Do sentiment analysis
sentiment_scores = df['dialogue'].apply(lambda x: sia.polarity_scores(x))
compound_scores = np.array(sentiment_scores.apply(lambda x: x['compound']))

# Fit a normal distribution to the compound scores
mu, std = norm.fit(compound_scores)
x = np.linspace(-1, 1, 100)
y = norm.pdf(x, mu, std)

# Set the figure size
plt.figure(figsize=(8, 6))

# Create a histogram of sentiment scores
sns.set_style("white") # set the style for the histplot
sns.histplot(compound_scores, bins=15, kde=True, edgecolor='none')
# Plot the fitted normal distribution as a line
plt.plot(x, y, lw=2)

plt.title("Sentiment Analysis Results")
plt.xlabel("Sentiment Score\n(-1: negative, 0: neutral, 1: positive)")
plt.ylabel("Frequency")
# plt.show()

# Save the hist plot as a PNG image
plt.savefig("../dataviz/sentimentAnalysis.png", dpi=300)
