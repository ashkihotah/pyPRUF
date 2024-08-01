import os
import sys
from unittest import TextTestRunner
import unittest

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    
    # Scopri e carica i test
    loader = unittest.TestLoader()
    suite = loader.discover('tests')

    # Esegui i test usando il runner personalizzato
    runner = TextTestRunner(verbosity=1)
    runner.run(suite)