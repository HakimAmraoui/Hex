import math, bisect
from tkinter import *

# TRAITEMENT DU FICHIER NOEUDS.CSV
fichier_noeuds = 'Noeuds.csv'

# PRAMETRES DEPENDANT DU FICHIER EN ENTREE

LesNoeuds = open(fichier_noeuds, "r")
# format du fichier : numero du noeud \t coord x \t coord y \n
tousLesNoeuds = LesNoeuds.readlines()
LesNoeuds.close()


# On initialise les listes a vide
X = []
Y = []

minX = 1
maxX = 100
minY = 1
maxY = 100


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

# NbSommets = max(max(Origine), max(Destination)) + 1
NbSommets = len(tousLesNoeuds)

# TRAITEMENT DU FICHIER NOEUDS.CSV
fichier_arcs = 'Arcs.csv'

# PRAMETRES DEPENDANT DU FICHIER EN ENTREE

LesArcs = open(fichier_arcs, "r")
# format du fichier : numero d'un noeud de l'arc avec l'autre noeud (le graphe est non orienté alors il n'y a pas d'orig ou de dest)
tousLesArcs = LesArcs.readlines()
LesArcs.close()

########################################################
# Dessin du graphe
########################################################

print('*****************************************')
print('* Dessin du graphe                      *')
print('*****************************************')


def cercle(x, y, r, couleur):
    can.create_oval(x - r, y - r, x + r, y + r, outline=couleur, fill=couleur)


def TraceCercle(j, couleur, rayon):
    x = (X[j] - minX) * ratioWidth + border
    y = ((Y[j] - minY) * ratioHeight) + border
    y = winHeight - y
    cercle(x, y, rayon, couleur)

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
    TraceCercle(i, 'grey', rayon)
TraceCercle(26, 'black', rayon)
TraceCercle(28, 'black', rayon)
TraceCercle(25, 'white', rayon)
TraceCercle(27, 'white', rayon)




def change_color_to_white(x, y):
    print("x : ", x, " y : ", y)
    case = y * 5 + x
    print("Case : ", case ,"Pos en x : ", X[case], " et Pos en y : ", Y[case])
    TraceCercle(case,"white",rayon)
#
# def button_command():
#     text = entryX.get()
#     print(text)
# entryX = Entry(fen, width = 20)
# entryX.pack()
# entryY = Entry(fen, width = 20)
# entryY.pack()
#
# Button(fen, text="Envoyer",command=button_command).pack()

# print(X)

fen.mainloop()

