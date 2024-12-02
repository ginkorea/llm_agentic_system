import unittest
from workbench.pso.pso_algorithm import PSOAlgorithm
from workbench.pso.cost_function import CostFunction

class TestMainFlow(unittest.TestCase):
    def test_main_flow(self):
        num_particles = 30
        max_iterations = 100
        bounds = [(-10, 10) for _ in range(2)]
        cost_function = CostFunction()

        pso = PSOAlgorithm(num_particles, max_iterations, bounds, cost_function)
        best_solution = pso.optimize()
        
        self.assertIsInstance(best_solution.position, list)
        self.assertIsInstance(best_solution.value, float)
        self.assertLessEqual(len(best_solution.position), len(bounds))

if __name__ == '__main__':
    unittest.main()