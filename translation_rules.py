import sys
import time
import pandas as pd

from pyPRUF.fuzzy_logic import FuzzyAnd, LinguisticModifiers
from pyPRUF.fuzzy_set import *
from pyPRUF.membership_functions import *
from fake_data import get_fake_people_df

# Creiamo un dizionario con altezze da 140 cm a 210 cm e gradi di appartenenza 
tall_fun =  Trapezoidal(a=160.0, b=180.0, c=sys.float_info.max, d=sys.float_info.max)
tall_dict = { (height,): tall_fun(float(height)) for height in range(161, 211) }
tall_fs = DiscreteFuzzySet(('Heights_cm', ), tall_dict)

# Creiamo un dizionario con età da 1 a 100 e gradi di appartenenza 
young_fun =  Trapezoidal(a=-1.0, b=0.0, c=20.0, d=50.0)
young_dict = { (age,): young_fun(float(age)) for age in range(1, 50) }
young_fs = DiscreteFuzzySet(('Ages', ), young_dict)

intelligent_fs = DiscreteFuzzySet(('Names', ), {('Carol', ): 0.65, ('John', ): 0.85, ('Pitt', ): 0.35})

# Create a dictionary with the people data
data = {
    'Names': ['Mario Rossi', 'Luigi Bianchi', 'Anna Verdi', 'Giulia Neri', 'Marco Gialli'],
    'Ages': [34, 28, 45, 38, 50],
    'Genders': ['Male', 'Male', 'Female', 'Female', 'Male'],
    'Heights_cm': [175, 180, 165, 170, 160],
    'Weights_kg': [70, 85, 60, 65, 72],
    'Cities': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo']
}

# df = get_fake_people_df(20)
df = pd.DataFrame(data)
people_fs = DiscreteFuzzySet(data=df)

small_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=-sys.float_info.max, b=-sys.float_info.max, c=10.0, d=20.0))
several_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=1.0, b=10.0, c=sys.float_info.max, d=sys.float_info.max))
most_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=0.2, b=0.65, c=0.99, d=1.0))
true_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=0.35, b=0.75, c=1.1, d=1.2))
likely_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=0.35, b=0.75, c=1.1, d=1.2))

prob = Bell(0.0, 5.0) # simulazione di una distribuzione di probabilità qualsiasi

print(people_fs.get_tabular_str() + '\n')
# print(tall_fs.get_tabular_str())
# print(young_fs.get_tabular_str())

# Query1: Most people are tall

start_time = time.time()

tall_people = people_fs @ tall_fs
prop = tall_people.mean_cardinality()
result = most_fs[prop]

elapsed_time = time.time() - start_time
print("Query1: 'Most people are tall' =================\n")
print(tall_people.get_tabular_str()) 
print("mean_cardinality(TALL_PEOPLE) = ", prop)
print("MOST(" + str(prop) + ") =", result)
print(f"\nElapsed time: {elapsed_time} seconds")

# Query2: Most males are tall

start_time = time.time()

males_tall = tall_people.particularization({'Genders': 'Male'})
prop = males_tall / tall_people
result = most_fs[prop]

elapsed_time = time.time() - start_time

print("Query2: 'Most males are tall' =================\n")
print(males_tall.get_tabular_str()) 
print("proportion(MALES_TALL / TALL_PEOPLE) = ", prop)
print("MOST(" + str(prop) + ") =", result)
print(f"\nElapsed time: {elapsed_time} seconds")

# Query3: Most young people are tall

start_time = time.time()

young_and_tall_people = tall_people @ young_fs
prop = young_and_tall_people / tall_people
result = most_fs[prop]

elapsed_time = time.time() - start_time

print("Query: 'Most young people are tall' =================\n")
print(young_and_tall_people.get_tabular_str())
print("proportion(YOUNG_AND_TALL_PEOPLE / TALL_PEOPLE) = ", prop)
print("Most(" + str(prop) + ") =", result)
print(f"\nElapsed time: {elapsed_time} seconds")

# Query4: Most young boys are tall

start_time = time.time()

young_and_tall_boys = young_and_tall_people.particularization({'Genders': 'Male'})
prop = young_and_tall_boys / young_and_tall_people
result = most_fs[prop]

elapsed_time = time.time() - start_time

print("Query: 'Most young boys are tall' =================\n")
print(young_and_tall_boys.get_tabular_str())
print("Prop(YOUNG_AND_TALL_BOYS / YOUNG_AND_TALL_PEOPLE) = ", prop)
print("Most(" + str(prop) + ") =", result)
print(f"\nElapsed time: {elapsed_time} seconds")

# Query5: Most tall people are young

start_time = time.time()

young_people = people_fs @ young_fs
prop = young_and_tall_people / young_people
result = most_fs[prop]

elapsed_time = time.time() - start_time
print("Query: 'Most tall people are young' =================\n")
print(young_people.get_tabular_str())
print("Prop(YOUNG_AND_TALL_PEOPLE / YOUNG_PEOPLE) = ", prop)
print("Most(" + str(prop) + ") =", result)
print(f"\nElapsed time: {elapsed_time} seconds")

# Query6: Carol is very intelligent is very likely
start_time = time.time()

very_inte_carol = LinguisticModifiers.VERY(intelligent_fs[('Carol', )])
result = likely_fs[very_inte_carol * prob(intelligent_fs[('Carol', )])]
result = LinguisticModifiers.VERY(result)

elapsed_time = time.time() - start_time
print("Query: 'Carol is very intelligent is very likely' =================\n")
print(intelligent_fs.get_tabular_str())
print("Result =", result)
print(f"\nElapsed time: {elapsed_time} seconds")
# plot_function(prob, x_range=(0, 1), title="prob_intelligent_carol")

# Query7: X is small is very true is likely

start_time = time.time()

x = -5.0
result = likely_fs[prob(x) * LinguisticModifiers.VERY(true_fs[small_fs[x]])]

elapsed_time = time.time() - start_time

print("Query: 'X is small is very true is likely' =================\n")
print("Result =", result)
print(f"\nElapsed time: {elapsed_time} seconds")

# Query8: Severall tall men

start_time = time.time()

men = people_fs.particularization({'Genders': 'Male'})
tall_men = men @ tall_fs
minimum = tall_men.collapse(FuzzyAnd.MIN)
result = FuzzyAnd.MIN(minimum, several_fs[tall_men.cardinality()])

elapsed_time = time.time() - start_time

print("Query: 'Severall tall men' =================\n")
print("Result =", result)
print(f"\nElapsed time: {elapsed_time} seconds")