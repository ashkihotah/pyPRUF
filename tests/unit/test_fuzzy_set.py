import unittest
from pyPRUF.fuzzy_set import *

class Test_DiscreteFuzzySet___init__(unittest.TestCase):

    # ======== data, domain TESTING ========

    def test_empty_domain(self):
        '''
        Check empty domain
        '''
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet((), {('a', 'b'): 0.5})
    
    def test_invalid_domain_type(self):
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(['x', 'y'], {('a', 'b'): 0.5})

    def test_duplicate_domain(self):
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(('x', 'x'), {('a', 'b'): 0.5})

    def test_invalid_data_type(self):
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(('x', 'y'), 'invalid_type')

    def test_invalid_membership_value_less_than_0(self):
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(('x', 'y'), {('a', 'b'): .0}) # -0.1

    def test_invalid_membership_value_greater_than_1(self):
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 1.1})
    
    def test_invalid_membership_value_type(self):
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 1})
    
    def test_invalid_element_length_more(self):
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(('x', 'y'), {('a', 'b', 'c'): .1, ('a', 'b'): .2})
    
    def test_invalid_element_length_less(self):
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(('x', 'y'), {('a', ): .1, ('a', 'b'): .2})

    def test_valid_dict(self):
        domain = ('x', 'y')
        data = {('a', 'b'): 0.5, ('c', 'd'): 0.8}
        fuzzy_set = DiscreteFuzzySet(domain, data)
        self.assertEqual(fuzzy_set.get_domain(), domain)
        self.assertEqual(fuzzy_set.to_dictionary(), data)

    def test_empty_dict(self):
        domain = ('x', 'y')
        data = {}
        fuzzy_set = DiscreteFuzzySet(domain, data)
        self.assertEqual(fuzzy_set.get_domain(), domain)
        self.assertEqual(fuzzy_set.to_dictionary(), data)   

    # ======== Dataframe TESTING ========

    def test_valid_dataframe(self):
        data = {'x': ['a', 'c'], 'y': ['b', 'd'], 'mu': [0.5, 0.8]}
        df = DataFrame(data)
        fuzzy_set = DiscreteFuzzySet(data=df)
        self.assertEqual(fuzzy_set.get_domain(), ('x', 'y'))
        self.assertEqual(fuzzy_set.to_dictionary(), {('a', 'b'): 0.5, ('c', 'd'): 0.8})

    def test_dataframe_without_mu_column(self):
        data = {'x': ['a', 'c'], 'y': ['b', 'd']}
        df = DataFrame(data)
        fuzzy_set = DiscreteFuzzySet(data=df)
        self.assertEqual(fuzzy_set.get_domain(), ('x', 'y'))
        self.assertEqual(fuzzy_set.to_dictionary(), {('a', 'b'): 1.0, ('c', 'd'): 1.0})

    def test_empty_dataframe(self):
        df = DataFrame()
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(data=df)
    
    def test_no_tuples_dataframe(self):
        df = DataFrame({'col': tuple()})
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(data=df)
    
    def test_dataframe_with_columns_with_different_lengths(self):
        df = DataFrame({80: (1, 2, 3), 90: (1, 2, 3)})
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(data=df)

    def test_invalid_membership_less_than_0(self):
        data = {'x': ['a', 'c'], 'y': ['b', 'd'], 'mu': [.0, .8]} # -0.1
        df = DataFrame(data)
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(data=df)
    
    def test_invalid_membership_greater_than_1(self):
        data = {'x': ['a', 'c'], 'y': ['b', 'd'], 'mu': [1.5, .8]}
        df = DataFrame(data)
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(data=df)
    
    def test_invalid_membership_type(self):
        data = {'x': ['a', 'c'], 'y': ['b', 'd'], 'mu': [1, 8]}
        df = DataFrame(data)
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(data=df)

