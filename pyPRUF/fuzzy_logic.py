from abc import abstractmethod
from decimal import Decimal, getcontext
from enum import Enum, member
import math

# getcontext().prec = 4

class FuzzyOperator(Enum):
    """
    An abstract base class that defines a generic fuzzy operator.
    A fuzzy operator is a function that takes memberships values
    and returns another membership value.

    This class is an enumeration (`Enum`) that requires derived classes
    to implement the `__call__()` method, which should return a `float`.
    In this way, it is possible to provide for each fuzzy operator,
    several implementations (or truth functions) that will correspond
    to the values of the Enum and call them all together with
    the `__call__()` method by using its operator `()`.

    This is useful in fuzzy logic where operators, such
    as fuzzy AND, OR, and NOT, have many truth functions such as
    t-norms and t-conorms.
    """

    @abstractmethod
    def __call__(self) -> float:
        """
        Perform the fuzzy operation.

        This method must be overridden by subclasses to define the
        specific behavior of the fuzzy operator.

        Returns:
            float: the result of the operation
        """
        pass

class FuzzyUnaryOperator(FuzzyOperator):
    """
    An abstract base class that defines a generic fuzzy unary operator
    by extending the `FuzzyOperator` `Enum` class.
    A fuzzy unary operator is a function that takes a
    membership value and returns another membership value.
    """

    @abstractmethod
    def __call__(self, a: float) -> float:
        """
        Perform the fuzzy unary operation.

        This method must be overridden by subclasses to define the
        specific behavior of the fuzzy unary operator.

        Parameters:
            a (float):  The membership value on which the
                operation is to be carried out.

        Returns:
            float: the result of the operation
        """
        pass

class FuzzyBinaryOperator(FuzzyOperator):
    """
    An abstract base class that defines a generic fuzzy binary operator
    by extending the `FuzzyOperator` `Enum` class.
    A fuzzy binary operator is a function that takes two
    memberships values and returns another membership value.
    """

    @abstractmethod
    def __call__(self, a: float, b: float) -> float:
        """
        Perform the fuzzy binary operation.

        This method must be overridden by subclasses to define the
        specific behavior of the fuzzy binary operator.

        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            float: the result of the operation
        """
        pass

