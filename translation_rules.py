import time
import pandas as pd

from pyPRUF.fuzzy_logic import FuzzyAnd, FuzzyOr, LinguisticModifiers
from pyPRUF.fuzzy_sets import *
from pyPRUF.membership_functions import *

# people_fs, tall_fs, tall_people, several_fs, most_fs
# young_fs, young_people, young_males, small_fs, true_fs
# intelligent_fs, likely_fs, products_fs

# Create a PEOPLE crisp set or relation
data = {
    'Names': ['Mario Rossi', 'Luigi Bianchi', 'Anna Verdi', 'Giulia Neri', 'Marco Gialli'],
    'Ages': [34, 28, 45, 38, 50],
    'Genders': ['Male', 'Male', 'Female', 'Female', 'Male'],
    'Heights_cm': [175, 180, 165, 170, 160],
    'Weights_kg': [70, 85, 60, 65, 72],
    'Cities': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo']
}
df = pd.DataFrame(data)
people_fs = DiscreteFuzzySet(mf=df)
print("PEOPLE = \n\n" + people_fs.tab_str())

# Create a TALL fuzzy set with heights from 140 cm to 210 cm
tall_fun =  Trapezoidal(a=160.0, b=180.0, c=MembershipFunction.INF, d=MembershipFunction.INF)
tall_dict = { (height,): tall_fun(float(height)) for height in range(161, 211) }
tall_fs = DiscreteFuzzySet(('Heights_cm', ), tall_dict)
tall_people = people_fs.particularization({'Heights_cm': tall_fs})
print("TALL_PEOPLE = \n\n" + tall_people.tab_str())

# calculate the answer of the query "A person is tall"
result = tall_people.collapse(FuzzyOr.MAX)
print("A person is tall:", result, "\n")

# calculate the answer of the query "All people are tall"
result = tall_people.collapse(FuzzyAnd.MIN)
print("All people are tall:", result, "\n")

# calculate the answer of the query "Very tall people"
result = tall_people.apply(LinguisticModifiers.VERY)
print("VERY_TALL_PEOPLE = \n\n" + result.tab_str())

# calculate the answer of the query "Mario Rossi is very tall"
mu = tall_people[('Mario Rossi', 34, 'Male', 175, 70, 'Rome')]
result = LinguisticModifiers.VERY(mu)
print("Mario Rossi is very tall =",  result)

data = {
    'Product_Names': ['Laptop', 'Smartphone', 'Tablet', 'Smartwatch', 'Headphones'],
    # 'Categories': ['Electronics', 'Electronics', 'Electronics', 'Wearables', 'Accessories'],
    'Prices_USD': [999.99, 699.99, 499.99, 199.99, 149.99],
    # 'Qt_In_Stock': [50, 120, 75, 200, 300],
    # 'Brands': ['Brand A', 'Brand B', 'Brand C', 'Brand D', 'Brand E'],
    # 'Ratings': [4.5, 4.7, 4.3, 4.2, 4.8]
}
df = pd.DataFrame(data)
products_fs = DiscreteFuzzySet(mf=df)
print("PRODUCTS =\n\n" + products_fs.tab_str())

expensive_fs = ContinuousFuzzySet(('Prices', ), Trapezoidal(0.0, 500.0, MembershipFunction.INF, MembershipFunction.INF))
expensive_products = products_fs.particularization({'Prices_USD': expensive_fs})

print("EXPENSIVE_PRODUCTS =\n\n" + expensive_products.tab_str())

# calculate the answer to the query "Tall people and expensive products"
A, B = tall_people.cylindrical_extension(expensive_products)
tall_people_and_expensive_products =  A & B
print("TALL_PEOPLE ∪ EXPENSIVE_PRODUCTS = \n\n" + tall_people_and_expensive_products.tab_str())

# calculate the answer to the query "Tall people or expensive products"
A, B = tall_people.cylindrical_extension(expensive_products)
tall_people_or_expensive_products =  A | B
print("TALL_PEOPLE ∩ EXPENSIVE_PRODUCTS = \n\n" + tall_people_or_expensive_products.tab_str())

# # calculate the answer to the query "Tall people and expensive products"
# A, B = tall_people.cylindrical_extension(expensive_products)
# tall_people_difference_expensive_products =  A - B
# print("TALL_PEOPLE \ EXPENSIVE_PRODUCTS = \n\n" + tall_people_difference_expensive_products.tab_str())

