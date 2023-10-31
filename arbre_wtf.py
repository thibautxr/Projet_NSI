from PyQt5.QtWidgets import *           # EN FIN DE PROJET REMPLACER LE * PAR LES FONCTIONS UTILISEES POUR OPTIMISER
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
import sqlite3
from time import *

database = "Film_realisateur_genre_nationalite.db"
print("j'ai eu ça sans faire exprès et vu que je trouve ça un peu goleri je l'ai mis la")

def main():
    '''
    CloseAll()                  : Ferme simplement une connexion à une base de donnée, fonction créée pour gagner de la place et avoir un code plus simple à comprendre
    TableExist()                : Permet de savoir si une table existe, évite d'avoir une fatal error dans la console qui ferait crash le programme
    ReturnAllTable()            : Renvoie une liste de toute les tables qui existent dans la base de donnée
    ReturnContentTable(table)   : Renvoie une liste de la composition d'une table
    AddRealisateur              : Ajoute graphiquement une entrée dans la table realisateur 
    AddFilm()                   : Ajoute graphiquement une entrée dans la table film
    AddActeur()                 : Ajoute une entrée à la table acteur
    TableActeur()               : Crée les tables xacteurfilm et acteur
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
        boool = False

    CloseAll(curseur, connexion)
    return boool
def ReturnAllTable():
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()

    curseur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Requête : SELECT name FROM sqlite_master WHERE type='table';")
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
def ReturnContentTable(table):
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()
    curseur.execute("PRAGMA table_info({})".format(table))
    print("Requête : PRAGMA table_info({})".format(table))
    ProprieteTable = curseur.fetchall()
    ContentTable = []
    for i in range(len(ProprieteTable)):
        ContentTable.append(ProprieteTable[i][1])
    print(ContentTable)
    CloseAll(curseur, connexion)
    return ContentTable
def TableActeur():
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()
    curseur.execute("CREATE TABLE acteur (id_acteur INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, nom_acteur TEXT NOT NULL, prenom_acteur TEXT NOT NULL)")
    curseur.execute("CREATE TABLE xacteurfilm (id_xaf INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, id_acteur_xaf INTEGER NOT NULL, id_film_xaf INTEGER NOT NULL, FOREIGN KEY(id_acteur_xaf) REFERENCES film (id_film) FOREIGN KEY(id_film_xaf) REFERENCES acteur (id_acteur))")
    CloseAll(curseur, connexion)
def AddActeur(self):
    self.WelcomeLabel = QLabel("Veuillez ajouter un Acteur à la table Acteur")
    self.setStyleSheet("background-color: #17181a")
    self.WelcomeLabel.setStyleSheet("color: red; font-size: 23px")
    self.layout = QVBoxLayout()
    self.layout.addWidget(self.WelcomeLabel, alignment=Qt.AlignCenter)
    self.NomLabel = QLabel("Nom de l'acteur :")
    self.NomActeurLine = QLineEdit("Texier")
    self.PrenomLabel = QLabel("Prenom de l'acteur :")
    self.PrenomActeurLine = QLineEdit("Thibaut")
    self.ConfirmButton = QPushButton("Insérer")

    self.NomLabel.setStyleSheet("color: white; font-size: 10px")
    self.NomActeurLine.setStyleSheet("color: white; font-size: 10px")
    self.PrenomLabel.setStyleSheet("color: white; font-size: 10px")
    self.PrenomActeurLine.setStyleSheet("color: white; font-size: 10px")
    self.ConfirmButton.setStyleSheet("color: white; font-size: 10px")    

    self.ConfirmButton.clicked.connect(self.ConfirmedActeur)
    self.layout.addWidget(self.NomLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.NomActeurLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.PrenomLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.PrenomActeurLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.ConfirmButton, alignment=Qt.AlignCenter)
def AddRealisateur(self, NomReal = "Texier", PrenomReal = "Thibaut", DndReal = "2006-05-06", NatioReal = "FR"):
    self.setStyleSheet("background-color: #17181a")
    self.connexion = sqlite3.connect(database)
    self.curseur = self.connexion.cursor()
    if not TableExist("nationalite"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table nationalite, relancez le programme après avoir résolu le preoblème")
        return 1
    self.curseur.execute("SELECT * FROM nationalite")
    print("Reuqête : SELECT * FROM nationalite")
    t = self.curseur.fetchall()
    temp = ''
    for i in t:
        temp = temp + i[1] + ", "
    self.WelcomeLabel = QLabel("Veuillez ajouter un réalisateur à la table realisateur")
    self.WelcomeLabel.setStyleSheet("color: red; font-size: 23px")
    self.layout = QVBoxLayout()
    self.layout.addWidget(self.WelcomeLabel, alignment=Qt.AlignCenter)

    self.NomLabel = QLabel("Nom du réalisateur :")
    self.NomRealisateurLine = QLineEdit(NomReal)
    self.PrenomLabel = QLabel("Prénom du réalisateur :")
    self.PrenomRealisateurLine = QLineEdit(PrenomReal)
    self.DdnLabel = QLabel("Date de naissance du réalisateur (aaaa-mm-jj) :")
    self.DdnRealisateurLine = QLineEdit(DndReal)
    self.NationaliteLabel = QLabel("Nationalité du réalisateur ({}) :".format(temp[:-2]))
    self.NationaliteRealisateurLine = QLineEdit(NatioReal)
    self.ConfirmButton = QPushButton("Insérer")

    self.NomLabel.setStyleSheet("color: white; font-size: 10px")    
    self.NomRealisateurLine.setStyleSheet("color: white; font-size: 10px")    
    self.PrenomLabel.setStyleSheet("color: white; font-size: 10px")    
    self.PrenomRealisateurLine.setStyleSheet("color: white; font-size: 10px")    
    self.DdnLabel.setStyleSheet("color: white; font-size: 10px")    
    self.DdnRealisateurLine.setStyleSheet("color: white; font-size: 10px")    
    self.NationaliteLabel.setStyleSheet("color: white; font-size: 10px")    
    self.NationaliteRealisateurLine.setStyleSheet("color: white; font-size: 10px")    
    self.ConfirmButton.setStyleSheet("color: white; font-size: 10px")    

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
def AddFilm(self):
    self.setStyleSheet("background-color: #17181a")
    self.connexion = sqlite3.connect(database)
    self.curseur = self.connexion.cursor()
    if not TableExist("nationalite"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table nationalite, relancez le programme après avoir résolu le problème")
        CloseAll(self.curseur, self.connexion)
        return 
    if not TableExist("genre"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table genre, relancez le programme après avoir résolu le problème")
        CloseAll(self.curseur, self.connexion)
        return 
    if not TableExist("realisateur"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table realisateur, relancez le programme après avoir résolu le problème")
        CloseAll(self.curseur, self.connexion)
        return 1
    
    self.curseur.execute("SELECT * FROM nationalite")
    print("Requête : SELECT * FROM nationalite")
    t = self.curseur.fetchall()
    temp = ''
    for i in t:
        temp = temp + i[1] + ", "
    self.WelcomeLabel = QLabel("Veuillez ajouter un film à la table film")
    self.WelcomeLabel.setStyleSheet("color: red; font-size: 23px")
    self.layout = QVBoxLayout()
    self.layout.addWidget(self.WelcomeLabel, alignment=Qt.AlignCenter)
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

    self.TitreLabel.setStyleSheet("color: white; font-size: 10px")
    self.TitreFilmLine.setStyleSheet("color: white; font-size: 10px")
    self.AnneeLabel.setStyleSheet("color: white; font-size: 10px")
    self.AnneeFilmLine.setStyleSheet("color: white; font-size: 10px")
    self.RealisateurLabel.setStyleSheet("color: white; font-size: 10px")
    self.RealisateurFilmLine.setStyleSheet("color: white; font-size: 10px")
    self.NationaliteLabel.setStyleSheet("color: white; font-size: 10px")
    self.NationaliteFilmLine.setStyleSheet("color: white; font-size: 10px")
    self.GenreLabel.setStyleSheet("color: white; font-size: 10px")
    self.GenreFilmLine.setStyleSheet("color: white; font-size: 10px")
    self.ConfirmButton.setStyleSheet("color: white; font-size: 10px")

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
        if sender.text().lower() == "realisateur" or sender.text().lower() == "film" or sender.text().lower() == "acteur":
            self.win = OtherWindow("Projet NSI", 450, 800, sender.text().lower())
            self.close()
            self.win.show()
        elif sender.text().lower() == "Creer les tables Acteur et XacteurFilm".lower():
            TableActeur()
            self.ActeurWasJustCreated = True
            self.close()
        elif sender.text().lower() == "genre" or sender.text().lower() == "nationalite" or sender.text().lower() == "xacteurfilm":
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
        elif Bouton == "acteur":
            AddActeur(self)
        self.setLayout(self.layout)
    def ConfirmedReal(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        req = 'INSERT INTO realisateur (nom_realisateur, prenom_realisateur, ddn_realisateur, id_nationalite_realisateur) VALUES (?, ?, ?, ?)'
        data = [self.NomRealisateurLine.text(), self.PrenomRealisateurLine.text(), self.DdnRealisateurLine.text()]
        self.curseur.execute('SELECT * FROM nationalite')
        print("Requête : SELECT * FROM nationalite")
        b = self.curseur.fetchall()
        self.curseur.execute('SELECT * FROM realisateur')
        print("Requête : SELECT * FROM realisateur")
        d = self.curseur.fetchall()
        Exist = False
        IsFound = False
        for c in range(len(d)):
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
            NomPrenom = self.RealisateurFilmLine.text().split(" ")
            self.EWin = EmergencyWindow(NomPrenom[0], NomPrenom[1])
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
                    data[len(data) - 3] = b[c][0]                                                                  #       |
                    IsFound = True                                                                                      #       |
            if not IsFound:                                                                                             #       |
                print("Ce réalisateur n'est pas présent dans la table, faites attention à taper le même réalisateur dans le programme et dans la sous-programme d'ajout")
                CloseAll(self.curseur, self.connexion)
                return 1
        self.curseur.execute("SELECT titre_film, annee_film, id_realisateur_film, id_nationalite_film, id_genre_film FROM film")
        a = self.curseur.fetchall()
        Exists = False
        for i in range(len(a)):
            if a[i][0] == data[0] and a[i][1] == data[1] and a[i][2] == data[2] and a[i][3] == data[3] and a[i][4] == data[4]:
                print("Ce film est déja dans la table, il se trouve à l'indice {} et son id est {}".format(i, a[i][0]))
                Exists = True
                CloseAll(self.curseur, self.connexion)
                break
        if not Exists:
            if type(data[2]) == type(int(2)):
                self.curseur.execute(req, data)    
                CloseAll(self.curseur, self.connexion)
                self.setLayout(self.layout)
            else:
                print("l'id du réalisateur doit être un entier, son type actuel est {}".format(type(data[2])))
        self.w = LastWindow("Contenu de la table film", self.X, self.Y, "film")
        self.close()
        self.w.show()
    def ConfirmedActeur(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        req = 'INSERT INTO acteur (nom_acteur, prenom_acteur) VALUES (?, ?)'
        data = [self.NomActeurLine.text(), self.PrenomActeurLine.text()]
        # Vérifier si l'entrée n'existe pas déjà
        Exists = False
        self.curseur.execute("SELECT * FROM acteur")
        b = self.curseur.fetchall()
        print(b)
        for i in range(len(b)):
            if data[0].lower() + ' ' + data[1].lower() == b[i][1].lower() + ' ' + b[i][2].lower():          # Si le nom prenom entré (en minuscule) est égal à l'un présent dans la table
                print("Cet acteur existe déjà dans la table, son id est {}".format(b[i][0]))
                Exists = True
        if not Exists:
            print(req, data)
            self.curseur.execute(req, data)
        CloseAll(self.curseur, self.connexion)
        self.w = LastWindow("Contenu de la table acteur", self.X, self.Y, "acteur")
        self.close()
        self.w.show()
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
class LastWindow(QWidget):
    def __init__(self, Title: str, X: int, Y: int, Table: str):
        super().__init__()
        self.setStyleSheet("background-color: #17181a")
        self.setWindowTitle(Title)
        self.resize(Y, X)
        self.Table = Table
        self.layout = QHBoxLayout()
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        self.curseur.execute("SELECT * FROM {}".format(Table))
        temp = self.curseur.fetchall()
        RealContent = []    
        if temp == []:
            self.resize(round(Y / 3), round(X / 3))
            self.layout.addWidget(QLabel("La table est vide"), alignment= Qt.AlignCenter)
            CloseAll(self.curseur, self.connexion)
            self.setLayout(self.layout)
        else:
            self.label = QLabel("Contenu de la table {}".format(Table))
            self.label.setStyleSheet("color: red; font-size: 23px")
            self.layout.addWidget(self.label, alignment= Qt.AlignCenter)
            self.ContentTable = ReturnContentTable(Table)
            self.tab = []
            self.c = ''
            for i in temp:
                RealContent.append(i)
            for k in range(len(self.ContentTable)):
                self.tab.append(self.ContentTable[k])
                for i in range(len(RealContent)):
                    self.tab.append(RealContent[i][k])
                for toujoursplus in self.tab:
                    self.c = self.c + str(toujoursplus) + '\n'
                self.b = QLabel(self.c)
                self.b.setStyleSheet("color: white; font-size: 10px")
                self.layout.addWidget(self.b, alignment=Qt.AlignCenter)
                self.tab = []
            print(RealContent)
            print(self.tab)
            for i in range(len(RealContent)):
                a = QLabel(str(RealContent[i]))
                a.setStyleSheet("font-weight: 600; word-spacing: 10px; color: white")
                self.layout.addWidget(a, alignment=Qt.AlignCenter)
            self.setLayout(self.layout)
            CloseAll(self.curseur, self.connexion)
class EmergencyWindow(QWidget):
    def __init__(self, NomReal, PrenomReal, DdnReal = "2006-05-06", NatioReal = "FR"):
        super().__init__()
        self.setWindowTitle("Ajout Realisateur")
        self.Y = 800
        self.X = 450
        self.resize(450, 800)
        self.layout = QVBoxLayout() 
        AddRealisateur(self, NomReal, PrenomReal, DdnReal, NatioReal)
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
            # print(data[0].lower() + ' ' + data[1].lower(), d[c][1].lower() + ' ' + d[c][2].lower(), data[0].lower() + ' ' + data[1].lower() == d[c][1].lower() + ' ' + d[c][2].lower())
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
        self.close()
app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
win = Window("Projet NSI", 450, 800)
win.show()
app.exec()
app2 = QApplication.instance() 
if not app2:
    app2 = QApplication(sys.argv)
if win.ActeurWasJustCreated:
    win.close()
    win2 = Window("Projet NSI", 450, 800)
    win2.show()
    app2.exec()