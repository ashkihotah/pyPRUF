# Translation Rules

The **translation rules** defined in Zadeh's paper are mechanisms used to transform expressions in natural language into **mathematical expressions**, or **procedures**, which can be processed within a **fuzzy logic framework** on a set of fuzzy relations in a **fuzzy database** for approximate reasoning purposes. These can be seen as abstract or generic examples of queries expressed in natural language that can be answered by translating them into procedures in PRUF, which is the fuzzy logic framework used by this library, and executing them on a reference fuzzy database. Thus, if $p$ is a proposition in a natural language which translates into a pyPRUF procedure $P$, then $P$ may be interpreted as the **meaning** of $p$ while its result as the **information conveyed** by $p$. For the present, at least, the translation rules in pyPRUF are human-use oriented in that they do not provide a system for an automatic translation from a natural language into PRUF.

The class [`DiscreteFuzzySet`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet) provides some **PRUF specific operators** defined by Zadeh in his [paper](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1977/ERL-m-77-61.pdf). These operations, in combination with the fuzzy relational algebra operations, allow us to perform all the translation rules proposed in it as well as all the example queries at its end, in the last section. The following sections refer to these operations and how they can be used to answer some example queries.

## Collapsing

A useful method is [`collapse`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.collapse) which, given a `FuzzyBinaryOperator`, collapse the entire fuzzy relation to a single membership value: the result of applying the `FuzzyBinaryOperator` iteratively across all membership values in the fuzzy set. This is useful when we need to calculate queries like *"A person is tall"* or *"All people are tall"*.

> **WARNING**: the [`collapse`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.collapse) method have a semantic sense due to the fact that only the `FuzzyOr` and the `FuzzyAnd` are `FuzzyBinaryOperator` and all implementations, t-norms and t-conorms, of them are **commutative**. If a non commutative custom `FuzzyBinaryOperator` is defined and used here, the resulting memberships could depend on the relative order of tuples in the data structure used to keep them.

**Queries**: *"A person is tall"* and *"All people are tall"*

```python
from pyPRUF.fuzzy_logic import *
from pyPRUF.membership_functions import *
from pyPRUF.fuzzy_set import *

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
people_fs = DiscreteFuzzySet(data=df)
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
```

In this example the **reference fuzzy database** is the set of all fuzzy sets involved in the queries such as the fuzzy sets `people_fs` and `tall_fs`. The **mathematical expression**, instead, corresponds to the **pyPRUF procedure** `people_fs.particularization({'Heights_cm': tall_fs}).collapse(FuzzyOr.MAX)` for the query *"A person is tall"* and `people_fs.particularization({'Heights_cm': tall_fs}).collapse(FuzzyOr.MIN)` for the query *"All people are tall"*.

## Type I (Modification)

The translation rules of type I are all the rules pertaining to **modification** of fuzzy sets or membership values according to a linguistic modifier. This can be done in two ways:

1. use the [`apply`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.apply) method on a `DiscreteFuzzySet`by specifying a `FuzzyUnaryOperator`
2. call a `LinguisticModifiers` on a membership value

As described in the [Fuzzy Logic section](fuzzy_logic.md), `FuzzyNot` is not of type `LinguisticModifiers` but it could semantically be also a `LinguisticModifiers`. That explains why you need to specify a `FuzzyUnaryOperator` rather than a `LinguisticModifiers`. This is also compatible with custom classes that extend `FuzzyUnaryOperator`.

**Queries**: *"Very tall people"* and *"Mario Rossi is very tall"*

```python
# assume there is people_fs, tall_fs and tall_people, like in the preceding code examples
# calculate the answer of the query "Very tall people"
result = tall_people.apply(LinguisticModifiers.VERY)
print("VERY_TALL_PEOPLE = \n\n" + result.tab_str())

# calculate the answer of the query "Mario Rossi is very tall"
mu = tall_people[('Mario Rossi', 34, 'Male', 175, 70, 'Rome')]
result = LinguisticModifiers.VERY(mu)
print("Mario Rossi is very tall =",  result)
```

## Type II (Composition)

