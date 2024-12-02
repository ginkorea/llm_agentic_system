from workbench.pso.pso_algorithm import PSOAlgorithm
from workbench.pso.cost_function import CostFunction

if __name__ == "__main__":
    num_particles = 30
    max_iterations = 100
    bounds = [(-10, 10) for _ in range(2)]  # Example bounds for a 2D problem
    cost_function = CostFunction()

    pso = PSOAlgorithm(num_particles, max_iterations, bounds, cost_function)
    best_solution = pso.optimize()
    print(f"Best solution found: {best_solution.position} with value {best_solution.value}")