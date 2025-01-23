from unittest import TextTestRunner
import unittest

from pyPRUF.fuzzy_logic import FuzzyAnd, FuzzyLogic, FuzzyNot, FuzzyOr

if __name__ == "__main__":
    loader = unittest.TestLoader()
    runner = TextTestRunner(verbosity=1)
    for and_fun in FuzzyAnd:
        for or_fun in FuzzyOr:
            for not_fun in FuzzyNot:
                print("\nAND:", and_fun)
                print("OR:", or_fun)
                print("NOT:", not_fun)
                FuzzyLogic.set_and_fun(and_fun)
                FuzzyLogic.set_or_fun(or_fun)
                FuzzyLogic.set_not_fun(not_fun)
                suite = loader.discover('tests')
                runner.run(suite)
                # input('> ')