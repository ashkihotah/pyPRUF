import unittest
from pyPRUF.fuzzy_logic import FuzzyAnd, FuzzyNot, FuzzyOr, LinguisticModifiers
from pyPRUF.fuzzy_sets import *

class Test_DiscreteFuzzySet___init__(unittest.TestCase):

    # ======== mf, schema TESTING ========

    def test_empty_schema(self):
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet((), {('a', 'b'): 0.5})
    
    def test_invalid_schema_type(self):
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(['x', 'y'], {('a', 'b'): 0.5})

    def test_duplicate_schema(self):
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
        schema = ('x', 'y')
        mf = {('a', 'b'): 0.5, ('c', 'd'): 0.8}
        fuzzy_set = DiscreteFuzzySet(schema, mf)
        self.assertEqual(fuzzy_set.get_schema(), schema)
        self.assertEqual(fuzzy_set.to_dictionary(), mf)

    def test_empty_dict(self):
        schema = ('x', 'y')
        mf = {}
        fuzzy_set = DiscreteFuzzySet(schema, mf)
        self.assertEqual(fuzzy_set.get_schema(), schema)
        self.assertEqual(fuzzy_set.to_dictionary(), mf)   

    # ======== Dataframe TESTING ========

    def test_valid_dataframe(self):
        mf = {'x': ['a', 'c'], 'y': ['b', 'd'], 'mu': [0.5, 0.8]}
        df = DataFrame(mf)
        fuzzy_set = DiscreteFuzzySet(mf=df)
        self.assertEqual(fuzzy_set.get_schema(), ('x', 'y'))
        self.assertEqual(fuzzy_set.to_dictionary(), {('a', 'b'): 0.5, ('c', 'd'): 0.8})

    def test_dataframe_without_mu_column(self):
        mf = {'x': ['a', 'c'], 'y': ['b', 'd']}
        df = DataFrame(mf)
        fuzzy_set = DiscreteFuzzySet(mf=df)
        self.assertEqual(fuzzy_set.get_schema(), ('x', 'y'))
        self.assertEqual(fuzzy_set.to_dictionary(), {('a', 'b'): 1.0, ('c', 'd'): 1.0})

    def test_empty_dataframe(self):
        df = DataFrame()
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(mf=df)
    
    def test_no_tuples_dataframe(self):
        df = DataFrame({'col': tuple()})
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(mf=df)
    
    def test_dataframe_with_columns_with_different_lengths(self):
        df = DataFrame({80: (1, 2, 3), 90: (1, 2, 3)})
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(mf=df)

    def test_invalid_membership_less_than_0(self):
        mf = {'x': ['a', 'c'], 'y': ['b', 'd'], 'mu': [.0, .8]} # -0.1
        df = DataFrame(mf)
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(mf=df)
    
    def test_invalid_membership_greater_than_1(self):
        mf = {'x': ['a', 'c'], 'y': ['b', 'd'], 'mu': [1.5, .8]}
        df = DataFrame(mf)
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(mf=df)
    
    def test_invalid_membership_type(self):
        mf = {'x': ['a', 'c'], 'y': ['b', 'd'], 'mu': [1, 8]}
        df = DataFrame(mf)
        with self.assertRaises(AssertionError):
            DiscreteFuzzySet(mf=df)

class Test_DiscreteFuzzySet___getitem__(unittest.TestCase):
    
    def setUp(self):
        self.schema = ('A', 'B')
        self.mf = {
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.7
        }
        self.fuzzy_set = DiscreteFuzzySet(schema=self.schema, mf=self.mf)

    def test_element_not_in_dict(self):
        element = 'fake'
        self.assertEqual(self.fuzzy_set[element], .0)
    
    def test_valid_element(self):
        element = ('A', 'B')
        self.assertEqual(self.fuzzy_set[element], .5)

