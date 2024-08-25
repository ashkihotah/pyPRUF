import time
from pyPRUF.fuzzy_logic import FuzzyAnd, FuzzyOr, LinguisticModifiers
from pyPRUF.fuzzy_set import DiscreteFuzzySet

if __name__ == "__main__":
    start_time = time.time()

    A = DiscreteFuzzySet(('D1', 'D2'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
    B = DiscreteFuzzySet(('D1', 'D2'), {(2, 'val4'): 0.1, ('val3', 4.4): 0.5, ('val1', 3.4): 0.7})
    C = DiscreteFuzzySet(('D1', ), {(2,): 0.1, ('val3',): 0.5})
    D = DiscreteFuzzySet(('n', ), {(0, ): .1, (1, ): .2, (2, ): 0.2, (3, ): 0.4, (4, ): 0.6, (5, ): 0.8})
    not_D = ~D
    E = DiscreteFuzzySet(('D1', 'D3'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
    F = DiscreteFuzzySet(('D6', 'D3'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})

    print("A[(1, 'val2')]:", A[(1, 'val2')])
    A[(1, 'val2')] = 0.7
    print("A[(1, 'val2')] (modified with 0.7):", A[(1, 'val2')])
    print("A =", A)
    print("B =", B)
    print("C =", C)
    print("D =", D)
    print("NOT(D) =", not_D)
    print("E =", E)

    union_set = A | B
    intersection_set = A & B
    difference_set = A - B
    complement_set = union_set - A # A complement relative to A ∪ B
    complement_set = ~A
    cartesian_product_set = A * F
    natural_join_set = A @ E
    or_projection_set = A.projection(('D2',), FuzzyOr.MAX)
    and_projection_set = A.projection(('D2',), FuzzyAnd.MIN)
    particularization = A.particularization({'D1': C})
    print("A ∪ B =", union_set, "\ndomain:", union_set.get_domain(), end="")
    print("    cardinality:", union_set.cardinality())
    print("A ∩ B =", intersection_set, "\ndomain:", intersection_set.get_domain(), end="")
    print("    cardinality:", intersection_set.cardinality())
    print("A - B =", difference_set, "\ndomain:", difference_set.get_domain(), end="")
    print("    cardinality:", difference_set.cardinality())
    print("~A rel_to(A ∪ B) =", complement_set, "\ndomain:", complement_set.get_domain(), end="")
    print("    cardinality:", complement_set.cardinality())
    print("~A =", complement_set, "\ndomain:", complement_set.get_domain(), end="")
    print("    cardinality:", complement_set.cardinality())
    print("A × F =", cartesian_product_set, "\ndomain:", cartesian_product_set.get_domain(), end="")
    print("    cardinality:", cartesian_product_set.cardinality())
    print("or_projection(A, ('D2'))", or_projection_set, "\ndomain:", or_projection_set.get_domain(), end="")
    print("    cardinality:", or_projection_set.cardinality())
    print("and_projection(A, ('D2'))", and_projection_set, "\ndomain:", and_projection_set.get_domain(), end="")
    print("    cardinality:", and_projection_set.cardinality())
    print("particularization(A, {'D1': C})", particularization)
    print("proportion{A/G} = ", A / B)
    print(not_D.compatibility(D))
    print("Cons{NOT(SMALL_INTEGER), SMALL_INTEGER} = ", not_D.consistency(D))
    print("A ⋈ E =", natural_join_set, "\ndomain: ", natural_join_set.get_domain(), end="")
    print("very(A) =", A.apply(LinguisticModifiers.VERY))
    print("Cilindrical_Extension(A, F) =\n", A.cylindrical_extension(F)[0].tab_str())

    A.rename_domain({'D1': 'X1', 'D2': 'X2'})
    print(A.get_domain())
    print(A)

    def example_function(element):
        if element == ('a', 'b'):
            return ('c', )
        elif element == ('c', 'd'):
            return ('c', )
        elif element == ('e', 'f'):
            return ('d', )
    
    original_set = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.5, ('c', 'd'): 0.8, ('e', 'f'): 0.4})
    image_set = original_set.image(example_function, ('z',))
    print(image_set.to_dictionary())
    print(image_set.get_domain())

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nElapsed time: {elapsed_time} seconds")