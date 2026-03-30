"""
Module définissant la classe Joueur.
"""

from ia import IAAleatoire, IAPrudente, IACourageuse

class Joueur:
    """
    Représente un joueur (humain ou IA) avec ses attributs de jeu.
    """

    def __init__(self, nom, couleur, est_ia=False, type_ia=None):
        """
        Initialise un joueur.
        - nom : son nom
        - couleur : sa couleur (utilisée pour l'affichage graphique)
        - est_ia : True si c'est une IA
        - type_ia : 'aleatoire', 'prudente' ou 'courageuse'
        """
        self.nom = nom
        self.couleur = couleur
        self.est_ia = est_ia
        self.type_ia = type_ia
        self.ia = None
        if est_ia:
            if type_ia == 'aleatoire':
                self.ia = IAAleatoire()
            elif type_ia == 'prudente':
                self.ia = IAPrudente()
            elif type_ia == 'courageuse':
                self.ia = IACourageuse()
            else:
                self.ia = IAAleatoire()
        # Attributs de jeu
        self.position = 0
        self.jetons_tenus = []
        self.est_rentre = False
        self.direction = 1
        self.a_change_direction = False
        self.score_total = 0

    def peut_changer_direction(self):
        """Retourne True si le joueur n'a pas encore changé de direction dans la manche."""
        return not self.a_change_direction

    def changer_direction(self):
        """Inverse la direction du joueur (vers le sous-marin ou vers le large)."""
        if self.peut_changer_direction():
            self.direction *= -1
            self.a_change_direction = True

    def reduire_air(self, plateau):
        """
        Réduit l'air du plateau du nombre de jetons tenus par le joueur.
        (étape 1 du tour)
        """
        plateau.air -= len(self.jetons_tenus)

    def __repr__(self):
        return f"{self.nom} ({self.couleur})"