class Test_DiscreteFuzzySet___setitem__(unittest.TestCase):
    
    def setUp(self):
        self.schema = ('A', 'B')
        self.mf = {
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.7
        }
        self.fuzzy_set = DiscreteFuzzySet(schema=self.schema, mf=self.mf)
    
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
        self.schema = ('A', 'B')
        self.mf = {
            ('A', 'B'): .5,
            ('A', 'C'): .7
        }
        self.fuzzy_set = DiscreteFuzzySet(schema=self.schema, mf=self.mf)

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
        self.schema = ('A', 'B')
        self.data1 = {
            ('V', 'D'): 0.1,
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.3,
            ('F', 'G'): 0.7
        }
        self.fuzzy_set1 = DiscreteFuzzySet(schema=self.schema, mf=self.data1)

    def test_disjoint_sets(self):
        data2 = {
            ('H', 'I'): 0.8,
            ('L', 'M'): 0.6
        }
        fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
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
        fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
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
        empty_set1 = DiscreteFuzzySet(schema=self.schema, mf={})
        empty_set2 = DiscreteFuzzySet(schema=self.schema, mf={})
        result = empty_set1 | empty_set2
        self.assertEqual(result.to_dictionary(), {})

    # def test_idempotence(self):
    #     '''
    #     \x1b[33mProprietà Idempotenza: A ∪ A = A \x1b[0m
    #     '''
    #     result = self.fuzzy_set1 | self.fuzzy_set1
    #     self.assertEqual(result.to_dictionary(), self.fuzzy_set1.to_dictionary())

    # def test_associativity(self):
    #     '''
    #     \x1b[33mProprietà Associatività: A ∪ (B ∪ C) = (A ∪ B) ∪ C \x1b[0m
    #     '''
    #     data2 = {
    #         ('H', 'I'): 0.8,
    #         ('L', 'M'): 0.6
    #     }
    #     data3 = {
    #         ('F', 'P'): 0.2,
    #         ('Z', 'X'): 0.9
    #     }
    #     fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
    #     fuzzy_set3 = DiscreteFuzzySet(schema=self.schema, mf=data3)
    #     result1 = self.fuzzy_set1 | (fuzzy_set2 | fuzzy_set3)
    #     result2 = (self.fuzzy_set1 | fuzzy_set2) | fuzzy_set3
    #     self.assertEqual(result1.to_dictionary(), result2.to_dictionary())

    def test_empty_with_non_empty_union(self):
        '''
        \x1b[33m Proprietà del dominio vuoto: A ∪ ∅ = A \x1b[0m
        '''
        empty_set1 = DiscreteFuzzySet(schema=self.schema, mf={})
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
        fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
        result1 = self.fuzzy_set1 | fuzzy_set2
        result2 = fuzzy_set2 | self.fuzzy_set1
        self.assertEqual(result1, result2)

    def test_different_schema(self):
        different_schema_fuzzy_set = DiscreteFuzzySet(schema=('X', 'Y'), mf={('X', 'Y'): 0.5})
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 | different_schema_fuzzy_set

    def test_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 | "invalid_type"   

class Test_DiscreteFuzzySet___and__(unittest.TestCase):

    def setUp(self):
        self.schema = ('A', 'B')
        self.data1 = {
            ('V', 'D'): 0.1,
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.3,
            ('F', 'G'): 0.7
        }
        self.fuzzy_set1 = DiscreteFuzzySet(schema=self.schema, mf=self.data1)

    def test_disjoint_sets(self):
        data2 = {
            ('H', 'I'): 0.8,
            ('L', 'M'): 0.6
        }
        fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
        result = self.fuzzy_set1 & fuzzy_set2
        self.assertEqual(result.to_dictionary(), {})

    def test_partial_overlap(self):
        data2 = {
            ('F', 'G'): 0.4,
            ('A', 'C'): 0.8,
            ('L', 'M'): 0.6,
            ('P', 'Q'): 0.2
        }
        fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
        result = self.fuzzy_set1 & fuzzy_set2
        expected_data = {}
        if FuzzyLogic.and_fun(.4, .7) > .0:
            expected_data[('F', 'G')] = FuzzyLogic.and_fun(.4, .7)
        if FuzzyLogic.and_fun(.3, .8) > .0:
            expected_data[('A', 'C')] = FuzzyLogic.and_fun(.3, .8)
        self.assertEqual(result.to_dictionary(), expected_data)

    def test_empty_sets(self):
        empty_set1 = DiscreteFuzzySet(schema=self.schema, mf={})
        empty_set2 = DiscreteFuzzySet(schema=self.schema, mf={})
        result = empty_set1 & empty_set2
        self.assertEqual(result.to_dictionary(), {})

    # def test_idempotence(self):
    #     '''
    #     \x1b[33mProprietà Idempotenza: A ∩ A = A \x1b[0m
    #     '''
    #     result = self.fuzzy_set1 & self.fuzzy_set1
    #     self.assertEqual(result.to_dictionary(), self.fuzzy_set1.to_dictionary())

        # def test_associativity(self):
    #     '''
    #     \x1b[33mProprietà Associatività: A ∩ (B ∩ C) = (A ∩ B) ∩ C \x1b[0m
    #     '''
    #     data2 = {
    #         ('H', 'I'): 0.8,
    #         ('F', 'G'): 0.6,
    #         ('A', 'B'): 0.4
    #     }
    #     data3 = {
    #         ('A', 'B'): 0.2,
    #         ('Z', 'X'): 0.9,
    #         ('A', 'C'): 0.2
    #     }
    #     fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
    #     fuzzy_set3 = DiscreteFuzzySet(schema=self.schema, mf=data3)
    #     result1 = self.fuzzy_set1 & (fuzzy_set2 & fuzzy_set3)
    #     result2 = (self.fuzzy_set1 & fuzzy_set2) & fuzzy_set3
    #     self.assertEqual(result1.to_dictionary(), result2.to_dictionary())

    def test_empty_with_non_empty_intersection(self):
        '''
        \x1b[33mProprietà del dominio vuoto: A ∩ ∅ = ∅ \x1b[0m
        '''
        empty_set1 = DiscreteFuzzySet(schema=self.schema, mf={})
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
        fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
        result1 = self.fuzzy_set1 & fuzzy_set2
        result2 = fuzzy_set2 & self.fuzzy_set1
        self.assertEqual(result1, result2)

    def test_different_schema(self):
        different_schema_fuzzy_set = DiscreteFuzzySet(schema=('X', 'Y'), mf={('X', 'Y'): 0.5})
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 & different_schema_fuzzy_set

    def test_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 & "invalid_type"

