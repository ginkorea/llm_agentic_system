import unittest
from workbench.pso.pso_algorithm import PSOAlgorithm
from workbench.pso.cost_function import CostFunction
from workbench.pso.solution import Solution

class TestPSOAlgorithm(unittest.TestCase):
    def setUp(self):
        self.num_particles = 10
        self.max_iterations = 50
        self.bounds = [(-5, 5) for _ in range(2)]
        self.cost_function = CostFunction()
        self.pso = PSOAlgorithm(self.num_particles, self.max_iterations, self.bounds, self.cost_function)

    def test_optimize_returns_solution(self):
        solution = self.pso.optimize()
        self.assertIsInstance(solution, Solution)

    def test_optimize_improves_solution(self):
        initial_solution = Solution()
        final_solution = self.pso.optimize()
        self.assertLess(final_solution.value, initial_solution.value)

if __name__ == '__main__':
    unittest.main()