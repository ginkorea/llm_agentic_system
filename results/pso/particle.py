from random import uniform

class Particle:
    def __init__(self, bounds):
        self.position = [uniform(bound[0], bound[1]) for bound in bounds]
        self.velocity = [0.0 for _ in bounds]
        self.bestPosition = self.position[:]

    def evaluate(self, cost_function):
        cost = cost_function.evaluate(self.position)
        if cost < cost_function.evaluate(self.bestPosition):
            self.bestPosition = self.position[:]
        return cost

    def updateVelocity(self, global_best_position):
        inertia = 0.5
        cognitive = 1.0
        social = 1.0
        self.velocity = [
            inertia * v +
            cognitive * uniform(0, 1) * (pbest - p) +
            social * uniform(0, 1) * (gbest - p)
            for v, p, pbest, gbest in zip(self.velocity, self.position, self.bestPosition, global_best_position)
        ]

    def updatePosition(self, bounds):
        self.position = [
            max(min(p + v, bound[1]), bound[0])
            for p, v, bound in zip(self.position, self.velocity, bounds)
        ]