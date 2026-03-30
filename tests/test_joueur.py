import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from joueur import Joueur
from plateau import Plateau
from jeton import Jeton

class TestJoueur(unittest.TestCase):
    def setUp(self):
        self.joueur = Joueur("Toto", "rouge")
        self.plateau = Plateau()
        # Créer un petit plateau pour les tests
        valeurs_test = [(1,0), (1,0), (1,1), (1,1), (1,2), (1,2)]  # 6 cases
        self.plateau.initialiser(valeurs_test)

    def test_changer_direction(self):
        self.assertEqual(self.joueur.direction, 1)
        self.joueur.changer_direction()
        self.assertEqual(self.joueur.direction, -1)
        self.assertTrue(self.joueur.a_change_direction)
        self.joueur.changer_direction()
        self.assertEqual(self.joueur.direction, -1)

    def test_reduire_air(self):
        self.joueur.jetons_tenus.append(Jeton('ruine', 1, 1))
        self.joueur.jetons_tenus.append(Jeton('ruine', 2, 2))
        self.plateau.air = 25
        self.joueur.reduire_air(self.plateau)
        self.assertEqual(self.plateau.air, 23)