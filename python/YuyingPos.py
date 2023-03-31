import spacy
import pandas as pd
import os
import glob
import string

# nlp = spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')

csv_files = glob.glob(os.path.join("../csv", "*.csv"))
df = pd.DataFrame({"character", "scene", "dialogue"})

for f in csv_files:
    current_df = pd.read_csv(f) # read csv files
    df = pd.concat([df, current_df]) # concat csv files

dialogue = df["dialogue"].to_string() # get all dialogues
dialogue = dialogue.translate(str.maketrans('','',string.punctuation)) # remove punctuation
nlpDialogue = nlp(dialogue)

verb_list = []
adj_list = []
for token in nlpDialogue:
    lemm = token.lemma_
    pos = token.pos_
    if len(lemm) > 2:
        if pos == "VERB":
            verb_list.append(lemm)
        if pos == "ADJ":
            adj_list.append(lemm)

print("VERBs: ", verb_list)
print("ADJs: ", adj_list)
