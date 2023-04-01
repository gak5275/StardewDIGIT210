import yaml
import csv
import glob
import os
import re

comment = re.compile(r'#!.+?\b')
placeholder = re.compile(r'\$\w')
placeholder2 = re.compile(r'%\w+?\b')
onomatopoeia = re.compile(r'\*.+?\*')
action = re.compile(r'[\-\"\d\w\s]+?\/.+?\b')
spaces = re.compile(r'[^\S\r]{2,}')


def converter(directory):
    # convert yaml files to csv files
    yaml_files = glob.glob('..\\RawYAMLFiles\\'+ directory +'\\*.yaml')
    rows = []
    for each_file in yaml_files:
        with open(each_file, encoding = 'utf8') as yaml_file:
            filename = yaml_file.name.split('\\')[::-1][0].replace('MarriageDialogue','')
            # load data from yaml file
            data = yaml.safe_load(yaml_file)

            character = filename.split('.')[0]
            for key, value in data['content'].items():
                scene = key
                dialogue = ''.join(str(element) for element in value)
                dialogue = comment.sub('',dialogue) # remove #!String
                dialogue = placeholder.sub(' ',dialogue) # remove placeholder such as $e, $8
                dialogue = placeholder2.sub(' ',dialogue) # remove placeholder such as %kid1
                dialogue = action.sub(' ',dialogue) # remove action such as
                dialogue = onomatopoeia.sub(' ',dialogue) # remove onomatopoeia such as *sigh*
                dialogue = spaces.sub(' ',dialogue)
                row = {'character':character, 'scene':scene, 'dialogue':dialogue}
                rows.append(row)
                # print(row)

    csv_path = '..\\csv\\' + directory.split('\\')[-1] + '.csv'
    mode = 'w' if os.path.exists(csv_path) else 'x'
    with open(csv_path, mode, newline='', encoding='utf-8') as f:
        header = ['character', 'scene', 'dialogue']
        csv_writer = csv.DictWriter(f, fieldnames=header)
        csv_writer.writeheader()
        csv_writer.writerows(rows)


print(">>>Start to convert YAML files to CSV files<<<")
directoryList= ['ExtraFiles\\MinorYAML','ExtraFiles\\NonDialogueYAML','FestivalsYAML','LocationsYAML','MainYAML','MajorYAML','MiscYAML']
for directory in directoryList:
    converter(directory)
    print(directory.split('\\')[-1], "is done.")
print(">>>Converting is completed!<<<")