import random
from jeton import Jeton

class Plateau:
    def __init__(self):
        self.cases = []
        self.air = 25
        self.sous_marin_index = 0

    def initialiser(self, valeurs=None):
        """
        Crée les jetons ruines.
        Si valeurs est None, crée les 32 jetons officiels (4 niveaux, valeurs 0-15, deux de chaque).
        Sinon, utilise la liste de valeurs fournie (chaque élément doit être un tuple (niveau, valeur)).
        """
        if valeurs is None:
            # Valeurs officielles
            toutes_valeurs = []
            for niveau, (debut, fin) in enumerate([(0,3), (4,7), (8,11), (12,15)], start=1):
                for v in range(debut, fin+1):
                    toutes_valeurs.append((niveau, v))
                    toutes_valeurs.append((niveau, v))
            random.shuffle(toutes_valeurs)
            self.cases = [Jeton('ruine', niveau, valeur) for niveau, valeur in toutes_valeurs]
        else:
            # Pour les tests : on crée les jetons à partir des valeurs fournies
            self.cases = [Jeton('ruine', niveau, valeur) for (niveau, valeur) in valeurs]
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