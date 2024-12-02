import unittest
from workbench.pso.solution import Solution

class TestSolution(unittest.TestCase):
    def test_initial_solution(self):
        solution = Solution()
        self.assertEqual(solution.position, [])
        self.assertEqual(solution.value, float('inf'))

    def test_update_solution(self):
        solution = Solution()
        solution.position = [1.0, 2.0]
        solution.value = 5.0
        self.assertEqual(solution.position, [1.0, 2.0])
        self.assertEqual(solution.value, 5.0)

if __name__ == '__main__':
    unittest.main()