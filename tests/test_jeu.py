import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jeu import Jeu
from joueur import Joueur
from plateau import Plateau

class TestJeu(unittest.TestCase):
    def setUp(self):
        self.j1 = Joueur("A", "rouge")
        self.j2 = Joueur("B", "bleu")
        self.jeu = Jeu([self.j1, self.j2])
        self.jeu.initialiser_partie()

    def test_initialisation(self):
        self.assertEqual(self.jeu.manche, 1)
        self.assertEqual(len(self.jeu.joueurs), 2)
        self.assertEqual(self.jeu.plateau.air, 25)

    def test_deplacement_saut(self):
        # Placer deux joueurs sur des cases
        self.j1.position = 0
        self.j2.position = 2
        self.jeu.plateau.cases = [None]*10  # simplifié
        # Déplacer j1 de 2 pas direction 1
        self.j1.direction = 1
        self.jeu.deplacer_joueur(self.j1, 2)
        # Doit sauter case 2 (occupée par j2) et atterrir case 3
        self.assertEqual(self.j1.position, 3)

    def test_action_ramasser(self):
        # Créer une ruine à la position 0
        from jeton import Jeton
        self.jeu.plateau.cases = [Jeton('ruine', 2)]
        self.j1.position = 0
        self.jeu.action_ramasser(self.j1)
        self.assertEqual(len(self.j1.jetons_tenus), 1)
        self.assertEqual(self.jeu.plateau.cases[0].type, 'blanc')

if __name__ == '__main__':
    unittest.main()