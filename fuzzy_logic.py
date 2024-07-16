from enum import Enum, member

class FuzzyAnd(Enum):
    MIN = min

    def __call__(self, a: float, b: float) -> float:
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyOr(Enum):
    MAX = max

    def __call__(self, a: float, b: float) -> float:
        assert isinstance(a, float) and isinstance(b, float), "'a' and 'b' values must be floats!"
        assert 0.0 <= a and a <= 1.0 and 0.0 <= b and b <= 1.0, "'a' and 'b' must be between [0, 1]!"
        return self.value(a, b)

class FuzzyNot(Enum):
    
    @member
    def STANDARD(value: float) -> float:
        return 1 - value

    def __call__(self, a: float) -> float:
        assert isinstance(a, float), "'a' value must be float!"
        assert 0.0 <= a and a <= 1.0, "'a' must be between [0, 1]!"
        return self.value(a)