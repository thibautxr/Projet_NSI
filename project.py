from PyQt5.QtWidgets import *           # EN FIN DE PROJET REMPLACER LE * PAR LES FONCTIONS UTILISEES POUR OPTIMISER
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
import sqlite3
from time import *

database = "Film_realisateur_genre_nationalite.db"
print("tapez help(main) pour avoir une explication rapide de chaque fonction")

def main():
    '''
    CloseAll()          : Ferme simplement une connexion à une base de donnée, fonction créée pour gagner de la place et avoir un code plus simple à comprendre
    TableExist()        : Permet de savoir si une table existe, évite d'avoir une fatal error dans la console qui ferait crash le programme
    ReturnAllTable()    : Renvoie une liste de toute les tables qui existent dans la base de donnée
    AddRealisateur      : Ajoute graphiquement une entrée dans la table realisateur 
    AddFilm()           : Ajoute graphiquement une entrée dans la table film
    AddActeur()         : Ajoute une entrée à la table acteur
    TableActeur()       : Crée les tables xacteurfilm et acteur
    '''

def CloseAll(cur, con):
    cur.close()
    con.commit()
    con.close()


def TableExist(table):
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()
    boool = True
    try:
        curseur.execute("SELECT * FROM {}".format(table))

    except sqlite3.OperationalError:            # Si la table n'existe pas
        print("ERREUR : La table {} n'existe pas".format(table))
        a = 0
        if str(input("Voulez vous la créer ? O/N").lower()) == 'o':
            req = "CREATE TABLE {} (id_{} INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, ".format(table, table)     # Requête de base 
            print("ATTENTION : par défaut un attribut \"id_{}\" est créé en tant que clé primaire, n'eesayez pas d'ajouter une clé primaire".format(table))
            while True:
                a = str(input("Attribut suivant (nom PARAMETRES exemple : age INTEGER NOT NULL): "))
                if a == '':
                    req = req[:-2] + ");"
                    print(req)
                    curseur.execute(req)
                    break
                req = req + a + ", "
                print(req)
        boool = False

    CloseAll(curseur, connexion)
    return boool


def ReturnAllTable():
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()

    curseur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    a = curseur.fetchall()
    l = []
    cas = "(),'"
    csc = a

    for row in a:
        csc = str(row)
        for caractere in cas:
            csc = csc.replace(caractere, '')
        l.append(csc)
    CloseAll(curseur, connexion)
    return list(reversed(l))[:-1]



