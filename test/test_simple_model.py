import random
import unittest

from src.simple_model import SimpleModelPool


class SimpleModelTests(unittest.TestCase):

    def test_simple_model_smoke_test(self):

        random.seed(0)
        model = SimpleModelPool(10, 2.0, 3, 2, 1.0, acquired_immunity=False)
        model.iterate(10, verbose=False)

        print(model.get_results())
        self.assertTrue(model.get_results().endswith('Cumulative Infected: 2\nR_0: 0.4'))