class Test_DiscreteFuzzySet___sub__(unittest.TestCase):

    def setUp(self):
        self.schema = ('A', 'B')
        self.data1 = {
            ('V', 'D'): 0.1,
            ('A', 'B'): 0.5,
            ('A', 'C'): 0.3,
            ('F', 'G'): 0.7
        }
        self.fuzzy_set1 = DiscreteFuzzySet(schema=self.schema, mf=self.data1)

    def test_disjoint_sets(self):
        data2 = {
            ('H', 'I'): 0.8,
            ('L', 'M'): 0.6
        }
        fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
        result = self.fuzzy_set1 - fuzzy_set2
        self.assertEqual(result.to_dictionary(), self.fuzzy_set1.to_dictionary())

    def test_partial_overlap(self):
        data2 = {
            ('F', 'G'): 0.4,
            ('A', 'C'): 0.8,
            ('L', 'M'): 0.6,
            ('P', 'Q'): 0.2
        }
        fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
        result = self.fuzzy_set1 - fuzzy_set2
        expected_data = {
            ('V', 'D'): 0.1,
            ('A', 'B'): 0.5
        }
        if FuzzyLogic.and_fun(self.fuzzy_set1[('A', 'C')], FuzzyLogic.not_fun(fuzzy_set2[('A', 'C')])) > .0:
            expected_data[('A', 'C')] = FuzzyLogic.and_fun(self.fuzzy_set1[('A', 'C')], FuzzyLogic.not_fun(fuzzy_set2[('A', 'C')]))
        if FuzzyLogic.and_fun(self.fuzzy_set1[('F', 'G')], FuzzyLogic.not_fun(fuzzy_set2[('F', 'G')])) > .0:
            expected_data[('F', 'G')] = FuzzyLogic.and_fun(self.fuzzy_set1[('F', 'G')], FuzzyLogic.not_fun(fuzzy_set2[('F', 'G')]))         
        self.assertEqual(result.to_dictionary(), expected_data)

    def test_empty_sets(self):
        empty_set1 = DiscreteFuzzySet(schema=self.schema, mf={})
        empty_set2 = DiscreteFuzzySet(schema=self.schema, mf={})
        result = empty_set1 - empty_set2
        self.assertEqual(result.to_dictionary(), {})

    # def test_inverse(self):
    #     '''
    #     \x1b[33mProprietà dell'inverso: A - A = ∅ \x1b[0m
    #     '''
    #     result = self.fuzzy_set1 - self.fuzzy_set1
    #     self.assertEqual(result.to_dictionary(), {})

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
    #     fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
    #     fuzzy_set3 = DiscreteFuzzySet(schema=self.schema, mf=data3)
    #     result1 = self.fuzzy_set1 - (fuzzy_set2 - fuzzy_set3)
    #     result2 = (self.fuzzy_set1 - fuzzy_set2) - fuzzy_set3
    #     self.assertNotEqual(result1.to_dictionary(), result2.to_dictionary())

    # def test_non_commutativity(self):
    #     '''
    #     \x1b[33mProprietà Commutatività: A - B != B - A \x1b[0m
    #     '''
    #     data2 = {
    #         ('F', 'G'): 0.4,
    #         ('A', 'C'): 0.8,
    #         ('L', 'M'): 0.6,
    #         ('P', 'Q'): 0.2
    #     }
    #     fuzzy_set2 = DiscreteFuzzySet(schema=self.schema, mf=data2)
    #     result1 = self.fuzzy_set1 - fuzzy_set2
    #     result2 = fuzzy_set2 - self.fuzzy_set1
    #     self.assertNotEqual(result1, result2)

    def test_empty_with_non_empty_difference(self):
        '''
        \x1b[33mProprietà del dominio vuoto: ∅ - A = ∅ \x1b[0m
        '''
        empty_set1 = DiscreteFuzzySet(schema=self.schema, mf={})
        result = empty_set1 - self.fuzzy_set1
        self.assertEqual(result.to_dictionary(), {})
    
    def test_non_empty_with_empty_difference(self):
        '''
        \x1b[33mProprietà del dominio vuoto: A - ∅ = A \x1b[0m
        '''
        empty_set1 = DiscreteFuzzySet(schema=self.schema, mf={})
        result = self.fuzzy_set1 - empty_set1
        self.assertEqual(result.to_dictionary(), self.fuzzy_set1.to_dictionary())

    def test_different_schema(self):
        different_schema_fuzzy_set = DiscreteFuzzySet(schema=('X', 'Y'), mf={('X', 'Y'): 0.5})
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 - different_schema_fuzzy_set

    def test_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.fuzzy_set1 - "invalid_type"

