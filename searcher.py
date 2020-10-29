import time, json
print("Loading RME source...")
start = time.time()
source_data = open('data.json')
weapons = json.loads(source_data.read())
print(f"Done! Finished reading in {(time.time() - start):.2f}s")
source_data.close()

def findweapon(name, source = weapons):
    for i, weapon in enumerate(weapons):
        if weapon['name'] == name:
            return weapon

def filterweapons(args):
    def mixtraits(weapon):
        alltraits = []
        for training in weapon['propertytable']:
            if training != 'Master Perk':
                for trait in weapon['propertytable'][training]:
                    if not trait in alltraits:
                        alltraits.append(trait)
        return sorted(alltraits)

    filters = {
        'training': None,
        'exclude': [],
        'required': []
    }
    if len(args) == 0: return
    for i, arg in enumerate(args):
        arg = arg.replace('_', ' ')
        if arg in ['Simple', 'Martial', 'Master']:
            filters['training'] = arg
        elif arg.startswith('-'):
            filters['exclude'].append(arg[1:])
        elif arg.startswith('+'):
            filters['required'].append(arg[1:])
    filters['required'].sort()
    filters['exclude'].sort()
    print(filters['required'])
    print(filters['exclude'])

    filtered = []
    for i, weapon in enumerate(weapons):
        traits = []
        if filters['training'] == None or not filters['training'] in weapon['propertytable']:
            traits = mixtraits(weapon)
            #print(f'Mixed {i} = {traits}')
        else:
            traits = weapon['propertytable'][filters['training']]
            #print(f'Filtered {i} = {traits}')
        requirements_met = []
        contains_excluded = False
        for trait in traits:
            if trait in filters['exclude']:
                contains_excluded = True
                break
            if trait in filters['required']:
                requirements_met.append(trait)
        # TODO: Consider using only the len of each of these lists to speed up run time.
        requirements_met.sort()
        if (not contains_excluded) and (requirements_met == filters['required']):
            filtered.append(weapon)
    return filtered

userinput = input()
while userinput != "EXIT":
    args = userinput.split(' ')
    # No switch-case in python :(
    #try:
    if args[0] == 'find':
        if len(args) > 1: 
            filtered = findweapon(args[1:])
            print(filtered)
            
        else: print('Provide the name of the weapon you\'re looking for')
    elif args[0] == 'filter':
        if len(args) > 1:
            filtered = filterweapons(args[1:])
            for weapon in filtered:
                print(weapon['name'])
            print(f'Done! {len(filtered)} weapons meet your criteria.')
        else:
            print('Please provide arguments.')
    else:
        print("Command not known.")
    #except:
    #    print('Something went wrong!')
    userinput = input()