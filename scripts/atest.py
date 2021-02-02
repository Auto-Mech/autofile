import automol

locs = [
    'InChI=1S/C10H19/c1-3-5-7-9-10-8-6-4-2/h3,5,7H,4,6,8-10H2,1-2H3',
    'InChI=1S/CH4/h1H4', 
    'InChI=1S/C10H20/c1-3-5-7-9-10-8-6-4-2/h3,5H,4,6-10H2,1-2H3/b5-3+',
    'InChI=1S/CH3/h1H3']

for ich in locs:
    print(ich)
    print(automol.inchi.is_complete(ich))

