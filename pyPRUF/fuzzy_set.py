# from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Tuple

from pandas import DataFrame
from pyPRUF.fuzzy_logic import FuzzyBinaryOperator, FuzzyLogic, FuzzyUnaryOperator
from pyPRUF.membership_functions import MembershipFunction

class FuzzySet(ABC):
    
    @abstractmethod
    def __getitem__(self, element) -> float: # membership: []
        pass

    @abstractmethod
    def __setitem__(self, element, membership: float) -> None: # add/update_element: []
        pass

    @abstractmethod
    def __delitem__(self, element) -> None: # del
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
    def particularization(self, assignment: dict): # particularization
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

    @abstractmethod
    def select(self, condition: Callable):
        pass

    @abstractmethod
    def apply(self, operator: FuzzyUnaryOperator):
        pass

    @abstractmethod  
    def extension_principle(self, function: Callable, out_domain: tuple):
        pass

    @abstractmethod
    def cilindrical_extension(self, set2):
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

    def __delitem__(self, element) -> None:
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

    def particularization(self, assignment: dict): # particularization
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
        assert isinstance(ren_dict, dict), "'ren_dict' must be a dictionary!"
        for key, value in ren_dict.items():
            assert isinstance(key, str) and isinstance(key, str), "All keys and values in 'ren_dict' must be strings!"
            assert key in self.__domain, key + " not in this FuzzySet domain!"
            assert value not in self.__domain, value + " already in this FuzzySet domain!"
            self.__domain[self.__domain.index(key)] = value
    
    def select(self, condition: Callable) -> FuzzySet:
        pass

    def apply(self, operator: FuzzyUnaryOperator) -> FuzzySet:
        pass

    def extension_principle(self, function: Callable, out_domain: tuple):
        pass

    def cilindrical_extension(self, set2: FuzzySet) -> Tuple[FuzzySet, FuzzySet]:
        pass