In addition to the method [`reorder`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.reorder) the class `DiscreteFuzzySet` provides also the method [`cylindrical_extension`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.cylindrical_extension) to allow the union, intersection and difference of `DiscreteFuzzySet`s with completely different domains. This method is useful in the **Translation Rules of Type II** where the composition of multiple fuzzy sets is required.

**Definition (Cylindrical Extension)**:

Let $A$ and $B$ be two fuzzy sets defined respectively in the domains $D_A := A_1 \times ... \times A_n$ and $D_B := B_1 \times ... \times B_m$. Let $\mu_A$ and $\mu_B$ be respectively the membership function of $A$ and $B$. Assume that:

1. $i_1, ..., i_k$ are indexes of sets in $D_A$ that differs from $D_B$
2. $j_1, ..., j_q$ are indexes of sets in $D_B$ that differs from $D_A$
 
Their cylindrical extension is a binary function that returns a pair $(C_A, C_B)$ where:

1. $C_A$ is a new fuzzy set defined on the domain $D_A \times B_{j_1} \times ... B_{j_q}$ and by the membership function:

\[
\mu_{C_A}((a_1, ..., a_n, b_{j_1}, ..., b_{j_q})) := \mu_A(a)
\]

\[
\forall a:=(a_1, ..., a_n)\text{∈}D_A, \forall (b_{j_1}, ..., b_{j_q})\text{∈}B_{j_1} \times ... B_{j_q}
\]

2. $C_B$ is a new fuzzy set defined on the domain $D_B \times A_{i_1} \times ... A_{i_k}$ and by the membership function:

\[
\mu_{C_A}((b_1, ..., b_m, a_{i_1}, ..., a_{i_k})) := \mu_B(b)
\]

\[
\forall b:=(b_1, ..., b_m)\text{∈}D_B, \forall (a_{i_1}, ..., a_{i_k})\text{∈}A_{i_1} \times ... A_{i_k}
\]

Simple queries where the composition is involved are: *"Tall people and expensive products"*, *"Tall people or expensive products"*. 

**Queries**: *"Tall people and expensive products"* and *"Tall people or expensive products"*
```python
data = {
    'Product_Names': ['Laptop', 'Smartphone', 'Tablet', 'Smartwatch', 'Headphones'],
    # 'Categories': ['Electronics', 'Electronics', 'Electronics', 'Wearables', 'Accessories'],
    'Prices_USD': [999.99, 699.99, 499.99, 199.99, 149.99],
    # 'Qt_In_Stock': [50, 120, 75, 200, 300],
    # 'Brands': ['Brand A', 'Brand B', 'Brand C', 'Brand D', 'Brand E'],
    # 'Ratings': [4.5, 4.7, 4.3, 4.2, 4.8]
}
df = pd.DataFrame(data)
products_fs = DiscreteFuzzySet(data=df)
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
```

The cartesian product is more convenient than the cylindrical extension when their results are equivalent (i.e. when the two fuzzy sets have completely different domains) because it is much more efficient. In other situations, the cylindrical extension could be the only choice.

A simple example of how to use it can be found in its [API doc](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.cylindrical_extension).

## Type III (Quantification)

The translation rules of type III are all the rules pertaining to the **quantification** of fuzzy sets. In order to be able to answer these queries, **quantification operators** such as [`cardinality`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.cardinality), [`mean_cardinality`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.mean_cardinality) and [`__truediv__`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.__truediv__) (**proportion**) must be available. The normal cardinality returns the sum of all membership values in the fuzzy relation while the mean cardinality returns the mean of this sum. This is a simple definition of the cardinality of a fuzzy set as proposed by Zadeh. These two operations are useful to answer queries such as *"Several people are tall"*, *"Most people are tall"*, *"Three tall people"*, *"Jill has many friends"* exc.

**Queries**: *"Several people are tall"* and *"Most people are tall"*

```python
# assume there is tall_people, like in the first code example of this section
# calculate the answer of the query "Several people are tall"
several_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=1.0, b=10.0, c=MembershipFunction.INF, d=MembershipFunction.INF))
result = several_fs[tall_people.cardinality()]
print("Several people are tall:", result)

# calculate the answer of the query "Most people are tall"
most_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=0.2, b=0.75, c=1.0, d=1.1))
result = most_fs[tall_people.mean_cardinality()]
print("Most people are tall:", result, "\n")
```