class FuzzyAnd(FuzzyBinaryOperator):
    """
    A class that defines the AND fuzzy binary operator
    and its truth functions, or t-norms, inheriting from
    `FuzzyBinaryOperator` `Enum` class.

    This class, currently, includes common t-norms, or AND truth functions,
    such as the minimum, Łukasiewicz, algebraic product, and drastic product.

    Attributes:
        MIN (function):
            A static method representing the minimum t-norm,
            which is the most common fuzzy 'AND' operation.
        LUKASIEWICZ (function):
            A static method implementing the
            Łukasiewicz t-norm, which is defined as `max(a + b - 1, 0)`.
        ALGEBRAIC_PRODUCT (function):
            A static method implementing the
            algebraic product t-norm, defined as `a * b`.
        DRASTIC_PRODUCT (function):
            A static method implementing the drastic
            product t-norm, which returns 0 unless one of the values is 1.

    Examples:
        >>> result = FuzzyAnd.MIN(0.7, 0.8)
        >>> print(result)
        0.7

        >>> result = FuzzyAnd.LUKASIEWICZ(0.7, 0.5)
        >>> print(result)
        0.2

        >>> result = FuzzyAnd.ALGEBRAIC_PRODUCT(0.7, 0.8)
        >>> print(result)
        0.56

        >>> result = FuzzyAnd.DRASTIC_PRODUCT(0.7, 0.8)
        >>> print(result)
        0.0
    """

    MIN = min

    @member
    def LUKASIEWICZ(a: float, b: float) -> float:
        """
        A binary function that implements the Lukasiewicz AND
        truth function.

        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            float: `max(a + b - 1.0, 0.0)`.
        """
        # return max(float(Decimal(a + b) - Decimal(1.0)), 0.0)
        return max(a + b - 1.0, 0.0)
    
    @member
    def ALGEBRAIC_PRODUCT(a: float, b: float) -> float:
        """
        Implements the algebraic product AND
        truth function.
        
        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            float: a * b.
        """
        # return float(Decimal(a) * Decimal(b))
        return a * b
    
    @member
    def DRASTIC_PRODUCT(a: float, b: float) -> float:
        """
        Implements the drastic product AND
        truth function.

        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            float: .0 if 1.0 != a and 1.0 != b
                and min(a, b) otherwise.
        """
        if 1.0 != a and 1.0 != b:
            return 0.0
        return min(a, b)

    def __call__(self, a: float, b: float) -> float:
        """
        Calculates the fuzzy AND of a and b.

        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            float: the result of the AND operation.

        Raises:
            AssertionError: If `a` and `b` are not of type
                `float` in the interval [0, 1].
        """
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyOr(FuzzyBinaryOperator):
    """
    A class that defines the OR fuzzy binary operator
    and its truth functions by inheriting from
    `FuzzyBinaryOperator` `Enum` class.

    This class, currently, includes common t-conorms such as the maximum, 
    Łukasiewicz, algebraic sum, and drastic sum.

    Attributes:
        MAX (function):
            A static method representing the maximum t-conorm,
            which is the most common fuzzy 'OR' operation.
        LUKASIEWICZ (function):
            A static method implementing the Łukasiewicz t-conorm,
            defined as `min(a + b, 1.0)`.
        ALGEBRAIC_SUM (function):
            A static method implementing the algebraic sum t-conorm,
            defined as `a + b - a * b`.
        DRASTIC_SUM (function):
            A static method implementing the drastic sum t-conorm,
            which returns 1.0 unless one of the values is 0.

    Examples:
        >>> result = FuzzyOr.MAX(0.3, 0.8)
        >>> print(result)
        0.8

        >>> result = FuzzyOr.LUKASIEWICZ(0.7, 0.5)
        >>> print(result)
        1.0

        >>> result = FuzzyOr.ALGEBRAIC_SUM(0.3, 0.8)
        >>> print(result)
        0.86

        >>> result = FuzzyOr.DRASTIC_SUM(0.0, 0.8)
        >>> print(result)
        0.8
    """

    MAX = max

    @member
    def LUKASIEWICZ(a: float, b: float) -> float: # sempre > .0
        """
        Implements the Lukasiewicz OR
        truth function.

        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            float: `min(a + b, 1.0)`.
        """
        return min(a + b, 1.0)
    
    @member
    def ALGEBRAIC_SUM(a: float, b: float) -> float: # sempre > .0
        """
        Implements the algebraic sum OR
        truth function.

        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            a + b - a * b.
        """
        # return float(Decimal(a + b) - Decimal(a) * Decimal(b))
        return a + b - a * b
    
    @member
    def DRASTIC_SUM(a: float, b: float) -> float:
        """
        Implements the drastic sum OR
        truth function.

        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            1.0 if .0 != a and .0 != b
            and `max(a, b)` otherwise.
        """
        if .0 != a and .0 != b:
            return 1.0
        return max(a, b)

    def __call__(self, a: float, b: float) -> float:
        """
        Calculates the fuzzy OR of `a` and `b`.

        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            the result of the OR operation.

        Raises:
            AssertionError: If `a` and `b` are not of type
                `float` in the interval [0, 1].
        """
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyNot(FuzzyUnaryOperator):
    """
    A class that defines the NOT fuzzy binary operator
    and its truth functions inheriting from
    `FuzzyUnaryOperator` `Enum` class.

    The `FuzzyNot` class provides various methods to perform fuzzy 'NOT' operations, which are used to 
    invert the membership values of fuzzy sets. This class includes common operations such as the standard 
    negation and cosine-based negation.

    Attributes:
        STANDARD (function):
            A static method representing the standard negation, defined as `1.0 - value`.
        COSINE (function):
            A static method implementing cosine-based negation, defined as `(1.0 + cos(π * value)) / 2.0`.

    Examples:
        >>> result = FuzzyNot.STANDARD(0.3)
        >>> print(result)
        0.7

        >>> result = FuzzyNot.COSINE(0.3)
        >>> print(result)
        0.9045084971874737
    """
    
    @member
    def STANDARD(value: float) -> float:
        """
        Implements the standard NOT
        truth function.

        Parameters:
            value (float): The membership value on which the
                operation is to be carried out.

        Returns:
            float: `1.0 - value`.
        """
        # return float(Decimal(1.0) - Decimal(value))
        return 1.0 - value
    
    @member
    def COSINE(value: float) -> float:
        """
        Implements the standard NOT
        truth function.

        Parameters:
            value (float): The membership value on which the
                operation is to be carried out.

        Returns:
            float: `(1.0 + math.cos(math.pi * value)) / 2.0`.
        """
        # return (1.0 + math.cos(float(Decimal(math.pi) * Decimal(value)))) / 2.0
        return (1.0 + math.cos(math.pi * value)) / 2.0

    def __call__(self, a: float) -> float:
        """
        Calculates the fuzzy NOT of `a`.

        Parameters:
            a (float): The membership value on which the
                operation is to be carried out.

        Returns:
            the result of the NOT operation.

        Raises:
            AssertionError: If `a` is not of type
                `float` in the interval [0, 1].
        """
        assert isinstance(a, float), "'a' value must be float!"
        assert 0.0 <= a and a <= 1.0, "'a' must be between [0, 1]!"
        return self.value(a)

