import copy
import numpy as np
import random
import time
import tkinter as tk

#################################################################################
#
#   Données de partie

Data = [[8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]


class Tetromino:
    def __init__(self, Tetro=None):
        I = [[1, 1, 1, 1]]
        O = [[2, 2],
             [2, 2]]
        T = [[3, 3, 3],
             [0, 3, 0]]
        J = [[4, 4, 4],
             [0, 0, 4]]
        L = [[5, 5, 5],
             [5, 0, 0]]
        S = [[0, 6, 6],
             [6, 6, 0]]
        Z = [[7, 7, 0],
             [0, 7, 7]]
        if Tetro == 'I':
            self.form = I
        elif Tetro == 'O':
            self.form = O
        elif Tetro == 'T':
            self.form = T
        elif Tetro == 'J':
            self.form = J
        elif Tetro == 'L':
            self.form = L
        elif Tetro == 'S':
            self.form = S
        elif Tetro == 'Z':
            self.form = Z
        else:
            self.__init__(random.choice(['I', 'O', 'T', 'J', 'L', 'S', 'Z']))
        self.x0, self.x1 = 12 // 2 - len(self.form) + 1, 12 // 2 + 1
        self.y0, self.y1 = 22 - len(self.form[0]) - 1, 22 - 1

    def rotate(self):
        self.form = np.flip(self.form, 0).transpose()
        x2, y2 = (self.x0 + self.x1) // 2, (self.y0 + self.y1) // 2
        l0, l1 = len(self.form) // 2, len(self.form[0]) // 2
        self.x0, self.x1 = x2 - len(self.form) + 1, x2 + 1
        self.y0, self.y1 = y2 - len(self.form[0]) - 1, y2 - 1

    def left(self):
        self.x0 -= 1
        self.x1 -= 1

    def right(self):
        self.x0 += 1
        self.x1 += 1


GInit = np.array(Data, dtype=np.int8)
GInit = np.flip(GInit, 0).transpose()
LARGEUR = 12
HAUTEUR = 21


# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, Score=0):
        self.Score = Score
        self.Grille = Grille

    def copy(self):
        return copy.deepcopy(self)


GameInit = Game(GInit)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L

Window = tk.Tk()
# taille de la fenetre
Window.geometry(str(largeurPix) + "x" + str(hauteurPix))
Window.title("Tetris")

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
            if Game.Grille[x, y] == 8:
                DrawCase(x, y, "gray")
            if Game.Grille[x, y] == 1:
                DrawCase(x, y, "#00ffff")
            if Game.Grille[x, y] == 2:
                DrawCase(x, y, "#ffff00")
            if Game.Grille[x, y] == 3:
                DrawCase(x, y, "#800080")
            if Game.Grille[x, y] == 4:
                DrawCase(x, y, "#0000ff")
            if Game.Grille[x, y] == 5:
                DrawCase(x, y, "#ff7f00")
            if Game.Grille[x, y] == 6:
                DrawCase(x, y, "#00ff00")
            if Game.Grille[x, y] == 7:
                DrawCase(x, y, "#ff0000")

    # dessin de la moto


def AfficheScore(Game):
    info = "SCORE : " + str(Game.Score)
    canvas.create_text(80, 13, font='Helvetica 12 bold',
                       fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA

# VOTRE CODE ICI


def Play(Game, tetro):
    x0, x1 = tetro.x0, tetro.x1
    y0, y1 = tetro.y0, tetro.y1
    if y0 == 1:
        return True
    Game.Grille[x0:x1, y0:y1] = np.zeros(np.shape(tetro.form))
    y0 -= 1
    y1 -= 1
    Game.Grille[x0:x1, y0:y1] = tetro.form
    tetro.y0 -= 1
    tetro.y1 -= 1
    Play(Game, tetro)


################################################################################

CurrentGame = GameInit.copy()


def Line(Game):
    pass


tetro = Tetromino()


def Partie():
    PartieTermine = Play(CurrentGame, tetro)
    if not PartieTermine:
        Affiche(CurrentGame)

        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(500, Partie)
    else:
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(50, Partie)
Window.mainloop()