The proportion between set $A$ and $B$, instead, is the cardinality of their intersection divided by the cardinality of the set $B$. This is useful in approximate reasoning tasks such as *"Most young people are tall"*, *"Most tall people are young"*, *"Most young males are tall"* and much more complicated queries.

**Queries**: *"Most young people are tall"*, *"Most tall people are young"* and *"Most young males are tall"*

```python
# assume there is tall_people and most_fs, like in the preceding code examples of this section
# calculate the answer of the query "Most young people are tall"
young_people = people_fs.particularization({'Ages': young_fs})
prop = young_people / tall_people
result = most_fs[prop]
print("YOUNG_PEOPLE = \n\n" + young_people.tab_str())
print("Most young people are tall:", result)

# calculate the answer of the query "Most tall people are young"
prop = tall_people / young_people
result = most_fs[prop]
print("Most tall people are young:", result)

# calculate the answer of the query "Most young males are tall"
young_males = people_fs.particularization({'Genders': 'Male', 'Ages': young_fs})
prop = young_males / tall_people
result = most_fs[prop]
print("YOUNG_MALES = \n\n" + young_males.tab_str())
print("Most young males are tall:", result)
```

## Type IV (Qualification)

In order to be able to perform **Translation Rules of Type IV** where **truth**, **probability** and **possibility** qualifications are involved, the [`consistency`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.consistency) and [`compatibility`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.compatibility) methods are required. Although Zadeh considers compatibility to be the most appropriate method for this purpose, consistency has nonetheless been implemented and made available. 

**Definition (Consistency and Compatibility)**:

Let $A$ and $B$ two fuzzy relations defined on the same domain $D$. Let $\mu_A$ and $\mu_B$ be respectively the membership function of $A$ and $B$. The consistency between $A$ and $B$ is defined as:

\[
Cons\{A, B\} := sup_{x\text{∈}D}\{\mu_A(x) \text{∧} \mu_B(x)\}
\]

The compatibility between $A$ and $B$ is a new fuzzy relation defined by the membership function $\mu_{Comp\{A, B\}}: [0, 1]\text{→}[0, 1]$ where:

\[
\mu_{Comp\{A, B\}}(y) := max_{x\text{∈}D | \mu_B(x) = y} \{\mu_A(x)\}
\]

Some qualification query examples are *"X is small is very true"*, *"Carol is very intelligent is very likely"* and *"X = -5 is small is very true is likely"*.

**Queries**: *"X is small is very true"*, *"Carol is very intelligent is very likely"* and *"X = -5 is small is very true is likely"*.

```python
small_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=-MembershipFunction.INF, b=-MembershipFunction.INF, c=10.0, d=20.0))
true_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=0.35, b=0.75, c=1.1, d=1.2))
prob = Bell(0.0, 5.0) # simulation of any probability distribution
intelligent_fs = DiscreteFuzzySet(('Names', ), {('Carol', ): 0.65, ('John', ): 0.85, ('Pitt', ): 0.35})
likely_fs = ContinuousFuzzySet(('Real Numbers', ), Trapezoidal(a=0.35, b=0.75, c=1.1, d=1.2))
x = -5.0

# calculate the answer of the query "X = -5 is small is very true"
result = LinguisticModifiers.VERY(true_fs[small_fs[x]])
print("INTELLIGENT = \n\n" + intelligent_fs.tab_str())
print("X = -5 is small is very true:", result)

# calculate the answer of the query "Carol is very intelligent is very likely"
very_inte_carol = LinguisticModifiers.VERY(intelligent_fs[('Carol', )])
result = likely_fs[very_inte_carol * prob(intelligent_fs[('Carol', )])]
result = LinguisticModifiers.VERY(result)
print("Carol is very intelligent is very likely:", result)

# calculate the answer of the query "X = -5 is small is very true is likely"
result = likely_fs[prob(x) * LinguisticModifiers.VERY(true_fs[small_fs[x]])]
print("X = -5 is small is very true is likely:", result)
```