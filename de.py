import random

class De:
    """Simule deux dés à 6 faces."""
    @staticmethod
    def lancer():
        """Retourne la somme de deux dés aléatoires (de 2 à 12)."""
        return random.randint(1, 6) + random.randint(1, 6)