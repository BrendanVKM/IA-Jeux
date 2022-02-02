import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import time

###############################################################################
# création de la fenetre principale  - ne pas toucher

LARG = 300
HAUT = 300

Window = tk.Tk()
Window.geometry(str(LARG) + "x" + str(HAUT))  # taille de la fenetre
Window.title("ESIEE - Morpion")

# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages = {}
PageActive = 0


def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame


def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()


Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0, width=LARG, height=HAUT, bg="black")
canvas.place(x=0, y=0)

#################################################################################
#
#  Parametres du jeu

Grille = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]  # attention les lignes représentent les colonnes de la grille

Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y

HAUTEUR = Grille.shape[1]
LARGEUR = Grille.shape[0]

###############################################################################
#
# gestion du joueur humain et de l'IA
score_joueur = 0
score_IA = 0
couleur = "blue"
debut_partie = False


def WIN():
    global score_joueur, score_IA, couleur
    if Grille[0][0] == 1 and Grille[0][1] == 1 and Grille[0][2] == 1:
        return True
    elif Grille[1][0] == 1 and Grille[1][1] == 1 and Grille[1][2] == 1:
        return True
    elif Grille[2][0] == 1 and Grille[2][1] == 1 and Grille[2][2] == 1:
        return True
    elif Grille[0][0] == 2 and Grille[0][1] == 2 and Grille[0][2] == 2:
        return True
    elif Grille[1][0] == 2 and Grille[1][1] == 2 and Grille[1][2] == 2:
        return True
    elif Grille[2][0] == 2 and Grille[2][1] == 2 and Grille[2][2] == 2:
        return True
    elif Grille[0][0] == 1 and Grille[1][0] == 1 and Grille[2][0] == 1:
        return True
    elif Grille[0][1] == 1 and Grille[1][1] == 1 and Grille[2][1] == 1:
        return True
    elif Grille[0][2] == 1 and Grille[1][2] == 1 and Grille[2][2] == 1:
        return True
    elif Grille[0][1] == 2 and Grille[1][1] == 2 and Grille[2][1] == 2:
        return True
    elif Grille[0][2] == 2 and Grille[1][2] == 2 and Grille[2][2] == 2:
        return True
    elif Grille[0][0] == 2 and Grille[1][0] == 2 and Grille[2][0] == 2:
        return True
    elif Grille[0][0] == 1 and Grille[1][1] == 1 and Grille[2][2] == 1:
        return True
    elif Grille[0][0] == 2 and Grille[1][1] == 2 and Grille[2][2] == 2:
        return True
    elif Grille[0][2] == 1 and Grille[1][1] == 1 and Grille[2][0] == 1:
        return True
    elif Grille[0][2] == 2 and Grille[1][1] == 2 and Grille[2][0] == 2:
        return True
    return False


def matchnul():
    global Grille, HAUTEUR, LARGEUR, couleur, vainqueur
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if Grille[x][y] == 0:
                return False
    return True


def finpartie():
    global Grille, debut_partie
    if WIN() or matchnul():
        return True
    else:
        return False


def tour_IA():
    global Grille, HAUTEUR, LARGEUR
    choix_poss = []
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if Grille[x][y] == 0:
                choix_poss.append((x, y))
    return choix_poss


def choix_IA(L):
    global Grille
    choix = random.randrange(len(L))
    Grille[L[choix][0]][L[choix][1]] = 2
    return [L[choix][0], L[choix][1]]


def Play(x, y):
    global Grille

    if Grille[x][y] == 0:
        return True
    else:
        return False


def JoueurSimuleIA():
    global Grille
    if finpartie():
        if WIN():
            return ("j", None)
        else:
            return ("p", None)
    L = tour_IA()
    results = []
    a = "j"
    for K in L:
        Grille[K[0]][K[1]] = 2
        # print(results)
        R = JoueurSimuleHumain()
        if a == "j":
            a = R[0]
            results.append((a, K))
        elif a == "p":
            if R[0] == "ia":
                a = R[0]
                results.append((a, K))
        Grille[K[0]][K[1]] = 0
    return results[-1]


def JoueurSimuleHumain():
    global Grille
    if finpartie():
        if WIN():
            return ("ia", None)
        else:
            return ("p", None)
        return results
    L = tour_IA()
    results = []
    a = "ia"
    for K in L:
        Grille[K[0]][K[1]] = 1
        # print(results)
        R = JoueurSimuleIA()
        if a == "ia":
            a = R[0]
            results.append((a, K))
        elif a == "p":
            if R[0] == "j":
                a = R[0]
                results.append((a, K))
        Grille[K[0]][K[1]] = 0
    return results[-1]


################################################################################
#
# Dessine la grille de jeu

def Dessine(PartieGagnee=False):
    ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
    canvas.delete("all")

    for i in range(4):
        canvas.create_line(i * 100, 0, i * 100, 300, fill=couleur, width="4")
        canvas.create_line(0, i * 100, 300, i * 100, fill=couleur, width="4")

    for x in range(3):
        for y in range(3):
            xc = x * 100
            yc = y * 100
            if (Grille[x][y] == 1):
                canvas.create_line(xc + 10, yc + 10, xc + 90, yc + 90, fill="red", width="4")
                canvas.create_line(xc + 90, yc + 10, xc + 10, yc + 90, fill="red", width="4")
            if (Grille[x][y] == 2):
                canvas.create_oval(xc + 10, yc + 10, xc + 90, yc + 90, outline="yellow", width="4")


####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
    global debut_partie, Grille, couleur, score_IA, score_joueur, r

    if debut_partie:
        Grille = [[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]]
        Dessine()
        debut_partie = False
        return

    Window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ((x < 0) or (x > 2) or (y < 0) or (y > 2)): return

    print("clicked at", x, y)

    if not (Play(x, y)):
        return

    Grille[x][y] = 1
    couleur = "blue"
    Dessine()
    print("Joué")

    if finpartie():
        couleur = "white"
        if WIN():
            score_joueur += 1
            couleur = "red"
        debut_partie = True
    else:
        r = JoueurSimuleIA()
        L = r[1]
        Grille[L[0]][L[1]] = 2
        if finpartie():
            couleur = "white"
            if WIN():
                score_IA += 1
                couleur = "yellow"
            debut_partie = True
        Dessine()



canvas.bind('<ButtonPress-1>', MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine()
Window.mainloop()