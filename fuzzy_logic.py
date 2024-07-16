from enum import Enum

class AND_FUNCTIONS(Enum):
    MIN = 0

class OR_FUNCTIONS(Enum):
    MAX = 0

class NOT_FUNCTIONS(Enum):
    STANDARD = 0

def standard_not(value: float) -> float:
    return 1 - value

class FuzzyLogic:

    __and_functions = [min]
    __or_functions = [max]
    __not_functions = [standard_not]

    __and: AND_FUNCTIONS = AND_FUNCTIONS.MIN
    __or: OR_FUNCTIONS = OR_FUNCTIONS.MAX
    __not: NOT_FUNCTIONS = NOT_FUNCTIONS.STANDARD

    @staticmethod
    def conjunction(a: float, b: float) -> float:
        return FuzzyLogic.__and_functions[FuzzyLogic.__and.value](a, b)

    @staticmethod
    def disjunction(a: float, b: float) -> float:
        return FuzzyLogic.__or_functions[FuzzyLogic.__or.value](a, b)
    
    @staticmethod
    def negation(a: float) -> float:
        return FuzzyLogic.__not_functions[FuzzyLogic.__not.value](a)
    
    @staticmethod
    def set_and_function(function: AND_FUNCTIONS) -> None:
        assert isinstance(function, AND_FUNCTIONS), 'The parameter function must be of type AND_FUNCTIONS'
        FuzzyLogic.__and = function
    
    @staticmethod
    def set_or_function(function: OR_FUNCTIONS) -> None:
        assert isinstance(function, OR_FUNCTIONS), 'The parameter function must be of type OR_FUNCTIONS'
        FuzzyLogic.__or = function

    @staticmethod
    def set_not_function(function: NOT_FUNCTIONS) -> None:
        assert isinstance(function, NOT_FUNCTIONS), 'The parameter function must be of type NOT_FUNCTIONS'
        FuzzyLogic.__not = function