# calculate the answer of the query "Several people are tall"
several_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=1.0, b=10.0, c=MembershipFunction.INF, d=MembershipFunction.INF))
result = several_fs[(tall_people.cardinality(), )]
print("Several people are tall:", result)

# calculate the answer of the query "Most people are tall"
most_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=0.2, b=0.75, c=1.0, d=1.1))
result = most_fs[(tall_people.mean_cardinality(), )]
print("Most people are tall:", result, "\n")

# Create a YOUNG fuzzy set with ages between 1 and 50
young_fun =  Trapezoidal(a=-1.0, b=0.0, c=20.0, d=50.0)
young_dict = { (age,): young_fun(float(age)) for age in range(1, 50) }
young_fs = DiscreteFuzzySet(('Ages', ), young_dict)

# calculate the answer of the query "Most young people are tall"
young_people = people_fs.particularization({'Ages': young_fs})
prop = young_people / tall_people
result = most_fs[(prop, )]
print("YOUNG_PEOPLE = \n\n" + young_people.tab_str())
print("Most young people are tall:", result)

# calculate the answer of the query "Most tall people are young"
prop = tall_people / young_people
result = most_fs[(prop, )]
print("Most tall people are young:", result)

# calculate the answer of the query "Most young males are tall"
young_males = people_fs.particularization({'Genders': 'Male', 'Ages': young_fs})
prop = young_males / tall_people
result = most_fs[(prop, )]
print("YOUNG_MALES = \n\n" + young_males.tab_str())
print("Most young males are tall:", result)

small_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=-MembershipFunction.INF, b=-MembershipFunction.INF, c=10.0, d=20.0))
true_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=0.35, b=0.75, c=1.1, d=1.2))
prob = Bell(0.0, 5.0) # simulation of any probability distribution
intelligent_fs = DiscreteFuzzySet(('Names', ), {('Carol', ): 0.65, ('John', ): 0.85, ('Pitt', ): 0.35})
likely_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=0.35, b=0.75, c=1.1, d=1.2))
x = -5.0

# calculate the answer of the query "X is small is very true"
result = LinguisticModifiers.VERY(true_fs[(small_fs[(x, )], )])
print("INTELLIGENT = \n\n" + intelligent_fs.tab_str())
print("X = -5 is small is very true:", result)

# calculate the answer of the query "Carol is very intelligent is very likely"
very_inte_carol = LinguisticModifiers.VERY(intelligent_fs[('Carol', )])
result = likely_fs[(very_inte_carol * prob(intelligent_fs[('Carol', )]), )]
result = LinguisticModifiers.VERY(result)
print("Carol is very intelligent is very likely:", result)

# calculate the answer of the query "X is small is very true is likely"
result = likely_fs[(prob(x) * LinguisticModifiers.VERY(true_fs[(small_fs[(x, )], )]), )]
print("X = -5 is small is very true is likely:", result)

# ADDITIONAL QUERIES =============================================================================

# Most males are tall

start_time = time.time()

males_tall = tall_people.particularization({'Genders': 'Male'})
prop = males_tall / tall_people
result = most_fs[(prop, )]

elapsed_time = time.time() - start_time

print("Query2: 'Most males are tall' =================\n")
print(males_tall.tab_str()) 
print("proportion(MALES_TALL / TALL_PEOPLE) = ", prop)
print("MOST(" + str(prop) + ") =", result)
print(f"\nElapsed time: {elapsed_time} seconds")

# Most young boys are tall

start_time = time.time()

young_boys = people_fs.particularization({'Genders': 'Male', 'Ages': young_fs})
prop = young_boys / tall_people
result = most_fs[(prop, )]

elapsed_time = time.time() - start_time

print("Query: 'Most young boys are tall' =================\n")
print(young_boys.tab_str())
print("Prop(YOUNG_AND_TALL_BOYS / YOUNG_AND_TALL_PEOPLE) = ", prop)
print("Most(" + str(prop) + ") =", result)
print(f"\nElapsed time: {elapsed_time} seconds")

# Query8: Severall men are tall

start_time = time.time()

tall_men = people_fs.particularization({'Genders': 'Male', 'Heights_cm': tall_fs})
minimum = tall_men.collapse(FuzzyAnd.MIN)
result = FuzzyAnd.MIN(minimum, several_fs[(tall_men.cardinality(), )])

elapsed_time = time.time() - start_time

print("Query: 'Severall tall men' =================\n")
print("Result =", result)
print(f"\nElapsed time: {elapsed_time} seconds")