from abc import ABC, abstractmethod
import math
import sys

class MembershipFunction(ABC):

    @abstractmethod
    def __call__(self, x) -> float:
        pass

class Triangular(MembershipFunction):

    def __init__(self, a: float, b: float, c: float) -> None:
        # super().__init__()
        assert isinstance(a, float), "'a' must be a float!"
        assert isinstance(b, float), "'b' must be a float!"
        assert isinstance(c, float), "'c' must be a float!"
        assert a < b and b < c, "The condition a < b < c must be satisfied!"
        self.a = a
        self.b = b
        self.c = c
    
    def __call__(self, x) -> float:
        assert isinstance(x, float), "'x' must be a float!"
        if self.a <= x and x <= self.b:
            return (x - self.a) / (self.b - self.a)
        elif self.b <= x and x <= self.c:
            return (self.c - x) / (self.c - self.b)
        return 0.0
    
class Trapezoidal(MembershipFunction):

    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        # super().__init__()
        assert isinstance(a, float), "'a' must be a float!"
        assert isinstance(b, float), "'b' must be a float!"
        assert isinstance(c, float), "'c' must be a float!"
        assert isinstance(d, float), "'c' must be a float!"
        assert (a < b or (a == -sys.float_info.max and a == b)), "The condition a < b or (a == -sys.float_info.max and a == b) must be satisfied!"
        assert b < c, "The condition b < c must be satisfied!" # se togli questo assert viene rappresentata correttamente anche la triangolare
        assert (c < d or (c == sys.float_info.max and c == d)), "The condition (c < d or (c == -sys.float_info.max and c == d)) must be satisfied!"
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
    def __call__(self, x) -> float:
        assert isinstance(x, float), "'x' must be a float!"
        if self.a <= x and x < self.b: # IMPORTANTE: il minore stretto a x < self.b evita che quando a = b = -Inf ci sia divisione per 0
            return (x - self.a) / (self.b - self.a)
        elif self.b <= x and x <= self.c:
            return 1.0
        elif self.c < x and x <= self.d: # IMPORTANTE: il minore stretto a self.c < x evita che quando c = d = Inf ci sia divisione per 0
            return (self.d - x) / (self.d - self.c)
        return 0.0

class Bell(MembershipFunction):

    def __init__(self, m: float, s: float) -> None:
        # super().__init__()
        assert isinstance(m, float), "'a' must be a float!"
        assert isinstance(s, float), "'b' must be a float!"
        self.m = m
        self.s = s
    
    def __call__(self, x) -> float:
        assert isinstance(x, float), "'x' must be a float!"
        return math.exp(-((x - self.m) ** 2) / (self.s ** 2))