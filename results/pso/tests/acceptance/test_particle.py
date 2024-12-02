import unittest
from workbench.pso.particle import Particle
from workbench.pso.cost_function import CostFunction

class TestParticle(unittest.TestCase):
    def setUp(self):
        self.bounds = [(-5, 5) for _ in range(2)]
        self.particle = Particle(self.bounds)
        self.cost_function = CostFunction()

    def test_initial_position_within_bounds(self):
        for pos, bound in zip(self.particle.position, self.bounds):
            self.assertGreaterEqual(pos, bound[0])
            self.assertLessEqual(pos, bound[1])

    def test_evaluate_cost_function(self):
        cost = self.particle.evaluate(self.cost_function)
        self.assertIsInstance(cost, float)

    def test_update_position_within_bounds(self):
        global_best_position = [0.0, 0.0]
        self.particle.updateVelocity(global_best_position)
        self.particle.updatePosition(self.bounds)
        for pos, bound in zip(self.particle.position, self.bounds):
            self.assertGreaterEqual(pos, bound[0])
            self.assertLessEqual(pos, bound[1])

if __name__ == '__main__':
    unittest.main()