class Test_DiscreteFuzzySet___mul__(unittest.TestCase):

    def setUp(self):
        self.set1 = DiscreteFuzzySet(('A', 'B'), {
            ('a', 'b'): 0.8,
            ('c', 'd'): 0.6
        })
        self.set2 = DiscreteFuzzySet(('C',), {
            ('e',): 0.7,
            ('f',): 0.5
        })
        self.set3 = DiscreteFuzzySet(('A', 'D'), {
            ('a', 'e'): 0.9,
            ('c', 'f'): 0.4
        })

    def test_valid_multiplication(self):
        result = self.set1 * self.set2
        expected_data = {}
        if FuzzyLogic.and_fun(self.set1[('a', 'b')], self.set2[('e', )]) > .0:
            expected_data[('a', 'b', 'e')] = FuzzyLogic.and_fun(self.set1[('a', 'b')], self.set2[('e', )])
        if FuzzyLogic.and_fun(self.set1[('a', 'b')], self.set2[('f', )]) > .0:
            expected_data[('a', 'b', 'f')] = FuzzyLogic.and_fun(self.set1[('a', 'b')], self.set2[('f', )])
        if FuzzyLogic.and_fun(self.set1[('c', 'd')], self.set2[('e', )]) > .0:
            expected_data[('c', 'd', 'e')] = FuzzyLogic.and_fun(self.set1[('c', 'd')], self.set2[('e', )])
        if FuzzyLogic.and_fun(self.set1[('c', 'd')], self.set2[('f', )]) > .0:
            expected_data[('c', 'd', 'f')] = FuzzyLogic.and_fun(self.set1[('c', 'd')], self.set2[('f', )])
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_schema(), ('A', 'B', 'C'))

    def test_empty_result(self):
        set4 = DiscreteFuzzySet(('C',))
        result = self.set1 * set4
        self.assertEqual(result.to_dictionary(), {})
        self.assertEqual(result.get_schema(), ('A', 'B', 'C'))

    # def test_associativity(self):
    #     '''
    #     \x1b[33mProprietà Associatività: A x (B x C) = (A x B) x C \x1b[0m
    #     '''
    #     data3 = {
    #         ('q', 'p'): 0.2,
    #         ('t', 'u'): 0.9
    #     }
    #     set3 = DiscreteFuzzySet(schema=('D', 'E'), mf=data3)
    #     result1 = self.set1 * (self.set2 * set3)
    #     result2 = (self.set1 * self.set2) * set3
    #     self.assertEqual(result1.to_dictionary(), result2.to_dictionary())

    def test_overlapping_schemas(self):
        with self.assertRaises(AssertionError) as context:
            self.set1 * self.set3
        self.assertIn("'A' is in both schemas", str(context.exception))

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
        expected_data = {}
        if FuzzyLogic.and_fun(.5, .3) > .0:
            expected_data[('a', 'b', 'r', 't')] = FuzzyLogic.and_fun(.5, .3)
        if FuzzyLogic.and_fun(.2, .8) > .0:
            expected_data[('c', 'd', 's', 'p')] = FuzzyLogic.and_fun(.2, .8)
        if FuzzyLogic.and_fun(.4, .7) > .0:
            expected_data[('e', 'f', 't', 'v')] = FuzzyLogic.and_fun(.4, .7)
        result = self.set1 @ self.set2
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_schema(), ('A', 'B', 'C', 'D'))
    
    def test_partial_overlapping_2(self):
        expected_data = {}
        if FuzzyLogic.and_fun(.5, .3) > .0:
            expected_data[('a', 'b', 't', 'r')] = FuzzyLogic.and_fun(.5, .3)
        if FuzzyLogic.and_fun(.2, .8) > .0:
            expected_data[('c', 'd', 'p', 's')] = FuzzyLogic.and_fun(.2, .8)
        if FuzzyLogic.and_fun(.4, .7) > .0:
            expected_data[('e', 'f', 'v', 't')] = FuzzyLogic.and_fun(.4, .7)
        result = self.set2 @ self.set1
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_schema(), ('A', 'B', 'D', 'C'))
    
    def test_same_schema(self):
        expected_data = self.set1 & self.set3
        result = self.set1 @ self.set3
        self.assertEqual(expected_data.to_dictionary(), result.to_dictionary())

    def test_inclusion_right(self):
        result = self.set3 @ self.set4
        expected_data = {}
        if FuzzyLogic.and_fun(.3, .2) > .0:
            expected_data[('a', 'b', 't')] = FuzzyLogic.and_fun(.3, .2)
        if FuzzyLogic.and_fun(.8, .1) > .0:
            expected_data[('c', 'd', 'p')] = FuzzyLogic.and_fun(.8, .1)
        if FuzzyLogic.and_fun(.6, .4) > .0:
            expected_data[('e', 'f', 'v')] = FuzzyLogic.and_fun(.6, .4)
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_schema(), ('A', 'B', 'C'))
        
    
    def test_inclusion_left(self):
        result = self.set4 @ self.set3
        expected_data = {}
        if FuzzyLogic.and_fun(.3, .2):
            expected_data[('a', 't', 'b')] = FuzzyLogic.and_fun(.3, .2)
        if FuzzyLogic.and_fun(.8, .1) > .0:
            expected_data[('c', 'p', 'd')] = FuzzyLogic.and_fun(.8, .1)
        if FuzzyLogic.and_fun(.6, .4) > .0:
            expected_data[('e', 'v', 'f')] = FuzzyLogic.and_fun(.6, .4)
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_schema(), ('A', 'C', 'B'))

    def test_disjoint_schemas(self):
        fset = DiscreteFuzzySet(schema=('D', 'E', 'F'))
        with self.assertRaises(AssertionError):
            self.set1 @ fset

