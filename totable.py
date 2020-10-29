# Run this script to rewrite and update data.json from source.txt. Feel free to mess around with the settings to accomodate this for other data structures.
# TODO: Documentation?
import json
source = open('source.txt', errors = 'replace')

weapons = []
readingtable = False

try:
    for i, line in enumerate(source):
        print(f'\r{((i+1)/1939*100):.0f}%', end = '', flush = True)
        if line.startswith('####'):
            weapon = {'name':line[5:-1].strip()}
            weapons.append(weapon)
            readingtable = False
            continue
        elif line == '|:--|:--|\n':
            weapons[-1]['propertytable'] = {}
            readingtable = True
        elif readingtable and line.startswith('| ') and 'propertytable' in weapons[-1]:
            training = line[2:line.index(' |')]
            if training == "Master Perk":
                weapons[-1]['propertytable'][training] = line[(4 + len(training)):-2].strip()
            else:
                weapons[-1]['propertytable'][training] = line[(4 + len(training)):-2].split(', ')
                for trait in weapons[-1]['propertytable'][training]:
                    trait = trait.strip()
        else:
            readingtable = False
except:
    print(f'Crashed on line {i}!')
    exit()

print()
source.close()
print('Done reading.')
#print(weapons)

f = open('RME searcher\data.json', 'w')
weapons_json = json.dumps(weapons, indent = 4)
chars_written = f.write(weapons_json)
print(f'{chars_written} characters written.')
f.close()