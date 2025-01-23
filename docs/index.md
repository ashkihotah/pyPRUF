# pyPRUF: Possibilistic Relational Universal Fuzzy

![Read the Docs (version)](https://img.shields.io/readthedocs/pypruf/latest)
![GitHub Release](https://img.shields.io/github/v/release/ashkihotah/pyPRUF)
![GitHub License](https://img.shields.io/github/license/ashkihotah/pyPRUF)


**pyPRUF** is a simple Python library implementation of the **PRUF** (**Possibilistic Relational Universal Fuzzy**) framework proposed by Lotfi A. Zadeh.

PRUF was an informal and incomplete mathematical framework, proposed by Lotfi A. Zadeh in his [paper](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1977/ERL-m-77-61.pdf), which extended classical relational algebra theory of databases to a fuzzy-like relational algebra theory by integrating it with the multi-valued fuzzy logic and fuzzy set theory to handle uncertainty and imprecision in reasoning processes.

This library provides tools and utilities for creating, manipulating, and reasoning with fuzzy sets in the context of possibilistic logic. In addition to **possibility** qualifications, this tool can be used, also, to perform **truth** and **probability** qualifications (as defined in the [paper](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1977/ERL-m-77-61.pdf)).

At the moment, this library provides facilities that manage only discrete fuzzy sets however, it is designed in such a way that it can easily be expanded in the future to also handle continuous fuzzy sets.

> *At present, pyPRUF is still in its intial stages of development. This library could be improved in many ways and, time to time, it will be done!*😊

It is recommended to have or obtain a solid foundation of knowledge in fuzzy logic and fuzzy set theory before reading the [docs](https://pypruf.readthedocs.io/en/latest/).

## Key Features

1. **Fuzzy Logic**
      1. t-norms, t-conorms and negations
      2. Linguistic Modifiers
2. **Fuzzy Relational Algebra**
      1. Discrete Fuzzy Sets as Fuzzy Relations
      2. Union, Intersection and Difference
      3. Cartesian Product and Natural Join
      4. Selection and Particularization
      5. Renaming and Projection
      6. Extension Principle
      7. Reorder and extra methods
3. **Translation Rules**
      1. Collapsing DiscreteFuzzySets
      2. Type I (Modification): Apply Linguistic Modifiers
      3. Type II (Composition): Cylindrical Extension 
      4. Type III (Quantification): Normal / Mean Cardinality and Proportion
      5. Type IV (Qualification): Consistency and Compatibility
4. **Some Continuous Fuzzy Set facilities**:
      1. Standard Membership Functions
      2. Temporary Implementation of some methods
   
**WARNING**: *A python version higher than 3.11 is required*.

## Installation

Installing **pyPRUF** is straightforward. You can install it via pip:

```
pip install pyPRUF
```

## License

**pyPRUF** is open-source and distributed under the GNU Lesser General Public License (LGPL) - see the [LICENSE](https://github.com/ashkihotah/pyPRUF/tree/dev?tab=License-1-ov-file) file for details.

## Contributing

We welcome contributions from the community! If you'd like to contribute to pyPRUF, [contact](./about.md#get-in-touch) us.

<!-- check out our Contributing Guide for more information on how to get started. -->