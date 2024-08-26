# Discrete Fuzzy Sets

Discrete fuzzy sets are defined as all those fuzzy sets whose domain is discrete and, therefore, is countable and finite as opposed to an infinite countable set. The following sections describe how this type of fuzzy sets are managed by the pyPRUF library.

## Fuzzy Relational Algebra

The pyPRUF framework is primarily based on the idea of a **fuzzy relational algebra** where a database, called **fuzzy database**, is a collection of **fuzzy relations**, which represent discrete fuzzy sets, and the classic relational algebra operators are adapted to the fuzzy context. pyPRUF assumes that such a database is completely managed by the user of this library and, instead, provides all the operations necessary to perform approximate reasoning on this fuzzy database. First things to introduce, then, are the basic fuzzy relational algebra operations, in order to do more sophisticated things later on.

A first important assumption done by Zadeh is the way in which discrete fuzzy sets are represented. A discrete fuzzy set is represented as a **fuzzy relation**. A fuzzy relation can be seen as a classic relation, of relational algebra, where tuples belong to it with a membership value in the interval [0, 1].

**Definition (Fuzzy Relation)**:

A fuzzy relation $R$ defined on a domain $D := D_1 \times D_2 \times ... \times D_n$ is defined by a function $\mu_R: D \text{→} [0, 1]$ which associates to each tuple $t\text{∈}D$ a membership degree $\mu_R(t)\text{∈}[0, 1]$.

> **WARNING**: In this release only tuples with a membership degree greater than 0 (the **support** of the fuzzy set) are mantained in memory. So only membership values in the interval (0, 1] are valid. This is a design choice that was decided to follow in order to make operations faster and avoid memory waste due to keeping elements with zero membership in memory. See the [`DiscreteFuzzySet` API](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet) for more info.

<!-- The schema of the fuzzy relation corresponds to the **domain** of the fuzzy set while the attributes of the schema correspond to **existing sets**, identified by their attribute names, whose their cartesian product forms the domain. The tuples of the fuzzy relation correspond to the **elements** of the fuzzy set and so the set of all elements in the fuzzy relation is the **domain** of the discrete fuzzy set. If two or more attributes of different fuzzy relations have the same name, they refer to the same set. This assumption was done in order to formally re-define all fuzzy relational algebra operators so that they make semantic sense. -->

