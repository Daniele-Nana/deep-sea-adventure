import random
from jeton import Jeton

import random
from jeton import Jeton

class Plateau:
    def __init__(self):
        self.cases = []
        self.air = 25
        self.sous_marin_index = 0

    def initialiser(self):
        """Crée 32 jetons : 8 cases par niveau, valeurs 0-3, 4-7, 8-11, 12-15, deux de chaque, mélangées dans chaque niveau."""
        valeurs_par_niveau = [
            [0,0,1,1,2,2,3,3],        # niveau 1
            [4,4,5,5,6,6,7,7],        # niveau 2
            [8,8,9,9,10,10,11,11],    # niveau 3
            [12,12,13,13,14,14,15,15] # niveau 4
        ]
        self.cases = []
        for niveau, valeurs in enumerate(valeurs_par_niveau, start=1):
            random.shuffle(valeurs)   # mélange des valeurs à l'intérieur du niveau
            for val in valeurs:
                self.cases.append(Jeton('ruine', niveau, val))
        self.air = 25

    def est_dans_plateau(self, index):
        return 0 <= index < len(self.cases)

    def obtenir_jeton(self, index):
        return self.cases[index]

    def remplacer_par_blanc(self, index):
        self.cases[index] = Jeton('blanc')

    def poser_jeton(self, index, jeton):
        self.cases[index] = jeton

    def tasser(self):
        """Retire tous les blancs et tasse les jetons restants."""
        self.cases = [j for j in self.cases if j.type != 'blanc']