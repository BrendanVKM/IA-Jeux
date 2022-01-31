import numpy as np

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

GInit = np.array(Data, dtype=np.int32)
GInit = np.flip(GInit, 0).transpose()


class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score = Score
        self.Grille = Grille

    def copy(self):
        return copy.deepcopy(self)


GameInit = Game(GInit, 3, 5)


#############################################################
#
#  affichage en mode texte


def AffGrilles(G, X, Y):
    nbG, larg, haut = G.shape
    for y in range(haut - 1, -1, -1):
        for i in range(nbG):
            for x in range(larg):
                g = G[i]
                c = ' '
                if G[i, x, y] == 1: c = 'M'  # mur
                if G[i, x, y] == 2: c = 'O'  # trace
                if (X[i], Y[i]) == (x, y): c = 'X'  # joueur
                print(c, sep='', end='')
            print(" ", sep='', end='')  # espace entre les grilles
        print("")  # retour à la ligne


###########################################################
#
# simulation en parallèle des parties


# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0, 1, 0], dtype=np.int32)
dy = np.array([0, 0, 1, 0, -1], dtype=np.int32)

# scores associés à chaque déplacement
ds = np.array([0, 1, 1, 1, 1], dtype=np.int32)

Debug = True
nb = 30000  # nb de parties


def Simulate(Game):
    # on copie les datas de départ pour créer plusieurs parties en //
    G = np.tile(Game.Grille, (nb, 1, 1))
    X = np.tile(Game.PlayerX, nb)
    Y = np.tile(Game.PlayerY, nb)
    S = np.tile(Game.Score, nb)
    I = np.arange(nb)  # 0,1,2,3,4,5...
    boucle = True

    # VOTRE CODE ICI

    # X[n] += dx[R[n]]
    # Y[n] += dy[R[n]]
    # S[n] += ds[R[n]]

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

        # marque le passage de la moto
        G[I, X, Y] = 2

        # Direction :
        Choix = np.ones(nb, dtype=np.uint32) * LPossibles[I, R]

        # DEPLACEMENT
        DX = dx[Choix]
        DY = dy[Choix]

        X += DX
        Y += DY
        S += np.where(Choix != 0, 1, Choix)

        if (np.array_equal(S, SI)): boucle = False
    print("Scores : ", np.mean(S))


Simulate(GameInit)