The [`fuzzy_set`](./api.md/#pyPRUF.fuzzy_set) module provides a class named [`DiscreteFuzzySet`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet) for creating discrete fuzzy sets and performing relational algebra operations on them. 

Example:

```python
>>> A = DiscreteFuzzySet(('D1', 'D2'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
>>> print(A)
A = 0.3/(1, 'val2') + 0.6/('val1', 3.4) + 0.9/(2, 'val2')
```

> *The output is in the Zadeh string format of the fuzzy set A where in each pair `<float> / <tuple>` the `<tuple>` represents the element in the domain of the fuzzy set and the `<float>` its membership value. The `+` operator denotes the union of the two sets in the form `{(<float>, <tuple>)}` denoted by the pair `<float> / <tuple>`.*

In this example a `DiscreteFuzzySet` has been initialized with the domain `('D1', 'D2')` representing the cartesian product of the sets `D1` and `D2` that compose it. The elements in this fuzzy sets are `(1, 'val2')`, `('val1', 3.4)`, `(2, 'val2')` with a membership value respectively of `0.3`, `0.6` and `0.9`. As we can see in this example, the tuples can be also composed by heterogeneous objects like `(1, 'val2')` exc.

Another way to initialize a `DiscreteFuzzySet` is by passing a well formatted pandas `DataFrame` as the `data` argument in input. In this way the parameter `domain` is no longer required and it will be inferred from the column names of the `DataFrame`.

Example:

```python
# Create a dictionary with the people data
data = {
    'Names': ['Mario Rossi', 'Luigi Bianchi', 'Anna Verdi', 'Giulia Neri', 'Marco Gialli'],
    'Ages': [34, 28, 45, 38, 50],
    'Genders': ['Male', 'Male', 'Female', 'Female', 'Male'],
    'Heights_cm': [175, 180, 165, 170, 160],
    'Weights_kg': [70, 85, 60, 65, 72],
    'Cities': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo'],
    # if missing all tuples are assumed to belong to the fuzzy relation with membership degree 1.
    'mu': [.3, .4, .1, .7, .9] 
}

df = pd.DataFrame(data)
people_fs = DiscreteFuzzySet(data=df)
```

This is useful when data is imported from an external source as a pandas `DataFrame`. The `DataFrame` must be a valid and well formatted `DataFrame` according to the [constructor API](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.__init__).

Another way to visualize the fuzzy set is by using the [`tab_str`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.tab_str) method:

```python
>>> A = DiscreteFuzzySet(('D1', 'D2'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
>>> print(A.tab_str())
D1             D2             mu

1              val2           0.3
val1           3.4            0.6
2              val2           0.9
```

A mapping (tuple, membership) can be added, updated and deleted in a fuzzy set by using the operators `[]`, `=` and `del`:

```python
>>> A[('val3', 4)] = 0.4 # add the element or tuple ('val3', 4) with membership 0.4
>>> print(A[('val3', 4)]) # get the membership of ('val3', 4)
0.4
>>> A[('val3', 4)] = 0.7 # update the element or tuple ('val3', 4) with membership 0.7
>>> print(A[('val3', 4)]) # get the new membership of ('val3', 4)
0.7
>>> del A[('val3', 4)] # delete the element ('val3', 4)
>>> print(A)
A = 0.3/(1, 'val2') + 0.6/('val1', 3.4) + 0.9/(2, 'val2')
```

It is also possible to checks if two `DiscreteFuzzySet` are equals by calling [`__eq__`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.__eq__) function using the operator `==`. They are considered equal if they have the same domain and are composed by the same set of tuples or elements:

```python
>>> A = DiscreteFuzzySet(('D1', 'D2'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
>>> B = DiscreteFuzzySet(('D1', 'D2'), {(2, 'val2'): 0.9, ('val1', 3.4): 0.6, (1, 'val2'): 0.3})
>>> print(A == B)
True
>>> B = DiscreteFuzzySet(('D1', 'D2'), {(2, 'val2'): 0.4, ('val1', 3.4): 0.6, (1, 'val2'): 0.3})
>>> print(A == B)
False
>>> B = DiscreteFuzzySet(('D1', 'D2'), {(2, 4): 0.9, ('val1', 3.4): 0.6, (1, 'val2'): 0.3})
>>> print(A == B)
False
>>> B = DiscreteFuzzySet(('D1', 'D3'), {(2, 'val2'): 0.9, ('val1', 3.4): 0.6, (1, 'val2'): 0.3})
>>> print(A == B)
False
```

## Fuzzy Set Operations

All the fuzzy set operations are calculated using the currently AND, OR and NOT truth functions set in the `FuzzyLogic` class. The default truth functions for this operations are respectively `FuzzyAnd.MIN`, `FuzzyOr.MAX` and `FuzzyNot.STANDARD`. Changing the default truth functions in the `FuzzyLogic` class, by using the methods [`set_and_fun`](./api.md/#pyPRUF.fuzzy_logic.FuzzyLogic.set_and_fun), [`set_or_fun`](./api.md/#pyPRUF.fuzzy_logic.FuzzyLogic.set_or_fun) and [`set_not_fun`](./api.md/#pyPRUF.fuzzy_logic.FuzzyLogic.set_not_fun), change the behaviour of the fuzzy set operations and their results. This was done in order to be able to leave the user free to use any kind of truth function depending on the use context. It is also possible to define custom **t-norms**, **t-conorms** and NOT truth functions by extending respectively the classes `FuzzyAnd`, `FuzzyOr` and `FuzzyNot`. By extending these classes it is possible to set custom truth function as the defaults for the `FuzzyLogic` class in order to customize the fuzzy set operations with appropriate custom truth functions. All the examples in the following sections are calculated using the default truth functions for the AND, OR and NOT operations.

> **WARNING**: In this release, for each operation, only tuples with resulting membership degree greater than 0 are mantained in memory as said above. 

## Union, Intersection and Difference

The first fuzzy set operations are: **Union**, **Intersection** and **Difference**. The relative or absolute complement can be derived by calculating the difference between a fuzzy set $U$, the universe of discourse or any normal fuzzy set, and a target fuzzy set $A$ i.e. $A^c_U := U \setminus A$. 

**Definition (Fuzzy Union, Intersection and Difference)**:

Let $A$ and $B$ be two fuzzy relations defined in the same domain $D$. Let $\mu_A$ and $\mu_B$ be respectively the membership functions of $A$ and $B$. Given a t-norm $\text{T}$, the fuzzy union is a binary function $\cup$ where the resulting fuzzy set $A \cup B$ is defined by the membership function:

\[
\mu_{A\cup B} (x) := \text{T}(\mu_A(x), \mu_B(x)) \space\space \forall x\text{∈}D.
\]

Given a t-conorm $\text{⊥}$, the fuzzy intersection is a binary function $\cap$ where the resulting fuzzy set $A \cap B$ is defined by the membership function:

\[
\mu_{A\cap B} (x) := \text{⊥}(\mu_A(x), \mu_B(x)) \space\space \forall x\text{∈}D.
\]

Given a negation $\text{~}$, the fuzzy difference is a binary function $\setminus$ where the resulting fuzzy set $A \setminus B$ is defined by the membership function:

\[
\mu_{A\setminus B} (x) := \text{T}(\mu_A(x), \text{~}\mu_B(x)) \space\space \forall x\text{∈}D.
\]

For each of these operation the resulting fuzzy set is defined on the same domain $D$.

The following is an example for each operation:

```python
>>> A = DiscreteFuzzySet(('D1', 'D2'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
>>> B = DiscreteFuzzySet(('D1', 'D2'), {(2, 'val4'): 0.1, ('val3', 4.4): 0.5, ('val1', 3.4): 0.7})

>>> union_set = A | B
>>> intersection_set = A & B
>>> difference_set = A - B
>>> complement_set = union_set - A # A complement relative to A ∪ B

>>> print("A ∪ B =", union_set)
A ∪ B = 0.1/(2, 'val4') + 0.5/('val3', 4.4) + 0.7/('val1', 3.4) + 0.7/(1, 'val2') + 0.9/(2, 'val2') 
>>> print("A ∩ B =", intersection_set)
A ∩ B = 0.6/('val1', 3.4) 
>>> print("A - B =", difference_set)
A - B = 0.7/(1, 'val2') + 0.3/('val1', 3.4) + 0.9/(2, 'val2')
>>> print("~A rel_to(A ∪ B) =", complement_set)
~A rel_to(A ∪ B) = 0.3/(1, 'val2') + 0.4/('val1', 3.4) + 0.1/(2, 'val2')
```

In order to work, for each operation, the two sets **must have the same domain** otherwise such operations have no semantic meaning. For more info, please refer to [`__and__`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.__and__), [`__or__`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.__or__) and [`__sub__`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.__sub__) API docs.

## Cartesian Product and Natural Join

Typical relational algebra operations such as **Cartesian Product** and **Natural Join** are also adapted to the fuzzy context. In order to have a semantic meaning, the cartesian product requires that the two fuzzy set operands **must have completely different domains** while natural join requires that the two fuzzy set operands **must have at least a set identifier in common**.

**Definition (Cartesian Product and Natural Join)**

Let $A$ and $B$ be two fuzzy sets defined in completely different domains $D_A := A_1 \times ... \times A_n$ and $D_B := B_1 \times ... \times B_m$. Let $\mu_A$ and $\mu_B$ be respectively the membership function of $A$ and $B$. Given a t-norm $\text{T}$, the fuzzy cartesian product is a binary function $\times$ where the resulting fuzzy set $A \times B$ is defined in the domain $D_A \times D_B$ and is defined by the membership function:

\[
\mu_{A\times B} ((a_1, ..., a_n, b_1, ..., b_m)) := \text{T}(\mu_A(a), \mu_B(b))
\]

\[
\forall a:=(a_1, ..., a_n)\text{∈}D_A, \forall b:=(b_1, ..., b_m)\text{∈}D_B
\]

Assuming that $A$ and $B$ are, now, two fuzzy sets defined with domains $D_A := A_1 \times ... \times A_n$ and $D_B := B_1 \times ... \times B_m$ where:

1. $i_1, ..., i_k$ are the indexes of the $D_B$ sets that differ from $D_A$ and
2. $j_1, ..., j_{l}$ and $q_1, ..., q_{l}$ are the indexes of sets in common between $D_A$ and $D_B$

then the fuzzy natural join is a binary function $\bowtie$ where the resulting fuzzy set $A \bowtie B$ is defined in the domain $D_A \times B_{i_1} \times ... B_{i_k}$ and is defined by the membership function:

\[
\mu_{A\bowtie B} ((a_1, ..., a_n, b_{i_1}, ..., b_{i_k})) := \text{T}(\mu_A(a), \mu_B(b))
\]

\[
\forall a:=(a_1, ..., a_n)\text{∈}D_A, \forall b:=(b_1, ..., b_m)\text{∈}D_B \space\space t.c. \space a_{j_i} = b_{q_i} \forall i\text{∈}\{1, ..., l\}
\]

The following is an example for each operation:

```python

>>> A = DiscreteFuzzySet(('D1', 'D2'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
>>> E = DiscreteFuzzySet(('D1', 'D3'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
>>> F = DiscreteFuzzySet(('D6', 'D3'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})

>>> cartesian_product_set = A * F
>>> natural_join_set = A @ E

>>> print("A × F =", cartesian_product_set, "\ndomain:", cartesian_product_set.get_domain())
A × F = 0.3/(1, 'val2', 1, 'val2') + 0.6/(1, 'val2', 'val1', 3.4) + 0.7/(1, 'val2', 2, 'val2') + 0.3/('val1', 3.4, 1, 'val2') + 0.6/('val1', 3.4, 'val1', 3.4) + 0.6/('val1', 3.4, 2, 'val2') + 0.3/(2, 'val2', 1, 'val2') + 0.6/(2, 'val2', 'val1', 3.4) + 0.9/(2, 'val2', 2, 'val2')
domain: ('D1', 'D2', 'D6', 'D3')
>>> print("A ⋈ E =", natural_join_set, "\ndomain:", natural_join_set.get_domain())
A ⋈ E = 0.3/(1, 'val2', 'val2') + 0.6/('val1', 3.4, 3.4) + 0.9/(2, 'val2', 'val2')
domain:  ('D1', 'D2', 'D3')
```

In this example the method [`get_domain`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.get_domain) has been used in order to obtain the domain of the fuzzy sets. For more info, please refer to [`__mul__`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.__mul__) and [`__matmul__`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.__matmul__) API docs.

## Selection and Particularization

Some useful operators in pyPRUF are select-like operators such as **selection** and **particularization**. The [`select`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.select) operator has the same behaviour and formal definition of classic relational algebra selection while the [`particularization`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.particularization) operator is a select-like operator where the condition can only be a conjunction of equalities. This equalities can require that some set identifiers are equal to specific values or `FuzzySet`. In the first case the behaviour of the condition is the same as the select: if the condition is not satisfied, a tuple is not included in the result. In the second case the tuple is included with a membership value equal to the result of the AND between the membership degree of that tuple and the membership degree of that tuple in the fuzzy set involved in the equality. The particularization is more convenient than the natural join when their results are equivalent because it is much more efficient. In other situations, the natural join could be the only choice. Some usage examples can be found in their API docs.

## Renaming and Projection

Others relational algebra operations such as **renaming** and **projection** are also adapted to the fuzzy context. Renaming is the same as the corresponding operator in classical relational algebra while projection has been adapted following the definition proposed by Zadeh in his [paper](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1977/ERL-m-77-61.pdf). The projection, in the fuzzy context, needs a binary operator that handles the common tuples and their memberships that appear in the projection result. Zadeh proposed an OR-based projection and an AND-based projection. pyPRUF allow users to directly communicate to the method which binary operation it has to use in order to leave them complete freedom to use available and existing binary operators or to define other custom binary operators and use them in the projection. 

**Definition (Projection)**

Let $A$ be a fuzzy set defined in the domain $D := D_1 \times ... \times D_n$. Let $\mu_A$ be the membership function of $A$. Let $D_{sub} := D_{i_1} \times ... \times D_{i_k}$ be the new domain on which project $A$ where $i_1, ..., i_k$ are all different indexes between $1$ and $n$. Given a `FuzzyBinaryOperator` $op$, the fuzzy projection is a unary function $\pi_{D_{sub}}$ where the resulting fuzzy set $\pi_{D_{sub}}(A)$ is defined in the domain $D_{sub}$ and is defined by the membership function:

\[
\mu_{A\times B} ((a_{i_1}, ..., a_{i_k})) := op_{a:=(a_1, ..., a_n)\text{∈}D | \{a_{i_1}, ..., a_{i_k}\} \subset \{a_1, ..., a_n\}}\{\mu_A(a)\}
\]

> **WARNING**: this projection have a semantic sense due to the fact that only the `FuzzyOr` and the `FuzzyAnd` are `FuzzyBinaryOperator` and all implementations, t-norms and t-conorms, of them are **commutative**. If a non commutative custom `FuzzyBinaryOperator` is defined and used here, the resulting memberships could depend on the relative order of tuples in the data structure used to keep them.

The following is an example for each operation:

```python
>>> A = DiscreteFuzzySet(('D1', 'D2'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
>>> A.rename_domain({'D1': 'X1', 'D2': 'X2'})
>>> print(A.get_domain())
('X1', 'X2')

>>> condition = lambda x: x[-1] > 0.6 and x[2] == 'val2'
>>> print("σA =", A.select(condition))
σA = 0.9 / (2, 'val2')

>>> or_projection_set = A.projection(('D2',), FuzzyOr.MAX)
>>> and_projection_set = A.projection(('D2',), FuzzyAnd.MIN)

>>> print("or_projection(A, ('D2')) =", or_projection_set, "\ndomain:", or_projection_set.get_domain())
or_projection(A, ('D2')) = 0.9/('val2',) + 0.6/(3.4,)
domain: ('D2',)
>>> print("and_projection(A, ('D2')) =", and_projection_set, "\ndomain:", and_projection_set.get_domain())
and_projection(A, ('D2')) = 0.7/('val2',) + 0.6/(3.4,)
domain: ('D2',)
```

Other join operations such as theta-join, equi-join, external-join are not implemented yet. They can be calculated in combination with natural join or cartesian product and selection. For more info, please refer to [`rename_domain`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.rename_domain), [`select`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.select) and [`projection`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.projection) API docs.

## Extension Principle

The last useful method in the fuzzy context is [`image`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.image) which calculates the image of a fuzzy set under a mapping given in input according to the extension principle of the fuzzy theory. This concept is called **Fuzzy Extension Principle** and it is a fundamental concept in fuzzy set theory, which generalizes classical mathematical functions to functions involving fuzzy sets. It provides a way to extend functions from crisp (non-fuzzy) domains to fuzzy domains. The Fuzzy Extension Principle allows the extension of a crisp function to operate on fuzzy sets by mapping the membership degrees from the domain to the codomain.

**Definition (Extension Principle)**

Let $f: X \rightarrow Y$ be a function from a crisp set $X$ to a crisp set $Y$, and let $\tilde{A}$ be a fuzzy set in $X$ with membership function $\mu_{\tilde{A}}(x)$. The goal is to define a fuzzy set $\tilde{B}$ in $Y$, denoted by $\tilde{B} = f(\tilde{A})$, that is the image of the fuzzy set $\tilde{A}$ under the function $f$. The membership function $\mu_{\tilde{B}}(y)$ of the fuzzy set $\tilde{B}$ in $Y$ is defined by the **Fuzzy Extension Principle** as:

\[
\mu_{\tilde{B}}(y) = \sup_{x \in f^{-1}(y)} \mu_{\tilde{A}}(x)
\]

where $f^{-1}(y)$  is the preimage of $y$  under the function $f$ , i.e., $f^{-1}(y) = \{ x \in X \mid f(x) = y \}$ .  A simple usage example can be found in its [API docs](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.image).

## Reorder and extra methods

Sometimes resulting `DiscreteFuzzySet`s from the preceding operations can have domains that differs from each other only by their domain tuple permutation. Two domains `('A1', 'A2')` and `('A2', 'A1')` are considered different and that's why if we wanted to perform the union of two fuzzy sets with these domains we could not do it. In order to always be able to calculate the result of an operation that requires a common domain between two fuzzy sets, pyPRUF provides the [`reorder`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.reorder) method that allows to reorder all the tuples in a fuzzy relation according to a permutation of the domain sets given in input. A simple example can be found in its [API doc](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.reorder).

Extra methods such as [`to_dictionary`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.to_dictionary), [`elements`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.elements), [`memberships`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.memberships) and [`items`](./api.md/#pyPRUF.fuzzy_set.DiscreteFuzzySet.items) are also available to respectively get a `dict` representation of the fuzzy set, a `set` of all elements in its support, a `set` of all their memberships and a `set` of pairs (element, membership) in the support of the fuzzy set.