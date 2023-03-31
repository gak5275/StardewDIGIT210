import spacy
# nlp = spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')

text = open('pythonfiles/txtfiles/Abigail.txt', 'r', encoding='utf8')
words = text.read()
wordstrings = str(words)
# print(wordstrings)

text = nlp(wordstrings)
for token in text:
    print(token.text, "---->", token.pos_, ":::::", token.lemma_)