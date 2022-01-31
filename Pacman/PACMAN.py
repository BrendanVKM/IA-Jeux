import random
import tkinter as tk
from tkinter import font as tkfont

import numpy as np


##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################

# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

def CreateArray(L):
    T = np.array(L, dtype=np.int32)
    T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
    return T


TBL = CreateArray([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

HAUTEUR = TBL.shape[1]
LARGEUR = TBL.shape[0]
HL = HAUTEUR * LARGEUR


# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
    GUM = np.zeros(TBL.shape, dtype=np.int32)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (TBL[x][y] == 0):
                GUM[x][y] = 1
    return GUM


def Balayage():
    global TBL, GUM, TB, HAUTEUR, LARGEUR, HL
    change = True
    while change == True:
        change = False
        for i in range(1, LARGEUR - 1):
            for j in range(1, HAUTEUR - 1):
                t = TB[i][j]
                if TB[i][j] == HL:
                    TB[i][j] = 1 if ((GUM[i][j - 1] == 0) or (GUM[i - 1][j] == 0) or (GUM[i + 1][j] == 0) or (
                            GUM[i][j + 1] == 0)) else TB[i][j]
                if 0 < TB[i][j] < HL:
                    TB[i][j] = min(TB[i][j - 1], TB[i - 1][j], TB[i + 1][j], TB[i][j + 1]) + 1
                change = True if t != TB[i][j] else False


def DistPG():
    global PacManPos, Ghosts, TGPC, TBL, HAUTEUR, LARGEUR, HL
    x, y = PacManPos
    change = True

    for i in range(1, LARGEUR - 1):
        for j in range(1, HAUTEUR - 1):
            if 0 <= TGPC[i][j] < 1000:
                TGPC[i][j] = HL

    while change == True:
        change = False

        for ghost in Ghosts:
            x, y = ghost[0:2]
            TGPC[x][y] = 0

        for i in range(1, LARGEUR - 1):
            for j in range(1, HAUTEUR - 1):
                t = TGPC[i][j]

                if 0 < TGPC[i][j] < 1000:
                    TGPC[i][j] = min(TGPC[i][j - 1], TGPC[i - 1][j], TGPC[i + 1][j], TGPC[i][j + 1]) + 1

                if t != TGPC[i][j] and not change:
                    change = True


GUM = PlacementsGUM()
SCORE = 0
PacManPos = [5, 5]

TB = np.where(TBL == 1, 1000, TBL)
TB = np.where(TBL == 2, 1000, TB)

Ghosts = []
Ghosts.append([LARGEUR // 2, HAUTEUR // 2, "pink", "up"])
Ghosts.append([LARGEUR // 2, HAUTEUR // 2, "orange", "up"])
Ghosts.append([LARGEUR // 2, HAUTEUR // 2, "cyan", "up"])
Ghosts.append([LARGEUR // 2, HAUTEUR // 2, "red", "up"])

TGPC = np.where(TBL == 1, 1000, TBL)

##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################


ZOOM = 40  # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR + 1) * ZOOM
screenHeight = (HAUTEUR + 2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth) + "x" + str(screenHeight))  # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False


def keydown(e):
    global PAUSE_FLAG
    if e.char == ' ':
        PAUSE_FLAG = not PAUSE_FLAG


Window.bind("<KeyPress>", keydown)

# création de la frame principale stockant plusieurs pages

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


def WindowAnim():
    MainLoop()
    Window.after(50, WindowAnim)


Window.after(100, WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas(Frame1, width=screeenWidth, height=screenHeight)
canvas.place(x=0, y=0)
canvas.configure(background='black')


#  FNT AFFICHAGE


def To(coord):
    return coord * ZOOM + ZOOM


# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [5, 10, 15, 10, 5]


def Affiche(PacmanColor, message, data1, data2):
    global anim_bouche

    def CreateCircle(x, y, r, coul):
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=coul, width=0)

    canvas.delete("all")

    # murs

    for x in range(LARGEUR - 1):
        for y in range(HAUTEUR):
            if (TBL[x][y] == 1 and TBL[x + 1][y] == 1):
                xx = To(x)
                xxx = To(x + 1)
                yy = To(y)
                canvas.create_line(xx, yy, xxx, yy, width=EPAISS, fill="blue")

    for x in range(LARGEUR):
        for y in range(HAUTEUR - 1):
            if (TBL[x][y] == 1 and TBL[x][y + 1] == 1):
                xx = To(x)
                yy = To(y)
                yyy = To(y + 1)
                canvas.create_line(xx, yy, xx, yyy, width=EPAISS, fill="blue")

    coins = ([1, 1], [1, HAUTEUR - 2], [LARGEUR - 2, 1], [LARGEUR - 2, HAUTEUR - 2])
    # pacgum
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (GUM[x][y] == 1):
                xx = To(x)
                yy = To(y)
                e = 5
                if [x, y] in coins:
                    canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill="#cc6600")
                else:
                    canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill="orange")

    # super pacgums

    # extra info
    # for x in range(LARGEUR):
    #    for y in range(HAUTEUR):
    #        xx = To(x)
    #        yy = To(y) - 11
    #        txt = data1[x][y]
    #        canvas.create_text(xx, yy, text=txt, fill="white", font=("Purisa", 8))

    # extra info 2
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x)
            yy = To(y) + 10
            txt = str(data1[x][y]) + "/" + str(data2[x][y])
            canvas.create_text(xx, yy, text=txt, fill="white", font=("Purisa", 6))

            # dessine pacman
    xx = To(PacManPos[0])
    yy = To(PacManPos[1])
    e = 20
    anim_bouche = (anim_bouche + 1) % len(animPacman)
    ouv_bouche = animPacman[anim_bouche]
    tour = 360 - 2 * ouv_bouche
    canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill=PacmanColor)
    canvas.create_polygon(xx, yy, xx + e, yy + ouv_bouche, xx + e, yy - ouv_bouche, fill="black")  # bouche

    # dessine les fantomes
    dec = -3
    for P in Ghosts:
        xx = To(P[0])
        yy = To(P[1])
        e = 16

        coul = P[2]
        # corps du fantome
        CreateCircle(dec + xx, dec + yy - e + 6, e, coul)
        canvas.create_rectangle(dec + xx - e, dec + yy - e, dec + xx + e + 1, dec + yy + e, fill=coul, width=0)

        # oeil gauche
        CreateCircle(dec + xx - 7, dec + yy - 8, 5, "white")
        CreateCircle(dec + xx - 7, dec + yy - 8, 3, "black")

        # oeil droit
        CreateCircle(dec + xx + 7, dec + yy - 8, 5, "white")
        CreateCircle(dec + xx + 7, dec + yy - 8, 3, "black")

        dec += 3

    # texte

    canvas.create_text(screeenWidth // 2, screenHeight - 50, text="PAUSE : PRESS SPACE", fill="yellow",
                       font=PoliceTexte)
    canvas.create_text(screeenWidth // 2, screenHeight - 20, text=message, fill="#421c78", font=PoliceTexte)


AfficherPage(0)

#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

CHASSE = 0


def PacManMove():
    global PacManPos, TGPC, HL, CHASSE
    i, j = PacManPos
    if 1 < CHASSE < 17:
        a, b, c, d = TGPC[i][j - 1], TGPC[i - 1][j], TGPC[i + 1][j], TGPC[i][j + 1]
        m = min(a, b, c, d)
        centre = ((8, 5), (9, 4), (9, 5), (10, 4), (10, 5), (11, 5))
        if m == a and (i, j - 1) not in centre:
            PacManPos[1] -= 1
        elif m == b and (i - 1, j) not in centre:
            PacManPos[0] -= 1
        elif m == c and (i + 1, j) not in centre:
            PacManPos[0] += 1
        elif m == d and (i, j + 1) not in centre:
            PacManPos[1] += 1
    elif TGPC[PacManPos[0]][PacManPos[1]] <= 3:
        cases = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
        maxi = 0
        best_case = None
        for case in cases:
            if 1000 > TGPC[case[0]][case[1]] >= maxi:
                maxi = TGPC[case[0]][case[1]]
                best_case = case
        PacManPos[0], PacManPos[1] = best_case[0], best_case[1]
    else:
        a, b, c, d = TB[i][j - 1], TB[i - 1][j], TB[i + 1][j], TB[i][j + 1]
        m = min(a, b, c, d)
        if m == a:
            PacManPos[1] -= 1
        elif m == b:
            PacManPos[0] -= 1
        elif m == c:
            PacManPos[0] += 1
        elif m == d:
            PacManPos[1] += 1
    TGPC[PacManPos[0]][PacManPos[1]] == HL
    CHASSE -= 1


def GhostsPossibleMove(x, y):
    L = []
    if (TBL[x][y - 1] != 1): L.append((0, -1))
    if (TBL[x][y + 1] != 1): L.append((0, 1))
    if (TBL[x + 1][y] != 1): L.append((1, 0))
    if (TBL[x - 1][y] != 1): L.append((-1, 0))
    return L


def GhostsMove():
    global Ghosts, PacManPos, TGPC
    for F in Ghosts:
        L = GhostsPossibleMove(F[0], F[1])
        if L == [(0, -1), (0, 1)] or L == [(1, 0), (-1, 0)]:
            if F[3] == "up" and (0, -1) in L:
                F[1] -= 1
            elif F[3] == "down" and (0, 1) in L:
                F[1] += 1
            elif F[3] == "left" and (-1, 0) in L:
                F[0] -= 1
            elif F[3] == "right" and (1, 0) in L:
                F[0] += 1
        else:
            choix = random.randrange(len(L))
            F[0] += L[choix][0]
            F[1] += L[choix][1]
            Lc = [L[choix][0], L[choix][1]]
            if Lc == [0, -1]:
                F[3] = "up"
            elif Lc == [0, 1]:
                F[3] = "down"
            elif Lc == [1, 0]:
                F[3] = "right"
            elif Lc == [-1, 0]:
                F[3] = "left"


def death():
    global PacManPos, Ghosts, PAUSE_FLAG, CHASSE, SCORE
    x, y = PacManPos
    for ghost in Ghosts:
        if (x, y) == (ghost[0], ghost[1]):
            if CHASSE != 0:
                SCORE += 2000
                ghost[0], ghost[1] = LARGEUR // 2, HAUTEUR // 2
            else:
                PAUSE_FLAG = not PAUSE_FLAG
            return True


def MangeGum():
    global PacManPos, GUM, SCORE, TB, HL, CHASSE, PacmanColor
    x, y = PacManPos
    if GUM[x][y] == 1:
        GUM[x][y] = 0
        SCORE += 100
        TB[x][y] = HL
        if PacManPos in ([1, 1], [1, HAUTEUR - 2], [LARGEUR - 2, 1], [LARGEUR - 2, HAUTEUR - 2]):
            CHASSE = 16
            PacManColor = "#cccc00"


def IA():
    PacManMove()
    MangeGum()
    Balayage()
    if death() == True: return
    GhostsMove()
    if death() == True: return
    DistPG()


#  Boucle principale de votre jeu appelée toutes les 500ms


def MainLoop():
    if not PAUSE_FLAG: IA()
    Affiche(PacmanColor="yellow" if CHASSE <= 1 else "#696969", message='Score : ' + str(SCORE), data1=TB, data2=TGPC)


###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()
