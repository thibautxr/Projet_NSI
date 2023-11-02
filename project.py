from PyQt5.QtWidgets import *           # EN FIN DE PROJET REMPLACER LE * PAR LES FONCTIONS UTILISEES POUR OPTIMISER
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys
import sqlite3
from time import *

database = "Film_realisateur_genre_nationalite.db"
print("tapez help(main) pour avoir une explication rapide de chaque fonction")

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
    return 0


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

    curseur.execute("SELECT name FROM sqlite_master WHERE type='table';")               # la table sqlite_master est une table créée dans chaque database SQLite, elle contient notamment
    print("Requête : SELECT name FROM sqlite_master WHERE type='table';")                # le nom de toutes les tables de la database, ce que nous récupérons ici
    a = curseur.fetchall()
    l = []
    cas = "(),'"                                                                        # la requête renvoie une chaine un peu bizarre, donc on retire ces caractères pour rendre 
    csc = a                                                                              # les données exploitables

    for row in a:
        csc = str(row)
        for caractere in cas:                                                          
            csc = csc.replace(caractere, '')                                            # on remplace tous les caracteres présents dans cas et on les remplace par '' (par rien quoi, on les supprimes)
        l.append(csc)
    CloseAll(curseur, connexion)
    return list(reversed(l))[:-1]                                                       # on retourne la liste finale, qu'on inverse et dont on retire le dernier élément (car le premier élément
                                                                                        # de la liste non-inversée est quelque chose dont on ne veut pas, je me souviens plus quoi exactement)



def ReturnContentTable(table):
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()
    curseur.execute("PRAGMA table_info({})".format(table))              # la requête PRAGMA table_info(table) retourne les attributs de la table, par exemple [[0, id_film], [1, titre_film], [2, nationalite_film], ...]
    print("Requête : PRAGMA table_info({})".format(table))              # le print est ajouté pour que le programme ne fasse pas "boite noire" et que les actions du programme soient affichées dans le prompt
    ProprieteTable = curseur.fetchall()
    ContentTable = []
    for i in range(len(ProprieteTable)):
        ContentTable.append(ProprieteTable[i][1])                       # le tableau ContentTable agit comme un filtre et ne contient que le nom des attributs
    CloseAll(curseur, connexion)
    return ContentTable





def TableActeur():
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()
    curseur.execute("CREATE TABLE acteur (id_acteur INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, nom_acteur TEXT NOT NULL, prenom_acteur TEXT NOT NULL)")
    curseur.execute("CREATE TABLE xacteurfilm (id_xaf INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, id_acteur_xaf INTEGER NOT NULL, id_film_xaf INTEGER NOT NULL, FOREIGN KEY(id_acteur_xaf) REFERENCES film (id_film) FOREIGN KEY(id_film_xaf) REFERENCES acteur (id_acteur))")
    CloseAll(curseur, connexion)

    return 0



def AddActeur(self):
    self.WelcomeLabel = QLabel("Veuillez ajouter un Acteur à la table Acteur")
    self.setStyleSheet("background-color: #17181a")
    self.WelcomeLabel.setStyleSheet("color: red; font-size: 23px")
    self.layout = QVBoxLayout()
    self.layout.addWidget(self.WelcomeLabel, alignment=Qt.AlignCenter)
    self.NomLabel = QLabel("Nom de l'acteur :")
    self.NomActeurLine = QLineEdit("Bergèse")
    self.PrenomLabel = QLabel("Prenom de l'acteur :")
    self.PrenomActeurLine = QLineEdit("Jerôme")
    self.ConfirmButton = QPushButton("Insérer")

    self.NomLabel.setStyleSheet("color: white; font-size: 13px")  
    self.NomActeurLine.setStyleSheet("color: white; font-size: 13px")  
    self.PrenomLabel.setStyleSheet("color: white; font-size: 13px")  
    self.PrenomActeurLine.setStyleSheet("color: white; font-size: 13px")  
    self.ConfirmButton.setStyleSheet("color: white; font-size: 13px")    

    self.ConfirmButton.clicked.connect(self.ConfirmedActeur)
    self.layout.addWidget(self.NomLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.NomActeurLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.PrenomLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.PrenomActeurLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.ConfirmButton, alignment=Qt.AlignCenter)

    return 0





