# Deep Sea Adventure

Implémentation en Python du jeu de société **Deep Sea Adventure** (Oink Games). Le jeu se joue de 2 à 6 joueurs qui explorent les fonds marins pour ramener le plus de trésors, tout en gérant une réserve d'air commune.

## Fonctionnalités

- **Moteur de jeu complet** – Respecte les règles officielles :
  - 32 jetons ruines (4 niveaux, valeurs 0 à 15)
  - Plateau en serpent pour une meilleure lisibilité
  - Réduction d'air en fonction des trésors tenus
  - Déplacement avec saut par‑dessus les autres pions
  - Actions : ramasser, poser, ne rien faire
  - Fin de manche : comptage des points et perte des trésors (empilement par 3)
- **Deux modes d'affichage** :
  - Console (affichage ASCII)
  - Graphique (Tkinter) avec fond marin, cases colorées, pions avec initiales
- **Intelligences artificielles** (3 comportements) :
  - Aléatoire
  - Prudente
  - Courageuse
- **Sauvegarde / Chargement** :
  - Nombreuses sauvegardes possibles (nom personnalisé)
  - Dossier `saves/` automatique
  - Chargement depuis le menu principal
- **Recommencer une partie** avec les mêmes paramètres (menu Fichier)
- **Interruption** par `Ctrl+C` (avec sauvegarde optionnelle)
- **Tests unitaires** avec `unittest`

## Prérequis

- Python 3.8 ou supérieur
- Aucune bibliothèque externe nécessaire (Tkinter est inclus avec Python)

## Installation

Clonez le dépôt et placez‑vous dans le dossier :
```bash
git clone https://github.com/Daniele-Nana/deep-sea-adventure.git
cd deep-sea-adventure
```

## Lancement du jeu
```bash
python main.py
```

Vous serez invité à choisir le mode d'affichage (console / graphique).
En mode graphique, un menu principal s'affiche avec les options : nouvelle partie, charger une sauvegarde, supprimer une sauvegarde, quitter.

### Mode console
Les saisies se font au clavier, les informations sont affichées en texte.

### Mode graphique
La fenêtre est redimensionnable et le plateau s'adapte.

Les actions sont choisies via des boutons.

Barre de menu pour sauvegarder, recommencer ou quitter.

## Comment jouer

Choisissez le nombre de joueurs (2 à 6) et leurs caractéristiques (nom, couleur, IA ou humain).

**Déroulement d'une manche :**

Chaque joueur joue à son tour.

L'air diminue du nombre de trésors que vous tenez.

Vous pouvez choisir de faire demi‑tour (rentrer) ou continuer.

Lancez les deux dés, soustrayez vos trésors tenus, avancez.

Arrêtez‑vous sur une case et choisissez une action.

**Actions possibles :**

- Ramasser un trésor (la case devient blanche).
- Poser un trésor (sur une case blanche).
- Ne rien faire.

**Fin de la manche :**

Les joueurs rentrés marquent les points de leurs trésors.

Les autres laissent tomber leurs trésors : ils sont empilés par 3 sur les cases blanches.

Les blancs sont retirés, le plateau se tasse.

Après 3 manches, le joueur avec le plus de points gagne.

## Structure du code
```text
deep-sea-adventure/
├── main.py                 # point d'entrée (menu principal)
├── jeu.py                  # classe principale du jeu
├── plateau.py              # gestion du plateau (32 cases)
├── joueur.py               # classe Joueur
├── jeton.py                # classe Jeton (ruine, blanc, pile)
├── ia.py                   # classes d'IA
├── de.py                   # classe Dé
├── affichage_console.py    # affichage en mode texte
├── affichage_graphique.py  # affichage Tkinter (ConfigDialog + fenêtre de jeu)
├── tests/                  # tests unitaires
└── saves/                  # dossier des sauvegardes (créé automatiquement)
```

## Tests

Exécutez les tests unitaires avec :
```bash
python -m unittest discover tests
```

## Crédits

Jeu original : Deep Sea Adventure – Oink Games

Implémentation Python : Daniele Nana
