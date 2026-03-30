import os
import tkinter as tk
from tkinter import ttk, messagebox
import glob
from joueur import Joueur
from jeu import Jeu
from affichage_graphique import AffichageGraphique, ConfigDialog

class MenuPrincipalGraphique:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Deep Sea Adventure")
        self.fenetre.geometry("400x300")
        self.fenetre.configure(bg='darkblue')
        self.fenetre.resizable(False, False)
        
        titre = tk.Label(self.fenetre, text="Deep Sea Adventure", font=('Arial', 20, 'bold'),
                         bg='darkblue', fg='white')
        titre.pack(pady=20)
        
        btn_nouvelle = tk.Button(self.fenetre, text="Nouvelle partie", width=25,
                                 command=self.nouvelle_partie)
        btn_nouvelle.pack(pady=5)
        
        btn_charger = tk.Button(self.fenetre, text="Charger une sauvegarde", width=25,
                                command=self.charger_partie)
        btn_charger.pack(pady=5)
        
        btn_supprimer = tk.Button(self.fenetre, text="Supprimer une sauvegarde", width=25,
                                  command=self.supprimer_sauvegarde)
        btn_supprimer.pack(pady=5)
        
        btn_quitter = tk.Button(self.fenetre, text="Quitter", width=25,
                                command=self.quitter)
        btn_quitter.pack(pady=5)
        
        self.fenetre.mainloop()
    
    def nouvelle_partie(self):
        # Utiliser la fenêtre principale comme parent
        config = ConfigDialog(self.fenetre)
        if config.result is None:
            return
        self.fenetre.destroy()
        joueurs = []
        for p in config.result:
            joueurs.append(Joueur(p['nom'], p['couleur'], p['est_ia'], p['type_ia']))
        jeu = Jeu(joueurs)
        aff = AffichageGraphique(jeu)
        jeu.affichage = aff
        aff.initialiser(jeu.plateau, jeu.joueurs)
        jeu.lancer_partie()
        MenuPrincipalGraphique()
    
    def charger_partie(self):
        saves = glob.glob("saves/*.pkl")
        if not saves:
            messagebox.showinfo("Info", "Aucune sauvegarde trouvée.")
            return
        select = tk.Toplevel(self.fenetre)
        select.title("Charger une sauvegarde")
        select.geometry("300x200")
        tk.Label(select, text="Choisissez une sauvegarde:").pack(pady=10)
        listbox = tk.Listbox(select)
        for f in saves:
            listbox.insert(tk.END, os.path.basename(f))
        listbox.pack(pady=5)
        def charger():
            selection = listbox.curselection()
            if selection:
                fichier = saves[selection[0]]
                select.destroy()
                self.fenetre.destroy()
                jeu = Jeu.charger(fichier)
                if jeu:
                    aff = AffichageGraphique(jeu)
                    jeu.affichage = aff
                    aff.initialiser(jeu.plateau, jeu.joueurs)
                    jeu.lancer_partie()
                MenuPrincipalGraphique()
            else:
                messagebox.showwarning("Attention", "Veuillez sélectionner une sauvegarde.")
        btn_charger = tk.Button(select, text="Charger", command=charger)
        btn_charger.pack(pady=10)
        btn_annuler = tk.Button(select, text="Annuler", command=select.destroy)
        btn_annuler.pack()
    
    def supprimer_sauvegarde(self):
        saves = glob.glob("saves/*.pkl")
        if not saves:
            messagebox.showinfo("Info", "Aucune sauvegarde à supprimer.")
            return
        select = tk.Toplevel(self.fenetre)
        select.title("Supprimer une sauvegarde")
        select.geometry("300x200")
        tk.Label(select, text="Choisissez une sauvegarde à supprimer:").pack(pady=10)
        listbox = tk.Listbox(select)
        for f in saves:
            listbox.insert(tk.END, os.path.basename(f))
        listbox.pack(pady=5)
        def supprimer():
            selection = listbox.curselection()
            if selection:
                fichier = saves[selection[0]]
                if messagebox.askyesno("Confirmation", f"Supprimer {os.path.basename(fichier)} ?"):
                    os.remove(fichier)
                    messagebox.showinfo("Succès", "Sauvegarde supprimée.")
                    select.destroy()
            else:
                messagebox.showwarning("Attention", "Veuillez sélectionner une sauvegarde.")
        btn_supprimer = tk.Button(select, text="Supprimer", command=supprimer)
        btn_supprimer.pack(pady=10)
        btn_annuler = tk.Button(select, text="Annuler", command=select.destroy)
        btn_annuler.pack()
    
    def quitter(self):
        self.fenetre.quit()
        self.fenetre.destroy()

def menu_principal():
    mode = input("Choisissez le mode d'affichage (console/graphique) : ").lower()
    while mode not in ['console', 'graphique']:
        mode = input("Choix invalide. Entrez 'console' ou 'graphique' : ")
    if mode == 'console':
        # Menu console (code inchangé, identique à celui fourni précédemment)
        while True:
            print("\n=== Deep Sea Adventure ===")
            print("1. Nouvelle partie")
            print("2. Charger une sauvegarde")
            print("3. Supprimer une sauvegarde")
            print("4. Quitter")
            choix = input("Votre choix : ")
            if choix == '1':
                nb_joueurs = int(input("Nombre de joueurs (2-6) : "))
                joueurs = []
                for i in range(nb_joueurs):
                    nom = input(f"Nom du joueur {i+1} : ")
                    couleur = input("Couleur : ")
                    est_ia = input("IA ? (o/n) : ").lower() == 'o'
                    type_ia = None
                    if est_ia:
                        print("Types : aleatoire, prudente, courageuse")
                        type_ia = input("Choisir : ").strip().lower()
                    joueurs.append(Joueur(nom, couleur, est_ia, type_ia))
                jeu = Jeu(joueurs)
                jeu.lancer_partie()
            elif choix == '2':
                saves = glob.glob("saves/*.pkl")
                if not saves:
                    print("Aucune sauvegarde trouvée.")
                    continue
                print("\nSauvegardes disponibles :")
                for i, f in enumerate(saves):
                    print(f"{i+1}. {os.path.basename(f)}")
                try:
                    idx = int(input("Numéro de la sauvegarde : ")) - 1
                    if 0 <= idx < len(saves):
                        fichier = saves[idx]
                        jeu = Jeu.charger(fichier)
                        if jeu:
                            jeu.lancer_partie()
                    else:
                        print("Numéro invalide.")
                except ValueError:
                    print("Entrée invalide.")
            elif choix == '3':
                saves = glob.glob("saves/*.pkl")
                if not saves:
                    print("Aucune sauvegarde à supprimer.")
                    continue
                print("\nSauvegardes disponibles :")
                for i, f in enumerate(saves):
                    print(f"{i+1}. {os.path.basename(f)}")
                try:
                    idx = int(input("Numéro de la sauvegarde à supprimer : ")) - 1
                    if 0 <= idx < len(saves):
                        os.remove(saves[idx])
                        print("Sauvegarde supprimée.")
                    else:
                        print("Numéro invalide.")
                except ValueError:
                    print("Entrée invalide.")
            elif choix == '4':
                print("Au revoir !")
                break
            else:
                print("Choix invalide.")
    else:
        # Créer le dossier saves s'il n'existe pas
        os.makedirs("saves", exist_ok=True)
        MenuPrincipalGraphique()

if __name__ == "__main__":
    menu_principal()