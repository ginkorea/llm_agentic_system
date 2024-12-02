import unittest
from workbench.chakin.word_vector import WordVector

class TestWordVector(unittest.TestCase):
    def test_word_vector_initialization(self):
        vector = WordVector(
            name='Vector1', dimension=300, corpus='Wikipedia',
            vocabulary_size=1000000, method='fastText', language='English',
            paper='Some Paper', author='Some Author', url='http://example.com'
        )
        self.assertEqual(vector.name, 'Vector1')
        self.assertEqual(vector.dimension, 300)
        self.assertEqual(vector.language, 'English')

if __name__ == '__main__':
    unittest.main()