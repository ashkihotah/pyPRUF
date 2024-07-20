from decimal import Decimal, getcontext
from enum import Enum, member
import math

getcontext().prec = 4

class FuzzyAnd(Enum):
    MIN = min

    @member
    def LUKASIEWICZ(a: float, b: float) -> float:
        return max(float(Decimal(a + b) - Decimal(1.0)), 0.0)
        # return max(a + b - 1.0, 0.0)
    
    @member
    def ALGEBRAIC_PRODUCT(a: float, b: float) -> float:
        return float(Decimal(a) * Decimal(b))
        # return a * b
    
    @member
    def DRASTIC_PRODUCT(a: float, b: float) -> float:
        if 1.0 != a and 1.0 != b:
            return 0.0
        return min(a, b)

    def __call__(self, a: float, b: float) -> float:
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyOr(Enum):
    MAX = max

    @member
    def LUKASIEWICZ(a: float, b: float) -> float:
        return min(a + b, 1.0)
    
    @member
    def ALGEBRAIC_SUM(a: float, b: float) -> float:
        return float(Decimal(a + b) - Decimal(a) * Decimal(b))
        # return a + b - a * b
    
    @member
    def DRASTIC_SUM(a: float, b: float) -> float:
        if 1.0 != a and 1.0 != b:
            return 0.0
        return max(a, b)

    def __call__(self, a: float, b: float) -> float:
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyNot(Enum):
    
    @member
    def STANDARD(value: float) -> float:
        return float(Decimal(1.0) - Decimal(value))
        # return 1.0 - value
    
    @member
    def COSINE(value: float) -> float:
        # return (1.0 + math.cos(float(Decimal(math.pi) * Decimal(value)))) / 2.0
        return (1.0 + math.cos(math.pi * value)) / 2.0

    def __call__(self, a: float) -> float:
        assert isinstance(a, float), "'a' value must be float!"
        assert 0.0 <= a and a <= 1.0, "'a' must be between [0, 1]!"
        return self.value(a)

class LinguisticModifiers(Enum):

    @member # da valutare
    def NOT(value: float) -> float:
        return float(Decimal(1.0) - Decimal(value))
        # return 1.0 - value

    @member
    def VERY(value: float) -> float:
        return float(Decimal(value) * Decimal(value))
        # return value * value
    
    @member
    def MORE_OR_LESS(value: float) -> float:
        return math.sqrt(value)
    
    def __call__(self, a: float) -> float:
        assert isinstance(a, float), "'a' value must be float!"
        assert 0.0 <= a and a <= 1.0, "'a' must be between [0, 1]!"
        return self.value(a)