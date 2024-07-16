# pyPRUF
A Python library for the PRUF language proposed by Zadeh.

## Assumptions
1. The domain of the variables involved in fuzzy relations is implicit (as opposed to explicit) in the sense that their domain is determined by the union of the values the variable takes on in the fuzzy relations (as specified by Zadeh in his article)
2. A variable is uniquely identified by its name. This goes against what Zadeh says about the article but it is not a problem
3. A fuzzy set saves only the elements belonging to its support i.e. only the elements with membership_degree > 0