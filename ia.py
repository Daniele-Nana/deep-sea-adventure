"""
Module contenant les classes d'IA.
"""

import random

class IA:
    """Classe abstraite pour une IA."""
    def choisir_rentrer(self, joueur, jeu):
        """Retourne True si l'IA décide de rentrer au sous-marin."""
        raise NotImplementedError

    def choisir_action(self, joueur, jeu):
        """
        Retourne 'ramasser', 'poser' ou 'rien' selon la stratégie.
        """
        raise NotImplementedError


class IAAleatoire(IA):
    """IA qui prend des décisions aléatoires."""

    def choisir_rentrer(self, joueur, jeu):
        return random.choice([True, False])

    def choisir_action(self, joueur, jeu):
        case = jeu.plateau.obtenir_jeton(joueur.position)
        if case.type == 'ruine':
            return 'ramasser'
        elif case.type == 'blanc' and joueur.jetons_tenus:
            return 'poser'
        else:
            return 'rien'


class IAPrudente(IA):
    def choisir_rentrer(self, joueur, jeu):
        if len(joueur.jetons_tenus) >= 2:
            return True
        if jeu.plateau.air < 10 and joueur.position > 3:
            return True
        return False

    def choisir_action(self, joueur, jeu):
        case = jeu.plateau.obtenir_jeton(joueur.position)
        # Si on peut poser un jeton et qu'on en a plusieurs, on le fait pour ralentir
        if case.type == 'blanc' and len(joueur.jetons_tenus) >= 2:
            return 'poser'
        if case.type == 'ruine' and len(joueur.jetons_tenus) < 3:
            return 'ramasser'
        return 'rien'


class IACourageuse(IA):
    """IA courageuse : prend des risques, va loin, ramasse beaucoup."""

    def choisir_rentrer(self, joueur, jeu):
        if len(joueur.jetons_tenus) >= 5:
            return True
        if jeu.plateau.air < 5 and joueur.position > 5:
            return True
        return False

    def choisir_action(self, joueur, jeu):
        case = jeu.plateau.obtenir_jeton(joueur.position)
        if case.type == 'ruine':
            return 'ramasser'
        return 'rien'