from workbench.pso.particle import Particle
from workbench.pso.cost_function import CostFunction
from workbench.pso.solution import Solution

class PSOAlgorithm:
    def __init__(self, num_particles, max_iterations, bounds, cost_function):
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.bounds = bounds
        self.cost_function = cost_function
        self.particles = [Particle(bounds) for _ in range(num_particles)]

    def optimize(self):
        best_solution = Solution()
        for iteration in range(self.max_iterations):
            for particle in self.particles:
                cost = particle.evaluate(self.cost_function)
                if cost < best_solution.value:
                    best_solution.position = particle.position
                    best_solution.value = cost
                particle.updateVelocity(best_solution.position)
                particle.updatePosition(self.bounds)
            self.displayIterationInfo(iteration, best_solution)
        return best_solution

    def displayIterationInfo(self, iteration, best_solution):
        print(f"Iteration {iteration}: Best Solution = {best_solution.value}")