def AddRealisateur(self, NomReal = "Texier", PrenomReal = "Thibaut", DndReal = "2006-05-06", NatioReal = "FR"):
    self.setStyleSheet("background-color: #17181a")
    if not TableExist("nationalite"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table nationalite, relancez le programme après avoir résolu le problème")
        CloseAll(self.curseur, self.connexion)
        return "nationalite"
    
    self.connexion = sqlite3.connect(database)
    self.curseur = self.connexion.cursor()
    self.curseur.execute("SELECT nom_nationalite FROM nationalite")     
    print("Requête : SELECT nom_nationalite FROM nationalite")                          #
    t = self.curseur.fetchall()                                                         #   on récupère le nom des nationalités et on en fait une
    temp = ''                                                                           #   chaine de charactères pour avertir l'utilisateur
    for i in t:                                                                         #   des nationalités existentes et du format qu'elles ont
        temp = temp + i[0] + ", "                                                       #
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

    self.NomLabel.setStyleSheet("color: white; font-size: 13px")  
    self.NomRealisateurLine.setStyleSheet("color: white; font-size: 13px")  
    self.PrenomLabel.setStyleSheet("color: white; font-size: 13px")  
    self.PrenomRealisateurLine.setStyleSheet("color: white; font-size: 13px")  
    self.DdnLabel.setStyleSheet("color: white; font-size: 13px")  
    self.DdnRealisateurLine.setStyleSheet("color: white; font-size: 13px")  
    self.NationaliteLabel.setStyleSheet("color: white; font-size: 13px")  
    self.NationaliteRealisateurLine.setStyleSheet("color: white; font-size: 13px")  
    self.ConfirmButton.setStyleSheet("color: white; font-size: 13px")  

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

    return 0









# Composition de la table film : id_film, titre_film, annee_film, id_realisateur_film, id_nationalite_film, id_genre_film
def AddFilm(self):
    self.setStyleSheet("background-color: #17181a")
    if not TableExist("nationalite"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table nationalite, relancez le programme après avoir résolu le problème")
        CloseAll(self.curseur, self.connexion)
        return "nationalite"                                                    #
    if not TableExist("genre"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table genre, relancez le programme après avoir résolu le problème")
        CloseAll(self.curseur, self.connexion)
        return "genre"                                                          #   Nécessaire pour créer la fenetre avec le message d'erreur correspondant
    if not TableExist("realisateur"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table realisateur, relancez le programme après avoir résolu le problème")
        CloseAll(self.curseur, self.connexion)
        return "realisateur"                                                    #
    
    self.connexion = sqlite3.connect(database)
    self.curseur = self.connexion.cursor()
    self.curseur.execute("SELECT nom_nationalite FROM nationalite")
    print("Requête : SELECT nom_nationalite FROM nationalite")
    t = self.curseur.fetchall()
    temp = ''
    for i in t:
        temp = temp + i[0] + ", "                                               # expliqué dans AddRealisateur()
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
    self.NationaliteLabel = QLabel("Nationalité du film ({}) :".format(temp[:-2]))      #   On supprime les 2 derniers charactères à cause de la composition de for i in t: (que j'ai la flemme de changer)   
    self.NationaliteFilmLine = QLineEdit("US")                                          #                                                                            temp = temp + i[0] + ", "
    self.GenreLabel = QLabel("Genre du film : ")
    self.GenreFilmLine = QLineEdit("Science-fiction")
    self.ConfirmButton = QPushButton("Insérer")
    CloseAll(self.curseur, self.connexion)

    self.TitreLabel.setStyleSheet("color: white; font-size: 13px")  
    self.TitreFilmLine.setStyleSheet("color: white; font-size: 13px")  
    self.AnneeLabel.setStyleSheet("color: white; font-size: 13px")  
    self.AnneeFilmLine.setStyleSheet("color: white; font-size: 13px")  
    self.RealisateurLabel.setStyleSheet("color: white; font-size: 13px")  
    self.RealisateurFilmLine.setStyleSheet("color: white; font-size: 13px")  
    self.NationaliteLabel.setStyleSheet("color: white; font-size: 13px")  
    self.NationaliteFilmLine.setStyleSheet("color: white; font-size: 13px")  
    self.GenreLabel.setStyleSheet("color: white; font-size: 13px")  
    self.GenreFilmLine.setStyleSheet("color: white; font-size: 13px")  
    self.ConfirmButton.setStyleSheet("color: white; font-size: 13px")  

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
    return 0






def AddLink(self):
    self.setStyleSheet("background-color: #17181a")
    if not TableExist("acteur"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table acteur, relancez le programme après avoir résolu le problème")
        CloseAll(self.curseur, self.connexion)
        return "acteur"
    if not TableExist("film"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table film, relancez le programme après avoir résolu le problème")
        CloseAll(self.curseur, self.connexion)
        return "film"
    
    self.connexion = sqlite3.connect(database)
    self.curseur = self.connexion.cursor()
    self.curseur.execute("SELECT * FROM acteur")
    print("Requête : SELECT * FROM acteur")
    t = self.curseur.fetchall()
    if t == []:
        CloseAll(self.curseur, self.connexion)
        print("Il n'y a pas d'acteur dans la table acteur, Redirection vers le programme d'ajout d'acteur")
        self.EWin = EmergencyWindow(1)
        self.EWin.show()
        return "xacteurfilm"
    self.temp = []
    for i in range(len(t)):
        self.temp.append([t[i][0], t[i][1] + ' ' + t[i][2]])
    self.curseur.execute("SELECT * FROM film ORDER BY titre_film")
    print("Requête : SELECT * FROM film ORDER BY titre_film")
    t = self.curseur.fetchall()
    self.TabTitreFilm = []
    for i in range(len(t)):
        self.TabTitreFilm.append([t[i][0], t[i][1]])
    self.MenuFilm = QComboBox()
    self.MenuActeur = QComboBox()
    self.MenuFilm.setStyleSheet("height: 150px; width: 200px;")
    self.ItemTitreFilm = []
    for i in range(len(self.TabTitreFilm)):
        self.ItemTitreFilm.append(' ')
    self.ItemActeur = []
    for i in range(len(self.temp)):
        self.ItemActeur.append(' ')
    print(len(self.TabTitreFilm))
    self.ModelTitre = QStandardItemModel()
    self.ModelActeur = QStandardItemModel()

    for i in range(len(self.TabTitreFilm)):
        self.ItemTitreFilm[i] = QStandardItem(t[i][1])
        self.ItemTitreFilm[i].setData(t[i][0], role=Qt.UserRole)
        self.ModelTitre.appendRow(self.ItemTitreFilm[i])

    for i in range(len(self.ItemActeur)):
        self.ItemActeur[i] = QStandardItem(self.temp[i][1])
        self.ItemActeur[i].setData(self.temp[i][0], role=Qt.UserRole)
        self.ModelActeur.appendRow(self.ItemActeur[i])

    
    
    self.WelcomeLabel = QLabel("Veuillez lier un acteur à un film")
    self.WelcomeLabel.setStyleSheet("color: red; font-size: 23px")
    self.layout = QVBoxLayout()
    self.layout.addWidget(self.WelcomeLabel, alignment=Qt.AlignCenter)
    self.MenuFilm.setModel(self.ModelTitre)
    self.MenuActeur.setModel(self.ModelActeur)
    self.TitreLabel = QLabel("Titre du film :")
    self.ActeurLabel = QLabel("Nom Prenom de l'Acteur :")
    self.ConfirmButton = QPushButton("Relier")
       # ça casse les couilles ya des trucs qui marchent pas, genre les boutons avec les bords arrondis, cette ligne de code elle sert à rien à par ce commentaire où c'est juste moi qui me plaint de cette librairie de MERDE

    self.TitreLabel.setStyleSheet("color: white; font-size: 13px")
    self.ConfirmButton.setStyleSheet("color: white; font-size: 13px")
    self.ActeurLabel.setStyleSheet("color: white; font-size: 13px")
    self.MenuActeur.setStyleSheet("color: white; font-size: 11px") 
    self.MenuFilm.setStyleSheet("color: white; font-size: 11px")

    

    self.layout.addWidget(self.TitreLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.MenuFilm, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.ActeurLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.MenuActeur, alignment=Qt.AlignCenter)
    self.curseur.execute("PRAGMA table_info(xacteurfilm)")
    if len(self.curseur.fetchall()) <= 3:
        self.AddPersonnage = QPushButton("Ajouter un Attribut \"Personnage\"")
        self.AddPersonnage.setStyleSheet("color: white; font-size: 11px")
        self.AddPersonnage.clicked.connect(self.AddPersonnageXacteurFilm)
        self.layout.addWidget(self.AddPersonnage, alignment=Qt.AlignCenter)
        self.PersonnageExists = False
    else:
        self.XacteurFilmPersonnage = QLineEdit("Eliott Alderson")
        self.XacteurFilmPersonnage.setStyleSheet("color: white; font-size: 11px")
        self.layout.addWidget(self.XacteurFilmPersonnage, alignment=Qt.AlignCenter)
        self.PersonnageExists = True
    self.ConfirmButton.clicked.connect(self.ConfirmedXacteurFilm)
    self.layout.addWidget(self.ConfirmButton, alignment=Qt.AlignCenter)
    self.layout.addWidget(QLabel())
    self.layout.addWidget(QLabel())

    CloseAll(self.curseur, self.connexion)
    return 0




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
        if len(self.l) <= 4:                                                            # Si il y a moins de 5 tables
            self.a = QPushButton("Creer les tables Acteur et XacteurFilm")              # On crée un Bouton
            self.a.clicked.connect(self.BoutonAppuye)                                   # Qui crée les tables Acteur et XacteurFilm
            self.layout.addWidget(self.a)
           
        
        
        self.setLayout(self.layout)

    def BoutonAppuye(self):
        sender = self.sender()                                                          # Contient le texte du bouton (putain ce que j'en ai chié pour trouver ça)
        if sender.text().lower() == "realisateur" or sender.text().lower() == "film" or sender.text().lower() == "acteur" or sender.text().lower() == "xacteurfilm":
            self.win = OtherWindow("Projet NSI", self.X, self.Y, sender.text().lower())
            self.close()
            self.win.show()
        elif sender.text().lower() == "Creer les tables Acteur et XacteurFilm".lower():
            TableActeur()
            self.ActeurWasJustCreated = True                                            # Permet de relancer le programme une seconde fois après la création des tables
            self.close()
        elif sender.text().lower() == "genre" or sender.text().lower() == "nationalite":
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
        if Bouton == "Lorem ipsum dolor sit amet":                      # si ce bouton n'a rien a foutre la 
            self.layout.addWidget(QLabel("Cette Table n'a pas été configurée"), alignment=Qt.AlignCenter)

        elif Bouton == "realisateur":
            a = AddRealisateur(self)
        elif Bouton == "film":
            a = AddFilm(self)
        elif Bouton == "acteur":
            a = AddActeur(self)
        elif Bouton == "xacteurfilm":
            a = AddLink(self)

        if a != 0:
            self.a = QLabel("La table {} est vide ou n'existe pas".format(a))
            self.a.setStyleSheet("color: red; font-size: 23px")
            self.layout.addWidget(self.a, alignment=Qt.AlignCenter)
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
            print("Requête : INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(data[len(data) - 2]))              #       |
            print("Cette nationalité n'était pas dans la table, elle a donc été ajoutée")
            data[len(data) - 2] = b[len(b) - 1][0] + 1
    
        self.curseur.execute('SELECT * FROM genre') 
        print("Requête : SELECT * FROM genre")                                                                                  #       |
        b = self.curseur.fetchall()                                                                                             #       |
        IsFound = False                                                                                                         #       |
        for c in range(len(b)):                                                                                                 #       |
            if data[len(data) - 1].lower() == b[c][1].lower():                                                                  #      PASSER D'UN
                data[len(data) - 1] = b[c][0]                                                                                   #      GENRE A UN ID
                IsFound = True                                                                                                  #       |
        if not IsFound:                                                                                                         #       |
            self.curseur.execute("INSERT INTO genre (nom_genre) VALUES ('{}')".format(data[len(data) - 1]))                     #       |
            print("Requête : INSERT INTO genre (nom_genre) VALUES ('{}')".format(data[len(data) - 1]))
            print("Ce genre n'était pas dans la table, il a donc été ajouté")
            data[len(data) - 1] = b[len(b) - 1][0] + 1

        self.curseur.execute("SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")
        print("Requête : SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")                          #       |
        b = self.curseur.fetchall()                                                                                             #       |
        IsFound = False                                                                                                         #       |
        for c in range(len(b)):                                                                                                 #       |
            ConcD = b[c][1] + ' ' + b[c][2]                                                                                     #      PASSER D'UN NOM/PRENOM A UN ID                                               
            if not IsFound and data[len(data) - 3].lower() == ConcD.lower():                                                                    #       |
                data[len(data) - 3] = b[c][0]                                                                                   #       |
                IsFound = True                                                                                                  #       |
        if not IsFound:                                                                                                         #       |
            print("Ce réalisateur n'est pas présent dans la table, vous allez être redirigé vers le programme d'ajout de réalisateur")
            CloseAll(self.curseur, self.connexion)
            NomPrenom = self.RealisateurFilmLine.text().split(" ")
            self.EWin = EmergencyWindow(0, NomPrenom[0], NomPrenom[1])
            self.EWin.show()
            self.connexion = sqlite3.connect(database)
            self.curseur = self.connexion.cursor()
            self.curseur.execute("SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")
            print("Requête : SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")                      #       |
            b = self.curseur.fetchall()                                                                                         #       |
            IsFound = False                                                                                                     #       |
            for c in range(len(b)):                                                                                             #       |
                ConcD = b[c][1] + ' ' + b[c][2]                                                                                 #      PASSER D'UN NOM/PRENOM A UN ID                                               
                if data[len(data) - 3].lower() == ConcD.lower():                                                                #       |
                    data[len(data) - 3] = b[c][0]                                                                               #       |
                    IsFound = True                                                                                              #       |
            if not IsFound:                                                                                                     #       |
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
                print("l'id du réalisateur doit être un entier, son type actuel est {}".format(type(data[2])))                  # ne s'executera normalement jamais car toutes les actions possibles sont couvertes, mais on sait jamais
        self.w = LastWindow("Contenu de la table film", self.X, self.Y, "film")
        self.close()
        self.w.show()


    def ConfirmedXacteurFilm(self):
        ActeurIndex = self.MenuActeur.currentIndex()
        ActeurId = self.MenuActeur.itemData(ActeurIndex)
        FilmIndex = self.MenuFilm.currentIndex()
        FilmId = self.MenuFilm.itemData(FilmIndex)
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        if not self.PersonnageExists:
            self.curseur.execute("SELECT id_acteur_xaf, id_film_xaf FROM xacteurfilm WHERE id_acteur_xaf = {} AND id_film_xaf = {}".format(ActeurId, FilmId))
            if self.curseur.fetchall() == []:
                self.curseur.execute("INSERT INTO xacteurfilm (id_acteur_xaf, id_film_xaf) VALUES ({}, {})".format(ActeurId, FilmId))
                CloseAll(self.curseur, self.connexion)
                self.w = LastWindow("Contenu de la table xacteurfilm", self.X, self.Y, "xacteurfilm")
                self.close()
                self.w.show()
            else:
                print("Cet acteur a déjà été lié à ce film")
                CloseAll(self.curseur, self.connexion)
        if self.PersonnageExists:
            self.curseur.execute("SELECT id_acteur_xaf, id_film_xaf, personnage_xaf FROM xacteurfilm WHERE id_acteur_xaf = {} AND id_film_xaf = {} AND personnage_xaf = '{}'".format(ActeurId, FilmId, self.XacteurFilmPersonnage.text()))
            if self.curseur.fetchall() == []:
                self.curseur.execute("INSERT INTO xacteurfilm (id_acteur_xaf, id_film_xaf, personnage_xaf) VALUES ({}, {}, '{}')".format(ActeurId, FilmId, self.XacteurFilmPersonnage.text()))
                CloseAll(self.curseur, self.connexion)
                self.w = LastWindow("Contenu de la table xacteurfilm", self.X, self.Y, "xacteurfilm")
                self.close()
                self.w.show()
            else:
                print("Cet acteur a déjà été lié à ce film")
                CloseAll(self.curseur, self.connexion)







    def AddPersonnageXacteurFilm(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        self.curseur.execute("ALTER TABLE xacteurfilm ADD personnage_xaf TEXT(64)")
        CloseAll(self.curseur, self.connexion)
        self.ActeurWasJustCreated = True                                            # Permet de relancer le programme une seconde fois après la création des tables
        self.close()






    def ConfirmedActeur(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        req = 'INSERT INTO acteur (nom_acteur, prenom_acteur) VALUES (?, ?)'
        data = [self.NomActeurLine.text(), self.PrenomActeurLine.text()]
        # Vérifier si l'entrée n'existe pas déjà
        Exists = False
        self.curseur.execute("SELECT * FROM acteur")
        b = self.curseur.fetchall()
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






class LastWindow(QWidget):
    def __init__(self, Title: str, X: int, Y: int, Table: str):
        super().__init__()
        self.setStyleSheet("background-color: #17181a")
        self.setWindowTitle(Title)
        self.resize(Y, X)
        self.Table = Table
        self.Hlayout = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        self.curseur.execute("SELECT * FROM {}".format(Table))
        temp = self.curseur.fetchall()
        
        if temp == []:                                                  #   Si la table séléctionnée est vide
            self.resize(round(Y / 3), round(X / 3))
            a = QLabel("La table est vide")
            a.setStyleSheet("Color: white; font-size: 18px")
            self.layout.addWidget(a, alignment= Qt.AlignCenter)
            CloseAll(self.curseur, self.connexion)
            self.setLayout(self.layout)
        else:
            self.label = QLabel("Contenu de la table {}".format(Table))
            self.label.setStyleSheet("color: red; font-size: 23px")
            self.layout.addWidget(self.label, alignment= Qt.AlignCenter)
            self.ContentTable = ReturnContentTable(Table)
            self.tab = []
            self.c = ''
            
            for k in range(len(self.ContentTable)):
                self.tab.append(self.ContentTable[k])                                       # Pour faire l'affichage vertical, on doit d'abord ajouter le nom de l'attribut dans la liste..
                for i in range(len(temp)):
                    self.tab.append(temp[i][k])                                             # .. puis ses valeurs
                for toujoursplus in self.tab:
                    self.c = self.c + str(toujoursplus) + '\n\n'                            # Comme c'est un affichage vertical, il faut mettre des sauts de ligne, on en met 2 pck c'est plus stylé
                self.b = QLabel(self.c)
                self.c = ''
                self.b.setStyleSheet("color: white; font-size: 15px; text-align: end")
                self.Hlayout.addWidget(self.b, alignment=Qt.AlignCenter)
                self.tab = []
           

            self.layout.addLayout(self.Hlayout)
            self.layout.addWidget(QLabel())                                                 # on rajoute des Labels vides pck sinon le rendu est dégueulasse et il y a beaucoup trop
            self.layout.addWidget(QLabel())                                                 # de place vide en bas fin bref c'est pas opti DU TOUT mais j'ai rien trouvé d'autre
            self.setLayout(self.layout)
            CloseAll(self.curseur, self.connexion)








class EmergencyWindow(QWidget):                                                             # Comme son nom l'indique, elle sert que quand c'est le zbeul, genre quand il faut ajouter un Réalisateur en urgence
    def __init__(self, EmergencyId: int = 0, NomReal: str = "Texier", PrenomReal: str = "Thibaut", DdnReal: str = "2006-05-06", NatioReal: str = "FR"):
        super().__init__()
        self.setWindowTitle("Ajout Realisateur")
        self.Y = 800
        self.X = 450
        self.resize(450, 800)
        self.layout = QVBoxLayout() 
        if EmergencyId == 0:
            self.setWindowTitle("Ajout Realisateur")
            AddRealisateur(self, NomReal, PrenomReal, DdnReal, NatioReal)
        elif EmergencyId == 1:
            self.setWindowTitle("Ajout Acteur")
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
            self.curseur.execute(req, data)
            print("Requête : INSERT INTO realisateur (nom_realisateur, prenom_realisateur, ddn_realisateur, id_nationalite_realisateur) VALUES ('{}', '{}', {}, {})".format(data[0], data[1], data[2], data[3]))
        CloseAll(self.curseur, self.connexion)
        self.close()



    def ConfirmedActeur(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        req = 'INSERT INTO acteur (nom_acteur, prenom_acteur) VALUES (?, ?)'
        data = [self.NomActeurLine.text(), self.PrenomActeurLine.text()]
        # Vérifier si l'entrée n'existe pas déjà
        Exists = False
        self.curseur.execute("SELECT * FROM acteur")
        b = self.curseur.fetchall()
        for i in range(len(b)):
            if data[0].lower() + ' ' + data[1].lower() == b[i][1].lower() + ' ' + b[i][2].lower():          # Si le nom prenom entré (en minuscule) est égal à l'un présent dans la table
                print("Cet acteur existe déjà dans la table, son id est {}".format(b[i][0]))
                Exists = True
        if not Exists:
            print(req, data)
            self.curseur.execute(req, data)

        CloseAll(self.curseur, self.connexion)
        self.close()
        














'''
class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajout Realisateur")
        self.Y = 800
        self.X = 450
        self.layout = QHBoxLayout()
        tab = 'id_realisateur \n 1 \n 2 \n 3 \n'
        tab2 = "nom_realisateur \n abrams \n BadHam \n Besson \n"
        self.layout.addWidget(QLabel(tab), alignment=Qt.AlignCenter)
        self.layout.addWidget(QLabel(tab2), alignment=Qt.AlignCenter)

        self.setLayout(self.layout)
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
if win.ActeurWasJustCreated:
    win.close()
    win2 = Window("Projet NSI", 450, 800)
    win2.show()
    app2.exec()
    app3 = QApplication.instance() 
    if not app3:
        app3 = QApplication(sys.argv)
    if win2.ActeurWasJustCreated:
        win.close()
        win3 = OtherWindow("Projet NSI", 450, 800, "xacteurfilm")
        win3.show()
        app3.exec()









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