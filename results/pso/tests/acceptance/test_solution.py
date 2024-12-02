import unittest
from workbench.pso.solution import Solution

class TestSolution(unittest.TestCase):
    def test_initial_solution(self):
        solution = Solution()
        self.assertEqual(solution.position, [])
        self.assertEqual(solution.value, float('inf'))

if __name__ == '__main__':
    unittest.main()