class Test_DiscreteFuzzySet___getitem__(unittest.TestCase):
    
    def setUp(self):
        self.domain = ('A', 'B')
        self.data = {
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.7
        }
        self.fuzzy_set = DiscreteFuzzySet(domain=self.domain, data=self.data)

    def test_element_not_in_dict(self):
        element = 'fake'
        self.assertEqual(self.fuzzy_set[element], .0)
    
    def test_valid_element(self):
        element = ('A', 'B')
        self.assertEqual(self.fuzzy_set[element], .5)

class Test_DiscreteFuzzySet___setitem__(unittest.TestCase):
    
    def setUp(self):
        self.domain = ('A', 'B')
        self.data = {
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.7
        }
        self.fuzzy_set = DiscreteFuzzySet(domain=self.domain, data=self.data)
    
    def test_update_element_membership(self):
        self.fuzzy_set[('A', 'B')] = 0.8
        self.assertEqual(self.fuzzy_set[('A', 'B')], 0.8)
    
    def test_add_element_with_membership(self):
        self.fuzzy_set[('A', 'D')] = 0.9
        self.assertEqual(self.fuzzy_set[('A', 'D')], 0.9)
    
    def test_invalid_membership_type(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set[('A', 'B')] = 1
    
    def test_membership_greater_than_1(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set[('A', 'B')] = 1.5
    
    def test_membership_less_than_0(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set[('A', 'B')] = .0 # -0.1
    
    def test_invalid_element_type(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set[123] = 0.5
    
    def test_element_length_mismatch_less(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set[('A',)] = 0.5
    
    def test_element_length_mismatch_greater(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set[('A', 'B', 'C')] = 0.5

class Test_DiscreteFuzzySet___delitem__(unittest.TestCase):
    
    def setUp(self):
        self.domain = ('A', 'B')
        self.data = {
            ('A', 'B'): .5,
            ('A', 'C'): .7
        }
        self.fuzzy_set = DiscreteFuzzySet(domain=self.domain, data=self.data)

    def test_valid_element(self):
        element = ('A', 'B')
        del self.fuzzy_set[element]
        self.assertEqual(self.fuzzy_set.to_dictionary(), {('A', 'C'): .7})
    
    def test_emptying(self):
        del self.fuzzy_set[('A', 'B')]
        del self.fuzzy_set[('A', 'C')]
        self.assertEqual(self.fuzzy_set.to_dictionary(), {})

    def test_invalid_element(self):
        pre = self.fuzzy_set.to_dictionary()
        del self.fuzzy_set[('fake', )]
        post = self.fuzzy_set.to_dictionary()
        self.assertEqual(pre, post)
    
class Test_DiscreteFuzzySet___or__(unittest.TestCase):

    def setUp(self):
        self.domain = ('A', 'B')
        self.data1 = {
            ('V', 'D'): 0.1,
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.3,
            ('F', 'G'): 0.7
        }
        self.fuzzy_set1 = DiscreteFuzzySet(domain=self.domain, data=self.data1)

    def test_disjoint_sets(self):
        data2 = {
            ('H', 'I'): 0.8,
            ('L', 'M'): 0.6
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        result = self.fuzzy_set1 | fuzzy_set2
        expected_data = {
            ('V', 'D'): 0.1,
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.3,
            ('F', 'G'): 0.7,
            ('H', 'I'): 0.8,
            ('L', 'M'): 0.6
        }
        self.assertEqual(result.to_dictionary(), expected_data)

    def test_partial_overlap(self):
        data2 = {
            ('F', 'G'): 0.4,
            ('A', 'C'): 0.8,
            ('L', 'M'): 0.6,
            ('P', 'Q'): 0.2
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        result = self.fuzzy_set1 | fuzzy_set2
        expected_data = {
            ('V', 'D'): 0.1,
            ('A', 'B'): 0.5,
            ('L', 'M'): 0.6,
            ('P', 'Q'): 0.2,
            ('F', 'G'): FuzzyLogic.or_fun(.4, .7),
            ('A', 'C'): FuzzyLogic.or_fun(.3, .8),
        }
        self.assertEqual(result.to_dictionary(), expected_data)

    def test_empty_sets(self):
        empty_set1 = DiscreteFuzzySet(domain=self.domain, data={})
        empty_set2 = DiscreteFuzzySet(domain=self.domain, data={})
        result = empty_set1 | empty_set2
        self.assertEqual(result.to_dictionary(), {})

    def test_idempotence(self):
        '''
        \x1b[33mProprietà Idempotenza: A ∪ A = A \x1b[0m
        '''
        result = self.fuzzy_set1 | self.fuzzy_set1
        self.assertEqual(result.to_dictionary(), self.fuzzy_set1.to_dictionary())

    def test_empty_with_non_empty_union(self):
        '''
        \x1b[33m Proprietà del dominio vuoto: A ∪ ∅ = A \x1b[0m
        '''
        empty_set1 = DiscreteFuzzySet(domain=self.domain, data={})
        result = empty_set1 | self.fuzzy_set1
        self.assertEqual(result.to_dictionary(), self.fuzzy_set1.to_dictionary())

    def test_commutativity(self):
        '''
        \x1b[33mProprietà Commutatività: A ∪ B = B ∪ A \x1b[0m
        '''
        data2 = {
            ('F', 'G'): 0.4,
            ('A', 'C'): 0.8,
            ('L', 'M'): 0.6,
            ('P', 'Q'): 0.2
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        result1 = self.fuzzy_set1 | fuzzy_set2
        result2 = fuzzy_set2 | self.fuzzy_set1
        self.assertEqual(result1, result2)

    def test_associativity(self):
        '''
        \x1b[33mProprietà Associatività: A ∪ (B ∪ C) = (A ∪ B) ∪ C \x1b[0m
        '''
        data2 = {
            ('H', 'I'): 0.8,
            ('L', 'M'): 0.6
        }
        data3 = {
            ('F', 'P'): 0.2,
            ('Z', 'X'): 0.9
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        fuzzy_set3 = DiscreteFuzzySet(domain=self.domain, data=data3)
        result1 = self.fuzzy_set1 | (fuzzy_set2 | fuzzy_set3)
        result2 = (self.fuzzy_set1 | fuzzy_set2) | fuzzy_set3
        self.assertEqual(result1.to_dictionary(), result2.to_dictionary())

    def test_different_domain(self):
        different_domain_fuzzy_set = DiscreteFuzzySet(domain=('X', 'Y'), data={('X', 'Y'): 0.5})
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 | different_domain_fuzzy_set

    def test_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 | "invalid_type"   

class Test_DiscreteFuzzySet___and__(unittest.TestCase):

    def setUp(self):
        self.domain = ('A', 'B')
        self.data1 = {
            ('V', 'D'): 0.1,
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.3,
            ('F', 'G'): 0.7
        }
        self.fuzzy_set1 = DiscreteFuzzySet(domain=self.domain, data=self.data1)

    def test_disjoint_sets(self):
        data2 = {
            ('H', 'I'): 0.8,
            ('L', 'M'): 0.6
        }
        expected_data = {
            # ('V', 'D'): .0,
            # ('A', 'B'): .0,
            # ('A', 'C'): .0,
            # ('F', 'G'): .0,
            # ('H', 'I'): .0,
            # ('L', 'M'): .0
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        result = self.fuzzy_set1 & fuzzy_set2
        self.assertEqual(result.to_dictionary(), expected_data)

    def test_partial_overlap(self):
        data2 = {
            ('F', 'G'): 0.4,
            ('A', 'C'): 0.8,
            ('L', 'M'): 0.6,
            ('P', 'Q'): 0.2
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        result = self.fuzzy_set1 & fuzzy_set2
        expected_data = {
            ('F', 'G'): FuzzyLogic.and_fun(.4, .7),
            ('A', 'C'): FuzzyLogic.and_fun(.3, .8),
        }
        self.assertEqual(result.to_dictionary(), expected_data)

    def test_empty_sets(self):
        empty_set1 = DiscreteFuzzySet(domain=self.domain, data={})
        empty_set2 = DiscreteFuzzySet(domain=self.domain, data={})
        result = empty_set1 & empty_set2
        self.assertEqual(result.to_dictionary(), {})

    def test_idempotence(self):
        '''
        \x1b[33mProprietà Idempotenza: A ∩ A = A \x1b[0m
        '''
        result = self.fuzzy_set1 & self.fuzzy_set1
        self.assertEqual(result.to_dictionary(), self.fuzzy_set1.to_dictionary())

    def test_empty_with_non_empty_intersection(self):
        '''
        \x1b[33mProprietà del dominio vuoto: A ∩ ∅ = ∅ \x1b[0m
        '''
        empty_set1 = DiscreteFuzzySet(domain=self.domain, data={})
        result = empty_set1 & self.fuzzy_set1
        self.assertEqual(result.to_dictionary(), {})

    def test_commutativity(self):
        '''
        \x1b[33mProprietà Commutatività: A ∩ B = B ∩ A \x1b[0m
        '''
        data2 = {
            ('F', 'G'): 0.4,
            ('A', 'C'): 0.8,
            ('L', 'M'): 0.6,
            ('P', 'Q'): 0.2
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        result1 = self.fuzzy_set1 & fuzzy_set2
        result2 = fuzzy_set2 & self.fuzzy_set1
        self.assertEqual(result1, result2)

    def test_associativity(self):
        '''
        \x1b[33mProprietà Associatività: A ∩ (B ∩ C) = (A ∩ B) ∩ C \x1b[0m
        '''
        # self.data1 = {
        #     ('V', 'D'): 0.1,
        #     ('A', 'B'): 0.5,
        #     ('A', 'C'): 0.3,
        #     ('F', 'G'): 0.7
        # }
        data2 = {
            ('H', 'I'): 0.8,
            ('F', 'G'): 0.6,
            ('A', 'B'): 0.4
        }
        data3 = {
            ('A', 'B'): 0.2,
            ('Z', 'X'): 0.9,
            ('A', 'C'): 0.2
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        fuzzy_set3 = DiscreteFuzzySet(domain=self.domain, data=data3)
        result1 = self.fuzzy_set1 & (fuzzy_set2 & fuzzy_set3)
        result2 = (self.fuzzy_set1 & fuzzy_set2) & fuzzy_set3
        self.assertEqual(result1.to_dictionary(), result2.to_dictionary())

    def test_different_domain(self):
        different_domain_fuzzy_set = DiscreteFuzzySet(domain=('X', 'Y'), data={('X', 'Y'): 0.5})
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 & different_domain_fuzzy_set

    def test_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 & "invalid_type"

class Test_DiscreteFuzzySet___sub__(unittest.TestCase):

    def setUp(self):
        self.domain = ('A', 'B')
        self.data1 = {
            ('V', 'D'): 0.1,
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.3,
            ('F', 'G'): 0.7
        }
        self.fuzzy_set1 = DiscreteFuzzySet(domain=self.domain, data=self.data1)

    def test_disjoint_sets(self):
        data2 = {
            ('H', 'I'): 0.8,
            ('L', 'M'): 0.6
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        result = self.fuzzy_set1 - fuzzy_set2
        self.assertEqual(result.to_dictionary(), self.fuzzy_set1.to_dictionary())

    def test_partial_overlap(self):
        data2 = {
            ('F', 'G'): 0.4,
            ('A', 'C'): 0.8,
            ('L', 'M'): 0.6,
            ('P', 'Q'): 0.2
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        result = self.fuzzy_set1 - fuzzy_set2
        expected_data = {
            ('V', 'D'): 0.1,
            ('A', 'B'): 0.5,
            ('A', 'C'): FuzzyLogic.and_fun(self.fuzzy_set1[('A', 'C')], FuzzyLogic.not_fun(fuzzy_set2[('A', 'C')])),
            ('F', 'G'): FuzzyLogic.and_fun(self.fuzzy_set1[('F', 'G')], FuzzyLogic.not_fun(fuzzy_set2[('F', 'G')]))
        }
        self.assertEqual(result.to_dictionary(), expected_data)

    def test_empty_sets(self):
        empty_set1 = DiscreteFuzzySet(domain=self.domain, data={})
        empty_set2 = DiscreteFuzzySet(domain=self.domain, data={})
        result = empty_set1 - empty_set2
        self.assertEqual(result.to_dictionary(), {})

    # def test_non_inverse(self):
    #     '''
    #     \x1b[33mProprietà dell'inverso: A - A != ∅ \x1b[0m
    #     '''
    #     result = self.fuzzy_set1 - self.fuzzy_set1
    #     self.assertNotEqual(result.to_dictionary(), {})

    def test_empty_with_non_empty_difference(self):
        '''
        \x1b[33mProprietà del dominio vuoto: ∅ - A = ∅ \x1b[0m
        '''
        empty_set1 = DiscreteFuzzySet(domain=self.domain, data={})
        result = empty_set1 - self.fuzzy_set1
        self.assertEqual(result.to_dictionary(), {})
    
    def test_non_empty_with_empty_difference(self):
        '''
        \x1b[33mProprietà del dominio vuoto: A - ∅ = A \x1b[0m
        '''
        empty_set1 = DiscreteFuzzySet(domain=self.domain, data={})
        result = self.fuzzy_set1 - empty_set1
        self.assertEqual(result.to_dictionary(), self.fuzzy_set1.to_dictionary())

    def test_non_commutativity(self):
        '''
        \x1b[33mProprietà Commutatività: A - B != B - A \x1b[0m
        '''
        data2 = {
            ('F', 'G'): 0.4,
            ('A', 'C'): 0.8,
            ('L', 'M'): 0.6,
            ('P', 'Q'): 0.2
        }
        fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
        result1 = self.fuzzy_set1 - fuzzy_set2
        result2 = fuzzy_set2 - self.fuzzy_set1
        self.assertNotEqual(result1, result2)

    # def test_non_associativity(self):
    #     '''
    #     \x1b[33mProprietà Associatività: A - (B - C) != (A - B) - C \x1b[0m
    #     '''
    #     data2 = {
    #         ('H', 'I'): 0.8,
    #         ('L', 'M'): 0.6
    #     }
    #     data3 = {
    #         ('F', 'P'): 0.2,
    #         ('Z', 'X'): 0.9
    #     }
    #     fuzzy_set2 = DiscreteFuzzySet(domain=self.domain, data=data2)
    #     fuzzy_set3 = DiscreteFuzzySet(domain=self.domain, data=data3)
    #     result1 = self.fuzzy_set1 - (fuzzy_set2 - fuzzy_set3)
    #     result2 = (self.fuzzy_set1 - fuzzy_set2) - fuzzy_set3
    #     self.assertNotEqual(result1.to_dictionary(), result2.to_dictionary())

    def test_different_domain(self):
        different_domain_fuzzy_set = DiscreteFuzzySet(domain=('X', 'Y'), data={('X', 'Y'): 0.5})
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 - different_domain_fuzzy_set

    def test_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 - "invalid_type"

class Test_DiscreteFuzzySet___mul__(unittest.TestCase):

    def setUp(self):
        # Set up some sample fuzzy sets for testing
        self.set1 = DiscreteFuzzySet(('A', 'B'), {
            ('a', 'b'): 0.8,
            ('c', 'd'): 0.6
        })
        self.set2 = DiscreteFuzzySet(('C',), {
            ('e',): 0.7,
            ('f',): 0.5
        })

        # Set up a set with overlapping domains to test assertion
        self.set3 = DiscreteFuzzySet(('A', 'D'), {
            ('a', 'e'): 0.9,
            ('c', 'f'): 0.4
        })

    def test_valid_multiplication(self):
        # Test valid multiplication
        result = self.set1 * self.set2
        expected_data = {
            ('a', 'b', 'e'): FuzzyLogic.and_fun(self.set1[('a', 'b')], self.set2[('e', )]),
            ('a', 'b', 'f'): FuzzyLogic.and_fun(self.set1[('a', 'b')], self.set2[('f', )]),
            ('c', 'd', 'e'): FuzzyLogic.and_fun(self.set1[('c', 'd')], self.set2[('e', )]),
            ('c', 'd', 'f'): FuzzyLogic.and_fun(self.set1[('c', 'd')], self.set2[('f', )])
        }
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_domain(), ('A', 'B', 'C'))

    def test_empty_result(self):
        set4 = DiscreteFuzzySet(('C',))
        result = self.set1 * set4
        self.assertEqual(result.to_dictionary(), {})
        self.assertEqual(result.get_domain(), ('A', 'B', 'C'))

    def test_associativity(self):
        '''
        \x1b[33mProprietà Associatività: A x (B x C) = (A x B) x C \x1b[0m
        '''
        data3 = {
            ('q', 'p'): 0.2,
            ('t', 'u'): 0.9
        }
        set3 = DiscreteFuzzySet(domain=('D', 'E'), data=data3)
        result1 = self.set1 * (self.set2 * set3)
        result2 = (self.set1 * self.set2) * set3
        self.assertEqual(result1.to_dictionary(), result2.to_dictionary())

    def test_overlapping_domains(self):
        with self.assertRaises(AssertionError) as context:
            self.set1 * self.set3
        self.assertIn("'A' is in both domains", str(context.exception))

class Test_DiscreteFuzzySet___matmul__(unittest.TestCase):

    def setUp(self):
        self.set1 = DiscreteFuzzySet(
            ('A', 'B', 'C'), {
            ('a', 'b', 'r'): 0.5,
            ('c', 'd', 's'): 0.2,
            ('e', 'f', 't'): 0.7,
            ('g', 'h', 'u'): 0.2,
            ('i', 'l', 'v'): 0.7,
        })
        self.set2 = DiscreteFuzzySet(
            ('A', 'B', 'D'), {
            ('a', 'b', 't'): 0.3,
            ('c', 'd', 'p'): 0.8,
            ('e', 'f', 'v'): 0.4,
            ('u', 'i' ,'v'): 0.1,
            ('x', 'm', 'y'): 0.6,
            ('z', 'o', 'k'): 0.9,
        })
        self.set3 = DiscreteFuzzySet(
            ('A', 'B', 'C'), {
            ('a', 'b', 't'): 0.3,
            ('c', 'd', 'p'): 0.8,
            ('e', 'f', 'v'): 0.4,
            ('u', 'i' ,'v'): 0.1,
            ('x', 'm', 'y'): 0.6,
            ('z', 'o', 'k'): 0.9,
        })
        self.set4 = DiscreteFuzzySet(
            ('A', 'C'), {
            ('a', 't'): 0.2,
            ('c', 'p'): 0.1,
            ('e', 'v'): 0.6,
            ('u', 'a'): 0.2,
            ('x', 'b'): 0.9,
            ('z', 'c'): 0.7,
        })
        self.set5 = DiscreteFuzzySet(
            ('A', 'C'), {
            ('u', 'f'): 0.2,
            ('x', 'd'): 0.9,
            ('z', 'x'): 0.7,
        })

    def test_join_with_empty_fuzzy_set(self):
        empty = DiscreteFuzzySet(('A', 'B'))
        result1 = empty @ self.set1
        result2 = self.set1 @ empty
        self.assertEqual(result1.to_dictionary(), {})
        self.assertEqual(result2.to_dictionary(), {})

    def test_empty_result(self):
        result1 = self.set4 @ self.set5
        result2 = self.set5 @ self.set4
        self.assertEqual(result2.to_dictionary(), {})
        self.assertEqual(result1.to_dictionary(), {})
    
    def test_partial_overlapping_1(self):
        expected_data = {
            ('a', 'b', 'r', 't'): FuzzyLogic.and_fun(.5, .3),
            ('c', 'd', 's', 'p'): FuzzyLogic.and_fun(.2, .8),
            ('e', 'f', 't', 'v'): FuzzyLogic.and_fun(.4, .7)
        }
        result = self.set1 @ self.set2
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_domain(), ('A', 'B', 'C', 'D'))
    
    def test_partial_overlapping_2(self):
        expected_data = {
            ('a', 'b', 't', 'r'): FuzzyLogic.and_fun(.5, .3),
            ('c', 'd', 'p', 's'): FuzzyLogic.and_fun(.2, .8),
            ('e', 'f', 'v', 't'): FuzzyLogic.and_fun(.4, .7)
        }
        result = self.set2 @ self.set1
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_domain(), ('A', 'B', 'D', 'C'))
    
    def test_same_domain(self):
        expected_data = self.set1 & self.set3
        result = self.set1 @ self.set3
        self.assertEqual(expected_data.to_dictionary(), result.to_dictionary())

    def test_inclusion_right(self):
        result = self.set3 @ self.set4
        self.assertEqual(result.to_dictionary(), {
            ('a', 'b', 't'): FuzzyLogic.and_fun(.3, .2),
            ('c', 'd', 'p'): FuzzyLogic.and_fun(.8, .1),
            ('e', 'f', 'v'): FuzzyLogic.and_fun(.6, .4)
        })
        self.assertEqual(result.get_domain(), ('A', 'B', 'C'))
    
    def test_inclusion_left(self):
        result = self.set4 @ self.set3
        self.assertEqual(result.to_dictionary(), {
            ('a', 't', 'b'): FuzzyLogic.and_fun(.3, .2),
            ('c', 'p', 'd'): FuzzyLogic.and_fun(.8, .1),
            ('e', 'v', 'f'): FuzzyLogic.and_fun(.6, .4)
        })
        self.assertEqual(result.get_domain(), ('A', 'C', 'B'))

    def test_disjoint_domains(self):
        fset = DiscreteFuzzySet(domain=('D', 'E', 'F'))
        with self.assertRaises(AssertionError):
            self.set1 @ fset

class Test_DiscreteFuzzySet_projection(unittest.TestCase):
    
    def setUp(self):
        self.domain = ('A', 'B', 'C')
        self.data = {
            ('a1', 'b1', 'c1'): 0.8,
            ('a3', 'b1', 'c1'): 0.2,
            ('a1', 'b2', 'c1'): 0.6,
            ('a1', 'b1', 'c2'): 0.3,
            ('a3', 'b2', 'c1'): 0.7,
            ('a3', 'b3', 'c1'): 0.1,
            ('a1', 'b2', 'c2'): 0.5,
        }
        self.fuzzy_set = DiscreteFuzzySet(self.domain, self.data)

    def test_and_projection_valid_subdomain(self):
        subdomain = ('A', 'C')
        operator = FuzzyLogic._FuzzyLogic__and_fun
        result = self.fuzzy_set.projection(subdomain, operator)
        expected_data = {
            ('a1', 'c1'): operator(.8, .6),
            ('a3', 'c1'): operator(operator(.2, .7), .1),
            ('a1', 'c2'): operator(.3, .5)
        }
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_domain(), subdomain)
    
    def test_or_projection_valid_subdomain(self):
        subdomain = ('A', 'C')
        operator = FuzzyLogic._FuzzyLogic__or_fun
        result = self.fuzzy_set.projection(subdomain, operator)

        expected_data = {
            ('a1', 'c1'): operator(.8, .6),
            ('a3', 'c1'): operator(operator(.2, .7), .1),
            ('a1', 'c2'): operator(.3, .5)
        }
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_domain(), subdomain)

    def test_invalid_subdomain(self):
        subdomain = ('A', 'D')
        with self.assertRaises(AssertionError):
            self.fuzzy_set.projection(subdomain, FuzzyLogic.and_fun)
    
    def test_empty_subdomain(self):
        subdomain = ()
        with self.assertRaises(AssertionError):
            self.fuzzy_set.projection(subdomain, FuzzyLogic.and_fun)

    def test_invalid_operator(self):
        subdomain = ('A', 'C')
        with self.assertRaises(AssertionError):
            self.fuzzy_set.projection(subdomain, None)