def AddRealisateur(self):
    self.connexion = sqlite3.connect(database)
    self.curseur = self.connexion.cursor()
    if not TableExist("nationalite"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table nationalite, relancez le programme après avoir résolu le preoblème")
        return 1
    self.curseur.execute("SELECT * FROM nationalite")
    t = self.curseur.fetchall()
    temp = ''
    for i in t:
        temp = temp + i[1] + ", "
    self.WelcomeLabel = QLabel("Veuillez ajouter un Réalisateur à la table Realisateur")
    self.layout = QVBoxLayout()
    self.layout.addWidget(QLabel("Veuillez ajouter un Réalisateur à la table Realisateur"), alignment=Qt.AlignCenter)
    self.NomLabel = QLabel("Nom du réalisateur :")
    self.NomRealisateurLine = QLineEdit("Texier")
    self.PrenomLabel = QLabel("Prénom du réalisateur :")
    self.PrenomRealisateurLine = QLineEdit("Thibaut")
    self.DdnLabel = QLabel("Date de naissance du réalisateur (aaaa:mm:jj) :")
    self.DdnRealisateurLine = QLineEdit("2006-05-06")
    self.NationaliteLabel = QLabel("Nationalité du réalisateur ({}) :".format(temp[:-2]))
    self.NationaliteRealisateurLine = QLineEdit("FR")
    self.ConfirmButton = QPushButton("Insérer")
    CloseAll(self.curseur, self.connexion)
    self.ConfirmButton.clicked.connect(self.ConfirmedReal)
    self.layout.addWidget(self.NomLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.NomRealisateurLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.PrenomLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.PrenomRealisateurLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.DdnLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.DdnRealisateurLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.NationaliteLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.NationaliteRealisateurLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.ConfirmButton, alignment=Qt.AlignCenter)

# Composition de la table film : id_film, titre_film, annee_film, id_realisateur_film, id_nationalite_film, id_genre_film
def AddFilm(self):
    self.connexion = sqlite3.connect(database)
    self.curseur = self.connexion.cursor()
    if not TableExist("nationalite"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table nationalite, relancez le programme après avoir résolu le preoblème")
        CloseAll(self.curseur, self.connexion)
        return 
    if not TableExist("genre"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table genre, relancez le programme après avoir résolu le preoblème")
        CloseAll(self.curseur, self.connexion)
        return 
    if not TableExist("realisateur"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table realisateur, relancez le programme après avoir résolu le preoblème")
        CloseAll(self.curseur, self.connexion)
        return 1
    
    self.curseur.execute("SELECT * FROM nationalite")
    print("Requête : SELECT * FROM nationalite")
    t = self.curseur.fetchall()
    temp = ''
    for i in t:
        temp = temp + i[1] + ", "
    self.WelcomeLabel = QLabel("Veuillez ajouter un Réalisateur à la table Realisateur")
    self.layout = QVBoxLayout()
    self.layout.addWidget(QLabel("Veuillez ajouter un Film à la table film"), alignment=Qt.AlignCenter)
    self.TitreLabel = QLabel("Titre du film :")
    self.TitreFilmLine = QLineEdit("Interstellar")
    self.AnneeLabel = QLabel("Année de sortie du film :")
    self.AnneeFilmLine = QLineEdit("2014")
    self.RealisateurLabel = QLabel("Nom Prenom du réalisateur :")
    self.RealisateurFilmLine = QLineEdit("Nolan Christopher")
    self.NationaliteLabel = QLabel("Nationalité du film ({}) :".format(temp[:-2]))
    self.NationaliteFilmLine = QLineEdit("US")
    self.GenreLabel = QLabel("Genre du film : ")
    self.GenreFilmLine = QLineEdit("Science-fiction")
    self.ConfirmButton = QPushButton("Insérer")
    CloseAll(self.curseur, self.connexion)
    self.ConfirmButton.clicked.connect(self.ConfirmedFilm)
    self.layout.addWidget(self.TitreLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.TitreFilmLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.AnneeLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.AnneeFilmLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.RealisateurLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.RealisateurFilmLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.NationaliteLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.NationaliteFilmLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.GenreLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.GenreFilmLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.ConfirmButton, alignment=Qt.AlignCenter)


def TableActeur():
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()
    curseur.execute("CREATE TABLE acteur (id_acteur INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, nom_acteur TEXT NOT NULL, prenom_acteur TEXT NOT NULL)")
    curseur.execute("CREATE TABLE xacteurfilm (id_xaf INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, id_acteur_xaf INTEGER NOT NULL, id_film_xaf INTEGER NOT NULL, FOREIGN KEY(id_acteur_xaf) REFERENCES film (id_film) FOREIGN KEY(id_film_xaf) REFERENCES acteur (id_acteur))")
    CloseAll(curseur, connexion)


def AddActeur():
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()

    try:
        curseur.execute("SELECT * FROM acteur")

    except sqlite3.OperationalError:
        TableActeur()

    if not TableExist("xacteurfilm"):
        CloseAll(curseur, connexion)
        #return 1

    req = 'INSERT INTO acteur (nom_acteur, prenom_acteur) VALUES (?, ?)'
    data = []
    a = ["Entrez le Nom de l'acteur : ", "Entrez le prénom de l'acteur : "]
    for i in range (len(a)):
        data.append(str(input(a[i])))
        if i == len(a) - 1:
            # Vérifier si l'entrée n'existe pas déjà
            Exists = False
            curseur.execute("SELECT * FROM acteur")
            b = curseur.fetchall()
            print(b)
            for i in range(len(b)):
                if data[0].lower() + ' ' + data[1].lower() == b[i][1].lower() + ' ' + b[i][2].lower():          # Si le nom prenom entré (en minuscule) est égal à l'un présent dans la table
                    print("Cet acteur existe déjà dans la table, son id est {}".format(b[i][0]))
                    Exists = True
            
            if not Exists:
                print(req, data)
                input()
                curseur.execute(req, data)

    CloseAll(curseur, connexion)








    



class Window(QWidget):
    def __init__(self, Title: str, X: int, Y: int):
        super().__init__()
        self.X, self.Y = X, Y
        self.setWindowTitle(Title)
        self.resize(Y, X)
        self.ActeurWasJustCreated = False 
        self.l = ReturnAllTable()
        self.lc = ReturnAllTable()
        self.layout = QVBoxLayout()
        for i in range(len(self.l)):
            self.l[i] = QPushButton(self.l[i].capitalize())
            self.layout.addWidget(self.l[i])
            self.l[i].clicked.connect(self.BoutonAppuye)
        if len(self.l) == 4:
            self.a = QPushButton("Creer les tables Acteur et XacteurFilm")
            self.layout.addWidget(self.a)
            self.a.clicked.connect(self.BoutonAppuye)
           
        
        
        self.setLayout(self.layout)

    def BoutonAppuye(self):
        sender = self.sender()
        if sender.text().lower() == "realisateur" or sender.text().lower() == "film":
            self.win = OtherWindow("Projet NSI", 450, 800, sender.text().lower())
            self.close()
            self.win.show()
        elif sender.text().lower() == "Creer les tables Acteur et XacteurFilm".lower():
            TableActeur()
            self.ActeurWasJustCreated = True
            self.close()
        elif sender.text().lower() == "genre" or sender.text().lower() == "nationalite" or "acteur" or sender.text().lower() == "xacteurfilm":
            self.win = LastWindow("Contenu de la table {}".format(sender.text().lower()), self.X, self.Y, sender.text().lower())
            self.close()
            self.win.show()
        
        else:
            self.win = OtherWindow("Projet NSI", round(self.X / 3), round(self.Y / 3), "Lorem ipsum dolor sit amet")
            self.close()
            self.win.show()








class OtherWindow(QWidget):
    def __init__(self, Title: str, X: int, Y: int, Bouton: str):
        super().__init__()
        self.setWindowTitle(Title)
        self.Y, self.X = Y, X
        self.resize(self.Y, self.X)
        self.layout = QVBoxLayout()
        if Bouton == "Lorem ipsum dolor sit amet":
            self.label = QLabel("Cette Table n'a pas été configurée")
            self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        elif Bouton == "realisateur":
            AddRealisateur(self)
            
        elif Bouton == "film":
            AddFilm(self)

        self.setLayout(self.layout)


    def ConfirmedReal(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        req = 'INSERT INTO realisateur (nom_realisateur, prenom_realisateur, ddn_realisateur, id_nationalite_realisateur) VALUES (?, ?, ?, ?)'
        data = [self.NomRealisateurLine.text(), self.PrenomRealisateurLine.text(), self.DdnRealisateurLine.text()]
        print(data)
        self.curseur.execute('SELECT * FROM nationalite')
        print("Requête : SELECT * FROM nationalite")
        b = self.curseur.fetchall()
        self.curseur.execute('SELECT * FROM realisateur')
        print("Requête : SELECT * FROM realisateur")
        d = self.curseur.fetchall()
        Exist = False
        IsFound = False
        for c in range(len(d)):
            print(data[0].lower() + ' ' + data[1].lower(), d[c][1].lower() + ' ' + d[c][2].lower(), data[0].lower() + ' ' + data[1].lower() == d[c][1].lower() + ' ' + d[c][2].lower())
            if data[0].lower() + ' ' + data[1].lower() == d[c][1].lower() + ' ' + d[c][2].lower():                  # Si le nom prenom entré (en minuscule) est égal à l'un présent dans la table realisateur
                print("Ce réalisateur existe déjà dans la table, son id est {}".format(d[c][0]))
                Exist = True
            
        for c in range(len(b)):
            if self.NationaliteRealisateurLine.text().upper() == b[c][1]:                                                                 # Si la fin du tableau data[], qui contient la nationalité, est identique à l'une des valeurs de la table nationalité (le tableau ressemble à [id, nationalite], [id, nationalite], ...)
                data.append(b[c][0])                                                                        # Alors on affecte à la fin du tableau l'id de la nationalite indiquée par l'utilisateur
                IsFound = True
                break
        if not IsFound:                                                                                             # Si la nationalite n'est pas dans la table    
            self.curseur.execute("INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(self.NationaliteRealisateurLine.text().upper()))     # Créer une nouvelle nationalité sachant que data[len(a) - 1] contient la nationalité entree par l'utilisateur
            print("Requête : INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(self.NationaliteRealisateurLine.text().upper()))
            data.append(len(b) + 1)
        if not Exist:
            print(data)
            self.curseur.execute(req, data)
            print("Requête : INSERT INTO realisateur (nom_realisateur, prenom_realisateur, ddn_realisateur, id_nationalite_realisateur) VALUES ('{}', '{}', {}, {})".format(data[0], data[1], data[2], data[3]))
        CloseAll(self.curseur, self.connexion)
        self.w = LastWindow("Contenu de la table Realisateur", self.Y, self.Y, "realisateur")
        self.close()
        self.w.show()
    



    def ConfirmedFilm(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        req = 'INSERT INTO film (titre_film, annee_film, id_realisateur_film, id_nationalite_film, id_genre_film) VALUES (?, ?, ?, ?, ?)'
        data = [self.TitreFilmLine.text(), int(self.AnneeFilmLine.text()), self.RealisateurFilmLine.text(), self.NationaliteFilmLine.text(), self.GenreFilmLine.text()]
        self.curseur.execute('SELECT * FROM nationalite')
        print("Requête : SELECT * FROM nationalite")                                                                            #       |
        b = self.curseur.fetchall()                                                                                             #       |
        IsFound = False                                                                                                         #       |
        for c in range(len(b)):                                                                                                 #       |
            if data[len(data) - 2].upper() == b[c][1]:                                                                          #       |
                data[len(data) - 2] = b[c][0]                                                                                   #       PASSER D'UNE NATIONALITE A UN ID
                IsFound = True                                                                                                  #       |
                break                                                                                                           #       |
        if not IsFound:                                                                                                         #       |
            self.curseur.execute("INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(data[len(data) - 2]))
            print("Requête : INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(data[len(data) - 2]))          #       |
            print("Cette nationalité n'était pas dans la table, elle a donc été ajoutée")
            data[len(data) - 2] = b[len(b) - 1][0] + 1
    
        self.curseur.execute('SELECT * FROM genre') 
        print("Requête : SELECT * FROM genre")                                                                      #       |
        b = self.curseur.fetchall()                                                                                      #       |
        IsFound = False                                                                                             #       |
        for c in range(len(b)):                                                                                     #       |
            if data[len(data) - 1].lower() == b[c][1].lower():                                                      #       PASSER D'UN
                data[len(data) - 1] = b[c][0]                                                                       #       GENRE A UN ID
                IsFound = True                                                                                      #       |
        if not IsFound:                                                                                             #       |
            self.curseur.execute("INSERT INTO genre (nom_genre) VALUES ('{}')".format(data[len(data) - 1]))              #       |
            print("Requête : INSERT INTO genre (nom_genre) VALUES ('{}')".format(data[len(data) - 1]))
            print("Ce genre n'était pas dans la table, il a donc été ajouté")
            data[len(data) - 1] = b[len(b) - 1][0] + 1

        self.curseur.execute("SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")
        print("Requête : SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")              #       |
        b = self.curseur.fetchall()                                                                                      #       |
        IsFound = False                                                                                             #       |
        for c in range(len(b)):                                                                                     #       |
            ConcD = b[c][1] + ' ' + b[c][2]                                                                         #       PASSER D'UN NOM/PRENOM A UN ID                                               
            if data[len(data) - 3].lower() == ConcD.lower():                                                        #       |
                data[len(data) - 3] = b[c][0]                                                                       #       |
                IsFound = True                                                                                      #       |
        if not IsFound:                                                                                             #       |
            print("Ce réalisateur n'est pas présent dans la table, vous allez être redirigé vers le programme d'ajout de réalisateur")
            CloseAll(self.curseur, self.connexion)
            self.EWin = EmergencyWindow()
            self.EWin.show()
            self.connexion = sqlite3.connect(database)
            self.curseur = self.connexion.cursor()
            self.curseur.execute("SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")
            print("Requête : SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")              #       |
            b = self.curseur.fetchall()                                                                                      #       |
            IsFound = False                                                                                             #       |
            for c in range(len(b)):                                                                                     #       |
                ConcD = b[c][1] + ' ' + b[c][2]                                                                         #       PASSER D'UN NOM/PRENOM A UN ID                                               
                if data[len(data) - 3].lower() == ConcD.lower():                                                        #       |
                    data[len(data) - 3] = b[c][0]                                                                       #       |
                    IsFound = True                                                                                      #       |
            if not IsFound:                                                                                             #       |
                print("Ce réalisateur n'est pas présent dans la table, faites attention à taper le même réalisateur dans le programme et dans la sous-programme d'ajout")
        
        self.curseur.execute("SELECT titre_film, annee_film, id_realisateur_film, id_nationalite_film, id_genre_film FROM film")
        a = self.curseur.fetchall()
        Exists = False
        for i in range(len(a)):
            if a[i][0] == data[0] and a[i][1] == data[1] and a[i][2] == data[2] and a[i][3] == data[3] and a[i][4] == data[4]:
                print("Ce film est déja dans la table, il se trouve à l'indice {} et son id est {}".format(i, a[i][0]))
                Exists = True
                break
        self.curseur.execute(req, data)    
        CloseAll(self.curseur, self.connexion)
        self.setLayout(self.layout)
        self.w = LastWindow("Contenu de la table film", self.X, self.Y, "film")
        self.close()
        self.w.show()
     




class LastWindow(QWidget):
    def __init__(self, Title: str, X: int, Y: int, Table: str):
        super().__init__()
        self.setWindowTitle(Title)
        self.resize(Y, X)
        self.layout = QVBoxLayout()
        self.label = QLabel("Contenu de la table {}".format(Table))
        self.label.setStyleSheet("color: red; font-size: 23px")
        self.layout.addWidget(self.label, alignment= Qt.AlignCenter)
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        self.curseur.execute("SELECT * FROM {}".format(Table))
        temp = self.curseur.fetchall()
        RealContent = []
        for i in temp:
            RealContent.append(i)
        for i in range(len(RealContent)):
            a = QLabel(str(RealContent[i]))
            a.setStyleSheet("font-weight: 600; word-spacing: 10px;")
            self.layout.addWidget(a, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)
        
        CloseAll(self.curseur, self.connexion)


    def ConfirmedReal(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        req = 'INSERT INTO realisateur (nom_realisateur, prenom_realisateur, ddn_realisateur, id_nationalite_realisateur) VALUES (?, ?, ?, ?)'
        data = [self.NomRealisateurLine.text(), self.PrenomRealisateurLine.text(), self.DdnRealisateurLine.text()]
        print(data)
        self.curseur.execute('SELECT * FROM nationalite')
        print("Requête : SELECT * FROM nationalite")
        b = self.curseur.fetchall()
        self.curseur.execute('SELECT * FROM realisateur')
        print("Requête : SELECT * FROM realisateur")
        d = self.curseur.fetchall()
        Exist = False
        IsFound = False
        for c in range(len(d)):
            print(data[0].lower() + ' ' + data[1].lower(), d[c][1].lower() + ' ' + d[c][2].lower(), data[0].lower() + ' ' + data[1].lower() == d[c][1].lower() + ' ' + d[c][2].lower())
            if data[0].lower() + ' ' + data[1].lower() == d[c][1].lower() + ' ' + d[c][2].lower():                  # Si le nom prenom entré (en minuscule) est égal à l'un présent dans la table realisateur
                print("Ce réalisateur existe déjà dans la table, son id est {}".format(d[c][0]))
                Exist = True
            
        for c in range(len(b)):
            if self.NationaliteRealisateurLine.text().upper() == b[c][1]:                                                                 # Si la fin du tableau data[], qui contient la nationalité, est identique à l'une des valeurs de la table nationalité (le tableau ressemble à [id, nationalite], [id, nationalite], ...)
                data.append(b[c][0])                                                                        # Alors on affecte à la fin du tableau l'id de la nationalite indiquée par l'utilisateur
                IsFound = True
                break
        if not IsFound:                                                                                             # Si la nationalite n'est pas dans la table    
            self.curseur.execute("INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(self.NationaliteRealisateurLine.text().upper()))     # Créer une nouvelle nationalité sachant que data[len(a) - 1] contient la nationalité entree par l'utilisateur
            print("Requête : INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(self.NationaliteRealisateurLine.text().upper()))
            data.append(len(b) + 1)
        if not Exist:
            print(data)
            self.curseur.execute(req, data)
            print("Requête : INSERT INTO realisateur (nom_realisateur, prenom_realisateur, ddn_realisateur, id_nationalite_realisateur) VALUES ('{}', '{}', {}, {})".format(data[0], data[1], data[2], data[3]))
        CloseAll(self.curseur, self.connexion)
        self.setLayout(self.layout)
        self.w = LastWindow("Contenu de la table Realisateur", self.Y, self.Y, "realisateur")
        self.close()
        self.w.show()


class EmergencyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajout Realisateur")
        self.Y = 800
        self.X = 450
        self.resize(450, 800)
        self.layout = QVBoxLayout()
        AddRealisateur(self)
        self.setLayout(self.layout)
        self.raise_()

'''
connexion = sqlite3.connect(database)
curseur = connexion.cursor()

curseur.execute("PRAGMA table_info({})".format("film"))
print(curseur.fetchall())

CloseAll(curseur, connexion)
input()
'''

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
win = Window("Projet NSI", 450, 800)
win.show()
app.exec()
app2 = QApplication.instance() 
if not app2:
    app2 = QApplication(sys.argv)
print(win.ActeurWasJustCreated)
if win.ActeurWasJustCreated:
    win.close()
    win2 = Window("Projet NSI", 450, 800)
    win2.show()
    app2.exec()































'''
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys

class Window(QWidget):
    def __init__(self, Title: str, X: int, Y: int):
        QWidget.__init__(self)
        self.setWindowTitle(Title)
        self.resize(Y, X)


        self.bouton1 = QPushButton("Bouton 1")
        self.bouton2 = QPushButton("Bouton 2")
        self.case = QCheckBox("CASE")
        self.label = QLabel("Voici mon premier texte avec un QLabel")
        self.champ = QLineEdit("Voici mon premier champ de texte")
        self.case.stateChanged.connect(self.caseEtat)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.bouton1)
        layout.addWidget(self.bouton2)
        layout.addWidget(self.case)
        layout.addWidget(self.champ)
        self.bouton1.clicked.connect(self.AppuiBouton)
        self.setLayout(layout)


    def mousePressEvent(self, event):
        print("CLICK SOURIS PLACE HOLDER en {}:{}".format(event.x(), event.y()))

    def AppuiBouton(self):
        print("appui sur le bouton")

    def caseEtat(self, etat):
        if etat == Qt.Checked:
            print("coche")
        else:
            print("decoche")
            self.case.setCheckState(Qt.Checked)



 
app = QApplication(sys.argv)
win = Window("Projet NSI", 450, 800)


win.show()
app.exec()
'''



'''
NOTE TRES IMPORTANTES :
- setWindowTitle(str)                           : titre de la fenetre
- resize(hauteur, largeur)                      : taille de la fenetre
- les event sont similaires à SDL
- event.x()   / event.y()                       : coordonnée de la souris
- Qlabel(str)                                   : Affiche le texte contenu dans str
- var.setStyleSheet(str)                        : applique le CSS contenu dans str à var    


- QPushButton(str)                              : crée un bouton avec les données de str écrites dessus
    - Bouton.clicked.connect(fonction)              : quand le Bouton est clické, lance la fonction             ATTENTION : ne pas mettre les () de la fonction
    - Bouton.text()                                 : Renvoie le texte affiché dans le bouton
    - Bouton.setText(str)                           : Modifie le texte du Bouton par celui contenu dans str


- QLineEdit(str)                                : Affiche une boite de texte éditable, avec str comme texte par défaut
    - text()                                        : Renvoie le Texte actuellement contenu dans un champ
    - setText(str)                                  : Modifie le Texte d'un label et le remplace par str


- QCheckBox(str)                                : Crée une case à cocher
    - Case.stateChanged.connect(fonction)           : Execute le code de la fonction quand coché/décoché    ATTENTION : ne pas mettre les () de la fonction
    - self.case.checkState()                        : Regarde si la case est cochée
        - Qt.Checked                                    : La case est cochée
    - self.case.setCheckState                       : change l'état de la case

- QVBoxLayout()                                 : Permet une mise en forme
    - .addWidget(var)                               : Ajoute un élément, pas besoin de rajouter de .show pour cet élément
    - .setLayout(var)                               : "confirme" la mise en forme
'''