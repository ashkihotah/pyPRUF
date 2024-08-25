# from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Tuple

from pandas import DataFrame
from pyPRUF.fuzzy_logic import FuzzyBinaryOperator, FuzzyLogic, FuzzyUnaryOperator
from pyPRUF.membership_functions import MembershipFunction, mf_of_tuple

class FuzzySet(ABC):

    """Abstract Base Class for representing a fuzzy set.

    A fuzzy set is a mathematical representation of a set where each
    element has a degree of membership ranging between 0 and 1.
    This class provides a framework for creating and managing fuzzy sets.

    Subclasses of `FuzzySet` must implement the required methods defined by the abstract base class.
    """
    
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
    def image(self, function: Callable, out_domain: tuple):
        pass

    @abstractmethod
    def cylindrical_extension(self, set2):
        pass

class ContinuousFuzzySet(FuzzySet):
    """A class representing a continuous fuzzy set,
    inheriting from `FuzzySet`.

    **WARNING**: This class is not fully implemented,
    please check the online documentation before using it.

    The `ContinuousFuzzySet` class is designed to handle
    fuzzy sets where their domain is continuous
    (such as Fuzzy Numbers), rather than discrete,
    allowing for smooth transitions between membership values.

    It is defined by a `MembershipFunction` and a domain that
    together fully characterize the continous fuzzy set.
    """

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
        return mf_of_tuple(element, self.mf)

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

    def image(self, function: Callable, out_domain: tuple):
        pass

    def cylindrical_extension(self, set2: FuzzySet) -> Tuple[FuzzySet, FuzzySet]:
        pass

