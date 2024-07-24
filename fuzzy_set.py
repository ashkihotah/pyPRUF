from abc import ABC, abstractmethod
import time

from pandas import DataFrame
from fuzzy_logic import FuzzyAnd, FuzzyBinaryOperator, FuzzyLogic, FuzzyNot, FuzzyOr
from membership_functions import MembershipFunction

class FuzzySet(ABC):
    
    @abstractmethod
    def __getitem__(self, element) -> float: # membership: []
        pass

    @abstractmethod
    def __setitem__(self, element, membership: float) -> None: # add/update_element: []
        pass

    @abstractmethod
    def __or__(self, set2): # union: |, |=
        pass

    @abstractmethod
    def __and__(self, set2): # intersection: &, &=
        pass

    @abstractmethod
    def __invert__(self): # complement: ~
        pass

    @abstractmethod
    def __mul__(self, set2): # cartesian_product: *, *=
        pass

    @abstractmethod
    def __matmul__(self, set2): # natural_join: @, @=
        pass

    @abstractmethod
    def __truediv__(self, set2) -> float: # proportion: /
        pass

    @abstractmethod
    def projection(self, subdomain: tuple, operator: FuzzyBinaryOperator):
        pass

    @abstractmethod
    def select(self, assignment: dict): # particularization
        pass

    @abstractmethod
    def cardinality(self) -> float:
        pass

    @abstractmethod
    def mean_cardinality(self) -> float:
        pass

    @abstractmethod
    def compatibility(self, reference_set):
        pass

    @abstractmethod
    def consistency(self, reference_set) -> float:
        pass

    @abstractmethod
    def get_domain(self):
        pass

    @abstractmethod
    def rename_domain(self, ren_dict: dict) -> None: # <<
        pass

class ContinuousFuzzySet(FuzzySet):
    def __init__(self, domain: tuple, mf: MembershipFunction):
        assert isinstance(domain, tuple) and len(domain) > 0, "'domain' must be a non-empty tuple of strings representing the domains name!"
        assert isinstance(mf, MembershipFunction), "'mf' must be of type 'MembershipFunction'!"
        sorted_domain = list(domain)
        sorted_domain.sort()
        for i in range(1, len(sorted_domain)):
            assert domain[i] != domain[i - 1], "'domain' must not contains duplicates!"

        self.__domain = list(domain)
        self.mf = mf

    def __getitem__(self, element) -> float: # membership: []
        return self.mf(element)

    def __setitem__(self, element, membership: float) -> None: # add/update_element: []
        pass

    def __or__(self, set2): # union: |, |=
        pass

    def __and__(self, set2): # intersection: &, &=
        pass

    def __invert__(self): # complement: ~
        pass

    def __mul__(self, set2): # cartesian_product: *, *=
        pass

    def __matmul__(self, set2): # natural_join: @, @=
        pass

    def __truediv__(self, set2) -> float: # proportion: /
        pass

    def projection(self, subdomain: tuple, operator: FuzzyBinaryOperator):
        pass

    def select(self, assignment: dict): # particularization
        pass

    def cardinality(self) -> float:
        pass

    def mean_cardinality(self) -> float:
        pass

    def compatibility(self, reference_set):
        pass

    def consistency(self, reference_set) -> float:
        pass

    def get_domain(self):
        return tuple(self.__domain)

    def rename_domain(self, ren_dict: dict) -> None:
        assert isinstance(ren_dict, dict), "'dict_relation' must be a dictionary!"
        for key, value in ren_dict.items():
            assert isinstance(key, str) and isinstance(key, str), "All keys and values in 'ren_dict' must be strings!"
            assert key in self.__domain, key + " not in this FuzzySet domain!"
            assert value not in self.__domain, value + " already in this FuzzySet domain!"
            self.__domain[self.__domain.index(key)] = value

