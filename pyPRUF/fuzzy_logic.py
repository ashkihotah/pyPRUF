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
    to implement the `__call__` method, which should return a `float`.
    In this way, it is possible to provide for each fuzzy operator,
    several implementations (or functions) that will correspond
    to the values of the Enum.

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

        :returns: the result of the operation
        :rtype: `float`
        """
        pass

class FuzzyUnaryOperator(FuzzyOperator):
    """
    An abstract base class that defines a generic fuzzy unary operator
    by extending the `FuzzyOperator` Enum class.
    A fuzzy unary operator is a function that takes a
    membership value and returns another membership value.
    """

    @abstractmethod
    def __call__(self, a: float) -> float:
        """
        Perform the fuzzy unary operation.

        This method must be overridden by subclasses to define the
        specific behavior of the fuzzy unary operator.

        :param float a: The membership value on which the
        operation is to be carried out.
        :returns: the result of the operation
        :rtype: `float`
        """
        pass

class FuzzyBinaryOperator(FuzzyOperator):
    """
    An abstract base class that defines a generic fuzzy binary operator
    by extending the `FuzzyOperator` Enum class.
    A fuzzy binary operator is a function that takes two
    memberships values and returns another membership value.
    """

    @abstractmethod
    def __call__(self, a: float, b: float) -> float:
        """
        Perform the fuzzy binary operation.

        This method must be overridden by subclasses to define the
        specific behavior of the fuzzy binary operator.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: the result of the operation
        :rtype: `float`
        """
        pass

class FuzzyAnd(FuzzyBinaryOperator):
    """
    A class that defines the AND fuzzy binary operator
    and its truth functions by extending the
    `FuzzyBinaryOperator` Enum class.

    Currently FuzzyAnd truth functions implemented are:
    1. MIN: The standard AND truth function.
    2. LUKASIEWICZ: The Lukasiewicz AND truth function.
    3. ALGEBRAIC_PRODUCT: the Algebraic Product AND truth function.
    4. DRASTIC_PRODUCT: the Drastic Product AND truth function.
    """

    MIN = min

    @member
    def LUKASIEWICZ(a: float, b: float) -> float:
        """
        A binary function that implements the Lukasiewicz AND
        truth function.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: `max(a + b - 1.0, 0.0)`.
        :rtype: `float`
        """
        # return max(float(Decimal(a + b) - Decimal(1.0)), 0.0)
        return max(a + b - 1.0, 0.0)
    
    @member
    def ALGEBRAIC_PRODUCT(a: float, b: float) -> float:
        """
        Implements the algebraic product AND
        truth function.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: `a * b`.
        :rtype: `float`
        """
        # return float(Decimal(a) * Decimal(b))
        return a * b
    
    @member
    def DRASTIC_PRODUCT(a: float, b: float) -> float:
        """
        Implements the drastic product AND
        truth function.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: `.0` if 1.0 != a and 1.0 != b
        and `min(a, b)` otherwise.
        :rtype: `float`
        """
        if 1.0 != a and 1.0 != b:
            return 0.0
        return min(a, b)

    def __call__(self, a: float, b: float) -> float:
        """
        Calculates the fuzzy AND of `a` and `b`.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: the result of the AND operation.
        :rtype: `float`

        :raises `AssertionError`: If `a` and `b` are not of type
        `float` in the interval [0, 1].
        """
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyOr(FuzzyBinaryOperator):
    """
    A class that defines the OR fuzzy binary operator
    and its truth functions by extending the
    `FuzzyBinaryOperator` Enum class.

    Currently FuzzyAnd truth functions implemented are:
    1. MAX: returns `max(a, b)`
    2. LUKASIEWICZ: returns `min(a + b, 1.0)`.
    3. ALGEBRAIC_SUM: returns `a + b - a * b`.
    4. DRASTIC_SUM: returns `1.0` if .0 != a and .0 != b
        and `max(a, b)` otherwise.
    """

    MAX = max

    @member
    def LUKASIEWICZ(a: float, b: float) -> float: # sempre > .0
        """
        Implements the Lukasiewicz OR
        truth function.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: `min(a + b, 1.0)`.
        :rtype: `float`
        """
        return min(a + b, 1.0)
    
    @member
    def ALGEBRAIC_SUM(a: float, b: float) -> float: # sempre > .0
        """
        Implements the algebraic sum OR
        truth function.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: `a + b - a * b`.
        :rtype: `float`
        """
        # return float(Decimal(a + b) - Decimal(a) * Decimal(b))
        return a + b - a * b
    
    @member
    def DRASTIC_SUM(a: float, b: float) -> float:
        """
        Implements the drastic sum OR
        truth function.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: `1.0` if .0 != a and .0 != b
        and `max(a, b)` otherwise.
        :rtype: `float`
        """
        if .0 != a and .0 != b:
            return 1.0
        return max(a, b)

    def __call__(self, a: float, b: float) -> float:
        """
        Calculates the fuzzy OR of `a` and `b`.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: the result of the OR operation.
        :rtype: `float`

        :raises `AssertionError`: If `a` and `b` are not of type
        `float` in the interval [0, 1].
        """
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyNot(FuzzyUnaryOperator):
    """
    A class that defines the NOT fuzzy binary operator
    and its truth functions by extending the
    `FuzzyUnaryOperator` Enum class.

    Currently FuzzyAnd truth functions implemented are:
    1. STANDARD: returns `1.0 - value`.
    2. COSINE: returns `(1.0 + math.cos(math.pi * value)) / 2.0`.
    """
    
    @member
    def STANDARD(value: float) -> float:
        """
        Implements the standard NOT
        truth function.

        :param float a: The membership value on which the
        operation is to be carried out.
        :returns: `1.0 - value`.
        :rtype: `float`
        """
        # return float(Decimal(1.0) - Decimal(value))
        return 1.0 - value
    
    @member
    def COSINE(value: float) -> float:
        """
        Implements the standard NOT
        truth function.

        :param float a: The membership value on which the
        operation is to be carried out.
        :returns: `(1.0 + math.cos(math.pi * value)) / 2.0`.
        :rtype: `float`
        """
        # return (1.0 + math.cos(float(Decimal(math.pi) * Decimal(value)))) / 2.0
        return (1.0 + math.cos(math.pi * value)) / 2.0

    def __call__(self, a: float) -> float:
        """
        Calculates the fuzzy NOT of `a`.

        :param float a: The membership value on which the
        operation is to be carried out.
        :returns: the result of the NOT operation.
        :rtype: `float`

        :raises `AssertionError`: If `a` is not of type
        `float` in the interval [0, 1].
        """
        assert isinstance(a, float), "'a' value must be float!"
        assert 0.0 <= a and a <= 1.0, "'a' must be between [0, 1]!"
        return self.value(a)

class FuzzyLogic():
    """
    A static class that encapsulates and handles all
    possible truth functions for fuzzy AND, OR and NOT operations
    that make up the fuzzy logic.
    """

    __and_fun: FuzzyAnd = FuzzyAnd.MIN
    __or_fun: FuzzyOr = FuzzyOr.MAX
    __not_fun: FuzzyNot = FuzzyNot.STANDARD

    def and_fun(a: float, b: float) -> float:
        """
        Calls the currently FuzzyAnd truth function set with
        `a` and `b` as parameters.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: the result of the currently
        FuzzyAnd truth function set.
        :rtype: `float`

        :raises `AssertionError`: If `a` and `b` are not of type
        `float` in the interval [0, 1].
        """
        return FuzzyLogic.__and_fun(a, b)

    def or_fun(a: float, b: float) -> float:
        """
        Calls the currently FuzzyOr truth function set with
        `a` and `b` as parameters.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: the result of the currently
        FuzzyOr truth function set.
        :rtype: `float`

        :raises `AssertionError`: If `a` and `b` are not of type
        `float` in the interval [0, 1].
        """
        return FuzzyLogic.__or_fun(a, b)

    def not_fun(a: float) -> float:
        """
        Calls the currently FuzzyNot truth function set with
        `a` as parameter.

        :param float a: The membership value on which the
        operation is to be carried out.
        :returns: the result of the currently
        FuzzyNot truth function set.
        :rtype: `float`

        :raises `AssertionError`: If `a` and `b` are not of type
        `float` in the interval [0, 1].
        """
        return FuzzyLogic.__not_fun(a)

    def set_and_fun(and_fun: FuzzyAnd) -> None:
        """
        Set `and_fun` as the current `FuzzyAnd` truth function.

        :param float and_fun: The `FuzzyAnd` truth function.

        :raises `AssertionError`: If `and_fun`
        is not of type `FuzzyAnd`.
        """
        assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"
        FuzzyLogic.__and_fun = and_fun

    def set_or_fun(or_fun: FuzzyOr) -> None:
        """
        Set `or_fun` as the current `FuzzyOr` truth function.

        :param float or_fun: The `FuzzyOr` truth function.

        :raises `AssertionError`: If `or_fun`
        is not of type `FuzzyOr`.
        """
        assert isinstance(or_fun, FuzzyOr), "'or_fun' must be of type 'FuzzyOr'!"
        FuzzyLogic.__or_fun = or_fun
        
    def set_not_fun(not_fun: FuzzyNot) -> None:
        """
        Set `not_fun` as the current `FuzzyNot` truth function.

        :param float not_fun: The `FuzzyNot` truth function.

        :raises `AssertionError`: If `not_fun`
        is not of type `FuzzyNot`.
        """
        assert isinstance(not_fun, FuzzyNot), "'not_fun' must be of type 'FuzzyNot'!"
        FuzzyLogic.__not_fun = not_fun

class LinguisticModifiers(FuzzyUnaryOperator):
    """
    A class that defines the linguistic modifiers
    by extending the `FuzzyUnaryOperator` Enum class.
    A linguistic modifier is a function that takes
    a membership value and returns a modified
    membership value according to a linguistic
    semantic.

    Currently `LinguisticModifiers` implemented are:
    1. VERY: returns the square power of the value in input.
    2. COSINE: returns the square root of the value in input.
    """

    @member
    def VERY(value: float) -> float:
        """
        Calculates the 'very' linguistic modifier value
        of the membership value `value`.

        :param float a: The first membership value on which the
        operation is to be carried out.
        :returns: `value * value`
        :rtype: `float`
        """
        # return float(Decimal(value) * Decimal(value))
        return value * value
    
    @member
    def MORE_OR_LESS(value: float) -> float:
        """
        Calculates the 'more or less' linguistic modifier value
        of the membership value `value`.

        :param float a: The first membership value on which the
        operation is to be carried out.
        :returns: `math.sqrt(value)`
        :rtype: `float`
        """
        return math.sqrt(value)
    
    def __call__(self, a: float) -> float:
        """
        Calculates the linguistic modifier value of `a`.

        :param float a: The membership value on which the
        operation is to be carried out.
        :returns: the result of the linguistic modifier applied.
        :rtype: `float`

        :raises `AssertionError`: If `a` is not of type
        `float` in the interval [0, 1].
        """
        assert isinstance(a, float), "'a' value must be float!"
        assert 0.0 <= a and a <= 1.0, "'a' must be between [0, 1]!"
        return self.value(a)