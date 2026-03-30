import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jeton import Jeton

class TestJeton(unittest.TestCase):
    def test_creation_ruine(self):
        j = Jeton('ruine', 2)
        self.assertEqual(j.type, 'ruine')
        self.assertEqual(j.niveau, 2)
        self.assertEqual(j.points, 2)
        self.assertFalse(j.est_pile)

    def test_creation_blanc(self):
        j = Jeton('blanc')
        self.assertEqual(j.type, 'blanc')
        self.assertEqual(j.points, 0)

    def test_pile(self):
        j1 = Jeton('ruine', 1)
        j2 = Jeton('ruine', 2)
        j1.empiler(j2)
        self.assertTrue(j1.est_pile)
        self.assertEqual(len(j1.pile), 1)      # un seul ajouté
        self.assertEqual(j1.points, 3)         # 1 + 2

    def test_empiler_sur_blanc(self):
        j1 = Jeton('blanc')
        j2 = Jeton('ruine', 1)
        j1.empiler(j2)
        self.assertTrue(j1.est_pile)
        self.assertEqual(j1.type, 'ruine')
        self.assertEqual(j1.points, 1)
        self.assertEqual(len(j1.pile), 1)

if __name__ == '__main__':
    unittest.main()