class DiscreteFuzzySet(FuzzySet):
    def __init__(self, domain: tuple = None, dict_relation: dict = None, dataframe: DataFrame = None):
        self.__non_membership_value = 0.0
        if dataframe is not None:
            dict_relation = {}
            for key, value in dataframe.to_dict().items():
                dict_relation[key] = tuple(value.values())
            keys = list(dict_relation.keys())
            assert len(keys) > 0, "There must be at least one column!"
            assert isinstance(keys[0], str), "All keys in 'dict_relation' must be strings representing the variables name!"
            assert isinstance(dict_relation[keys[0]], list) or isinstance(dict_relation[keys[0]], tuple), "All the values in 'dict_relation' must be lists or tuples with the same length!"
            length = len(dict_relation[keys[0]])
            assert length > 0, "The fuzzy set must contain at least a tuple!"
            for key, value in dict_relation.items():
                assert isinstance(key, str), "All keys in 'dict_relation' must be strings representing the variables name!"
                assert (isinstance(value, list) or isinstance(value, tuple)) and len(value) == length, "All the values in the dictionary must be lists or tuples with the same length!"
            
            self.__fuzzy_set = {}
            for i in range(0, length):
                variables = []
                mu = 1.0
                for key in keys:
                    if key != 'mu':
                        variables.append(dict_relation[key][i])
                    else:
                        mu = dict_relation[key][i]
                        assert isinstance(mu, float) and 0.0 <= mu and mu <= 1.0, "All values in 'mu' must be floats between [0, 1]!"
                self.__fuzzy_set[tuple(variables)] = mu

            if 'mu' in keys:
                keys.remove('mu')
            self.__domain = list(keys)
        else:
            assert isinstance(domain, tuple) and len(domain) > 0, "'domain' must be a non-empty tuple of strings representing the domains name!"
            assert isinstance(dict_relation, dict), "'dict_relation' must be a dictionary!"
            length = len(domain)
            sorted_domain = list(domain)
            sorted_domain.sort()
            for i in range(1, len(sorted_domain)):
                assert domain[i] != domain[i - 1], "'domain' must not contains duplicates!"

            
            self.__fuzzy_set = {}
            for element, mu in dict_relation.items():
                assert (isinstance(element, list) or isinstance(element, tuple)) and len(element) == length, "All keys in 'dict_relation' must be lists or tuples with the same length as the domain!"
                assert isinstance(mu, float) and 0.0 <= mu and mu <= 1.0, "All memberships values must be floats between [0, 1]!"
                self.__fuzzy_set[tuple(element)] = mu

            self.__domain = list(domain)
    
    def __getitem__(self, element) -> float: # membership: []
        if element in self.__fuzzy_set.keys():
            return self.__fuzzy_set[element]
        return self.__non_membership_value
    
    def __setitem__(self, element, membership: float) -> None: # add/update_element: []
        assert isinstance(membership, float), "'membership' must be a float!"
        assert 0 <= membership and membership <= 1, "'membership' must be between 0 and 1 inclusive!"
        assert isinstance(element, tuple), "'element' must be a tuple! "
        assert len(self.__domain) == len(element), "'element' must be a tuple of the same length of the domain!"

        self.__fuzzy_set[element] = membership

    def __or__(self, set2: FuzzySet) -> FuzzySet: # union: |, |=
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        assert self.get_domain() == set2.get_domain(), "'set2' must have the same domain!"

        new_set = set2.to_dictionary()
        for element, membership1 in self.__fuzzy_set.items():
            new_set[element] = FuzzyLogic.or_fun(membership1, set2[element])
        fs = DiscreteFuzzySet(self.get_domain(), new_set)
        return fs
    
    def __and__(self, set2: FuzzySet) -> FuzzySet: # intersection: &, &=
        assert isinstance(set2, FuzzySet), "'set2' must be of type 'FuzzySet'!"
        assert self.get_domain() == set2.get_domain(), "'set2' must have the same domain!"
        
        new_set = {}
        for element, membership1 in self.__fuzzy_set.items():
            membership2 = set2[element]
            new_membership = FuzzyLogic.and_fun(membership1, membership2)
            # if new_membership > .0: # scelta progettuale: gli elementi con mu == 0 li mantieni oppure no? -> scelgo no
            #     new_set[element] = new_membership
            new_set[element] = new_membership
        fs = DiscreteFuzzySet(self.get_domain(), new_set)
        return fs
    
    def __invert__(self) -> FuzzySet: # complement: ~
        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            new_set[element] = FuzzyLogic.not_fun(membership)

        fs = DiscreteFuzzySet(self.get_domain(), new_set)
        fs.__non_membership_value = FuzzyLogic.not_fun(fs.__non_membership_value)
        return fs
    
    def __mul__(self, set2: FuzzySet) -> FuzzySet: # cartesian_product: *, *=
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        set1_domain = self.get_domain()
        set2_domain = set2.get_domain()
        for var in set2_domain:
            assert var not in set1_domain, "'" + var + "' is in both domains: " + str(set1_domain) + "\n'set1' and 'set2' must have different domains!"

        new_set = {}
        for element1, membership1 in self.__fuzzy_set.items():
            for element2, membership2 in set2.to_dictionary().items():
                new_set[element1 + element2] = FuzzyLogic.and_fun(membership1, membership2)
        fs = DiscreteFuzzySet(set1_domain + set2_domain, new_set)
        return fs

    def __matmul__(self, set2: FuzzySet) -> FuzzySet: # natural_join: @, @=
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"

        domain1 = self.get_domain()
        domain2 = list(set2.get_domain())
        indexes1 = []
        indexes2 = []
        for index, var in enumerate(domain1):
            if var in domain2:
                indexes1.append(index)
                indexes2.append(domain2.index(var))
                domain2.remove(var)
        assert len(indexes1) > 0, "'set1' and 'set2' must have at least one set in common in their domain!"

        new_set = {}
        for element1, membership1 in self.__fuzzy_set.items():
            for element2, membership2 in set2.to_dictionary().items():
                to_insert = True
                for index in range(0, len(indexes1)):
                    if element1[indexes1[index]] != element2[indexes2[index]]:
                        to_insert = False
                        break
                if to_insert:
                    new_elem = list(element1)
                    for index, var in enumerate(element2):
                        if index not in indexes2:
                            new_elem.append(var)
                    new_set[tuple(new_elem)] = FuzzyLogic.and_fun(membership1, membership2)
        return DiscreteFuzzySet(domain1 + tuple(domain2), new_set)

    def __truediv__(self, set2) -> float: # proportion: /
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        new_set = self & set2
        return new_set.cardinality() / set2.cardinality()

    def projection(self, subdomain: tuple, operator: FuzzyBinaryOperator) -> FuzzySet:
        assert isinstance(subdomain, tuple), "'subdomain' must be a sub-tuple of sets from the domain of the fuzzy set!"
        assert isinstance(operator, FuzzyBinaryOperator), "'operator' must be of type 'FuzzyBinaryOperator'!"

        domain = self.get_domain()
        indexes = []
        for var in subdomain:
            assert var in domain, "'" + str(var) + "' not in the domain of the fuzzy set!"
            indexes.append(domain.index(var))

        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            new_tuple = []
            for index in indexes:
                new_tuple.append(element[index])

            new_tuple = tuple(new_tuple)
            if new_tuple in new_set.keys():
                new_set[new_tuple] = operator(new_set[new_tuple], membership)
            else:
                new_set[new_tuple] = membership

        fs = DiscreteFuzzySet(subdomain, new_set)
        return fs
    
    def select(self, assignment: dict) -> FuzzySet:
        assert isinstance(assignment, dict), "'assignment' must be a dictionary!"

        domain = self.get_domain()
        indexes = []
        fs_indexes = []
        for var in assignment.keys():
            assert var in domain, "'" + str(var) + "' not in the domain of the fuzzy set!"
            index = domain.index(var)
            if isinstance(assignment[domain[index]], DiscreteFuzzySet):
                fs_indexes.append(index)
            else:
                indexes.append(index)

        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            for index in indexes:
                if element[index] != assignment[domain[index]]:
                    membership = 0
                    break
            for index in fs_indexes:
                membership = FuzzyLogic.and_fun(assignment[domain[index]][(element[index],)], membership)
            if membership > 0:
                new_set[element] = membership

        fs = DiscreteFuzzySet(domain, new_set)
        return fs

    def cardinality(self) -> float:
        memberships_sum = 0.0
        for value in self.__fuzzy_set.values():
            memberships_sum += value
        return memberships_sum
    
    def mean_cardinality(self) -> float:
        memberships_sum = 0.0
        n = 0
        for value in self.__fuzzy_set.values():
            memberships_sum += value
            n += 1
        return memberships_sum / n

    def compatibility(self, reference_set: FuzzySet) -> FuzzySet:
        assert isinstance(reference_set, DiscreteFuzzySet), "'reference_set' must be of type 'DiscreteFuzzySet'!"
        assert self.get_domain() == reference_set.get_domain(), "'reference_set' must have the same domain!"

        new_set = {}
        for element, membership in reference_set.to_dictionary().items():
            key = (reference_set[element], )
            if key in new_set.keys():
                new_set[key] = max(self[element], new_set[key])
            else:
                new_set[key] = self[element]
            
        return DiscreteFuzzySet(self.get_domain(), new_set)

    def consistency(self, reference_set: FuzzySet) -> float:
        assert isinstance(reference_set, DiscreteFuzzySet), "'reference_set' must be of type 'DiscreteFuzzySet'!"
        assert self.get_domain() == reference_set.get_domain(), "'reference_set' must have the same domain!"

        consistency = -1
        for element, mu1 in reference_set.to_dictionary().items():
            consistency = max(FuzzyLogic.and_fun(mu1, self[element]), consistency)

        return consistency

    def get_domain(self) -> tuple:
        return tuple(self.__domain)

    def rename_domain(self, ren_dict: dict) -> None:
        assert isinstance(ren_dict, dict), "'dict_relation' must be a dictionary!"
        for key, value in ren_dict.items():
            assert isinstance(key, str) and isinstance(key, str), "All keys and values in 'ren_dict' must be strings!"
            assert key in self.__domain, key + " not in this FuzzySet domain!"
            assert value not in self.__domain, value + " already in this FuzzySet domain!"
            self.__domain[self.__domain.index(key)] = value

    def to_dictionary(self) -> dict: # differentia
        return self.__fuzzy_set.copy()
    
    def get_tabular_str(self) -> str: # differentia
        s = ''
        for key in self.__domain:
            s += "{:<15}".format(key)
        s += 'mu\n\n'
        for key, value in self.__fuzzy_set.items():
            for var in key:
                s += "{:<15}".format(var)
            s += "{:<15}\n".format(value)
        return s

    def __repr__(self) -> str: # differentia
        s = ''
        for value, membership in self.__fuzzy_set.items():
            s += str(membership) + '/' + str(value) + ' + '
        if len(self.__fuzzy_set.items()) > 0:
            return s[:-3]
        return '∅'
    
    def __str__(self) -> str: # differentia
        return self.__repr__()

