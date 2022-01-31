import random
import tkinter as tk

import numpy as np

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


###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI


def win():
    dd = 0
    dg = 0
    for i in range(len(Grille)):
        if np.array_equal(Grille[i, :], np.ones(3)): return 1
        if np.array_equal(Grille[:, i
                          ], np.ones(3)): return 1
        if Grille[i][i] == 1: dd += 1
        if Grille[len(Grille) - 1 - i][i] == 1: dg += 1
    if dg == 3: return 1
    if dd == 3: return 1

    dd = 0
    dg = 0
    for i in range(len(Grille)):
        if np.array_equal(Grille[i, :], np.full(3, 2)): return 2
        if np.array_equal(Grille[:, i
                          ], np.full(3, 2)): return 2
        if Grille[i][i] == 2: dd += 1
        if Grille[len(Grille) - 1 - i][i] == 2: dg += 1
    if dg == 3: return 2
    if dd == 3: return 2

    if np.array_equal(np.where(Grille == 2, 1, Grille), np.ones(Grille.shape)):
        return 3
    return 0


def PlayP(x, y):
    Grille[x][y] = 1
    Dessine()


def PlayIA():
    global Grille
    x = random.randrange(len(Grille))
    y = random.randrange(len(Grille))
    while Grille[x][y] == 1 or Grille[x][y] == 2:
        x = random.randrange(len(Grille))
        y = random.randrange(len(Grille))
    Grille[x][y] = 2
    Dessine()


################################################################################
#    
# Dessine la grille de jeu

def Dessine(PartieGagnee=0):
    ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
    canvas.delete("all")
    color = "blue"
    if PartieGagnee == 1:
        color = "red"
    elif PartieGagnee == 2:
        color = "yellow"
    elif PartieGagnee == 3:
        color = "white"

    for i in range(4):
        canvas.create_line(i * 100, 0, i * 100, 300, fill=color, width="4")
        canvas.create_line(0, i * 100, 300, i * 100, fill=color, width="4")

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
Begin = True


def MouseClick(event):
    global Begin, Grille
    if Begin == True:
        Grille = np.zeros((3, 3))
        Dessine()
        Begin = False
    Window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ((x < 0) or (x > 2) or (y < 0) or (y > 2)): return
    if Grille[x][y] == 1 or Grille[x][y] == 2: return
    PlayP(x, y)  # gestion du joueur humain
    if win() == 1:
        Begin = True
        Dessine((win()))
    else:
        PlayIA()
        if win() == 2:
            Begin = True
            Dessine(win())


canvas.bind('<ButtonPress-1>', MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine()
Window.mainloop()
