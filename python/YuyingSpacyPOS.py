import spacy
import pandas as pd
import os
import glob
import string
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

output = open('POS.txt', 'a')
output.write("\n\n\n====SPACY====")
output.write("\nVERBs: ")
output.write(str(verb_list))
output.write("\nADJs: ")
output.write(str(adj_list))
output.close()