class FuzzyLogic():
    """
    A static class that encapsulates and manages all possible truth functions 
    for fuzzy AND, OR, and NOT operations within fuzzy logic.

    The `FuzzyLogic` class provides static methods to perform fuzzy logical operations, 
    such as AND, OR, and NOT, by utilizing configurable truth functions. These functions 
    are used in the `DiscreteFuzzySet` class to perform operations involving fuzzy logic.

    By using this class, it is possible to change the behavior of the `DiscreteFuzzySet` 
    class by altering the current truth functions for the fuzzy AND, OR, and NOT operations.
    """

    __and_fun: FuzzyAnd = FuzzyAnd.MIN
    __or_fun: FuzzyOr = FuzzyOr.MAX
    __not_fun: FuzzyNot = FuzzyNot.STANDARD

    def and_fun(a: float, b: float) -> float:
        """
        Calls the currently `FuzzyAnd` truth function set with
        `a` and `b` as parameters.

        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            float: the result of the currently
                `FuzzyAnd` truth function set.

        Raises:
            AssertionError: If `a` and `b` are not of type
                `float` in the interval [0, 1].
        """
        return FuzzyLogic.__and_fun(a, b)

    def or_fun(a: float, b: float) -> float:
        """
        Calls the currently `FuzzyOr` truth function set with
        `a` and `b` as parameters.

        Parameters:
            a (float): The first membership value.
            b (float): The second membership value.

        Returns:
            float: the result of the currently
                `FuzzyOr` truth function set.

        Raises:
            AssertionError: If `a` and `b` are not of type
                `float` in the interval [0, 1].
        """
        return FuzzyLogic.__or_fun(a, b)

    def not_fun(a: float) -> float:
        """
        Calls the currently `FuzzyNot` truth function set with
        `a` as parameter.

        Parameters:
            a (float): The membership value on which the
                operation is to be carried out.

        Returns:
            float: the result of the currently
                FuzzyNot truth function set.

        Raises:
            AssertionError: If `a` and `b` are not of type
                float in the interval [0, 1].
        """
        return FuzzyLogic.__not_fun(a)

    def set_and_fun(and_fun: FuzzyAnd) -> None:
        """
        Set `and_fun` as the current `FuzzyAnd` truth function.

        Parameters:
            and_fun (FuzzyAnd): The `FuzzyAnd` truth function.

        Raises:
            AssertionError: If `and_fun`
                is not of type `FuzzyAnd`.
        """
        assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"
        FuzzyLogic.__and_fun = and_fun

    def set_or_fun(or_fun: FuzzyOr) -> None:
        """
        Set `or_fun` as the current `FuzzyOr` truth function.

        Parameters:
            or_fun (FuzzyOr): The `FuzzyOr` truth function.

        Raises:
            AssertionError: If `or_fun`
                is not of type `FuzzyOr`.
        """
        assert isinstance(or_fun, FuzzyOr), "'or_fun' must be of type 'FuzzyOr'!"
        FuzzyLogic.__or_fun = or_fun
        
    def set_not_fun(not_fun: FuzzyNot) -> None:
        """
        Set `not_fun` as the current `FuzzyNot` truth function.

        Parameters:
            not_fun (FuzzyNot): The `FuzzyNot` truth function.

        Raises:
            AssertionError: If `not_fun`
                is not of type `FuzzyNot`.
        """
        assert isinstance(not_fun, FuzzyNot), "'not_fun' must be of type 'FuzzyNot'!"
        FuzzyLogic.__not_fun = not_fun

class LinguisticModifiers(FuzzyUnaryOperator):
    """
    A class that defines the linguistic modifiers
    inheriting from `FuzzyUnaryOperator` `Enum` class.
    A linguistic modifier is a function that takes
    a membership value and returns a modified
    membership value according to a linguistic
    semantic.

    The `LinguisticModifiers` class provides various methods to apply linguistic modifiers to 
    fuzzy sets, which adjust the degree of membership in a fuzzy set. This class includes common 
    modifiers such as 'VERY' (which intensifies the membership) and 'MORE_OR_LESS' (which softens the membership).

    Attributes:
        VERY (function):
            A static method representing the 'VERY' linguistic modifier, defined as `value * value`.
        MORE_OR_LESS (function):
            A static method representing the 'MORE_OR_LESS' linguistic modifier, defined as `sqrt(value)`.

    Examples:
        >>> result = LinguisticModifiers.VERY(0.7)
        >>> print(result)
        0.49

        >>> result = LinguisticModifiers.MORE_OR_LESS(0.49)
        >>> print(result)
        0.7
    """

    @member
    def VERY(value: float) -> float:
        """
        Calculates the 'very' linguistic modifier value
        of the membership value value.

        Parameters:
            value (float): The membership value on which the
                operation is to be carried out.

        Returns:
            float: `value * value`
        """
        # return float(Decimal(value) * Decimal(value))
        return value * value
    
    @member
    def MORE_OR_LESS(value: float) -> float:
        """
        Calculates the 'more or less' linguistic modifier value
        of the membership value value.

        Parameters:
            value (float): The membership value on which the
                operation is to be carried out.

        Returns:
            float: `math.sqrt(value)`
        """
        return math.sqrt(value)
    
    def __call__(self, a: float) -> float:
        """
        Calculates the linguistic modifier value of `a`.

        Parameters:
            a (float): The membership value on which the
                operation is to be carried out.

        Returns:
            float: the result of the linguistic modifier applied.

        Raises:
            AssertionError: If `a` is not of type
                `float` in the interval [0, 1].
        """
        assert isinstance(a, float), "'a' value must be float!"
        assert 0.0 <= a and a <= 1.0, "'a' must be between [0, 1]!"
        return self.value(a)