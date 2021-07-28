import random
from tkinter import *

# TRAITEMENT DU FICHIER NOEUDS.CSV
fichier_noeuds = 'Noeuds.csv'

# PRAMETRES DEPENDANT DU FICHIER EN ENTREE

LesNoeuds = open(fichier_noeuds, "r")
# format du fichier : numero du noeud \t coord x \t coord y \n
tousLesNoeuds = LesNoeuds.readlines()
LesNoeuds.close()

NbSommets = len(tousLesNoeuds)

########################################################
# Variables
########################################################
# On initialise les listes a vide
X = []
Y = []
MovesAvailable = [i for i in range(25)]
EtatsNoeuds = ['Grey' for i in range(NbSommets)]
EtatsNoeuds[25], EtatsNoeuds[27] = 'White', 'White'
EtatsNoeuds[26], EtatsNoeuds[28] = 'Black', 'Black'
Case = [24]

minX = 1
maxX = 100
minY = 1
maxY = 100

IsGameFinished = False

for un_noeud in tousLesNoeuds:
    un_noeud.strip("\n")
    ce_noeud = un_noeud.split()

    # print(ce_noeud)
    x = int(ce_noeud[1])
    y = int(ce_noeud[2])

    X.append(x)
    Y.append(y)

    if (minY > y): minY = y
    if (maxY < y): maxY = y
    if (minX > x): minX = x
    if (maxX < x): maxX = x

# TRAITEMENT DU FICHIER NOEUDS.CSV
fichier_arcs = 'Arcs.csv'

# PRAMETRES DEPENDANT DU FICHIER EN ENTREE

LesArcs = open(fichier_arcs, "r")
# format du fichier : numero d'un noeud de l'arc \t l'autre noeud (le graphe est non orienté alors il n'y a pas d'orig ou de dest)
tousLesArcs = LesArcs.readlines()
LesArcs.close()

NbArcs = len(tousLesArcs)

Origine = []
Destination = []
EtatsArcs = ['Grey' for i in range(NbArcs)]

Succ = [[] for i in range(NbSommets)]

for un_arc in tousLesArcs:
    un_arc.strip("\n")
    cet_arc = un_arc.split()

    Orig = int(cet_arc[0])
    Origine.append(Orig)

    Dest = int(cet_arc[1])
    Destination.append(Dest)

for u in range(0, len(Origine)):
    orig = Origine[u]
    dest = Destination[u]
    Succ[orig].append(dest)
    # orig = Destination[u]
    # dest = Origin[u]
    Succ[dest].append(orig)

########################################################
# Dessin du graphe
########################################################

print('*****************************************')
print('* Dessin du graphe                      *')
print('*****************************************')


def cercle(x, y, r, couleur):
    return can.create_oval(x - r, y - r, x + r, y + r, outline=couleur, fill=couleur)


def TraceCercle(j, couleur, rayon):
    x = (X[j] - minX) * ratioWidth + border
    y = ((Y[j] - minY) * ratioHeight) + border
    y = winHeight - y
    return cercle(x, y, rayon, couleur)


def TraceSegment(i, j, colour):
    # Coordonnees de i
    x1 = (X[i] - minX) * ratioWidth + border
    y1 = ((Y[i] - minY) * ratioHeight) + border
    y1 = winHeight - y1

    # Coordonnees de j
    x2 = (X[j] - minX) * ratioWidth + border
    y2 = ((Y[j] - minY) * ratioHeight) + border
    y2 = winHeight - y2

    can.create_line(x1, y1, x2, y2, fill=colour)


########################################################
# Initialisation de la fenetre
########################################################

fen = Tk()
fen.title('Graphe')
coul = "dark green"  # ['purple','cyan','maroon','green','red','blue','orange','yellow']

Delta_Long = maxX - minX
Delta_Lat = maxY - minY
border = 20  # taille en px des bords
winWidth_int = 500
winWidth = winWidth_int + 2 * border  # largeur de la fenetre
winHeight_int = 500
winHeight = winHeight_int + 2 * border  # hauteur de la fenetre : recalculee en fonction de la taille du graphe
# ratio= 1.0          # rapport taille graphe / taille fenetre
ratioWidth = winWidth_int / (maxX - minX)  # rapport largeur graphe/ largeur de la fenetre
ratioHeight = winHeight_int / (maxY - minY)  # rapport hauteur du graphe hauteur de la fenetre

can = Canvas(fen, width=winWidth, height=winHeight, bg='dark grey')
can.pack(padx=5, pady=5)

#  cercles
rayon = 20  # rayon pour dessin des sommets
rayon_od = 5  # rayon pour sommet origine et destination
# Affichage de tous les sommets
for i in range(NbSommets - 4):
    Case.append(TraceCercle(i, 'grey', rayon))
CercleNoirHautDroite = TraceCercle(26, 'black', rayon)
CercleNoirBasGauche = TraceCercle(28, 'black', rayon)
CercleBlancBasDroite = TraceCercle(25, 'white', rayon)
CercleBlancHautGauche = TraceCercle(27, 'white', rayon)


# for i in range(NbArcs):
#     TraceSegment(Origine[i], Destination[i], 'grey')


########################################################
# Methode utilisees lors de la partie
########################################################

