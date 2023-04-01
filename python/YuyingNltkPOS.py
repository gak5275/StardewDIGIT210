import pandas as pd
import os
import glob
import string
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import nltk
from nltk.stem import WordNetLemmatizer
import re

# nlp = spacy.cli.download("en_core_web_md")
nlp = spacy.load('en_core_web_md')

csv_files = glob.glob(os.path.join("../csv", "*.csv"))
df = pd.DataFrame({"character", "scene", "dialogue"})

for f in csv_files:
    current_df = pd.read_csv(f) # read csv files
    df = pd.concat([df, current_df]) # concat csv files

dialogue = df["dialogue"].to_string() # get all dialogues
dialogue = re.sub('[%s]' % re.escape(string.punctuation.replace('-', '')), ' ', dialogue) # remove punctuation except hyphen

## spacy
# nlpDialogue = nlp(dialogue)
# lemm_tokens = []
# for token in nlpDialogue:
#     lemm = token.lemma_.lower()
#     if len(lemm) > 2 and lemm.isalpha() and lemm not in STOP_WORDS:
#         lemm_tokens.append(lemm)
#

tokens = [token for token in dialogue.split() if len(token) > 2 and token.isalpha() and token not in STOP_WORDS]
lemmatizer = WordNetLemmatizer()
lemm_tokens = [lemmatizer.lemmatize(token) for token in tokens]


pos_tags = nltk.pos_tag(lemm_tokens)

verb_list = []
adj_list = []
for tag in pos_tags:
    if "VBP" in tag or "VB" in tag:
        verb_list.append(tag[0].lower())
    if "JJ" in tag:
        adj_list.append(tag[0].lower())

print("VERBs: ", verb_list)
print("ADJs: ", adj_list)


output = open('POS.txt', 'a')
output.write("\n\n\n====NLTK====")
output.write("\nVERBs: ")
output.write(str(verb_list))
output.write("\nADJs: ")
output.write(str(adj_list))
output.close()
