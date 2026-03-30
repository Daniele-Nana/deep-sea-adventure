import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from de import De

class TestDe(unittest.TestCase):
    def test_lancer(self):
        for _ in range(100):
            valeur = De.lancer()
            self.assertGreaterEqual(valeur, 2)
            self.assertLessEqual(valeur, 12)

if __name__ == '__main__':
    unittest.main()