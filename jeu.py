import pickle
import os
from plateau import Plateau
from de import De
from affichage_console import AffichageConsole

class RestartGameException(Exception):
    pass

class Jeu:
    def __init__(self, joueurs, affichage=None):
        self.plateau = Plateau()
        self.joueurs = joueurs
        self.manche = 1
        self.premier_joueur_index = 0
        self.affichage = affichage if affichage else AffichageConsole()
        self.nom_sauvegarde = None

    def __getstate__(self):
        state = self.__dict__.copy()
        state['affichage'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        from affichage_console import AffichageConsole
        self.affichage = AffichageConsole()

    def initialiser_partie(self):
        self.plateau.initialiser()
        for j in self.joueurs:
            j.position = -1
            j.est_rentre = False
            j.jetons_tenus = []
            j.direction = 1
            j.a_change_direction = False
            j.score_total = 0

    def demarrer_manche(self):
        for j in self.joueurs:
            j.est_rentre = False
            j.jetons_tenus = []
            j.direction = 1
            j.a_change_direction = False
            j.position = -1
        self.plateau.air = 25
        print(f"\n--- Manche {self.manche} ---")
        if hasattr(self.affichage, 'mettre_a_jour_infos'):
            self.affichage.mettre_a_jour_infos(self.plateau.air, self.manche)
        self.affichage.afficher_plateau(self.plateau, self.joueurs)

    def est_premier_tour_manche(self):
        return all(j.position == -1 and not j.est_rentre for j in self.joueurs)

    def jouer_tour(self, joueur):
        print(f"\nTour de {joueur.nom}")
        if hasattr(self.affichage, 'mettre_a_jour_joueur'):
            self.affichage.mettre_a_jour_joueur(joueur)

        # Étape 1 : Réduction d'air
        joueur.reduire_air(self.plateau)
        print(f"Air après réduction : {self.plateau.air}")
        if hasattr(self.affichage, 'mettre_a_jour_infos'):
            self.affichage.mettre_a_jour_infos(self.plateau.air, self.manche)

        # Étape 2 : Choix de rentrer ou pas (sauf premier tour)
        if not self.est_premier_tour_manche():
            if joueur.est_ia:
                choix_rentrer = joueur.ia.choisir_rentrer(joueur, self)
            else:
                choix_rentrer = self.affichage.demander_choix_rentrer(joueur)
            if choix_rentrer:
                joueur.changer_direction()
                print(f"{joueur.nom} fait demi-tour !")

        # Étape 3 : Lancer les dés et se déplacer
        des = De.lancer()
        jetons_tenus = len(joueur.jetons_tenus)
        deplacement = max(0, des - jetons_tenus)
        print(f"Dés: {des}, jetons tenus: {jetons_tenus} -> déplacement = {des} - {jetons_tenus} = {deplacement}")
        if hasattr(self.affichage, 'afficher_message'):
            self.affichage.afficher_message(f"{joueur.nom} a fait {des} aux dés. Déplacement de {deplacement} cases.")
        self.deplacer_joueur(joueur, deplacement)

        self.affichage.afficher_plateau(self.plateau, self.joueurs)

        # Étape 4 : Action
        self.effectuer_action(joueur)

        if joueur.position == -1:
            joueur.est_rentre = True
            print(f"{joueur.nom} est rentré au sous-marin !")

        self.affichage.afficher_plateau(self.plateau, self.joueurs)

    def deplacer_joueur(self, joueur, pas):
        pos = joueur.position
        direction = joueur.direction
        while pas > 0:
            nouvelle = pos + direction
            if direction > 0 and nouvelle >= len(self.plateau.cases):
                nouvelle = len(self.plateau.cases) - 1
                pos = nouvelle
                break
            if direction < 0 and nouvelle < -1:
                pos = -1
                break
            occupee = any(j.position == nouvelle and not j.est_rentre for j in self.joueurs if j != joueur)
            if occupee:
                pos = nouvelle
            else:
                pos = nouvelle
                pas -= 1
        joueur.position = pos
        if pos == -1:
            print(f"{joueur.nom} se déplace au sous‑marin")
        else:
            print(f"{joueur.nom} se déplace à la case {pos+1}")

    def effectuer_action(self, joueur):
        if joueur.position == -1:
            print(f"{joueur.nom} est au sous‑marin, aucune action.")
            return
        case = self.plateau.obtenir_jeton(joueur.position)
        actions_possibles = []
        if case.type == 'ruine':
            actions_possibles.append('ramasser')
        if case.type == 'blanc' and joueur.jetons_tenus:
            actions_possibles.append('poser')
        actions_possibles.append('rien')

        if joueur.est_ia:
            action = joueur.ia.choisir_action(joueur, self)
            if action == 'poser' and joueur.jetons_tenus:
                jeton_a_poser = joueur.jetons_tenus[0]
                self.action_poser(joueur, jeton_a_poser)
            elif action == 'ramasser' and case.type == 'ruine':
                self.action_ramasser(joueur)
            else:
                print(f"{joueur.nom} ne fait rien.")
        else:
            print(f"Actions possibles : {actions_possibles}")
            choix = self.affichage.demander_action(joueur, actions_possibles)
            if choix == 'ramasser' and 'ramasser' in actions_possibles:
                self.action_ramasser(joueur)
            elif choix == 'poser' and 'poser' in actions_possibles:
                jeton_a_poser = joueur.jetons_tenus[0]
                self.action_poser(joueur, jeton_a_poser)
            else:
                print(f"{joueur.nom} ne fait rien.")

    def action_ramasser(self, joueur):
        if joueur.position == -1:
            return
        case = self.plateau.obtenir_jeton(joueur.position)
        if case.type == 'ruine':
            joueur.jetons_tenus.append(case)
            self.plateau.remplacer_par_blanc(joueur.position)
            print(f"{joueur.nom} ramasse un jeton de valeur {case.valeur}")

    def action_poser(self, joueur, jeton):
        if joueur.position == -1:
            return
        if (self.plateau.obtenir_jeton(joueur.position).type == 'blanc'
                and jeton in joueur.jetons_tenus):
            joueur.jetons_tenus.remove(jeton)
            self.plateau.poser_jeton(joueur.position, jeton)
            print(f"{joueur.nom} pose un jeton de valeur {jeton.valeur}")

    def fin_manche(self):
        print("\n--- Fin de la manche ---")
        rentres = [j for j in self.joueurs if j.est_rentre]
        non_rentres = [j for j in self.joueurs if not j.est_rentre]

        for j in rentres:
            points = sum(jeton.points for jeton in j.jetons_tenus)
            j.score_total += points
            print(f"{j.nom} rentre avec {len(j.jetons_tenus)} jetons, "
                  f"gagne {points} points. Total: {j.score_total}")

        if non_rentres:
            print("Placement des jetons perdus :")
            non_rentres.sort(key=lambda j: j.position, reverse=True)
            case_index = len(self.plateau.cases) - 1
            for joueur in non_rentres:
                for jeton in joueur.jetons_tenus:
                    while case_index >= 0:
                        case = self.plateau.obtenir_jeton(case_index)
                        if case.type == 'blanc':
                            self.plateau.poser_jeton(case_index, jeton)
                            print(f"  Pose de {jeton} sur case {case_index} (blanc)")
                            break
                        elif case.est_pile and len(case.pile) < 3:
                            case.empiler(jeton)
                            print(f"  Ajout de {jeton} à la pile case {case_index}")
                            break
                        case_index -= 1
                    else:
                        print("  Plus de cases pour placer les jetons perdus !")
            self.plateau.tasser()
            print("Tassement du plateau effectué.")

        if non_rentres:
            nouveau_premier = max(non_rentres, key=lambda j: j.position)
            self.premier_joueur_index = self.joueurs.index(nouveau_premier)
            print(f"Prochain premier joueur : {nouveau_premier.nom} (le plus éloigné)")
        else:
            dernier_rentre = rentres[-1]
            self.premier_joueur_index = self.joueurs.index(dernier_rentre)

        self.manche += 1

        if self.manche <= 3 and hasattr(self.affichage, 'demander_sauvegarde'):
            if self.affichage.demander_sauvegarde():
                self.sauvegarder()

    def partie_terminee(self):
        return self.manche > 3

    def lancer_partie(self):
        self.initialiser_partie()
        try:
            while not self.partie_terminee():
                self.demarrer_manche()
                while True:
                    if all(j.est_rentre for j in self.joueurs) or self.plateau.air <= 0:
                        break
                    joueur_courant = self.joueurs[self.premier_joueur_index]
                    self.jouer_tour(joueur_courant)
                    next_index = (self.premier_joueur_index + 1) % len(self.joueurs)
                    while self.joueurs[next_index].est_rentre and next_index != self.premier_joueur_index:
                        next_index = (next_index + 1) % len(self.joueurs)
                    self.premier_joueur_index = next_index
                self.fin_manche()
            self.afficher_resultats()
        except RestartGameException:
            self.lancer_partie()
        except KeyboardInterrupt:
            if hasattr(self.affichage, 'demander_sauvegarde') and self.affichage.demander_sauvegarde():
                self.sauvegarder()
            print("\nPartie interrompue.")
        finally:
            if self.partie_terminee() and self.nom_sauvegarde and os.path.exists(self.nom_sauvegarde):
                os.remove(self.nom_sauvegarde)
                print("Sauvegarde supprimée (partie terminée).")
            if hasattr(self.affichage, 'fermer'):
                self.affichage.fermer()

    def afficher_resultats(self):
        print("\n--- Fin de la partie ---")
        for j in self.joueurs:
            print(f"{j.nom}: {j.score_total} points")
        gagnant = max(self.joueurs, key=lambda j: j.score_total)
        print(f"Le gagnant est {gagnant.nom} !")

    def sauvegarder(self, nom_suggestion=None):
        if nom_suggestion is None and hasattr(self.affichage, 'demander_nom_sauvegarde'):
            nom_suggestion = self.affichage.demander_nom_sauvegarde()
            if nom_suggestion is None:
                return
        if nom_suggestion is None:
            nom = input("Nom de la sauvegarde : ").strip()
            if not nom:
                print("Nom invalide, sauvegarde annulée.")
                return
        else:
            nom = nom_suggestion
        os.makedirs("saves", exist_ok=True)
        fichier = os.path.join("saves", nom + ".pkl")
        try:
            with open(fichier, 'wb') as f:
                pickle.dump(self, f)
            print(f"Partie sauvegardée dans {fichier}")
            self.nom_sauvegarde = fichier
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    @staticmethod
    def charger(fichier):
        try:
            with open(fichier, 'rb') as f:
                jeu = pickle.load(f)
            jeu.nom_sauvegarde = fichier
            print(f"Partie chargée depuis {fichier}")
            return jeu
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
            return None

    def recommencer(self):
        """Redémarre une partie avec les mêmes joueurs."""
        # Réinitialiser les joueurs
        for j in self.joueurs:
            j.position = -1
            j.est_rentre = False
            j.jetons_tenus = []
            j.direction = 1
            j.a_change_direction = False
            j.score_total = 0
        # Réinitialiser le plateau
        self.plateau.initialiser()
        self.manche = 1
        self.premier_joueur_index = 0
        self.nom_sauvegarde = None
        # Lever l'exception pour relancer la partie
        raise RestartGameException()