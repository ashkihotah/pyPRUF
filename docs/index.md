# pyPRUF: Possibilistic Relational Universal Fuzzy

[![Documentation Status](https://readthedocs.org/projects/pypruf/badge/?version=latest)](https://pypruf.readthedocs.io/en/latest/?badge=latest)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![GitHub release](https://img.shields.io/github/release/ashkihotah/pyPRUF)](https://github.com/ashkihotah/pyPRUF)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

**pyPRUF** is a simple Python library implementation of the **PRUF** (**Possibilistic Relational Universal Fuzzy**) framework proposed by Lotfi A. Zadeh.

PRUF was an informal and incomplete mathematical framework, proposed by Lotfi A. Zadeh in his [paper](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1977/ERL-m-77-61.pdf), which extended classical Relational Algebra theory of databases to a Fuzzy-like Relational Algebra theory by integrating it with the multi-valued Fuzzy Logic and Fuzzy Set theory to handle uncertainty and imprecision in reasoning processes.

This library provides tools and utilities for creating, manipulating, and reasoning with fuzzy sets in the context of possibilistic logic. In addition to possibility qualifications, this tool can be used, also, to perform truth and probability qualifications (as defined in the [paper](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1977/ERL-m-77-61.pdf)).

At the moment, this library provides facilities that manage only discrete fuzzy sets however, it is designed in such a way that it can easily be expanded in the future to also handle continuous fuzzy sets.

>> *At present, pyPRUF is still in its intial stages of development. This library could be improved in many ways and, time to time, it will be done!*😊

It is recommended to have or obtain a solid foundation of knowledge in fuzzy logic and fuzzy set theory before reading the user guide to this library.

## Key Features

1. **Fuzzy Logic**
      1. t-norms, t-conorms and negations
      2. Linguistic Modifiers
2. **Fuzzy Relational Algebra**
      1. Discrete Fuzzy Relations
      2. Union, Intersection and Difference
      3. Cartesian Product and Natural Join
      4. Renaming, Projection and Select
3. **PRUF specific operators**
      1. Cylindrical Extension
      2. Normal / Mean Cardinality and Proportion
      3. Consistency and Compatibility
      4. Extension Principle
   
**WARNING**: *A python version higher than 3.11 is required*.

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

prova webhook