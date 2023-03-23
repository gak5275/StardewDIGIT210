# method from: https://www.section.io/engineering-education/nlp-based-detection-model-using-neattext-and-scikit-learn/
import pandas as pd

# Load data
df1 = pd.read_csv('..\csv\MainYAML.csv', encoding='utf8')
df2 = pd.read_csv('..\csv\MajorYAML.csv', encoding='utf8')
df = pd.concat([df1, df2])