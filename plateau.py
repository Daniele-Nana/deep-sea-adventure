import random
from jeton import Jeton

class Plateau:
    def __init__(self):
        self.cases = []
        self.air = 25
        self.sous_marin_index = 0

    def initialiser(self):
        """
        Crée 32 jetons ruines dans l'ordre des niveaux :
        - cases 0 à 7 : niveau 1, valeurs 0,1,2,3 (deux de chaque, mélangées)
        - cases 8 à 15 : niveau 2, valeurs 4,5,6,7 (deux de chaque, mélangées)
        - cases 16 à 23 : niveau 3, valeurs 8,9,10,11 (deux de chaque, mélangées)
        - cases 24 à 31 : niveau 4, valeurs 12,13,14,15 (deux de chaque, mélangées)
        """
        valeurs_par_niveau = [
            ([0,0,1,1,2,2,3,3]),        # niveau 1
            ([4,4,5,5,6,6,7,7]),        # niveau 2
            ([8,8,9,9,10,10,11,11]),    # niveau 3
            ([12,12,13,13,14,14,15,15]) # niveau 4
        ]
        self.cases = []
        for niveau, valeurs in enumerate(valeurs_par_niveau, start=1):
            # Mélanger les valeurs de ce niveau
            valeurs_melangees = valeurs[:]
            random.shuffle(valeurs_melangees)
            for val in valeurs_melangees:
                self.cases.append(Jeton('ruine', niveau, val))
        self.air = 25
        # Vérification du nombre de cases
        assert len(self.cases) == 32, f"Erreur : {len(self.cases)} cases créées au lieu de 32"

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