class DiscreteFuzzySet(FuzzySet):
    """A class that defines a generic discrete fuzzy set
    and all the operations that can be performed on it
    by extending the abstract class FuzzySet.
    This implementation makes the following assumptions:\n
    - A DiscreteFuzzySet is equivalent to a fuzzy version of a
    relation in the Relational Algebra where the tuples
    in it belong to the relation with a membership degree
    .0 <= mu <= .1.\n
    - A DiscreteFuzzySet is defined by a tuple of strings
    where each string uniquely identifies a set name
    and the entire tuple represents the cartesian product
    of the sets in it that corresponds to the domain of
    the DiscreteFuzzySet.\n
    - As proposed by Zadeh, the domain is implicit in the sense
    that the domain of a fuzzy relation is defined only
    by the set of the tuples in it.\n
    - Only the elements in the support of the fuzzy set
    are kept as tuples of the fuzzy relations.
    """

    def __init__(self, domain: Tuple[str] = None, data = None):
        """Constructs the DiscreteFuzzySet object with the domain
        and data given in input. This constructor can initialize
        the fuzzy set from either a pandas DataFrame or a dictionary.

        Args:
            domain (tuple): A non-empty tuple of strings without
                duplicates representing the domain of the
                `DiscreteFuzzySet`
            data: Can be `None`, a `dict` or a pandas `DataFrame`
                representing the tuples in the fuzzy relation. If
                data is `None`, it will construct an empty fuzzy relation
                with the domain specified. If data is a `dict`,
                it must have the tuples of the fuzzy relation as keys
                and their membership as the value of the (key, value)
                pair. Each key in the dict must be a tuple of the same
                length as the domain. If data is a `DataFrame`, it must
                have\n
                - at least one column and at least one tuple
                - for each column a string representing the set name
                - a column named 'mu' containing the membership value of
                the corresponding tuple. If this column is missing, all
                tuples are assumed to belong to the fuzzy relation with
                membership degree 1. All memberships value in data
                must be floats in the interval (0, 1].
        If data is a DataFrame, it is not required to also specify the domain
        parameter. If it is done anyway, it will be ignored and the domain will
        be inferred from the DataFrame columns names. If data is a tuple
        of strings or None, it is required to specify also the domain.

        Raises:
            AssertionError: If one of the preceding assumptions is
                breached.

        Examples:
            >>> A = DiscreteFuzzySet(('D1', 'D2'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
            >>> print(A.to_dictionary())
            {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9}
            >>> print(A.get_domain())
            ('D1', 'D2')

            >>> df = pd.DataFrame({
            ...     'x': [1, 2],
            ...     'y': [3, 4],
            ...     'mu': [0.5, 0.7]
            ... })
            >>> fuzzy_set = FuzzySet(data=df)
            >>> print(fuzzy_set.get_domain())
            ('x', 'y')
            >>> print(fuzzy_set.to_dictionary())
            {(1, 3): 0.5, (2, 4): 0.7}
        """
        if isinstance(data, DataFrame):
            dict_relation = {}
            for key, value in data.to_dict().items():
                assert isinstance(key, str), "All keys in 'dict_relation' must be strings representing the variables name!"
                dict_relation[key] = tuple(value.values())
            keys = list(dict_relation.keys())
            assert len(keys) > 0, "There must be at least one column!"
            assert len(keys) != 1 or keys[0] != 'mu', "With the only column named 'mu' the resulting domain is empty!"
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
                        assert isinstance(mu, float) and 0.0 < mu and mu <= 1.0, "All values in 'mu' must be floats between (0, 1]!"
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
                    assert isinstance(mu, float) and 0.0 < mu and mu <= 1.0, "All memberships values must be floats between (0, 1]!"
                    self.__fuzzy_set[element] = mu

            self.__domain = list(domain)
    
    def __getitem__(self, element) -> float: # membership: []
        """Retrieves the membership value of an element from the `DiscreteFuzzySet`.

        If the `element` exists in the set, its membership value is returned;
        otherwise, a membership value of 0.0 is returned.

        Args:
            element (tuple): The element for which to retrieve the
                membership value.

        Returns:
            float: The membership value of the `element`.
                Returns 0.0 if the `element` is not in the set.

        Examples:
            >>> set_a = DiscreteFuzzySet(('a',), {('x',): 0.7, ('y',): 0.5})
            >>> membership_x = set_a[('x',)]
            >>> membership_z = set_a[('z',)]
            >>> membership_fake = set_a['fake']
            >>> print(membership_x)
            0.7
            >>> print(membership_z)
            0.0
            >>> print(membership_fake)
            0.0

            In this example, the membership value for `('x',)` is retrieved and found to be 0.7.
            For the element `('z',)`, which does not exist in the set, the method returns a membership
            value of 0.0.
        """
        if element in self.__fuzzy_set.keys():
            return self.__fuzzy_set[element]
        return .0
    
    def __setitem__(self, element: tuple, membership: float) -> None: # add/update_element: []
        """Adds or updates (the membership value of) an element in the `DiscreteFuzzySet`.

        The `element` must be a tuple with the same length as the domain,
        and the `membership` must be a float value in the interval (0, 1].

        Args:
            element (tuple): The element to add or update in the
                `DiscreteFuzzySet`.
            membership (float): The membership value associated with the
                `element`.

        Raises:
            AssertionError: If `membership` is not a float in the
                interval (0, 1] or if `element` is not a tuple with
                the same length as the domain of the current fuzzy set.

        Examples:
            >>> set_a = DiscreteFuzzySet(('a',), {('x',): 0.7})
            >>> set_a[('y',)] = 0.5
            >>> set_a[('x',)] = 0.8
            >>> print(set_a.to_dictionary())
            {('x',): 0.8, ('y',): 0.5}

            In this example, the `element` `('y',)` is added to `set_a` with a membership value of 0.5,
            and the membership value of the existing element `('x',)` is updated to 0.8. The resulting
            set reflects these changes.
        """
        assert isinstance(membership, float), "'membership' must be a float!"
        assert .0 < membership and membership <= 1.0, "'membership' must be in (0, 1] interval!"
        assert isinstance(element, tuple), "'element' must be a tuple! "
        assert len(self.__domain) == len(element), "'element' must be a tuple of the same length of the domain!"

        self.__fuzzy_set[element] = membership

    def __delitem__(self, element) -> None:
        """Deletes an element from the `DiscreteFuzzySet`.

        If the `element` exists in the set, it is deleted;
        otherwise, the operation has no effect.

        Args:
            element (tuple): The element to remove from the
                `DiscreteFuzzySet`.

        Examples:
            >>> set_a = DiscreteFuzzySet(('a',), {('x',): 0.7, ('y',): 0.5})
            >>> del set_a[('x',)]
            >>> print(set_a.to_dictionary())
            {('y',): 0.5}

            In this example, the element `('x',)` is deleted from `set_a`. After deletion,
            the resulting set only contains the remaining element `('y',)`.
        """
        if element in self.__fuzzy_set:
            del self.__fuzzy_set[element]

    def __eq__(self, set2: FuzzySet) -> bool:
        """Determines whether two `DiscreteFuzzySet` instances are equal.

        Two `DiscreteFuzzySet` instances are considered equal if they have the same domain
        and identical membership values for all elements.

        Args:
            set2 (DiscreteFuzzySet): The `DiscreteFuzzySet` instance to
                compare with `self`.

        Raises:
            AssertionError: If `set2` is not an instance of
                `DiscreteFuzzySet`.

        Returns:
            bool: `True` if `self` and `set2` are identical fuzzy sets;
                `False` otherwise.

        Examples:
            >>> set_a = DiscreteFuzzySet(('a',), {('x',): 0.7, ('y',): 0.5})
            >>> set_b = DiscreteFuzzySet(('a',), {('x',): 0.7, ('y',): 0.5})
            >>> set_c = DiscreteFuzzySet(('a',), {('x',): 0.4, ('y',): 0.8})
            >>> set_d = DiscreteFuzzySet(('d',), {('x',): 0.7, ('y',): 0.5})
            >>> result1 = (set_a == set_b)
            >>> result2 = (set_a == set_c)
            >>> result3 = (set_a == set_d)
            >>> print(result1)
            True
            >>> print(result2)
            False
            >>> print(result3)
            False

            In this example, `set_a` is equal to `set_b` because they have the same domain and identical
            membership values for all elements. However, `set_a` is not equal to `set_c` due to differences
            in their membership values while `set_a` is not equal to `set_d` due to to differences in
            their domains.
        """
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        return set2.__fuzzy_set == self.__fuzzy_set and set2.get_domain() == self.get_domain()

    def __or__(self, set2: FuzzySet) -> FuzzySet: # union: |, |=
        """Computes the fuzzy union of two `DiscreteFuzzySet` instances.

        The fuzzy union is calculated by applying the `FuzzyLogic.or_fun()`
        function to the membership values of corresponding elements in both sets.

        Args:
            set2 (DiscreteFuzzySet): The `DiscreteFuzzySet` instance to
                unite with `self`.

        Raises:
            AssertionError: If `set2` is not an instance of
                `DiscreteFuzzySet` or if `self` and `set2`
                do not have the same domain.

        Returns:
            DiscreteFuzzySet: A new `DiscreteFuzzySet` representing the
                union of `self` and `set2`.

        Examples:
            >>> set_a = DiscreteFuzzySet(('a',), {('x',): 0.7, ('y',): 0.5})
            >>> set_b = DiscreteFuzzySet(('a',), {('x',): 0.4, ('y',): 0.8})
            >>> result = set_a | set_b
            >>> print(result.to_dictionary())
            {('x',): 0.7, ('y',): 0.8}

            In this example, the union of `set_a` and `set_b` is computed by applying the `FuzzyOr.MAX`,
            set as the default `OR` truth function of the class `FuzzyLogic`,
            function to the membership values of corresponding elements. The resulting set
            contains elements with membership values that represent the maximum of the
            corresponding values in `set_a` and `set_b`.
        """
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
        """Computes the intersection of two `FuzzySet` instances.

        The intersection is calculated by applying `FuzzyLogic.and_fun()`
        function to the membership values of corresponding elements in both sets.

        >> **WARNING**: only tuples with a membership value greater than 0 are kept.

        Args:
            set2 (FuzzySet): The `FuzzySet` instance to intersect with
                `self`.

        Raises:
            AssertionError: If `set2` is not an instance of `FuzzySet`
                or if `self` and `set2` do not have the same domain.

        Returns:
            DiscreteFuzzySet: A new `DiscreteFuzzySet` representing the
                intersection of `self` and `set2`.

        Examples:
            >>> set_a = DiscreteFuzzySet(('a',), {('x',): 0.7, ('y',): 0.5, ('z', ): .3})
            >>> set_b = DiscreteFuzzySet(('a',), {('x',): 0.4, ('y',): 0.8})
            >>> result = set_a & set_b
            >>> print(result.to_dictionary())
            {('x',): 0.4, ('y',): 0.5}

            In this example, the intersection of `set_a` and `set_b` is computed by applying
            the `FuzzyAnd.MIN` function, set as the default `AND` truth function of the class `FuzzyLogic`,
            to the membership values of corresponding elements. The resulting set contains elements
            with membership values that represent the minimum of the
            corresponding values in `set_a` and `set_b`.
        """
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
        """Computes the current fuzzy set applied to the NOT FuzzyUnaryOperator.

        The result is calculated by applying `FuzzyLogic.not_fun()`
        function to the membership values of all elements in the set.

        >> **WARNING**: This operation corresponds neither to the
        set absolute complement nor to the relative complement.
        The set absolute/relative complement could be derived
        by calculating it as the difference between a fuzzy set
        (eventually the universe of discourse) and another fuzzy set.
        This correspond simply to the NOT FuzzyUnaryOperator
        applied to the tuples of this fuzzy set. Semantically
        corresponds to an application of a linguistic modifier.

        >> **WARNING**: only tuples with a membership value greater than 0 are kept.

        Returns:
            DiscreteFuzzySet: A new `DiscreteFuzzySet` representing the
                fuzzy complement of `self`.

        Examples:
            >>> set_a = DiscreteFuzzySet(('a',), {('x',): 0.7, ('y',): 0.4}, ('z', ): 1.0)
            >>> result = ~set_a
            >>> print(result.to_dictionary())
            {('x',): 0.3, ('y',): 0.6}

            In this example, the result is computed by applying the
            `FuzzyNot.STANDARD` function, set as the default `NOT` truth
            function of the class `FuzzyLogic`, to each membership value in the set.
            The resulting set contains only the elements with a positive membership value.
        """
        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            new_set[element] = FuzzyLogic.not_fun(membership)
        fs = DiscreteFuzzySet(self.get_domain(), new_set)
        return fs

    def __sub__(self, set2: FuzzySet) -> FuzzySet: # differenza: - # corrisponde al complemento relativo insiemistico di set2 rispetto a set1
        """Computes the difference (relative complement) between two `DiscreteFuzzySet` instances.

        The difference is calculated by applying `FuzzyLogic.and_fun()` operation between the
        membership values of `self` and the negated membership values of `set2` calculated
        using `FuzzyLogic.not_fun()`.

        >> **WARNING**: only tuples with a membership value greater than 0 are kept.

        Args:
            set2 (DiscreteFuzzySet): The `DiscreteFuzzySet` instance to
                subtract from `self`.

        Raises:
            AssertionError: If `set2` is not an instance of
                `DiscreteFuzzySet` or if `self` and `set2`
                do not have the same domain.

        Returns:
            DiscreteFuzzySet: A new `DiscreteFuzzySet` representing the
                difference between `self` and `set2`.

        Examples:
            >>> set_a = DiscreteFuzzySet(('a',), {('x',): 0.7, ('y',): 0.5, ('z', ): 0.3})
            >>> set_b = DiscreteFuzzySet(('a',), {('x',): 0.4, ('y',): 0.5}, ('z', ): 1.0)
            >>> result = set_a - set_b
            >>> print(result.to_dictionary())
            {('x',): 0.6, ('y',): 0.5}

            In this example, the result is computed using the `FuzzyAnd.MIN` and
            `FuzzyNot.STANDARD` truth functions, set as the default `AND` and `NOT` truth
            functions of the class `FuzzyLogic`.
            The resulting set contains only the elements with a positive membership value.
        """
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
        """Computes the Cartesian product of two `DiscreteFuzzySet` instances.

        The Cartesian product creates new elements from the two sets as their concatenation
        and applies `FuzzyLogic.and_fun()` operation to their membership values.

        >> **WARNING**: only tuples with a membership value greater than 0 are kept.

        Args:
            set2 (DiscreteFuzzySet): The `DiscreteFuzzySet` instance to
                combine with.

        Raises:
            AssertionError: If `set2` is not an instance of
                `DiscreteFuzzySet` or if `self` and `set2`
                have overlapping domains.

        Returns:
            DiscreteFuzzySet: A new `DiscreteFuzzySet` representing the
                Cartesian product of `self` and `set2`.

        Examples:
            >>> set_a = DiscreteFuzzySet(('a',), {('x',): 0.7, ('y',): 0.4})
            >>> set_b = DiscreteFuzzySet(('b',), {('1',): 0.8, ('2',): 0.6})
            >>> result = set_a * set_b
            >>> print(result.to_dictionary())
            {('x', '1'): 0.7, ('x', '2'): 0.6, ('y', '1'): 0.4, ('y', '2'): 0.4}

            In this example, the Cartesian product of `set_a` and `set_b` is computed by
            pairing each element from `set_a` with each element from `set_b`. The resulting set
            contains tuples representing all possible combinations of elements from both sets,
            with membership values calculated using the `FuzzyAnd.MIN`,
            set as the default `AND` truth function in the class `FuzzyLogic`.
        """
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
        """Computes the natural join of two `DiscreteFuzzySet` instances.

        The natural join combines elements from the two sets based on common domains,
        and applies `FuzzyLogic.and_fun()` operation to their membership values.
        The domain of the resulting fuzzy set is composed by the domain
        of the current fuzzy set concatenated with the remaining not in common
        sets in the domain of 'set2'.

        >> **WARNING**: only tuples with a membership value greater than 0 are kept.

        Args:
            set2 (DiscreteFuzzySet): The `DiscreteFuzzySet` instance to
                join with.

        Raises:
            AssertionError: If `set2` is not an instance of
                `DiscreteFuzzySet` or If `self` and `set2`
                do not have at least one domain in common.

        Returns:
            DiscreteFuzzySet: A new `DiscreteFuzzySet` representing the
                natural join of `self` and `set2`.

        Examples:
            >>> set_a = DiscreteFuzzySet(('a', 'b'), {('x', 'y'): 0.8, ('x', 'z'): 0.5})
            >>> set_b = DiscreteFuzzySet(('b', 'c'), {('y', 'w'): 0.7, ('z', 'v'): 0.6})
            >>> result = set_a @ set_b
            >>> print(result.to_dictionary())
            {('x', 'y', 'w'): 0.7, ('x', 'z', 'v'): 0.5}

            In this example, the natural join of `set_a` and `set_b` is computed by combining elements
            based on the common domain 'b'. The resulting set contains tuples from the combined domains
            ('a', 'b', 'c') with membership values computed using the `FuzzyAnd.MIN`,
            set as the default `AND` truth function in the class `FuzzyLogic`.
        """
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
        """Computes the proportion of elements in the intersection of `self` and `set2`
        relative to the total number of elements in `set2`.

        Args:
            set2 (DiscreteFuzzySet): The `DiscreteFuzzySet` instance to
                divide by.

        Raises:
            AssertionError: If `set2` is not an instance of
                `DiscreteFuzzySet`, if the cardinality of `set2` is zero
                or if the assumprions of the fuzzy union are breached.

        Returns:
            float: The proportion of elements in the intersection of
                `self` and `set2` relative to `set2`.

        Examples:
            >>> set_a = DiscreteFuzzySet(('X', ), {('a', ): 0.7, ('b', ): 0.3, ('c', ): 0.5})
            >>> set_b = DiscreteFuzzySet(('X', ), {('b', ): 0.4, ('c', ): 0.5, ('d', ): 0.6})
            >>> proportion = set_a / set_b
            >>> print(proportion)
            0.5333333333333333

            In this example, the intersection of `set_a` and `set_b` contains the elements
            {('b', ), ('c', )} with a combined cardinality of 2, while `set_b` has a cardinality of 3.
            Therefore, the proportion returned is 2/3.
        """
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        assert set2.cardinality() > 0, "'set2' must have cardinality greater than 0!" 
        new_set = self & set2
        return new_set.cardinality() / set2.cardinality()

    def projection(self, subdomain: Tuple[str], operator: FuzzyBinaryOperator) -> FuzzySet:
        """Projects the fuzzy set onto a specified subdomain using a binary operator.

        This method creates a new fuzzy set by projecting the current set onto a given subdomain. The
        projection involves combining membership values according to the provided binary operator. Only the
        elements in the new subdomain are retained, and membership values are computed using the operator
        applied to the corresponding elements from the original fuzzy set.

        >> **WARNING**: only tuples with a membership value greater than 0 are kept.

        Args:
            subdomain (Tuple[str]): A tuple representing the subdomain
                to project onto. It must be a non-empty subset of the
                domain of the current fuzzy set.
            operator (FuzzyBinaryOperator): A binary operator used to
                combine membership values during the projection.

        Raises:
            AssertionError: If `subdomain` is not a non-empty tuple or
                if any variable in `subdomain` is not in the domain of
                the fuzzy set, or if `operator` is not of type
                `FuzzyBinaryOperator`.

        Returns:
            FuzzySet: A new `DiscreteFuzzySet` object representing the
                projection of the original fuzzy set onto the specified
                subdomain.

        Examples:
            >>> original_set = DiscreteFuzzySet(('x', 'y', 'z'), {('a', 'b', 'c'): 0.7, ('a', 'b', 'f'): 0.5, ('a', 'f', 'c'): 0.3})
            >>> subdomain = ('x', 'y')
            >>> projected_set = original_set.projection(subdomain, FuzzyAnd.MIN)
            >>> print(projected_set.to_dictionary())
            {('a', 'b'): 0.5, ('a', 'f'): .0.3}
        """
        assert isinstance(subdomain, tuple) and len(subdomain) > 0, "'subdomain' must be a non empty sub-tuple of sets from the domain of the fuzzy set!"
        assert isinstance(operator, FuzzyBinaryOperator), "'operator' must be of type 'FuzzyBinaryOperator'!"

        domain = self.get_domain()
        indexes = set()
        for var in subdomain:
            assert var in domain, "'" + str(var) + "' not in the domain of the fuzzy set!"
            indexes.add(domain.index(var))

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
    
    def particularization(self, assignment: dict) -> FuzzySet:
        """Performs particularization of the fuzzy set based on a given assignment.

        This method creates a new fuzzy set by specializing the current set according to the provided
        assignment. The assignment is a dictionary where each key is a set in the domain, and each
        value specifies a particular value or a fuzzy set. The resulting fuzzy set includes only the elements
        that match the specified assignments. If a variable in the assignment maps to a specific value,
        only elements with that value are retained. If it maps to another fuzzy set, the membership values
        are combined using fuzzy AND operations.

        >> **WARNING**: only tuples with a membership value greater than 0 are kept.

        Args:
            assignment (dict): A dictionary where each key is a variable
                from the domain of the fuzzy set, and each value is
                either a specific value or a `DiscreteFuzzySet` to match
                against.

        Raises:
            AssertionError: If `assignment` is not a dictionary, if any
                key is not in the fuzzy set's domain, or if the
                assignment values do not match the expected types.

        Returns:
            FuzzySet: A new `DiscreteFuzzySet` object that represents
                the particularized fuzzy set.

        Examples:
            >>> domain = ('x', 'y')
            >>> fuzzy_set = DiscreteFuzzySet(domain, {('a', 'b'): 0.5, ('c', 'd'): 0.7})
            >>> assignment = {'x': 'a', 'y': DiscreteFuzzySet(('y',), {('b',): 0.3})}
            >>> particularized_set = fuzzy_set.particularization(assignment)
            >>> print(particularized_set.to_dictionary())
            {('a', 'b'): 0.3}
        """
        assert isinstance(assignment, dict), "'assignment' must be a dictionary!"

        domain = self.get_domain()
        indexes = []
        fs_indexes = []
        for var in assignment.keys():
            assert var in domain, "'" + str(var) + "' not in the domain of the fuzzy set!"
            index = domain.index(var)
            if isinstance(assignment[domain[index]], FuzzySet):
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
        """Computes the cardinality of the fuzzy set.

        This method calculates the total sum of all membership values in the fuzzy set. The cardinality
        represents the aggregate degree of membership of all elements in the set.

        Returns:
            float: The sum of the membership values of all elements in
                the fuzzy set.

        Examples:
            >>> fuzzy_set = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.4, ('c', 'd'): 0.6})
            >>> total_cardinality = fuzzy_set.cardinality()
            >>> print(total_cardinality)
            1.0
        """
        memberships_sum = 0.0
        for value in self.__fuzzy_set.values():
            memberships_sum += value
        return memberships_sum
    
    def mean_cardinality(self) -> float:
        """Calculates the mean cardinality of the fuzzy set.

        This method computes the average membership value of all elements in the fuzzy set. The mean
        cardinality provides an indication of the average degree of membership of the elements in the set.

        Returns:
            float: The mean membership value of the fuzzy set. If the
                set is empty, the method returns 0.0.

        Examples:
            >>> fuzzy_set = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.4, ('c', 'd'): 0.6})
            >>> mean_cardinality = fuzzy_set.mean_cardinality()
            >>> print(mean_cardinality)
            0.5
        """
        memberships_sum = 0.0
        n = 0
        for value in self.__fuzzy_set.values():
            memberships_sum += value
            n += 1
        if n:
            return memberships_sum / n
        else:
            return .0

    def compatibility(self, set2: FuzzySet) -> FuzzySet:
        """Computes the compatibility of the current fuzzy set with another fuzzy set.

        This method calculates a new fuzzy set based on the membership values of `set2`,
        with each membership value in the new set representing the maximum compatibility
        with the corresponding membership value in the current set.
        Both fuzzy sets must have the same domain for the operation to be valid.

        >> **WARNING**: only tuples with a membership value greater than 0 are kept.

        Args:
            set2 (FuzzySet): Another fuzzy set to compare with.
                It must have the same domain as the current fuzzy set.

        Raises:
            AssertionError: If `set2` is not of type `DiscreteFuzzySet`
                or if the domains of the two fuzzy sets do not match.

        Returns:
            FuzzySet: A new `DiscreteFuzzySet` object where each element
                is associated with the maximum membership value between the
                two fuzzy sets.

        Examples:
            >>> fuzzy_set1 = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.3, ('d', 'e'): 0.6, ('c', 'd'): 0.8, ('h', 'i'): 0.4})
            >>> fuzzy_set2 = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.5, ('d', 'e'): 0.5, ('e', 'f'): 0.7, ('c', 'd'): 0.2})
            >>> compatible_set = fuzzy_set1.compatibility(fuzzy_set2)
            >>> print(compatible_set.to_dictionary())
            {(0.5, ): 0.6, (0.2, ): 0.8}
        """
        assert isinstance(set2, DiscreteFuzzySet), "'set2' must be of type 'DiscreteFuzzySet'!"
        assert self.get_domain() == set2.get_domain(), "'set2' must have the same domain!"

        new_set = {}
        for element, membership in set2.to_dictionary().items():
            key = (membership, )
            if key in new_set.keys():
                new_set[key] = max(self[element], new_set[key])
            elif self[element] > .0:
                new_set[key] = self[element]
        
        return DiscreteFuzzySet(('membership', ), new_set)

    def consistency(self, reference_set: FuzzySet) -> float:
        """Computes the consistency level between the fuzzy set and a reference fuzzy set.

        This method calculates the consistency of the current fuzzy set with a provided reference set.
        Consistency is defined as the maximum of the fuzzy AND operation applied to the membership
        values of corresponding elements in both sets. The two fuzzy sets must have the same domain
        for this operation to be valid.

        Args:
            reference_set (FuzzySet): A reference fuzzy set to compare
                with. It must have the same domain as the current fuzzy
                set.

        Raises:
            AssertionError: If `reference_set` is not of type
                `DiscreteFuzzySet` or if the domains of the two fuzzy
                sets do not match.

        Returns:
            float: The consistency value, representing the maximum
                consistency level between the two sets.

        Examples:
            >>> fuzzy_set = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.7, ('c', 'd'): 0.4})
            >>> reference_set = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.6, ('c', 'd'): 0.5})
            >>> consistency_value = fuzzy_set.consistency(reference_set)
            >>> print(consistency_value)
            0.6
        """
        assert isinstance(reference_set, DiscreteFuzzySet), "'reference_set' must be of type 'DiscreteFuzzySet'!"
        assert self.get_domain() == reference_set.get_domain(), "'reference_set' must have the same domain!"

        consistency = .0
        for element, mu1 in reference_set.to_dictionary().items():
            consistency = max(FuzzyLogic.and_fun(mu1, self[element]), consistency)

        return consistency

    def get_domain(self) -> Tuple[str]: # NON TESTATO : Banale
        """Retrieves the domain of the fuzzy set.

        This method returns the domain of the fuzzy set as a tuple of strings. The domain consists
        of the set names that define the fuzzy set.

        Returns:
            (Tuple[str]): A tuple representing the domain of the fuzzy set.

        Examples:
            >>> fuzzy_set = DiscreteFuzzySet(('x', 'y', 'z'), {('a', 'b', 'c'): 0.5})
            >>> domain = fuzzy_set.get_domain()
            >>> print(domain)
            ('x', 'y', 'z').
        """
        return tuple(self.__domain)

    def rename_domain(self, ren_dict: dict) -> None: # NON TESTATO : Banale
        """Renames elements in the domain of the fuzzy set based on a provided dictionary.

        This method updates the domain of the fuzzy set by renaming its elements according to the
        mappings provided in `ren_dict`. Each key in `ren_dict` corresponds to an existing element
        in the domain, and the associated value is the new name for that element. The method performs
        in-place modification of the domain.

        Args:
            ren_dict (dict): A dictionary where each key is an existing
                element in the domain and each value is the new name for
                that element.

        Raises:
            AssertionError: If `ren_dict` is not a dictionary, if any
                key or value in `ren_dict` is not a string, if any key
                is not found in the current domain, or if any value
                already exists in the current domain.

        Examples:
            >>> original_domain = ('x', 'y', 'z')
            >>> renaming_dict = {'x': 'a', 'y': 'b'}
            >>> fuzzy_set = DiscreteFuzzySet(original_domain, {('x_val', 'y_val', 'z_val'): 0.7})
            >>> fuzzy_set.rename_domain(renaming_dict)
            >>> domain = fuzzy_set.get_domain()
            >>> print(domain)
            ('a', 'b', 'z')
        """
        assert isinstance(ren_dict, dict), "'ren_dict' must be a dictionary!"
        for key, value in ren_dict.items():
            assert isinstance(key, str) and isinstance(key, str), "All keys and values in 'ren_dict' must be strings!"
            assert key in self.__domain, "'" + key + "' not in this FuzzySet domain!"
            assert value not in self.__domain, "'" + value + "' already in this FuzzySet domain!"
            self.__domain[self.__domain.index(key)] = value

    def select(self, condition: Callable) -> FuzzySet: # NON TESTATO : Banale
        """Selects elements from the fuzzy set based on a condition.

        This method filters the fuzzy set by applying a specified condition to each element and its
        membership value. The condition is a callable that takes a tuple consisting of the element and
        its membership value, and returns a boolean indicating whether the element should be included
        in the new fuzzy set. The resulting fuzzy set contains only the elements that satisfy the condition.

        Args:
            condition (Callable): A callable function that takes a tuple
                (element, membership) and returns `True` if the element
                should be included in the resulting set, `False`
                otherwise.

        Raises:
            AssertionError: If `condition` is not a callable function.

        Returns:
            FuzzySet: A new `DiscreteFuzzySet` object containing only
                the elements that satisfy the condition.

        Examples:
            >>> condition = lambda x: x[-1] > 0.6
            >>> original_set = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.5, ('c', 'd'): 0.8})
            >>> selected_set = original_set.select(condition)
            >>> print(selected_set)
            {('c', 'd'): 0.8}
        """
        assert isinstance(condition, Callable), "'function' must be a callable function!"
        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            if condition(tuple(list(element) + [membership])):
                new_set[element] = membership
        return DiscreteFuzzySet(self.get_domain(), new_set)
    
    def apply(self, operator: FuzzyUnaryOperator) -> FuzzySet:
        """Applies a fuzzy unary operator to all membership values in the fuzzy set.

        This method applies a specified 'FuzzyUnaryOperator' to each membership value in the fuzzy set,
        producing a new fuzzy set with the modified membership values.

        >> **WARNING**: only tuples with a membership value greater than 0 are kept.

        Args:
            operator (FuzzyUnaryOperator): A unary operator that
                operates on the membership values of the fuzzy set.

        Raises:
            AssertionError: If `operator` is not of type
                `FuzzyUnaryOperator`.

        Returns:
            FuzzySet: A new `DiscreteFuzzySet` object where the
                membership values have been modified according to the given
                unary operator.

        Examples:
            >>> operator = LinguisticModifiers.VERY
            >>> original_set = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.5, ('c', 'd'): 0.8})
            >>> modified_set = original_set.apply(operator)
            >>> print(modified_set.to_dictionary())
            {('a', 'b'): 0.25, ('c', 'd'): 0.64}
        """
        assert isinstance(operator, FuzzyUnaryOperator), "'operator' must be of type 'FuzzyUnaryOperator'!"
        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            new_membership = operator(membership)
            if new_membership > .0:
                new_set[element] = new_membership
        return DiscreteFuzzySet(self.get_domain(), new_set)

    def image(self, function: Callable, out_domain: tuple) -> FuzzySet: # NON TESTATO
        """Computes the image of the fuzzy set under a given function.

        This method applies a specified function to each element in the fuzzy set, mapping it to a new
        domain (`out_domain`). The resulting fuzzy set consists of the function's output as the new
        elements and their associated membership values. If multiple elements map to the same output,
        their membership values are combined using the fuzzy OR operation.

        Args:
            function (Callable): A callable function that maps
            out_domain (tuple): The domain of the resulting fuzzy
                elements from the original domain to the output domain.
                set after applying the function.

        Raises:
            AssertionError: If 'function' is not a callable.

        Returns:
            FuzzySet: A new 'DiscreteFuzzySet' object representing
                the image of the original fuzzy set under the given function.

        Examples:
            >>> def example_function(element):
            ...     if element == ('a', 'b'):
            ...         return ('c', )
            ...     elif element == ('c', 'd'):
            ...         return ('c', )
            ...     elif element == ('e', 'f'):
            ...         return ('d', )

            >>> original_set = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.5, ('c', 'd'): 0.8, ('e', 'f'): 0.4})
            >>> out_domain = ('z',)
            >>> image_set = original_set.image(example_function, out_domain)
            >>> print(image_set.to_dictionary())
            {('c', ): 0.8, ('d', ): 0.4}
            >>> print(image_set.get_domain())
            ('z',)
        """
        assert isinstance(function, Callable), "'function' must be a callable function!"
        new_set = {}
        for element, membership in self.__fuzzy_set.items():
            y = function(element)
            if y in new_set:
                new_set[y] = FuzzyLogic.or_fun(new_set[y], membership)
            else:
                new_set[y] = membership
        return DiscreteFuzzySet(out_domain, new_set)
    
    def cylindrical_extension(self, set2: FuzzySet) -> Tuple[FuzzySet, FuzzySet]:
        """Computes the cylindrical extension of two fuzzy sets over a combined domain.

        This method extends the current fuzzy set and `set2` to a common domain
        that includes all variables from both sets. The resulting sets have the same domain, with
        membership values adjusted according to the cylindrical extension. The new domain is created by
        merging the domains of the two sets:\n
        - First the common sets are added in the same order as their appear in the `self` domain
        - Second the unique sets of the `self` domain are concatenated in the same order as their appear in it
        - Third the unique sets of the `set2` domain are concatenated in the same order as their appear in it

        Args:
            set2 (DiscreteFuzzySet): Another fuzzy set to be extended.
                It must be an instance of `DiscreteFuzzySet`.

        Raises:
            AssertionError: If `set2` is not of type `DiscreteFuzzySet`.

        Returns:
            (Tuple[FuzzySet, FuzzySet]): A tuple containing two
                `DiscreteFuzzySet` objects \n
                - The first is the cylindrical
                extension of the original set.
                - The second is the
                cylindrical extension of `set2`.

        Examples:
            >>> set1 = DiscreteFuzzySet(('x', 'y'), {('a', 'b'): 0.5, ('c', 'd'): 0.4})
            >>> set2 = DiscreteFuzzySet(('y', 'z'), {('e', 'f'): 0.7, ('g', 'h'): 0.3})
            >>> extended_set1, extended_set2 = set1.cylindrical_extension(set2)
            >>> print(extended_set1.get_domain())
            ('y', 'x', 'z')
            >>> print(extended_set2.get_domain())
            ('y', 'x', 'z')
            >>> print(extended_set1.to_dictionary())
            {('b', 'a', 'f'): 0.5, ('b', 'a', 'h'): 0.5, ('d', 'c', 'f'): 0.4, ('d', 'c', 'h'): 0.4}
            >>> print(extended_set2.to_dictionary())
            {('e', 'a', 'f'): 0.7, ('e', 'c', 'f'): 0.7, ('g', 'a', 'h'): 0.3, ('g', 'c', 'h'): 0.3}
        """
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
        """Collapses the fuzzy set into a single membership value using a specified binary operator.

        This method reduces the fuzzy set to a single membership value by applying a binary operator
        iteratively across all membership values in the fuzzy set. The operator must be an instance
        of `FuzzyBinaryOperator`, and the fuzzy set must contain at least two elements.

        Args:
            operator (FuzzyBinaryOperator): A binary operator used to
                collapse the fuzzy set.

        Raises:
            AssertionError: If 'operator' is not of type
                `FuzzyBinaryOperator` or if the fuzzy set contains fewer
                than two elements.

        Returns:
            float: The resulting membership value after applying the
                binary operator across all elements.

        Examples:
            >>> operator = FuzzyAnd.MIN  # Example operator: minimum of two values
            >>> fuzzy_set = DiscreteFuzzySet(domain, {('a', 'b'): 0.4, ('c', 'd'): 0.6})
            >>> collapsed_value = fuzzy_set.collapse(operator)
            >>> print(collapsed_value)
            0.4
        """
        assert isinstance(operator, FuzzyBinaryOperator), "'operator' must be of type 'FuzzyBinaryOperator'!"
        assert len(self.__fuzzy_set.keys()) > 1, "The fuzzy set must have at least two elements!"
        memberships = list(self.__fuzzy_set.values())
        result = memberships[0]
        for membership in memberships[1:]:
            result = operator(result, membership)
        return result
    
    def reorder(self, new_domain: tuple) -> FuzzySet:
        """Reorders the elements of the fuzzy set according to a new domain permutation.

        This method takes a new domain represented by a tuple, which should be a permutation of the current domain,
        and reorders the elements of the fuzzy set to match the order of the variables in the new domain.
        The method returns a new `FuzzySet` object with the updated domain and reordered elements.

        Args:
            new_domain (tuple): A tuple representing a permutation of
                the original domain. The length of `new_domain` must be
                the same as the original domain.

        Raises:
            AssertionError: If `new_domain` is not a tuple, if its
                length differs from the original domain, or if any
                element in `new_domain` is not present in the original
                domain.

        Returns:
            FuzzySet: A new `FuzzySet` object with the reordered domain
                and elements.

        Examples:
            >>> original_domain = ('x', 'y', 'z')
            >>> new_domain = ('z', 'x', 'y')
            >>> fuzzy_set = DiscreteFuzzySet(original_domain, {('a', 'b', 'c'): 0.5, ('d', 'e', 'f'): 0.2})
            >>> reordered_set = fuzzy_set.reorder(new_domain)
            >>> print(reordered_set.to_dictionary())
            {('c', 'a', 'b'): 0.5, ('f', 'd', 'e'): 0.2}
        """
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

    def to_dictionary(self) -> dict: # differentia
        """Returns a dictionary where in the (key, value) pair
        the key represents the element in the fuzzy relation
        and the value represents its membership degree.

        Returns:
            dict: A dictionary representing the fuzzy relation.
        """
        return self.__fuzzy_set.copy()
    
    def elements(self) -> set: # differentia
        """Returns the set of all tuples in this fuzzy relation.

        Returns:
            set: The set of all tuples in this fuzzy relation.
        """
        return set(self.__fuzzy_set.keys())

    def memberships(self) -> set: # differentia
        """Returns the set of all memberships in this fuzzy relation.

        Returns:
            set: The set of all memberships in this fuzzy relation.
        """
        return set(self.__fuzzy_set.values())
    
    def items(self) -> set: # differentia
        """Returns the set of all (tuple, memberships) pairs
        in this fuzzy relation.

        Returns:
            set: The set of all (tuple, memberships) pairs
                in this fuzzy relation.
        """
        return set(self.__fuzzy_set.items())
    
    def tab_str(self) -> str: # differentia
        """Returns the tabular format string of this
        fuzzy relation.

        Returns:
            str: The tabular format string of this
                fuzzy relation.
        """
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
        """Returns the Zadeh inline string representation of this
        fuzzy set.

        Returns:
            str: Returns the Zadeh inline string
                representation of this fuzzy set.
        """
        s = ''
        for value, membership in self.__fuzzy_set.items():
            if membership > .0:
                s += str(membership) + '/' + str(value) + ' + '
        if len(self.__fuzzy_set.items()) > 0:
            return s[:-3]
        return '∅'
    
    def __str__(self) -> str: # differentia
        """Returns string representation of this
        fuzzy set.

        Returns:
            str: Returns the string representation of this
                fuzzy set.
        """
        return self.__repr__()