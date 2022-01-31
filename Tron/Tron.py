import copy
import random
import tkinter as tk

import numpy as np

#################################################################################
#
#   Données de partie

Data = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

GInit = np.array(Data, dtype=np.int8)
GInit = np.flip(GInit, 0).transpose()

LARGEUR = 13
HAUTEUR = 17


# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score = Score
        self.Grille = Grille

    def copy(self):
        return copy.deepcopy(self)


GameInit = Game(GInit, 3, 5)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L

Window = tk.Tk()
# taille de la fenetre
Window.geometry(str(largeurPix) + "x" + str(hauteurPix))
Window.title("TRON")

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

canvas = tk.Canvas(Frame0, width=largeurPix, height=hauteurPix, bg="black")
canvas.place(x=0, y=0)


#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()

    def DrawCase(x, y, coul):
        x *= L
        y *= L
        canvas.create_rectangle(x, H - y, x + L, H - y - L, fill=coul)

    # dessin des murs

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if Game.Grille[x, y] == 1:
                DrawCase(x, y, "gray")
            if Game.Grille[x, y] == 2:
                DrawCase(x, y, "cyan")

    # dessin de la moto
    DrawCase(Game.PlayerX, Game.PlayerY, "red")


def AfficheScore(Game):
    info = "SCORE : " + str(Game.Score)
    canvas.create_text(80, 13, font='Helvetica 12 bold',
                       fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA

# VOTRE CODE ICI
def PossibleMove(Game):
    grille, x, y = Game.Grille, Game.PlayerX, Game.PlayerY
    L = []
    if grille[x][y - 1] == 0:
        L.append((0, -1))
    if grille[x][y + 1] == 0:
        L.append((0, 1))
    if grille[x + 1][y] == 0:
        L.append((1, 0))
    if grille[x - 1][y] == 0:
        L.append((-1, 0))
    return L


def Play(Game):
    L = PossibleMove(Game)
    if len(L) == 0:
        return True

    CoupFuture(Game, 30000)


################################################################################

CurrentGame = GameInit.copy()


def Simulate(Game, nb):
    dx = np.array([0, -1, 0, 1, 0], dtype=np.int32)
    dy = np.array([0, 0, 1, 0, -1], dtype=np.int32)
    ds = np.array([0, 1, 1, 1, 1], dtype=np.int32)

    G = np.tile(Game.Grille, (nb, 1, 1))
    X = np.tile(Game.PlayerX, nb)
    Y = np.tile(Game.PlayerY, nb)
    S = np.tile(Game.Score, nb)
    I = np.arange(nb)
    boucle = True

    while (boucle):
        SI = np.copy(S)
        LPossibles = np.zeros((nb, 4), dtype=np.int32)
        Tailles = np.zeros(nb, dtype=np.int32)
        Vgauche = (G[I, X - 1, Y] == 0) * 1
        Vhaut = (G[I, X, Y + 1] == 0) * 1
        Vdroite = (G[I, X + 1, Y] == 0) * 1
        Vbas = (G[I, X, Y - 1] == 0) * 1
        LPossibles[I, Tailles] = Vgauche * 1
        Tailles += Vgauche
        LPossibles[I, Tailles] = Vhaut * 2
        Tailles += Vhaut
        LPossibles[I, Tailles] = Vdroite * 3
        Tailles += Vdroite
        LPossibles[I, Tailles] = Vbas * 4
        Tailles += Vbas
        Tailles[Tailles == 0] = 1
        R = np.random.randint(Tailles)

        G[I, X, Y] = 2

        Choix = np.ones(nb, dtype=np.uint32) * LPossibles[I, R]

        DX = dx[Choix]
        DY = dy[Choix]
        X += DX
        Y += DY
        S += np.where(Choix != 0, 1, Choix)
        # debug
        if (np.array_equal(S, SI)): boucle = False

    return np.mean(S)


def SimulationPartie(Game):
    imp = 1
    while imp == 1:
        x, y = Game.PlayerX, Game.PlayerY
        L = PossibleMove(Game)
        if len(L) == 0:
            return Game.Score
        choix = random.randrange(len(L))
        Game.Grille[x, y] = 2
        Game.PlayerX += L[choix][0]
        Game.PlayerY += L[choix][1]
        Game.Score += 1


def MonteCarlo(Game, NbrParties):
    Total = 0
    for i in range(NbrParties):
        Game2 = Game.copy()
        Total += SimulationPartie(Game2)
    return Total


def CoupFuture(Game, NbParties):
    L = PossibleMove(Game)
    moy = []
    x, y = Game.PlayerX, Game.PlayerY
    Game2 = Game.copy()
    for i in L:
        Game2.PlayerX += i[0]
        Game2.PlayerY += i[1]
        moy.append(Simulate(Game2, NbParties))
    ind = L[moy.index(max(moy))]
    Game.Grille[x, y] = 2
    Game.PlayerX = x + ind[0]
    Game.PlayerY = y + ind[1]
    Game.Score += 1


def Partie():
    PartieTermine = Play(CurrentGame)
    if not PartieTermine:
        Affiche(CurrentGame)

        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(1, Partie)
    else:
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(50, Partie)
Window.mainloop()
