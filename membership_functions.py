from abc import ABC, abstractmethod
import math
import sys

from matplotlib import pyplot as plt
import numpy as np

def plot_function(f, x_range=(-1000, 1000), num_points=1000, title="Grafico della funzione"):
    """
    Plotta il grafico di una funzione data.
    
    Parametri:
    f (function): La funzione da plottare. Deve essere una funzione di una variabile reale.
    x_range (tuple): Una tupla (min, max) che definisce l'intervallo dell'asse x.
    num_points (int): Il numero di punti da plottare tra x_range[0] e x_range[1].
    title (str): Il titolo del grafico.
    """
    x = np.linspace(x_range[0], x_range[1], num_points, dtype=float)
    y = [f(value) for value in x]
    # print(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='f(x)')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

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
        assert b < c, "The condition b < c must be satisfied!"
        assert (c < d or (c == sys.float_info.max and c == d)), "The condition (c < d or (c == -sys.float_info.max and c == d)) must be satisfied!"
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
    def __call__(self, x) -> float:
        assert isinstance(x, float), "'x' must be a float!"
        if self.a <= x and x < self.b:
            return (x - self.a) / (self.b - self.a)
        elif self.b <= x and x <= self.c:
            return 1.0
        elif self.c <= x and x <= self.d:
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
    

# plot_function(f = Trapezoidal(-sys.float_info.max, -sys.float_info.max, 20.0, 50.0),
#               title = 'f(x)')

# plot_function(f = Trapezoidal(20.0, 50.0, sys.float_info.max, sys.float_info.max),
#               title = 'f(x)')

# plot_function(f = Trapezoidal(-sys.float_info.max, -sys.float_info.max, sys.float_info.max, sys.float_info.max),
#               title = 'f(x)')

# plot_function(f = Trapezoidal(-200.0, -100.0, 100.0, 200.0),
#               title = 'f(x)')

# plot_function(f = Trapezoidal(-sys.float_info.max, -100.0, 100.0, sys.float_info.max),
#               title = 'f(x)')
# print(Trapezoidal(-sys.float_info.max, -100.0, 100.0, sys.float_info.max)(50.0))