# Example usage:
if __name__ == "__main__":
    start_time = time.time()

    A = DiscreteFuzzySet(('D1', 'D2'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
    B = DiscreteFuzzySet(('D1', 'D2'), {(2, 'val4'): 0.1, ('val3', 4.4): 0.5, ('val1', 3.4): 0.7})
    C = DiscreteFuzzySet(('D1', ), {(2,): 0.1, ('val3',): 0.5})
    D = DiscreteFuzzySet(('n', ), {(0, ): .0, (1, ): .0, (2, ): 0.2, (3, ): 0.4, (4, ): 0.6, (5, ): 0.8})
    not_D = ~D
    E = DiscreteFuzzySet(('D1', 'D3'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
    F = DiscreteFuzzySet(('D6', 'D3'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})

    print("non_membership_value of not_D:", not_D['ciaofra'])
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
    complement_set = ~A
    cartesian_product_set = A * F
    or_projection_set = A.projection(('D2',), FuzzyOr.MAX)
    and_projection_set = A.projection(('D2',), FuzzyAnd.MIN)
    select = A.select({'D1': C})
    print("A ∪ B =", union_set, "\ndomain:", union_set.get_domain(), end="")
    print("    cardinality:", union_set.cardinality())
    print("A ∩ B =", intersection_set, "\ndomain:", intersection_set.get_domain(), end="")
    print("    cardinality:", intersection_set.cardinality())
    print("~A =", complement_set, "\ndomain:", complement_set.get_domain(), end="")
    print("    cardinality:", complement_set.cardinality())
    print("A × F =", cartesian_product_set, "\ndomain:", cartesian_product_set.get_domain(), end="")
    print("    cardinality:", cartesian_product_set.cardinality())
    print("or_projection(A, ('D2'))", or_projection_set, "\ndomain:", or_projection_set.get_domain(), end="")
    print("    cardinality:", or_projection_set.cardinality())
    print("and_projection(A, ('D2'))", and_projection_set, "\ndomain:", and_projection_set.get_domain(), end="")
    print("    cardinality:", and_projection_set.cardinality())
    print("select(A, {'D1': C})", select)
    print("proportion{A/G} = ", A / B)
    print(not_D.compatibility(D))
    print("Cons{NOT(SMALL_INTEGER), SMALL_INTEGER} = ", not_D.consistency(D))
    print("A ⋈ E =", (A @ E))

    A.rename_domain({'D1': 'X1', 'D2': 'X2'})
    print(A.get_domain())
    print(A)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nElapsed time: {elapsed_time} seconds")