def changeState(i, colour):
    xNoeud, yNoeud = X[i], Y[i]
    # print("x : ", xNoeud, " y : ", yNoeud)
    # case = yNoeud * 5 + xNoeud
    # print("Case : ", i, "Pos en x : ", xNoeud, " et Pos en y : ", yNoeud)
    # On mofidi l'aspect graphique du sommet
    # print('Objet n° : ', TraceCercle(i, colour, rayon))
    TraceCercle(i, colour, rayon)
    # Mais il faut aussi changer l'etat du sommet
    EtatsNoeuds[i] = colour

    # On doit maintenant verifier l'etat de l'arc entre les deux sommets
    checkStateArcs()

    # On le retire des coups disponible
    MovesAvailable.remove(i)
    # print('Moves played : ', i)
    # print('Moves available : ', MovesAvailable)

    # Il faut verifier si le coup a ete gagnant
    result = checkGameWinnedByWhite()
    if (result == True):
        can.itemconfig(text1, text="White wins !")
        IsGameFinished = True
        print('IsGameFinished : ', IsGameFinished)

    # S'il n'est pas gagnant l'IA joue derriere
    else:
        # L'ia doit jouer
        IAPlay()
        result = checkGameWinnedByBlack()

        if (result == True):
            can.itemconfig(text1, text='Black wins !')
            IsGameFinished = True
            print('IsGameFinished : ', IsGameFinished)


def checkStateArcs():
    for arc in range(NbArcs):
        # print('Origine : ', Origine[arc], ' et destination : ', Destination[arc])
        if (EtatsNoeuds[Origine[arc]] == EtatsNoeuds[Destination[arc]] and EtatsNoeuds[Destination[arc]] == 'White'
                or EtatsNoeuds[Origine[arc]] == EtatsNoeuds[Destination[arc]] and EtatsNoeuds[
                    Destination[arc]] == 'Black'):
            TraceSegment(Origine[arc], Destination[arc], EtatsNoeuds[Origine[arc]])
            # print('Etat identique')
        # else:
        # print('Etat diff')


def checkGameWinnedByWhite():
    liste_sommets = [27]
    marque = [0 for j in range(NbSommets)]

    Dans_Pile = [0 for j in range(NbSommets)]
    Dans_Pile[27] = 1

    while liste_sommets:
        k = liste_sommets[0]
        liste_sommets.pop(0)
        if (k == 25):
            # print('Finish')
            # break
            return True
        # print(k)
        marque[k] = 1

        for l in Succ[k]:
            if not Dans_Pile[l] and not marque[l] and EtatsNoeuds[l] == 'White':
                liste_sommets.append(l)
                Dans_Pile[l] = 1


def checkGameWinnedByBlack():
    liste_sommets = [28]
    marque = [0 for j in range(NbSommets)]

    Dans_Pile = [0 for j in range(NbSommets)]
    Dans_Pile[28] = 1

    while liste_sommets:
        k = liste_sommets[0]
        liste_sommets.pop(0)
        if (k == 26):
            # print('Finish')
            # break
            return True
        # print(k)
        marque[k] = 1

        for l in Succ[k]:
            if not Dans_Pile[l] and not marque[l] and EtatsNoeuds[l] == 'Black':
                liste_sommets.append(l)
                Dans_Pile[l] = 1


def IAPlay():
    # print('Nombre de coups dispo : ', len(MovesAvailable))
    random.shuffle(MovesAvailable)
    moveNotPlayed = True
    # print(EtatsNoeuds[moves[0]])
    i = 0
    while moveNotPlayed:

        if EtatsNoeuds[MovesAvailable[i]] == 'Grey':
            # print('After IA played, ', MovesAvailable[i], '. Their is ', len(MovesAvailable) - 1,
            #       ' : Move(s) available')
            MovePlayedByIAText = 'Move played by IA is : ' + str(MovesAvailable[i])
            can.itemconfig(text1, text=MovePlayedByIAText)
            moveNotPlayed = False
            TraceCercle(MovesAvailable[i], 'Black', rayon)
            EtatsNoeuds[MovesAvailable[i]] = 'Black'
            MovesAvailable.pop(i)
            checkStateArcs()
            # print('Pop moves : ', i)
            # MovesAvailable.pop(i)

        i = + 1

        # else:
        #     print(moves[i], ' : Move unvailable')


def clicOnCase(event):
    if not IsGameFinished:
        print('IsGameFinished :', IsGameFinished)
        clic = event.x, event.y
        case = can.find_closest(*clic)
        # print('Object n° : ',case[0])
        # can.delete(case[0])
        # can.itemconfig(clic[0])
        changeState(case[0] - 1, 'White')
    else:
        print('Cannot')



can.bind("<Button-1>", clicOnCase)

# print(EtatsNoeuds)
# changeState(0, 'White')
# changeState(24, 'Black')
# changeState(23, 'Black')
# print(EtatsNoeuds)


text1 = can.create_text(20, 30, font=("Purisa", 24), text="It is your turn to play", anchor="w")

# can.itemconfigure(text1, text="New")
# print(text1)

# text = Text(fen, width=40, height=1)
# text.insert(END, "Quelle case voulez vous jouer ? ")
# text.pack()
# entryX = Entry(fen, width = 20)
# entryX.pack()
# entryY = Entry(fen, width = 20)
# entryY.pack()
#
# Button(fen, text="Envoyer",command=button_command).pack()

# print(X)

# print(Succ)
fen.mainloop()
