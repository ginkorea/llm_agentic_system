class CostFunction:
    def evaluate(self, position):
        return sum(x**2 for x in position)  # Example: Sphere function