import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import signal
import os

class ConfigDialog:
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configuration de la partie")
        self.dialog.geometry("500x500")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.lift()
        self.dialog.focus_force()
        
        self.nb_joueurs = tk.IntVar(value=2)
        self.players_data = []
        
        frame_nb = ttk.Frame(self.dialog)
        frame_nb.pack(pady=10)
        ttk.Label(frame_nb, text="Nombre de joueurs (2-6) :").pack(side=tk.LEFT)
        self.spin_nb = ttk.Spinbox(frame_nb, from_=2, to=6, textvariable=self.nb_joueurs,
                                   width=5, command=self.actualiser_formulaires)
        self.spin_nb.pack(side=tk.LEFT, padx=5)
        
        self.frame_players = ttk.LabelFrame(self.dialog, text="Joueurs")
        self.frame_players.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.actualiser_formulaires()
        
        frame_buttons = ttk.Frame(self.dialog)
        frame_buttons.pack(pady=10)
        ttk.Button(frame_buttons, text="OK", command=self.valider).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Annuler", command=self.annuler).pack(side=tk.LEFT, padx=5)
        
        self.dialog.wait_window()
    
    def actualiser_formulaires(self):
        for widget in self.frame_players.winfo_children():
            widget.destroy()
        nb = self.nb_joueurs.get()
        self.players_data = []
        couleurs_dispo = ['rouge', 'bleu', 'vert', 'jaune', 'noir', 'blanc',
                          'violet', 'orange', 'rose', 'gris', 'cyan', 'magenta',
                          'marron', 'beige']
        for i in range(nb):
            frame = ttk.LabelFrame(self.frame_players, text=f"Joueur {i+1}")
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(frame, text="Nom :").grid(row=0, column=0, sticky='w', padx=5, pady=2)
            entry_nom = ttk.Entry(frame)
            entry_nom.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(frame, text="Couleur :").grid(row=1, column=0, sticky='w', padx=5, pady=2)
            combo_couleur = ttk.Combobox(frame, values=couleurs_dispo, width=15)
            combo_couleur.grid(row=1, column=1, padx=5, pady=2)
            combo_couleur.set(couleurs_dispo[i % len(couleurs_dispo)])
            
            var_ia = tk.BooleanVar(value=False)
            cb_ia = ttk.Checkbutton(frame, text="IA", variable=var_ia)
            cb_ia.grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=2)
            
            frame_ia = ttk.Frame(frame)
            frame_ia.grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky='w')
            ttk.Label(frame_ia, text="Type IA :").pack(side=tk.LEFT)
            combo_ia = ttk.Combobox(frame_ia, values=['aleatoire', 'prudente', 'courageuse'], width=15)
            combo_ia.pack(side=tk.LEFT, padx=5)
            combo_ia.set('aleatoire')
            frame_ia.grid_remove()
            
            def toggle_ia(idx=i):
                if self.players_data[idx]['est_ia'].get():
                    self.players_data[idx]['frame_ia'].grid()
                else:
                    self.players_data[idx]['frame_ia'].grid_remove()
            cb_ia.config(command=toggle_ia)
            
            self.players_data.append({
                'nom': entry_nom,
                'couleur': combo_couleur,
                'est_ia': var_ia,
                'type_ia': combo_ia,
                'frame_ia': frame_ia
            })
    
    def valider(self):
        noms = [data['nom'].get().strip() for data in self.players_data]
        if any(n == '' for n in noms):
            messagebox.showerror("Erreur", "Tous les noms doivent être remplis.")
            return
        if len(set(noms)) != len(noms):
            messagebox.showerror("Erreur", "Les noms doivent être uniques.")
            return
        self.result = []
        for data in self.players_data:
            self.result.append({
                'nom': data['nom'].get().strip(),
                'couleur': data['couleur'].get().strip(),
                'est_ia': data['est_ia'].get(),
                'type_ia': data['type_ia'].get() if data['est_ia'].get() else None
            })
        self.dialog.destroy()
    
    def annuler(self):
        self.result = None
        self.dialog.destroy()