class DiscreteFuzzySet(FuzzySet):

    def __init__(self, domain: tuple = None, data = None):
        if isinstance(data, DataFrame):
            dict_relation = {}
            for key, value in data.to_dict().items():
                assert isinstance(key, str), "All keys in 'dict_relation' must be strings representing the variables name!"
                dict_relation[key] = tuple(value.values())
            keys = list(dict_relation.keys())
            assert len(keys) > 0, "There must be at least one column!"
            length = len(dict_relation[keys[0]])
            assert length > 0, "The fuzzy set must contain at least a tuple!"
            
            self.__fuzzy_set = {}
            for i in range(0, length):
                variables = []
                mu = 1.0
                for key in keys:
                    if key != 'mu':
                        variables.append(dict_relation[key][i])
                    else:
                        mu = dict_relation[key][i]
                        assert isinstance(mu, float) and 0.0 < mu and mu <= 1.0, "All values in 'mu' must be floats between [0, 1]!"
                self.__fuzzy_set[tuple(variables)] = mu

            if 'mu' in keys:
                keys.remove('mu')
            self.__domain = keys
        else:
            assert isinstance(domain, tuple) and len(domain) > 0, "'domain' must be a non-empty tuple of strings representing the domains name!"
            length = len(domain)
            sorted_domain = list(domain)
            sorted_domain.sort()
            for i in range(1, len(sorted_domain)):
                assert domain[i] != domain[i - 1], "'domain' must not contains duplicates!"

            self.__fuzzy_set = {}
            if data is not None:
                assert isinstance(data, dict), "'data' must be 'None', a dictionary or a Dataframe!"
                for element, mu in data.items():
                    assert isinstance(element, tuple) and len(element) == length, "All keys in 'data' must be tuples with the same length as the domain!"
                    assert isinstance(mu, float) and 0.0 < mu and mu <= 1.0, "All memberships values must be floats between [0, 1]!"
                    self.__fuzzy_set[element] = mu

            self.__domain = list(domain)
    
    def __getitem__(self, element) -> float: # membership: []
        if element in self.__fuzzy_set.keys():
            return self.__fuzzy_set[element]
        return .0
    
    def __setitem__(self, element, membership: float) -> None: # add/update_element: []
        assert isinstance(membership, float), "'membership' must be a float!"
        assert .0 < membership and membership <= 1.0, "'membership' must be in [0, 1] interval!"
        assert isinstance(element, tuple), "'element' must be a tuple! "
        assert len(self.__domain) == len(element), "'element' must be a tuple of the same length of the domain!"

        self.__fuzzy_set[element] = membership

    def __delitem__(self, element) -> None:
        if element in self.__fuzzy_set:
            del self.__fuzzy_set[element]

    def __eq__(self, set2: FuzzySet) -> bool:
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        return set2.__fuzzy_set == self.__fuzzy_set and set2.get_domain() == self.get_domain()

    def __or__(self, set2: FuzzySet) -> FuzzySet: # union: |, |=
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        assert self.get_domain() == set2.get_domain(), "'set2' must have the same domain!"

        new_set = set2.to_dictionary()
        for element, membership1 in self.__fuzzy_set.items():
            new_membership = FuzzyLogic.or_fun(membership1, set2[element])
            if new_membership > .0:
                new_set[element] = new_membership
        fs = DiscreteFuzzySet(self.get_domain(), new_set)
        return fs
    
    def __and__(self, set2: FuzzySet) -> FuzzySet: # intersection: &, &=
        assert isinstance(set2, FuzzySet), "'set2' must be of type 'FuzzySet'!"
        assert self.get_domain() == set2.get_domain(), "'set2' must have the same domain!"
        
        new_set = {}
        for element, membership1 in self.__fuzzy_set.items():
            new_membership = FuzzyLogic.and_fun(membership1, set2[element])
            if new_membership > .0:
                new_set[element] = new_membership
        fs = DiscreteFuzzySet(self.get_domain(), new_set)
        return fs
    
    # ATTENZIONE: non corrisponde nè al complemento assoluto insiemistico nè a quello relativo
    def __invert__(self) -> FuzzySet: # fuzzy_not unary operator: ~ # NON TESTATO : Banale
        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            new_set[element] = FuzzyLogic.not_fun(membership)
        fs = DiscreteFuzzySet(self.get_domain(), new_set)
        return fs

    def __sub__(self, set2: FuzzySet) -> FuzzySet: # differenza: - # corrisponde al complemento relativo insiemistico di set2 rispetto a set1
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        assert self.get_domain() == set2.get_domain(), "'set2' must have the same domain!"
        
        new_set = {}
        for element, membership1 in self.__fuzzy_set.items():
            new_membership = FuzzyLogic.and_fun(membership1, FuzzyLogic.not_fun(set2[element]))
            if new_membership > .0:
                new_set[element] = new_membership
        fs = DiscreteFuzzySet(self.get_domain(), new_set)
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
                new_membership = FuzzyLogic.and_fun(membership1, membership2)
                if new_membership > .0:
                    new_set[element1 + element2] = new_membership
        fs = DiscreteFuzzySet(set1_domain + set2_domain, new_set)
        return fs

    def __matmul__(self, set2: FuzzySet) -> FuzzySet: # natural_join: @, @=
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"

        domain1 = self.get_domain()
        domain2 = set2.get_domain()
        domain2_rem = list(domain2)
        indexes_to_check_1 = []
        indexes_to_check_2 = []
        indexes_to_insert_2 = list(range(0, len(domain2)))
        for index, var in enumerate(domain1):
            if var in domain2:
                indexes_to_check_1.append(index)
                indexes_to_check_2.append(domain2.index(var))
                indexes_to_insert_2.remove(domain2.index(var))
                domain2_rem.remove(var)
        assert len(indexes_to_check_1) > 0, "'set1' and 'set2' must have at least one set in common in their domain!"

        new_set = {}
        for element1, membership1 in self.__fuzzy_set.items():
            for element2, membership2 in set2.to_dictionary().items():
                to_insert = True
                for index in range(0, len(indexes_to_check_1)):
                    if element1[indexes_to_check_1[index]] != element2[indexes_to_check_2[index]]:
                        to_insert = False
                        break
                if to_insert:
                    new_elem = list(element1)
                    for index in indexes_to_insert_2:
                        new_elem.append(element2[index])
                    new_membership = FuzzyLogic.and_fun(membership1, membership2)
                    if new_membership > .0:
                        new_set[tuple(new_elem)] = new_membership
        return DiscreteFuzzySet(domain1 + tuple(domain2_rem), new_set)

    # NON TESTATO : Banale
    def __truediv__(self, set2) -> float: # proportion: /
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        assert set2.cardinality() > 0, "'set2' must have cardinality greater than 0!" 
        new_set = self & set2
        return new_set.cardinality() / set2.cardinality()

    def projection(self, subdomain: tuple, operator: FuzzyBinaryOperator) -> FuzzySet:
        assert isinstance(subdomain, tuple) and len(subdomain) > 0, "'subdomain' must be a non empty sub-tuple of sets from the domain of the fuzzy set!"
        assert isinstance(operator, FuzzyBinaryOperator), "'operator' must be of type 'FuzzyBinaryOperator'!"

        domain = self.get_domain()
        indexes = []
        for var in subdomain:
            assert var in domain, "'" + str(var) + "' not in the domain of the fuzzy set!"
            indexes.append(domain.index(var))

        new_set = {}
        to_remove = set()
        for element, membership in self.__fuzzy_set.items():
            new_tuple = []
            for index in indexes:
                new_tuple.append(element[index])

            new_tuple = tuple(new_tuple)
            if new_tuple in new_set.keys():
                new_set[new_tuple] = operator(new_set[new_tuple], membership)
            else:
                new_set[new_tuple] = membership

            if new_set[new_tuple] == .0:
                to_remove.add(new_tuple)

        for t in to_remove:
            del new_set[t]

        fs = DiscreteFuzzySet(subdomain, new_set)
        return fs
    
    def particularization(self, assignment: dict) -> FuzzySet: # ATTENZIONE: VERIFICA SOLO L'UGUAGLIANZA E PERTANTO NON è UNA SELEZIONE
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
                    membership = .0
                    break
            for index in fs_indexes:
                membership = FuzzyLogic.and_fun(assignment[domain[index]][(element[index],)], membership)
            if membership > .0:
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
        if n:
            return memberships_sum / n
        else:
            return .0

    def compatibility(self, set2: FuzzySet) -> FuzzySet: # returns Comp{self / set2}
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        assert self.get_domain() == set2.get_domain(), "'set2' must have the same domain!"

        new_set = {}
        for element, membership in set2.to_dictionary().items():
            key = (membership, )
            if key in new_set.keys():
                new_set[key] = max(self[element], new_set[key])
            else:
                new_set[key] = self[element]
            
        return DiscreteFuzzySet(self.get_domain(), new_set)

    def consistency(self, reference_set: FuzzySet) -> float:
        assert isinstance(reference_set, DiscreteFuzzySet), "'reference_set' must be of type 'DiscreteFuzzySet'!"
        assert self.get_domain() == reference_set.get_domain(), "'reference_set' must have the same domain!"

        consistency = .0
        for element, mu1 in reference_set.to_dictionary().items():
            consistency = max(FuzzyLogic.and_fun(mu1, self[element]), consistency)

        return consistency

    def get_domain(self) -> tuple: # NON TESTATO : Banale
        return tuple(self.__domain)

    def rename_domain(self, ren_dict: dict) -> None: # NON TESTATO : Banale
        assert isinstance(ren_dict, dict), "'ren_dict' must be a dictionary!"
        for key, value in ren_dict.items():
            assert isinstance(key, str) and isinstance(key, str), "All keys and values in 'ren_dict' must be strings!"
            assert key in self.__domain, "'" + key + "' not in this FuzzySet domain!"
            assert value not in self.__domain, "'" + value + "' already in this FuzzySet domain!"
            self.__domain[self.__domain.index(key)] = value

    def select(self, condition: Callable) -> FuzzySet: # NON TESTATO : Banale
        assert isinstance(condition, Callable), "'function' must be a callable function!"
        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            if condition(tuple(list(element) + [membership])):
                new_set[element] = membership
        return DiscreteFuzzySet(self.get_domain(), new_set)
    
    def apply(self, operator: FuzzyUnaryOperator) -> FuzzySet:
        assert isinstance(operator, FuzzyUnaryOperator), "'operator' must be of type 'FuzzyUnaryOperator'!"
        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            new_membership = operator(membership)
            if new_membership > .0:
                new_set[element] = new_membership
        return DiscreteFuzzySet(self.get_domain(), new_set)

    def extension_principle(self, function: Callable, out_domain: tuple) -> FuzzySet: # NON TESTATO
        assert isinstance(function, Callable), "'function' must be a callable function!"
        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            y = function(element)
            if y in new_set:
                new_set[y] = FuzzyLogic.or_fun(new_set[y], membership)
            else:
                new_set[y] = membership
        return DiscreteFuzzySet(out_domain, new_set)
    
    def cilindrical_extension(self, set2: FuzzySet) -> Tuple[FuzzySet, FuzzySet]:
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'"
        domain1 = self.get_domain()
        domain2 = set2.get_domain()
        to_insert_1 = list(range(len(domain1)))
        to_insert_2 = list(range(len(domain2)))
        common1 = []
        common2 = []
        for index, var in enumerate(domain1):
            if var in domain2:
                common1.append(index)
                to_insert_1.remove(index)
                index2 = domain2.index(var)
                to_insert_2.remove(index2)
                common2.append(index2)
        
        new_domain = []
        for index in common1:
            new_domain.append(domain1[index])
        for index in to_insert_1:
            new_domain.append(domain1[index])
        for index in to_insert_2:
            new_domain.append(domain2[index])
        new_domain = tuple(new_domain)

        set1_extension = {}
        set2_extension = {}
        for element1, membership1 in self.__fuzzy_set.items():
            for element2, membership2 in set2.to_dictionary().items():

                new_elem = []
                for index in common1:
                    new_elem.append(element1[index])
                for index in to_insert_1:
                    new_elem.append(element1[index])
                for index in to_insert_2:
                    new_elem.append(element2[index])
                set1_extension[tuple(new_elem)] = membership1

                new_elem = []
                for index in common2:
                    new_elem.append(element2[index])
                for index in to_insert_1:
                    new_elem.append(element1[index])
                for index in to_insert_2:
                    new_elem.append(element2[index])
                set2_extension[tuple(new_elem)] = membership2

        return DiscreteFuzzySet(new_domain, set1_extension), DiscreteFuzzySet(new_domain, set2_extension)

    def collapse(self, operator: FuzzyBinaryOperator) -> float: # differentia # NON TESTATO : Banale
        assert isinstance(operator, FuzzyBinaryOperator), "'operator' must be of type 'FuzzyBinaryOperator'!"
        assert len(self.__fuzzy_set.keys()) > 1, "The fuzzy set must have at least two elements!"
        memberships = list(self.__fuzzy_set.values())
        result = memberships[0]
        for membership in memberships[1:]:
            result = operator(result, membership)
        return result
    
    def reorder(self, new_domain: tuple) -> FuzzySet:
        assert isinstance(new_domain, tuple), "'tuple' must be a tuple representing a permutation of the domain!"
        assert len(new_domain) == len(self.__domain), "'tuple' must be of the same length as the original domain!"
        perm = []
        for var in new_domain:
            assert var in self.__domain, "'" + str(var) + "' not in the domain!"
            index = self.__domain.index(var)
            perm.append(index)
        
        new_dict = {}
        for key, value in self.__fuzzy_set.items():
            new_elem = []
            for i in perm:
                new_elem.append(key[i])
            new_dict[tuple(new_elem)] = value

        return DiscreteFuzzySet(new_domain, new_dict)

    # FINE DEI METODI DA TESTARE

    def to_dictionary(self) -> dict: # differentia
        return self.__fuzzy_set.copy()
    
    def elements(self): # differentia
        return self.__fuzzy_set.keys()

    def memberships(self): # differentia
        return self.__fuzzy_set.values()
    
    def items(self): # differentia
        return self.__fuzzy_set.items()
    
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
            if membership > .0:
                s += str(membership) + '/' + str(value) + ' + '
        if len(self.__fuzzy_set.items()) > 0:
            return s[:-3]
        return '∅'
    
    def __str__(self) -> str: # differentia
        return self.__repr__()