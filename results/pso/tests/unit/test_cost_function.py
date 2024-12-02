import unittest
from workbench.pso.cost_function import CostFunction

class TestCostFunction(unittest.TestCase):
    def setUp(self):
        self.cost_function = CostFunction()

    def test_evaluate(self):
        position = [1.0, 2.0]
        cost = self.cost_function.evaluate(position)
        self.assertEqual(cost, 5.0)  # 1^2 + 2^2 = 5

    def test_evaluate_zero(self):
        position = [0.0, 0.0]
        cost = self.cost_function.evaluate(position)
        self.assertEqual(cost, 0.0)

    def test_evaluate_negative(self):
        position = [-1.0, -2.0]
        cost = self.cost_function.evaluate(position)
        self.assertEqual(cost, 5.0)  # (-1)^2 + (-2)^2 = 5

if __name__ == '__main__':
    unittest.main()