class Test_DiscreteFuzzySet_projection(unittest.TestCase):
    
    def setUp(self):
        self.schema = ('A', 'B', 'C')
        self.mf = {
            ('a1', 'b1', 'c1'): 0.8,
            ('a3', 'b1', 'c1'): 0.2,
            ('a1', 'b2', 'c1'): 0.6,
            ('a1', 'b1', 'c2'): 0.3,
            ('a3', 'b2', 'c1'): 0.7,
            ('a3', 'b3', 'c1'): 0.1,
            ('a1', 'b2', 'c2'): 0.5,
        }
        self.fuzzy_set = DiscreteFuzzySet(self.schema, self.mf)

    def test_and_projection_valid_subschema(self):
        subschema = ('A', 'C')
        operator = FuzzyLogic._FuzzyLogic__and_fun
        result = self.fuzzy_set.projection(subschema, operator)
        expected_data = {}
        if operator(.8, .6) > .0:
            expected_data[('a1', 'c1')] = operator(.8, .6)
        if operator(operator(.2, .7), .1) > .0:
            expected_data[('a3', 'c1')] = operator(operator(.2, .7), .1)
        if operator(.3, .5) > .0:
            expected_data[('a1', 'c2')] = operator(.3, .5)
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_schema(), subschema)
    
    def test_or_projection_valid_subschema(self):
        subschema = ('A', 'C')
        operator = FuzzyLogic._FuzzyLogic__or_fun
        result = self.fuzzy_set.projection(subschema, operator)

        expected_data = {}
        if operator(.8, .6) > .0:
            expected_data[('a1', 'c1')] = operator(.8, .6)
        if operator(operator(.2, .7), .1) > .0:
            expected_data[('a3', 'c1')] = operator(operator(.2, .7), .1)
        if operator(.3, .5) > .0:
            expected_data[('a1', 'c2')] = operator(.3, .5)
        self.assertEqual(result.to_dictionary(), expected_data)
        self.assertEqual(result.get_schema(), subschema)

    def test_invalid_subschema(self):
        subschema = ('A', 'D')
        with self.assertRaises(AssertionError):
            self.fuzzy_set.projection(subschema, FuzzyLogic.and_fun)
    
    def test_empty_subschema(self):
        subschema = ()
        with self.assertRaises(AssertionError):
            self.fuzzy_set.projection(subschema, FuzzyLogic.and_fun)

    def test_invalid_operator(self):
        subschema = ('A', 'C')
        with self.assertRaises(AssertionError):
            self.fuzzy_set.projection(subschema, None)

class Test_DiscreteFuzzySet_particularization(unittest.TestCase):

    def setUp(self):
        self.data_fs = DiscreteFuzzySet(
            ('A', 'B', 'C', 'D'), {
            ('a1', 'b1', 'c1', 'd1'): 0.8,
            ('a3', 'b1', 'c1', 'd1'): 0.2,
            ('a1', 'b2', 'c1', 'd1'): 0.6,
            ('a1', 'b1', 'c2', 'd2'): 0.3,
            ('a3', 'b2', 'c1', 'd3'): 0.7,
            ('a3', 'b3', 'c1', 'd1'): 0.1,
            ('a1', 'b2', 'c2', 'd1'): 0.5,
        })
        self.fs_ass1 = DiscreteFuzzySet(
            ('B', ), {
            ('b1', ): 0.7,
            ('b2', ): 0.4,
            ('b3', ): 0.2,
        })
        self.fs_ass2 = DiscreteFuzzySet(
            ('C', ), {
            ('c1', ): 0.4,
            ('c2', ): 0.1,
        })
    
    def test_invalid_assignment_type(self):
        with self.assertRaises(AssertionError):
            self.data_fs.particularization('fake')
    
    def test_invalid_assignment_keys(self):
        with self.assertRaises(AssertionError):
            self.data_fs.particularization({'A': 3, 'fake': 2})
    
    def test_valid_assignment(self):
        result = self.data_fs.particularization({'A': 'a1', 'B': self.fs_ass1, 'C': self.fs_ass2, 'D': 'd1'})
        expected_data = {}
        if FuzzyLogic.and_fun(FuzzyLogic.and_fun(.8, .7), .4) > .0:
            expected_data[('a1', 'b1', 'c1', 'd1')] = FuzzyLogic.and_fun(FuzzyLogic.and_fun(.8, .7), .4)
        if FuzzyLogic.and_fun(FuzzyLogic.and_fun(.6, .4), .4) > .0:
            expected_data[('a1', 'b2', 'c1', 'd1')] = FuzzyLogic.and_fun(FuzzyLogic.and_fun(.6, .4), .4)
        if FuzzyLogic.and_fun(FuzzyLogic.and_fun(.5, .4), .1) > .0:
            expected_data[('a1', 'b2', 'c2', 'd1')] = FuzzyLogic.and_fun(FuzzyLogic.and_fun(.5, .4), .1)
        self.assertEqual(result.to_dictionary(), expected_data)

class Test_DiscreteFuzzySet_cardinality(unittest.TestCase):

    def setUp(self):
        self.fs1 = DiscreteFuzzySet(
            ('A', ), {
            ('a1', ): 0.8,
            ('a2', ): 0.2,
            ('a3', ): 0.6,
            ('a4', ): 0.3,
            ('a5', ): 0.7,
            ('a6', ): 0.1,
            ('a7', ): 0.5,
        })
    
        self.empty = DiscreteFuzzySet( ('A', ), {} )
        self.fs2 = DiscreteFuzzySet(('A', ), {('a', ): .3})
    
    def test_empty_fs(self):
        self.assertEqual(self.empty.cardinality(), .0)
    
    def test_non_empty_fs(self):
        self.assertEqual(self.fs1.cardinality(), 3.2)
    
    def test_single_element_fs(self):
        self.assertEqual(self.fs2.cardinality(), .3)

