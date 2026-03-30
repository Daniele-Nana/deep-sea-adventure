import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plateau import Plateau
from jeton import Jeton

class TestPlateau(unittest.TestCase):
    def setUp(self):
        self.plateau = Plateau()
        # Pour les tests, on utilise un petit plateau avec 6 cases
        valeurs_test = [(1,0), (1,0), (1,1), (1,1), (1,2), (1,2)]  # 6 cases
        self.plateau.initialiser(valeurs_test)

    def test_initialisation(self):
        self.assertEqual(len(self.plateau.cases), 6)
        self.assertEqual(self.plateau.air, 25)

    def test_remplacer_par_blanc(self):
        ancien = self.plateau.cases[0]
        self.plateau.remplacer_par_blanc(0)
        self.assertEqual(self.plateau.cases[0].type, 'blanc')

    def test_poser_jeton(self):
        jeton = Jeton('ruine', 1, 3)
        self.plateau.remplacer_par_blanc(0)
        self.plateau.poser_jeton(0, jeton)
        self.assertEqual(self.plateau.cases[0], jeton)

    def test_tasser(self):
        self.plateau.remplacer_par_blanc(1)
        self.plateau.remplacer_par_blanc(3)
        self.plateau.tasser()
        for j in self.plateau.cases:
            self.assertNotEqual(j.type, 'blanc')
        self.assertEqual(len(self.plateau.cases), 4)