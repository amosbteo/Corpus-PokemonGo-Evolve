# -*- coding: utf-8 -*-
"""
"Evolve" concordance

@author: amosbteo

"""
# Import data
from nltk import corpus
from nltk.text import Text

corpus_root = 'data/'
raw = corpus.PlaintextCorpusReader(corpus_root, '.*')
raw.fileids()
test = raw.words()
text = Text(test)
text.concordance('evolve')

# Get indices of all 'evolve' followed by 'a'
evolve_set = set(['evolve', 'evolved'])
indices = [w for w, x in enumerate(text) if x in evolve_set]

#indices = [w for w, x in enumerate(text) if x == "evolve"]
print(indices)
evolve_list1 = [text[i] for i in indices]
evolve_list2 = [text[i+1] for i in indices]
evolve_list3 = [text[i+2] for i in indices]
evolve_list = list(map(list, zip(evolve_list1, evolve_list2, evolve_list3))) # Create list of word token lists

# Import dictionary with pokemon name and evolution stage
# 1,2,3 -> 3-stage evolution; A,B -> 2-stage evolution; 0 -> no evolution
# Ignore mega-evolutions: 4, C, 0.5
import pandas as pd

pokename = pd.read_csv('pokemon.csv', header=0)
pokename.head()
pokedict = dict(zip(pokename['Name'].str.lower(), pokename['Evolution']))
pokenames = set(pokename['Name'].str.lower())


# Get list of evolved pokemon and only keep examples of pokemon names

# Get list of pokemon from frame 'evolve [pokemon]'
evolved_listA = [x[1].lower() for x in evolve_list]
evolved_listB = [x for x in evolved_listA if x in pokenames]

# Get list of pokemon from frame 'evolve a/an [pokemon]'
condition1 = set(['a', 'an'])
evolve_a_list = [x for x in evolve_list if x[1] in condition1]
evolved_pokemon_list0 = [x[2].lower() for x in evolve_a_list]
evolved_pokemon_list1 = [x for x in evolved_pokemon_list0 if x in pokenames]

# Combine lists
evolved_pokemon_list_combine = evolved_listB + evolved_pokemon_list1

# Get frequency count
from collections import Counter
evolved_pokemon_list_all = [str(r) for r in evolved_pokemon_list_combine]
len(evolved_pokemon_list_all)
counts = Counter(evolved_pokemon_list_all)
print(counts)
#with open("output/evolve_pokemon.txt", "w") as output:
#    output.write(str(counts1))
    

# Map pokemon dictionary to list to show evolution stage
evolution_stage = map(pokedict.get, evolved_pokemon_list_all)

# Get frequency information
stage3 = set(['1','2','3'])
stage2 = set(['A', 'B'])

evolution_stage_dict = zip(evolved_pokemon_list_all, map(pokedict.get, evolved_pokemon_list_all))
counts2 = Counter(evolution_stage_dict)
print(counts2)

cols = [(k[0], k[1], v) for k, v in counts2.items()] # where p_counter is your Counter object
evolve_df = pd.DataFrame(cols, columns=["Pokemon", "Stage", "Count"])

# Get frequency counts for each evolution stage
counts_by_stage = evolve_df.groupby('Stage').sum().reset_index()
counts_by_stage
len(evolution_stage)

# Get frequency counts by pokemon
for name, group in evolve_df.groupby('Stage'):
    print(group)

evolve_df.to_csv(r'output/evolve_pokemon.csv')
