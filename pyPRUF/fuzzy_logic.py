from abc import abstractmethod
from decimal import Decimal, getcontext
from enum import Enum, member
import math

# getcontext().prec = 4

class FuzzyOperator(Enum):

    @abstractmethod
    def __call__(self) -> float:
        pass

class FuzzyUnaryOperator(FuzzyOperator):

    @abstractmethod
    def __call__(self, a: float) -> float:
        pass

class FuzzyBinaryOperator(FuzzyOperator):

    @abstractmethod
    def __call__(self, a: float, b: float) -> float:
        pass

class FuzzyAnd(FuzzyBinaryOperator):
    MIN = min

    @member
    def LUKASIEWICZ(a: float, b: float) -> float:
        # return max(float(Decimal(a + b) - Decimal(1.0)), 0.0)
        return max(a + b - 1.0, 0.0)
    
    @member
    def ALGEBRAIC_PRODUCT(a: float, b: float) -> float:
        # return float(Decimal(a) * Decimal(b))
        return a * b
    
    @member
    def DRASTIC_PRODUCT(a: float, b: float) -> float:
        if 1.0 != a and 1.0 != b:
            return 0.0
        return min(a, b)

    def __call__(self, a: float, b: float) -> float:
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyOr(FuzzyBinaryOperator):
    MAX = max

    @member
    def LUKASIEWICZ(a: float, b: float) -> float: # sempre > .0
        return min(a + b, 1.0)
    
    @member
    def ALGEBRAIC_SUM(a: float, b: float) -> float: # sempre > .0
        # return float(Decimal(a + b) - Decimal(a) * Decimal(b))
        return a + b - a * b
    
    @member
    def DRASTIC_SUM(a: float, b: float) -> float:
        if .0 != a and .0 != b:
            return 1.0
        return max(a, b)

    def __call__(self, a: float, b: float) -> float:
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyNot(FuzzyUnaryOperator):
    
    @member
    def STANDARD(value: float) -> float:
        # return float(Decimal(1.0) - Decimal(value))
        return 1.0 - value
    
    @member
    def COSINE(value: float) -> float:
        # return (1.0 + math.cos(float(Decimal(math.pi) * Decimal(value)))) / 2.0
        return (1.0 + math.cos(math.pi * value)) / 2.0

    def __call__(self, a: float) -> float:
        assert isinstance(a, float), "'a' value must be float!"
        assert 0.0 <= a and a <= 1.0, "'a' must be between [0, 1]!"
        return self.value(a)

class FuzzyLogic():

    __and_fun: FuzzyAnd = FuzzyAnd.MIN
    __or_fun: FuzzyOr = FuzzyOr.MAX
    __not_fun: FuzzyNot = FuzzyNot.STANDARD

    def and_fun(a: float, b: float) -> float:
        return FuzzyLogic.__and_fun(a, b)

    def or_fun(a: float, b: float) -> float:
        return FuzzyLogic.__or_fun(a, b)

    def not_fun(a: float) -> float:
        return FuzzyLogic.__not_fun(a)

    def set_and_fun(and_fun: FuzzyAnd) -> None:
        assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"
        FuzzyLogic.__and_fun = and_fun

    def set_or_fun(or_fun: FuzzyOr) -> None:
        assert isinstance(or_fun, FuzzyOr), "'or_fun' must be of type 'FuzzyOr'!"
        FuzzyLogic.__or_fun = or_fun
        
    def set_not_fun(not_fun: FuzzyNot) -> None:
        assert isinstance(not_fun, FuzzyNot), "'not_fun' must be of type 'FuzzyNot'!"
        FuzzyLogic.__not_fun = not_fun

class LinguisticModifiers(FuzzyUnaryOperator):

    @member
    def VERY(value: float) -> float:
        # return float(Decimal(value) * Decimal(value))
        return value * value
    
    @member
    def MORE_OR_LESS(value: float) -> float:
        return math.sqrt(value)
    
    def __call__(self, a: float) -> float:
        assert isinstance(a, float), "'a' value must be float!"
        assert 0.0 <= a and a <= 1.0, "'a' must be between [0, 1]!"
        return self.value(a)