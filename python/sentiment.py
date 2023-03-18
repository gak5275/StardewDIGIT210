import yaml
import csv
import glob
import os

def convertor(directory):
    # convert yaml files to csv files
    yamlFiles = glob.glob('..\\StardewText\\RawYAMLFiles\\'+ directory +'\\*.yaml')
    rows = []
    for eachFile in yamlFiles:
        with open(eachFile, encoding = 'utf8') as yamlFile:
            filename = yamlFile.name.split('\\')[::-1][0].replace('MarriageDialogue','')
            # load data from yaml file
            data = yaml.safe_load(yamlFile)

            character = filename.split('.')[0]
            for key, value in data['content'].items():
                scene = key
                dialogue = ''.join(str(element) for element in value.split('#')[::-1])
                row = {'character':character, 'scene':scene, 'dialogue':dialogue}
                rows.append(row)
                # print(row)

    csvPath = '..\\csv\\' + directory.split('\\')[-1] + '.csv'
    mode = 'w' if os.path.exists(csvPath) else 'x'
    with open(csvPath, mode, newline='', encoding='utf-8') as f:
        header = ['character', 'scene', 'dialogue']
        csv_writer = csv.DictWriter(f, fieldnames=header)
        csv_writer.writeheader()
        csv_writer.writerows(rows)

directoryList= ['ExtraFiles\\MinorYAML','ExtraFiles\\NonDialogueYAML','FestivalsYAML','LocationsYAML','MainYAML','MajorYAML','MiscYAML']
for directory in directoryList:
    convertor(directory)