class Test_DiscreteFuzzySet_mean_cardinality(unittest.TestCase):

    def setUp(self):
        self.fs1 = DiscreteFuzzySet(
            ('A', ), {
            ('a1', ): 0.8,
            ('a2', ): 0.2,
            ('a3', ): 0.6,
            ('a4', ): 0.3,
            ('a5', ): 0.7,
            ('a6', ): 0.1,
            ('a7', ): 0.5,
        })
    
        self.empty = DiscreteFuzzySet( ('A', ), {} )
        self.fs2 = DiscreteFuzzySet(('A', ), {('a', ): .3})
    
    def test_empty_fs(self):
        self.assertEqual(self.empty.mean_cardinality(), .0)
    
    def test_non_empty_fs(self):
        self.assertEqual(self.fs1.mean_cardinality(), 3.2 / 7.0)
    
    def test_single_element_fs(self):
        self.assertEqual(self.fs2.mean_cardinality(), .3)

class Test_DiscreteFuzzySet_compatibility(unittest.TestCase):

    def setUp(self):
        self.fs1 = DiscreteFuzzySet(
            ('A', ), {
            ('a1', ): 0.6,
            ('a2', ): 0.7,
            ('a3', ): 0.2,
            ('a4', ): 0.4,
            ('a5', ): 0.6,
            ('a6', ): 0.9,
            ('a7', ): 0.3,
            ('a8', ): 0.7,
            ('a9', ): 0.1,
            ('a10', ): 0.6,
            ('a11', ): 0.5,
            ('a12', ): 0.9,
            ('a13', ): 0.3,
            ('a14', ): 0.4
        })
        self.fs2 = DiscreteFuzzySet(
            ('A', ), {
            ('a1', ): 0.3,
            ('a2', ): 0.3,
            ('a3', ): 0.4,
            ('a4', ): 0.4,
            ('a5', ): 0.5,
            ('a6', ): 0.5,
            ('a7', ): 0.6,
            ('a8', ): 0.6,
            ('a9', ): 0.7,
            ('a10', ): 0.8,
            ('a11', ): 0.9,
            ('a12', ): 0.9,
            ('a13', ): 0.9,
            ('a14', ): 0.2,
        })
    
    def test_valid_set(self):
        result = self.fs1.compatibility(self.fs2)
        self.assertEqual(result.to_dictionary(), {
            (.2, ): .4,
            (.3, ): .7,
            (.4, ): .4,
            (.5, ): .9,
            (.6, ): .7,
            (.7, ): .1,
            (.8, ): .6,
            (.9, ): .9
        })

    def test_invalid_fs_type(self):
        with self.assertRaises(AssertionError):
            self.fs1.compatibility('fake')

    def test_different_schemas(self):
        with self.assertRaises(AssertionError):
            self.fs1.compatibility(DiscreteFuzzySet(('C', ), {}))

class Test_DiscreteFuzzySet_consistency(unittest.TestCase):

    def setUp(self):
        self.fs1 = DiscreteFuzzySet(
            ('A', ), {
            ('a', ): 0.3,
            ('b', ): 0.2,
            ('c', ): 0.7,
            ('d', ): 0.6,
            ('e', ): 0.9,
            ('f', ): 0.5
        })
        self.fs2 = DiscreteFuzzySet(
            ('A', ), {
            ('a', ): 0.7,
            ('b', ): 0.5,
            ('c', ): 0.3,
            ('d', ): 0.4,
            ('e', ): 0.1,
            ('f', ): 0.8
        })
    
    def test_valid_sets(self):
        result = self.fs1.consistency(self.fs2)
        self.assertEqual(result, FuzzyLogic.and_fun(.5, .8))
    
    def test_commutativity(self):
        result1 = self.fs1.consistency(self.fs2)
        result2 = self.fs2.consistency(self.fs1)
        self.assertEqual(result1, result2)
    
    def test_with_empty_sets(self):
        empty = DiscreteFuzzySet(('A', ), {})
        self.assertEqual(empty.consistency(empty), .0)
    
    def test_with_a_empty_set(self):
        empty = DiscreteFuzzySet(('A', ), {})
        self.assertEqual(self.fs1.consistency(empty), .0)

    def test_invalid_fs_type(self):
        with self.assertRaises(AssertionError):
            self.fs1.consistency('fake')
    
    def test_different_schemas(self):
        with self.assertRaises(AssertionError):
            self.fs1.consistency(DiscreteFuzzySet(('C', ), {}))

