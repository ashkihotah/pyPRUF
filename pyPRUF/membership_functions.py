from abc import ABC, abstractmethod
import math
import sys

class MembershipFunction(ABC):
    """Abstract base class for a membership function used
    in fuzzy logic.

    Subclasses must implement the `__call__`
    method, which defines the membership function
    for a given element `x`.
    """

    @abstractmethod
    def __call__(self, x) -> float:
        """Calculate the degree of membership for a given input `x`.

        Args:
            x: The element for which to
                calculate the membership degree.

        Returns:
            float: The degree of membership for the
                element `x`, in the range [0, 1].
        """
        pass

class Triangular(MembershipFunction):
    """A triangular membership function for all those fuzzy sets
    with domain the set of real numbers.
    """

    def __init__(self, a: float, b: float, c: float) -> None:
        """Initialize the triangular membership function.

        Args:
            a (float): The left endpoint of the triangle.
            b (float): The peak of the triangle.
            c (float): The right endpoint of the triangle.

        Raises:
            AssertionError: If the input values
                do not satisfy the condition `a < b < c`.
        """
        # super().__init__()
        assert isinstance(a, float), "'a' must be a float!"
        assert isinstance(b, float), "'b' must be a float!"
        assert isinstance(c, float), "'c' must be a float!"
        assert a < b and b < c, "The condition a < b < c must be satisfied!"
        self.a = a
        self.b = b
        self.c = c
    
    def __call__(self, x) -> float:
        """Calculate the membership degree for a given
        element x based on the triangular function.

        Args:
            x (float): The element for which to
                calculate the membership degree.

        Returns:
            float: - (x - self.a) / (self.b - self.a) if self.a <= x and x <= self.b \n
                - (self.c - x) / (self.c - self.b) if self.b <= x and x <= self.c \n
                - .0 otherwise \n

        Raises:
            AssertionError: If `x` is not of type `float`.
        """
        assert isinstance(x, float), "'x' must be a float!"
        if self.a <= x and x <= self.b:
            return (x - self.a) / (self.b - self.a)
        elif self.b <= x and x <= self.c:
            return (self.c - x) / (self.c - self.b)
        return 0.0
    
class Trapezoidal(MembershipFunction):
    """A trapezoidal membership function for all those fuzzy sets
    with domain the set of real numbers.
    """

    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        """Initialize the trapezoidal membership function.

        Args:
            a (float): The left endpoint of the trapezoid.
            b (float): The start of the top of the trapezoid.
            c (float): The end of the top of the trapezoid.
            d (float): The right endpoint of the trapezoid.

        Raises:
            AssertionError: If the input values do not satisfy the
                conditions \n
                - `a < b or (a == -sys.float_info.max and a == b)`
                - `b < c`
                - `c < d or (c == sys.float_info.max and c == d)`
        """
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
        """Calculate the membership degree for a given element `x` based on the trapezoidal function.

        Args:
            x (float): The element for which to calculate the membership
                degree.

        Returns:
            float: - 0 if x < a or x > d \n
                - (x - a) / (b - a) if a <= x < b
                - 1 if b <= x <= c
                - (d - x) / (d - c) if c < x <= d

        Raises:
            AssertionError: If `x` is not of type float.
        """
        assert isinstance(x, float), "'x' must be a float!"
        if self.a <= x and x < self.b: # IMPORTANTE: il minore stretto a x < self.b evita che quando a = b = -Inf ci sia divisione per 0
            return (x - self.a) / (self.b - self.a)
        elif self.b <= x and x <= self.c:
            return 1.0
        elif self.c < x and x <= self.d: # IMPORTANTE: il minore stretto a self.c < x evita che quando c = d = Inf ci sia divisione per 0
            return (self.d - x) / (self.d - self.c)
        return 0.0

class Bell(MembershipFunction):
    """A bell membership function for all those fuzzy sets
    with domain the set of real numbers.
    """

    def __init__(self, m: float, s: float) -> None:
        """Initialize the bell-shaped membership function.

        Args:
            m (float): The center of the bell curve.
            s (float): The width of the bell curve.

        Raises:
            AssertionError: If the input values for `m` or `s` are not
                of type `float`.
        """
        # super().__init__()
        assert isinstance(m, float), "'a' must be a float!"
        assert isinstance(s, float), "'b' must be a float!"
        self.m = m
        self.s = s
    
    def __call__(self, x) -> float:
        """Calculate the membership degree for a given
        element `x` based on the bell-shaped function.

        Args:
            x (float): The element for which to calculate the membership
                degree.

        Returns:
            float: math.exp(-((x - self.m) ** 2) / (self.s ** 2))

        Raises:
            AssertionError: If `x` is not of type `float`.
        """
        assert isinstance(x, float), "'x' must be a float!"
        return math.exp(-((x - self.m) ** 2) / (self.s ** 2))