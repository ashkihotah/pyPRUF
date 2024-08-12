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

    This class is an enumeration (Enum) that requires derived classes
    to implement the __call__() method, which should return a float.
    In this way, it is possible to provide for each fuzzy operator,
    several implementations (or truth functions) that will correspond
    to the values of the Enum and call them all together with
    the __call__() method by using its operator '()'.

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
        :rtype: float
        """
        pass

class FuzzyUnaryOperator(FuzzyOperator):
    """
    An abstract base class that defines a generic fuzzy unary operator
    by extending the FuzzyOperator Enum class.
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
        :rtype: float
        """
        pass

class FuzzyBinaryOperator(FuzzyOperator):
    """
    An abstract base class that defines a generic fuzzy binary operator
    by extending the FuzzyOperator Enum class.
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
        :rtype: float
        """
        pass

class FuzzyAnd(FuzzyBinaryOperator):
    """
    A class that defines the AND fuzzy binary operator
    and its truth functions, or t-norms, inheriting from
    FuzzyBinaryOperator Enum class.

    This class, currently, includes common t-norms, or AND truth functions,
    such as the minimum, Łukasiewicz, algebraic product, and drastic product.

    Attributes
    ----------
    MIN : function
        A static method representing the minimum t-norm, which is the most common fuzzy 'AND' operation.
    LUKASIEWICZ : function
        A static method implementing the Łukasiewicz t-norm, which is defined as `max(a + b - 1, 0)`.
    ALGEBRAIC_PRODUCT : function
        A static method implementing the algebraic product t-norm, defined as `a * b`.
    DRASTIC_PRODUCT : function
        A static method implementing the drastic product t-norm, which returns 0 unless one of the values is 1.

    Methods
    -------
    __call__(a: float, b: float) -> float\n
        Apply the selected fuzzy 'AND' operation to the inputs `a` and `b`.

    :param a: The first membership value in the fuzzy 'AND' operation.
    :type a: float
    :param b: The second membership value in the fuzzy 'AND' operation.
    :type b: float

    :raises AssertionError: If `a` or `b` are not floats or are not within the range [0, 1].

    :return: The result of the fuzzy 'AND' operation using the selected t-norm.
    :rtype: float

    :example:

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

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: max(a + b - 1.0, 0.0).
        :rtype: float
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
        :returns: a * b.
        :rtype: float
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
        :returns: .0 if 1.0 != a and 1.0 != b
        and min(a, b) otherwise.
        :rtype: float
        """
        if 1.0 != a and 1.0 != b:
            return 0.0
        return min(a, b)

    def __call__(self, a: float, b: float) -> float:
        """
        Calculates the fuzzy AND of a and b.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: the result of the AND operation.
        :rtype: float

        :raises AssertionError: If a and b are not of type
        float in the interval [0, 1].
        """
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyOr(FuzzyBinaryOperator):
    """
    A class that defines the OR fuzzy binary operator
    and its truth functions by inheriting from
    FuzzyBinaryOperator Enum class.

    This class, currently, includes common t-conorms such as the maximum, 
    Łukasiewicz, algebraic sum, and drastic sum.

    Attributes
    ----------
    MAX : function
        A static method representing the maximum t-conorm, which is the most common fuzzy 'OR' operation.
    LUKASIEWICZ : function
        A static method implementing the Łukasiewicz t-conorm, defined as `min(a + b, 1.0)`.
    ALGEBRAIC_SUM : function
        A static method implementing the algebraic sum t-conorm, defined as `a + b - a * b`.
    DRASTIC_SUM : function
        A static method implementing the drastic sum t-conorm, which returns 1.0 unless one of the values is 0.

    Methods
    -------
    __call__(a: float, b: float) -> float
        Apply the selected fuzzy 'OR' operation to the inputs `a` and `b`.

    :param float a: The first membership value in the fuzzy 'OR' operation.
    :param float b: The second membership value in the fuzzy 'OR' operation.

    :raises AssertionError: If `a` or `b` are not floats or are not within the range [0, 1].

    :returns: The result of the fuzzy 'OR' operation using the selected t-conorm.
    :rtype: float

    Example:
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

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: min(a + b, 1.0).
        :rtype: float
        """
        return min(a + b, 1.0)
    
    @member
    def ALGEBRAIC_SUM(a: float, b: float) -> float: # sempre > .0
        """
        Implements the algebraic sum OR
        truth function.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: a + b - a * b.
        :rtype: float
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
        :returns: 1.0 if .0 != a and .0 != b
        and max(a, b) otherwise.
        :rtype: float
        """
        if .0 != a and .0 != b:
            return 1.0
        return max(a, b)

    def __call__(self, a: float, b: float) -> float:
        """
        Calculates the fuzzy OR of a and b.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: the result of the OR operation.
        :rtype: float

        :raises AssertionError: If a and b are not of type
        float in the interval [0, 1].
        """
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyNot(FuzzyUnaryOperator):
    """
    A class that defines the NOT fuzzy binary operator
    and its truth functions inheriting from
    FuzzyUnaryOperator Enum class.

    The `FuzzyNot` class provides various methods to perform fuzzy 'NOT' operations, which are used to 
    invert the membership values of fuzzy sets. This class includes common operations such as the standard 
    negation and cosine-based negation.

    Attributes
    ----------
    STANDARD : function
        A static method representing the standard negation, defined as `1.0 - value`.
    COSINE : function
        A static method implementing cosine-based negation, defined as `(1.0 + cos(π * value)) / 2.0`.

    Methods
    -------
    __call__(a: float) -> float
        Apply the selected fuzzy 'NOT' operation to the input `a`.

    :param float a: The membership value to be negated in the fuzzy 'NOT' operation.

    :raises AssertionError: If `a` is not a float or is not within the range [0, 1].

    :returns: The result of the fuzzy 'NOT' operation.
    :rtype: float

    Example:
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

        :param float a: The membership value on which the
        operation is to be carried out.
        :returns: 1.0 - value.
        :rtype: float
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
        :returns: (1.0 + math.cos(math.pi * value)) / 2.0.
        :rtype: float
        """
        # return (1.0 + math.cos(float(Decimal(math.pi) * Decimal(value)))) / 2.0
        return (1.0 + math.cos(math.pi * value)) / 2.0

    def __call__(self, a: float) -> float:
        """
        Calculates the fuzzy NOT of a.

        :param float a: The membership value on which the
        operation is to be carried out.
        :returns: the result of the NOT operation.
        :rtype: float

        :raises AssertionError: If a is not of type
        float in the interval [0, 1].
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
        Calls the currently FuzzyAnd truth function set with
        a and b as parameters.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: the result of the currently
        FuzzyAnd truth function set.
        :rtype: float

        :raises AssertionError: If a and b are not of type
        float in the interval [0, 1].
        """
        return FuzzyLogic.__and_fun(a, b)

    def or_fun(a: float, b: float) -> float:
        """
        Calls the currently FuzzyOr truth function set with
        a and b as parameters.

        :param float a: The first membership value.
        :param float b: The second membership value.
        :returns: the result of the currently
        FuzzyOr truth function set.
        :rtype: float

        :raises AssertionError: If a and b are not of type
        float in the interval [0, 1].
        """
        return FuzzyLogic.__or_fun(a, b)

    def not_fun(a: float) -> float:
        """
        Calls the currently FuzzyNot truth function set with
        a as parameter.

        :param float a: The membership value on which the
        operation is to be carried out.
        :returns: the result of the currently
        FuzzyNot truth function set.
        :rtype: float

        :raises AssertionError: If a and b are not of type
        float in the interval [0, 1].
        """
        return FuzzyLogic.__not_fun(a)

    def set_and_fun(and_fun: FuzzyAnd) -> None:
        """
        Set and_fun as the current FuzzyAnd truth function.

        :param float and_fun: The FuzzyAnd truth function.

        :raises AssertionError: If and_fun
        is not of type FuzzyAnd.
        """
        assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"
        FuzzyLogic.__and_fun = and_fun

    def set_or_fun(or_fun: FuzzyOr) -> None:
        """
        Set or_fun as the current FuzzyOr truth function.

        :param float or_fun: The FuzzyOr truth function.

        :raises AssertionError: If or_fun
        is not of type FuzzyOr.
        """
        assert isinstance(or_fun, FuzzyOr), "'or_fun' must be of type 'FuzzyOr'!"
        FuzzyLogic.__or_fun = or_fun
        
    def set_not_fun(not_fun: FuzzyNot) -> None:
        """
        Set not_fun as the current FuzzyNot truth function.

        :param float not_fun: The FuzzyNot truth function.

        :raises AssertionError: If not_fun
        is not of type FuzzyNot.
        """
        assert isinstance(not_fun, FuzzyNot), "'not_fun' must be of type 'FuzzyNot'!"
        FuzzyLogic.__not_fun = not_fun

class LinguisticModifiers(FuzzyUnaryOperator):
    """
    A class that defines the linguistic modifiers
    inheriting from FuzzyUnaryOperator Enum class.
    A linguistic modifier is a function that takes
    a membership value and returns a modified
    membership value according to a linguistic
    semantic.

    The `LinguisticModifiers` class provides various methods to apply linguistic modifiers to 
    fuzzy sets, which adjust the degree of membership in a fuzzy set. This class includes common 
    modifiers such as 'VERY' (which intensifies the membership) and 'MORE_OR_LESS' (which softens the membership).

    Attributes
    ----------
    VERY : function
        A static method representing the 'VERY' linguistic modifier, defined as `value * value`.
    MORE_OR_LESS : function
        A static method representing the 'MORE_OR_LESS' linguistic modifier, defined as `sqrt(value)`.

    Methods
    -------
    __call__(a: float) -> float
        Apply the selected linguistic modifier to the input `a`.

    :param float a: The membership value to be modified using the selected linguistic modifier.

    :raises AssertionError: If `a` is not a float or is not within the range [0, 1].

    :returns: The result of applying the linguistic modifier to the input value.
    :rtype: float

    Example:
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

        :param float a: The first membership value on which the
        operation is to be carried out.
        :returns: value * value
        :rtype: float
        """
        # return float(Decimal(value) * Decimal(value))
        return value * value
    
    @member
    def MORE_OR_LESS(value: float) -> float:
        """
        Calculates the 'more or less' linguistic modifier value
        of the membership value value.

        :param float a: The first membership value on which the
        operation is to be carried out.
        :returns: math.sqrt(value)
        :rtype: float
        """
        return math.sqrt(value)
    
    def __call__(self, a: float) -> float:
        """
        Calculates the linguistic modifier value of a.

        :param float a: The membership value on which the
        operation is to be carried out.
        :returns: the result of the linguistic modifier applied.
        :rtype: float

        :raises AssertionError: If a is not of type
        float in the interval [0, 1].
        """
        assert isinstance(a, float), "'a' value must be float!"
        assert 0.0 <= a and a <= 1.0, "'a' must be between [0, 1]!"
        return self.value(a)