class Test_DiscreteFuzzySet_apply(unittest.TestCase):

    def setUp(self):
        self.fs1 = DiscreteFuzzySet(
            ('A', ), {
            ('a1', ): 0.6,
            ('a2', ): 0.3,
            ('a3', ): 0.2,
            ('a4', ): 0.4,
            ('a5', ): 0.3
        })
    
    def test_valid_apply(self):
        operator = LinguisticModifiers.VERY
        result = self.fs1.apply(operator)
        self.assertEqual(result.to_dictionary(), {
            ('a1', ): operator(.6),
            ('a2', ): operator(.3),
            ('a3', ): operator(.2),
            ('a4', ): operator(.4),
            ('a5', ): operator(.3)
        })
    
    def test_with_empty_fs(self):
        operator = LinguisticModifiers.VERY
        empty = DiscreteFuzzySet(('A', ), {})
        result = empty.apply(operator)
        self.assertEqual(result.to_dictionary(), {})
    
    def test_elements_with_mu_0(self):
        operator = FuzzyNot.STANDARD
        self.fs1[('h', )] = 1.0
        result = self.fs1.apply(operator)
        self.assertEqual(result.to_dictionary(), {
            ('a1', ): operator(.6),
            ('a2', ): operator(.3),
            ('a3', ): operator(.2),
            ('a4', ): operator(.4),
            ('a5', ): operator(.3)
        })

    def test_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.fs1.apply('fake')

class Test_DiscreteFuzzySet_cylindrical_extension(unittest.TestCase):

    def setUp(self):
        self.fs1 = DiscreteFuzzySet(
            ('H', 'A', 'I', 'B', 'D', 'C', 'E'), {
            ('h1', 'a1','i1', 'b1', 'd1', 'c1', 'e1'): .4,
            ('h2', 'a2','i2', 'b2', 'd2', 'c2', 'e2'): .2,
            ('h3', 'a3','i3', 'b3', 'd3', 'c3', 'e3'): .6
        })
        self.fs2 = DiscreteFuzzySet(
            ('F', 'B', 'G', 'C', 'Q', 'A', 'R'), {
            ('f1', 'b4','g1', 'c4', 'q1', 'a4', 'r1'): .2,
            ('f2', 'b5','g2', 'c5', 'q2', 'a5', 'r2'): .5,
            ('f3', 'b6','g3', 'c6', 'q3', 'a6', 'r3'): .9
        })
        self.fs3 = DiscreteFuzzySet(
            ('X', 'Y'), {
            ('x1', 'y1'): .8,
            ('x2', 'y2'): .7,
            ('x3', 'y3'): .2
        })
        self.res1, self.res2 = self.fs1.cylindrical_extension(self.fs2)
        self.dis_res1, self.dis_res2 = self.fs1.cylindrical_extension(self.fs3)

    def test_partial_overlapping_res1(self):
        self.assertEqual(self.res1.to_dictionary(), {
            ('a1', 'b1', 'c1', 'h1', 'i1', 'd1', 'e1', 'f1', 'g1', 'q1', 'r1'): .4,
            ('a1', 'b1', 'c1', 'h1', 'i1', 'd1', 'e1', 'f2', 'g2', 'q2', 'r2'): .4,
            ('a1', 'b1', 'c1', 'h1', 'i1', 'd1', 'e1', 'f3', 'g3', 'q3', 'r3'): .4,

            ('a2', 'b2', 'c2', 'h2', 'i2', 'd2', 'e2', 'f1', 'g1', 'q1', 'r1'): .2,
            ('a2', 'b2', 'c2', 'h2', 'i2', 'd2', 'e2', 'f2', 'g2', 'q2', 'r2'): .2,
            ('a2', 'b2', 'c2', 'h2', 'i2', 'd2', 'e2', 'f3', 'g3', 'q3', 'r3'): .2,

            ('a3', 'b3', 'c3', 'h3', 'i3', 'd3', 'e3', 'f1', 'g1', 'q1', 'r1'): .6,
            ('a3', 'b3', 'c3', 'h3', 'i3', 'd3', 'e3', 'f2', 'g2', 'q2', 'r2'): .6,
            ('a3', 'b3', 'c3', 'h3', 'i3', 'd3', 'e3', 'f3', 'g3', 'q3', 'r3'): .6
        })
    
    def test_partial_overlapping_res2(self):
        self.assertEqual(self.res2.to_dictionary(), {
            ('a4', 'b4', 'c4', 'h1', 'i1', 'd1', 'e1', 'f1', 'g1', 'q1', 'r1'): .2,
            ('a5', 'b5', 'c5', 'h1', 'i1', 'd1', 'e1', 'f2', 'g2', 'q2', 'r2'): .5,
            ('a6', 'b6', 'c6', 'h1', 'i1', 'd1', 'e1', 'f3', 'g3', 'q3', 'r3'): .9,

            ('a4', 'b4', 'c4', 'h2', 'i2', 'd2', 'e2', 'f1', 'g1', 'q1', 'r1'): .2,
            ('a5', 'b5', 'c5', 'h2', 'i2', 'd2', 'e2', 'f2', 'g2', 'q2', 'r2'): .5,
            ('a6', 'b6', 'c6', 'h2', 'i2', 'd2', 'e2', 'f3', 'g3', 'q3', 'r3'): .9,

            ('a4', 'b4', 'c4', 'h3', 'i3', 'd3', 'e3', 'f1', 'g1', 'q1', 'r1'): .2,          
            ('a5', 'b5', 'c5', 'h3', 'i3', 'd3', 'e3', 'f2', 'g2', 'q2', 'r2'): .5,
            ('a6', 'b6', 'c6', 'h3', 'i3', 'd3', 'e3', 'f3', 'g3', 'q3', 'r3'): .9
        })
    
    def test_check_schemas(self):
        res1_schema = self.res1.get_schema()
        self.assertEqual(res1_schema, ('A', 'B', 'C', 'H', 'I', 'D', 'E', 'F', 'G', 'Q', 'R'))
        self.assertEqual(self.res2.get_schema(), res1_schema)
    
    def test_disjoint_sets_res1(self):
        self.assertEqual(self.dis_res1.to_dictionary(), {
            ('h1', 'a1','i1', 'b1', 'd1', 'c1', 'e1', 'x1', 'y1'): .4,
            ('h1', 'a1','i1', 'b1', 'd1', 'c1', 'e1', 'x2', 'y2'): .4,
            ('h1', 'a1','i1', 'b1', 'd1', 'c1', 'e1', 'x3', 'y3'): .4,
            ('h2', 'a2','i2', 'b2', 'd2', 'c2', 'e2', 'x1', 'y1'): .2,
            ('h2', 'a2','i2', 'b2', 'd2', 'c2', 'e2', 'x2', 'y2'): .2,
            ('h2', 'a2','i2', 'b2', 'd2', 'c2', 'e2', 'x3', 'y3'): .2,
            ('h3', 'a3','i3', 'b3', 'd3', 'c3', 'e3', 'x1', 'y1'): .6,
            ('h3', 'a3','i3', 'b3', 'd3', 'c3', 'e3', 'x2', 'y2'): .6,
            ('h3', 'a3','i3', 'b3', 'd3', 'c3', 'e3', 'x3', 'y3'): .6
        })

    def test_disjoint_sets_res2(self):
        self.assertEqual(self.dis_res2.to_dictionary(), {
            ('h1', 'a1','i1', 'b1', 'd1', 'c1', 'e1', 'x1', 'y1'): .8,
            ('h1', 'a1','i1', 'b1', 'd1', 'c1', 'e1', 'x2', 'y2'): .7,
            ('h1', 'a1','i1', 'b1', 'd1', 'c1', 'e1', 'x3', 'y3'): .2,
            ('h2', 'a2','i2', 'b2', 'd2', 'c2', 'e2', 'x1', 'y1'): .8,
            ('h2', 'a2','i2', 'b2', 'd2', 'c2', 'e2', 'x2', 'y2'): .7,
            ('h2', 'a2','i2', 'b2', 'd2', 'c2', 'e2', 'x3', 'y3'): .2,
            ('h3', 'a3','i3', 'b3', 'd3', 'c3', 'e3', 'x1', 'y1'): .8,
            ('h3', 'a3','i3', 'b3', 'd3', 'c3', 'e3', 'x2', 'y2'): .7,
            ('h3', 'a3','i3', 'b3', 'd3', 'c3', 'e3', 'x3', 'y3'): .2
        })
    
    def test_disjoint_sets_schemas(self):
        self.assertEqual(self.dis_res1.get_schema(), self.dis_res2.get_schema())

    def test_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.fs1.cylindrical_extension('fake')

