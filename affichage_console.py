class AffichageConsole:
    """Affichage en mode texte (ASCII)."""

    @staticmethod
    def afficher_plateau(plateau, joueurs):
        """Affiche le plateau, les indices, les jetons et les positions des joueurs."""
        # Indices
        print(" ".join(f"{i:2}" for i in range(len(plateau.cases))))
        # Cases
        cases_str = []
        for jeton in plateau.cases:
            if jeton.type == 'blanc':
                cases_str.append(" .")
            elif jeton.est_pile:
                cases_str.append(f" P{len(jeton.pile)+1}")
            else:
                cases_str.append(f" {jeton.niveau}")
        print(" ".join(cases_str))
        # Pions
        positions = {}
        for j in joueurs:
            if not j.est_rentre:
                positions[j.position] = positions.get(j.position, []) + [j.nom[0]]
        ligne_pions = ["  "] * len(plateau.cases)
        for idx, pions in positions.items():
            ligne_pions[idx] = "".join(pions)
        print(" ".join(ligne_pions))
        # Air
        print(f"Air: {plateau.air}\n")

    @staticmethod
    def demander_choix_rentrer(joueur):
        """Demande à l'utilisateur s'il veut rentrer (o/n)."""
        rep = input(f"{joueur.nom}, voulez-vous rentrer ? (o/n) : ").lower()
        return rep == 'o'

    @staticmethod
    def demander_action(joueur, actions_possibles):
        """Demande à l'utilisateur de choisir une action parmi celles possibles."""
        print(f"Actions possibles : {actions_possibles}")
        return input("Que voulez-vous faire ? ").strip().lower()
    
    @staticmethod
    def demander_sauvegarde():
        return input("Voulez-vous sauvegarder la partie ? (o/n) : ").lower() == 'o'