class AffichageGraphique:
    def __init__(self, jeu):
        self.jeu = jeu
        self.fenetre = None
        self.canvas = None
        self.label_info = None
        self.label_joueur = None
        self.label_jetons = None
        self.frame_boutons = None
        self.boutons = {}
        self.attente = None
        self.reponse = None
        self.plateau = None
        self.joueurs = None
        self.air = 0
        self.manche = 0
        self.joueur_courant = None

        self.couleurs = {
            'rouge': 'red', 'bleu': 'blue', 'vert': 'green', 'jaune': 'yellow',
            'noir': 'black', 'blanc': 'white', 'violet': 'purple', 'orange': 'orange',
            'rose': 'pink', 'gris': 'gray', 'cyan': 'cyan', 'magenta': 'magenta',
            'marron': 'brown', 'beige': 'beige'
        }

    def initialiser(self, plateau, joueurs):
        self.plateau = plateau
        self.joueurs = joueurs
        self.fenetre = tk.Tk()
        self.fenetre.title("Deep Sea Adventure")
        self.fenetre.geometry("1100x750")
        self.fenetre.minsize(800, 600)
        self.fenetre.configure(bg='darkblue')

        # Barre de menu
        menubar = tk.Menu(self.fenetre)
        self.fenetre.config(menu=menubar)
        fichier_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=fichier_menu)
        fichier_menu.add_command(label="Sauvegarder", command=self.sauvegarder_partie)
        fichier_menu.add_command(label="Recommencer", command=self.recommencer_partie)
        fichier_menu.add_separator()
        fichier_menu.add_command(label="Quitter", command=self.quitter_partie)

        # Gestion Ctrl+C
        def signal_handler(sig, frame):
            print("\nInterruption reçue, fermeture de la fenêtre...")
            self.fermer()
            raise KeyboardInterrupt
        signal.signal(signal.SIGINT, signal_handler)

        # Informations
        frame_info = tk.Frame(self.fenetre, bg='darkblue')
        frame_info.pack(fill=tk.X, padx=10, pady=5)
        self.label_info = tk.Label(frame_info, text="", font=('Arial', 14, 'bold'),
                                   bg='darkblue', fg='white')
        self.label_info.pack(side=tk.LEFT, padx=20)
        self.label_joueur = tk.Label(frame_info, text="", font=('Arial', 12),
                                     bg='darkblue', fg='white')
        self.label_joueur.pack(side=tk.LEFT, padx=20)
        self.label_jetons = tk.Label(frame_info, text="", font=('Arial', 12),
                                     bg='darkblue', fg='white')
        self.label_jetons.pack(side=tk.LEFT, padx=20)

        # Canvas redimensionnable
        self.canvas = tk.Canvas(self.fenetre, bg='lightblue', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame pour les boutons
        self.frame_boutons = tk.Frame(self.fenetre, bg='darkblue')
        self.frame_boutons.pack(pady=10)

        # Création des boutons
        self.boutons['rentrer'] = tk.Button(self.frame_boutons, text="Rentrer", bg='lightgreen', width=15,
                                            command=self.choix_rentrer)
        self.boutons['continuer'] = tk.Button(self.frame_boutons, text="Continuer", bg='lightyellow', width=15,
                                              command=self.choix_non_rentrer)
        self.boutons['ramasser'] = tk.Button(self.frame_boutons, text="Ramasser", bg='lightblue', width=15,
                                             command=self.choix_ramasser)
        self.boutons['poser'] = tk.Button(self.frame_boutons, text="Poser", bg='orange', width=15,
                                          command=self.choix_poser)
        self.boutons['rien'] = tk.Button(self.frame_boutons, text="Ne rien faire", bg='lightgray', width=15,
                                         command=self.choix_rien)

        self.fenetre.bind("<Configure>", lambda e: self.redessiner_plateau())
        self.fenetre.update()
        self.fenetre.lift()

    def redessiner_plateau(self):
        if self.plateau is not None and self.joueurs is not None:
            self.afficher_plateau(self.plateau, self.joueurs)

    def _couleur_tk(self, couleur):
        return self.couleurs.get(couleur.lower(), couleur.lower())

    def afficher_plateau(self, plateau, joueurs):
        self.plateau = plateau
        self.joueurs = joueurs
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 200 or h < 200:
            return

        colonnes = 8
        nb_cases = len(plateau.cases)
        lignes = (nb_cases + colonnes - 1) // colonnes
        espacement = 10
        largeur_case = min(80, (w - 100) // colonnes - espacement)
        hauteur_case = min(80, (h - 100) // lignes - espacement)
        if largeur_case < 30 or hauteur_case < 30:
            largeur_case = 70
            hauteur_case = 70

        # Calcul de la largeur totale du plateau
        largeur_plateau = colonnes * (largeur_case + espacement) - espacement
        # Marge horizontale pour centrer le plateau
        marge_x = max(50, (w - largeur_plateau) // 2)
        y_first = 50  # marge verticale fixe (on pourrait la centrer aussi si besoin)

        positions = []
        for i in range(nb_cases):
            ligne = i // colonnes
            col = i % colonnes
            if ligne % 2 == 0:
                x = marge_x + col * (largeur_case + espacement)
            else:
                x = marge_x + (colonnes - 1 - col) * (largeur_case + espacement)
            y = y_first + ligne * (hauteur_case + espacement)
            positions.append((x, y))

        # Sous‑marin à gauche de la première case
        x1, y1 = positions[0]
        sub_x = x1 - largeur_case - espacement
        # Si le sous‑marin dépasse à gauche, on décale tout le plateau vers la droite
        if sub_x < 0:
            decalage = -sub_x + 10
            sub_x += decalage
            new_positions = []
            for (x, y) in positions:
                new_positions.append((x + decalage, y))
            positions = new_positions
            x1, y1 = positions[0]
            sub_x = x1 - largeur_case - espacement

        # Dessiner le sous‑marin
        self.canvas.create_oval(sub_x, y1, sub_x+largeur_case, y1+hauteur_case,
                                fill='gray', outline='black', width=2)
        self.canvas.create_text(sub_x+largeur_case//2, y1+hauteur_case//2,
                                text="⚓", font=('Arial', int(largeur_case*0.4), 'bold'))
        self.canvas.create_text(sub_x+largeur_case//2, y1+hauteur_case+10,
                                text="Sous-marin", font=('Arial', 8))

        # Pions sur le sous‑marin (position -1)
        pions_sous_marin = [j for j in joueurs if j.position == -1 and not j.est_rentre]
        for idx, j in enumerate(pions_sous_marin):
            color = self._couleur_tk(j.couleur)
            dx = (idx - (len(pions_sous_marin)-1)/2) * (largeur_case*0.3)
            self.canvas.create_oval(sub_x+largeur_case//2-8+dx, y1+hauteur_case-15,
                                    sub_x+largeur_case//2+8+dx, y1+hauteur_case-5,
                                    fill=color, outline='black')
            self.canvas.create_text(sub_x+largeur_case//2+dx, y1+hauteur_case-10,
                                    text=j.nom[0].upper(), font=('Arial', int(largeur_case*0.1)), fill='white')

        # Cases et pions
        for i, (x, y) in enumerate(positions):
            jeton = plateau.cases[i]
            if jeton.type == 'ruine':
                if jeton.niveau == 1:
                    couleur = '#CD7F32'
                elif jeton.niveau == 2:
                    couleur = '#C0C0C0'
                elif jeton.niveau == 3:
                    couleur = '#FFD700'
                else:
                    couleur = '#B87333'
                texte = str(jeton.valeur)
            else:
                couleur = 'white'
                texte = ""

            self.canvas.create_rectangle(x, y, x+largeur_case, y+hauteur_case,
                                        fill=couleur, outline='black', width=2)
            if texte:
                self.canvas.create_text(x+largeur_case//2, y+hauteur_case//2,
                                        text=texte, font=('Arial', int(largeur_case*0.25), 'bold'))
            self.canvas.create_text(x+5, y+5, text=str(i+1), font=('Arial', 7), anchor='nw')

            pions_case = [j for j in joueurs if j.position == i and not j.est_rentre]
            for idx, j in enumerate(pions_case):
                color = self._couleur_tk(j.couleur)
                dx = (idx - (len(pions_case)-1)/2) * (largeur_case*0.3)
                self.canvas.create_oval(x+largeur_case//2-8+dx, y+hauteur_case-15,
                                        x+largeur_case//2+8+dx, y+hauteur_case-5,
                                        fill=color, outline='black')
                self.canvas.create_text(x+largeur_case//2+dx, y+hauteur_case-10,
                                        text=j.nom[0].upper(), font=('Arial', int(largeur_case*0.1)), fill='white')

        # Légende
        self.canvas.create_text(marge_x, y_first + lignes*(hauteur_case+espacement) + 20,
                                text="Pile = plusieurs jetons empilés (ex: P2 = 2 jetons)",
                                font=('Arial', 8), anchor='nw', fill='darkblue')
        self.label_info.config(text=f"Air: {self.air}   Manche: {self.manche}")

    def mettre_a_jour_infos(self, air, manche):
        self.air = air
        self.manche = manche
        if self.label_info:
            self.label_info.config(text=f"Air: {air}   Manche: {manche}")

    def mettre_a_jour_joueur(self, joueur):
        self.joueur_courant = joueur
        if self.label_joueur:
            self.label_joueur.config(text=f"Tour: {joueur.nom} ({joueur.couleur})")
        if self.label_jetons:
            jetons = len(joueur.jetons_tenus)
            self.label_jetons.config(text=f"Jetons tenus: {jetons}")

    def demander_choix_rentrer(self, joueur):
        self.mettre_a_jour_joueur(joueur)
        self.boutons['rentrer'].pack(side=tk.LEFT, padx=5)
        self.boutons['continuer'].pack(side=tk.LEFT, padx=5)
        self.attente = tk.BooleanVar()
        self.fenetre.wait_variable(self.attente)
        self.boutons['rentrer'].pack_forget()
        self.boutons['continuer'].pack_forget()
        return self.reponse

    def choix_rentrer(self):
        self.reponse = True
        self.attente.set(True)

    def choix_non_rentrer(self):
        self.reponse = False
        self.attente.set(True)

    def demander_action(self, joueur, actions_possibles):
        self.mettre_a_jour_joueur(joueur)
        if 'ramasser' in actions_possibles:
            self.boutons['ramasser'].pack(side=tk.LEFT, padx=5)
        if 'poser' in actions_possibles:
            self.boutons['poser'].pack(side=tk.LEFT, padx=5)
        self.boutons['rien'].pack(side=tk.LEFT, padx=5)
        self.attente = tk.BooleanVar()
        self.fenetre.wait_variable(self.attente)
        self.boutons['ramasser'].pack_forget()
        self.boutons['poser'].pack_forget()
        self.boutons['rien'].pack_forget()
        return self.reponse

    def choix_ramasser(self):
        self.reponse = 'ramasser'
        self.attente.set(True)

    def choix_poser(self):
        self.reponse = 'poser'
        self.attente.set(True)

    def choix_rien(self):
        self.reponse = 'rien'
        self.attente.set(True)

    def afficher_message(self, texte):
        messagebox.showinfo("Info", texte)

    def demander_sauvegarde(self):
        return messagebox.askyesno("Sauvegarde", "Voulez-vous sauvegarder la partie ?")

    def demander_nom_sauvegarde(self):
        return simpledialog.askstring("Sauvegarde", "Nom de la sauvegarde :", parent=self.fenetre)

    def sauvegarder_partie(self):
        nom = self.demander_nom_sauvegarde()
        if nom:
            self.jeu.sauvegarder(nom)
        else:
            messagebox.showinfo("Sauvegarde", "Sauvegarde annulée.")

    def recommencer_partie(self):
        if messagebox.askyesno("Recommencer", "Voulez-vous recommencer la partie ? (La partie actuelle sera perdue)"):
            if messagebox.askyesno("Sauvegarde", "Sauvegarder avant de recommencer ?"):
                self.sauvegarder_partie()
            self.jeu.recommencer()

    def quitter_partie(self):
        if messagebox.askyesno("Quitter", "Voulez-vous quitter la partie ?"):
            if messagebox.askyesno("Sauvegarde", "Sauvegarder avant de quitter ?"):
                self.sauvegarder_partie()
            self.fermer()
            raise KeyboardInterrupt

    def fermer(self):
        if self.fenetre:
            self.fenetre.quit()
            self.fenetre.destroy()