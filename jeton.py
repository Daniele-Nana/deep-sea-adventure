class Jeton:
    """Représente un jeton sur le plateau (ruine, blanc, ou pile)."""
    def __init__(self, type_jeton, niveau=None, valeur=None):
        self.type = type_jeton          # 'ruine' ou 'blanc'
        self.niveau = niveau if niveau is not None else 0   # niveau 1..4 pour les ruines
        self.valeur = valeur if valeur is not None else 0   # points réels (0..15)
        self.est_pile = False
        self.pile = []
        self.valeur_pile = 0

    @property
    def points(self):
        if self.type == 'blanc':
            return 0
        if self.est_pile:
            return self.valeur + self.valeur_pile
        return self.valeur

    def empiler(self, autre_jeton):
        if self.type == 'blanc':
            self.type = 'ruine'
            self.niveau = 0
            self.valeur = 0
            self.est_pile = True
            self.valeur_pile = 0
        elif not self.est_pile:
            self.est_pile = True
            self.valeur_pile = 0
        self.valeur_pile += autre_jeton.points
        self.pile.append(autre_jeton)

    def __repr__(self):
        if self.type == 'blanc':
            return 'Blanc'
        if self.est_pile:
            return f'Pile({len(self.pile) + 1})'
        return f'Ruine({self.valeur})'