class Test_DiscreteFuzzySet_reorder(unittest.TestCase):

    def setUp(self):
        self.set1 = DiscreteFuzzySet(
            ('A', 'B', 'C', 'D'), {
            ('a', 'b', 'c', 'd'): .1,
            ('e', 'f', 'g', 'h'): .2,
            ('i', 'l', 'm', 'n'): .3,
        })
        self.set2 = DiscreteFuzzySet(
            ('A', 'B', 'C'), {
            ('a', 'b', 'c'): .3,
            ('e', 'f', 'g'): .2,
            ('i', 'l', 'm'): .1,
        })
        self.set3 = DiscreteFuzzySet(
            ('A', 'B'), {
            ('a', 'b'): .1,
            ('e', 'f'): .2,
            ('i', 'l'): .3,
        })
        self.set4 = DiscreteFuzzySet(
            ('A', ), {
            ('a', ): .3,
            ('e', ): .2,
            ('i', ): .1,
        })
    
    def test_single_set_schema(self):
        res = self.set1.reorder(('C', 'A', 'D', 'B'))
        self.assertEqual(res.to_dictionary(), {
            ('c', 'a', 'd', 'b'): .1,
            ('e', 'g', 'h', 'f'): .2,
            ('i', 'm', 'n', 'l'): .3,
        })
        self.assertEqual(res.get_schema(), ('C', 'A', 'D', 'B'))
    
    def test_single_set_schema(self):
        res = self.set2.reorder(('C', 'A', 'B'))
        self.assertEqual(res.to_dictionary(), {
            ('c', 'a', 'b'): .3,
            ('e', 'g', 'f'): .2,
            ('i', 'm', 'l'): .1,
        })
        self.assertEqual(res.get_schema(), ('C', 'A', 'B'))
    
    def test_single_set_schema(self):
        res = self.set3.reorder(('B', 'A'))
        self.assertEqual(res.to_dictionary(), {
            ('b', 'a'): .1,
            ('f', 'e'): .2,
            ('l', 'i'): .3,
        })
        self.assertEqual(res.get_schema(), ('B', 'A'))
    
    def test_invalid_perm(self):
        with self.assertRaises(AssertionError):
            self.set4.reorder((5, ))
    
    def test_invalid_length(self):
        with self.assertRaises(AssertionError):
            self.set1.reorder(('B', 'A'))
    
    def test_both_assertions(self):
        with self.assertRaises(AssertionError):
            self.set1.reorder(('B', 'A', 5))