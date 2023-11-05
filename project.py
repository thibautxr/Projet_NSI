from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QWidget, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sqlite3


database = "Film_realisateur_genre_nationalite.db"
Memory = 15  # Modifier selon la quantité de RAM de l'utilisateur    (conseillé : 2Go : 5, 4Go : 15, 8Go : 30, 16Go : 50, 32Go : 100)    la valeur de base est faible pour être compatible avec des systèmes peu performants (en accord avec le choix du SGBD : SQLite)
DefaultCSS = "color: white; font-size: 13px"
BackgroundCSS = "background-color: #17181a"
X = 450
Y = 800


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
        print("29 \t: SELECT * FROM {}".format(table))
    except sqlite3.OperationalError:            # Si la table n'existe pas
        print("31\tERREUR : La table {} n'existe pas".format(table))
        boool = False
    CloseAll(curseur, connexion)
    return boool



def ReturnAllTable():
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()
    curseur.execute("SELECT name FROM sqlite_master WHERE type='table';")               # la table sqlite_master est une table créée dans chaque database SQLite, elle contient notamment
    print("42 \t: SELECT name FROM sqlite_master WHERE type='table';")                         # le nom de toutes les tables de la database, ce que nous récupérons ici
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
    print("62 \t: PRAGMA table_info({})".format(table))                        # le print est ajouté pour que le programme ne fasse pas "boite noire" et que les actions du programme soient affichées dans le prompt
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
    print("76 \t: CREATE TABLE acteur (id_acteur INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, nom_acteur TEXT NOT NULL, prenom_acteur TEXT NOT NULL)")
    curseur.execute("CREATE TABLE xacteurfilm (id_xaf INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, id_acteur_xaf INTEGER NOT NULL, id_film_xaf INTEGER NOT NULL, FOREIGN KEY(id_acteur_xaf) REFERENCES film (id_film) FOREIGN KEY(id_film_xaf) REFERENCES acteur (id_acteur))")
    print("78 \t: CREATE TABLE xacteurfilm (id_xaf INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, id_acteur_xaf INTEGER NOT NULL, id_film_xaf INTEGER NOT NULL, FOREIGN KEY(id_acteur_xaf) REFERENCES film (id_film) FOREIGN KEY(id_film_xaf) REFERENCES acteur (id_acteur))")
    CloseAll(curseur, connexion)
    return 0



def AddActeur(self):
    self.connexion = sqlite3.connect(database)
    self.curseur = self.connexion.cursor()
    self.WelcomeLabel = QLabel("Veuillez ajouter un Acteur à la table Acteur")
    self.setStyleSheet(BackgroundCSS)
    self.WelcomeLabel.setStyleSheet("color: red; font-size: 23px")
    self.layout = QVBoxLayout()
    self.layout.addWidget(self.WelcomeLabel, alignment=Qt.AlignCenter)
    self.NomLabel = QLabel("Nom de l'acteur :")
    self.NomActeurLine = QLineEdit("Bergèse")                               # La valeur entrée dans QLineEdit(str) est la valeur par défaut du champ
    self.PrenomLabel = QLabel("Prenom de l'acteur :")
    self.PrenomActeurLine = QLineEdit("Jerôme")
    self.ConfirmButton = QPushButton("Insérer")

    self.NomLabel.setStyleSheet(DefaultCSS)  
    self.NomActeurLine.setStyleSheet(DefaultCSS)  
    self.PrenomLabel.setStyleSheet(DefaultCSS)  
    self.PrenomActeurLine.setStyleSheet(DefaultCSS)  
    self.ConfirmButton.setStyleSheet(DefaultCSS)    

    self.ConfirmButton.clicked.connect(self.ConfirmedActeur)
    self.layout.addWidget(self.NomLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.NomActeurLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.PrenomLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.PrenomActeurLine, alignment=Qt.AlignCenter)
    self.curseur.execute("PRAGMA table_info(acteur)")
    print("110 \t: PRAGMA table_info(acteur)")
    if len(self.curseur.fetchall()) <= 3:                                   # Si la table acteur a moins de 4 attributs
        self.AddNationaliteActeur = QPushButton("Ajouter un attribut \"id_nationalite_acteur\"")
        self.AddNationaliteActeur.setStyleSheet(DefaultCSS)
        self.AddNationaliteActeur.clicked.connect(self.AddIdNationaliteActeur)
        self.layout.addWidget(self.AddNationaliteActeur, alignment=Qt.AlignCenter)
    else:
        self.curseur.execute("SELECT * FROM nationalite")
        print("118 \t: SELECT * FROM nationalite")
        a = self.curseur.fetchall()
        self.temp = ''                                                                           #   chaine de charactères pour avertir l'utilisateur
        for i in a:                                                                         #   des nationalités existentes et du format qu'elles ont
            self.temp = self.temp + i[1] + ", "
        self.NationaliteLabel = QLabel("Entrez la nationalité de l'acteur ({}) : ".format(self.temp[:-2]))
        self.NationaliteLine = QLineEdit("FR")
        self.NationaliteLabel.setStyleSheet(DefaultCSS)
        self.NationaliteLine.setStyleSheet(DefaultCSS) 
        self.layout.addWidget(self.NationaliteLabel, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.NationaliteLine, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.ConfirmButton, alignment=Qt.AlignCenter)
    CloseAll(self.curseur, self.connexion)
    return 0



def AddRealisateur(self, NomReal = "Texier", PrenomReal = "Thibaut", DndReal = "2006-05-06", NatioReal = "FR"):
    self.setStyleSheet(BackgroundCSS)
    if not TableExist("nationalite"):
        self.WelcomeLabel = QLabel("Impossible de trouver la table nationalite, relancez le programme après avoir résolu le problème")
        CloseAll(self.curseur, self.connexion)
        return "nationalite"
    self.connexion = sqlite3.connect(database)
    self.curseur = self.connexion.cursor()
    self.curseur.execute("SELECT nom_nationalite FROM nationalite")     
    print("144 \t: SELECT nom_nationalite FROM nationalite")                                    #
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

    self.NomLabel.setStyleSheet(DefaultCSS)  
    self.NomRealisateurLine.setStyleSheet(DefaultCSS)  
    self.PrenomLabel.setStyleSheet(DefaultCSS)  
    self.PrenomRealisateurLine.setStyleSheet(DefaultCSS)  
    self.DdnLabel.setStyleSheet(DefaultCSS)  
    self.DdnRealisateurLine.setStyleSheet(DefaultCSS)  
    self.NationaliteLabel.setStyleSheet(DefaultCSS)  
    self.NationaliteRealisateurLine.setStyleSheet(DefaultCSS)  
    self.ConfirmButton.setStyleSheet(DefaultCSS)  

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
    self.setStyleSheet(BackgroundCSS)
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
    print("206 \t: SELECT nom_nationalite FROM nationalite")
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

    self.TitreLabel.setStyleSheet(DefaultCSS)
    self.TitreFilmLine.setStyleSheet(DefaultCSS)
    self.AnneeLabel.setStyleSheet(DefaultCSS)
    self.AnneeFilmLine.setStyleSheet(DefaultCSS)
    self.RealisateurLabel.setStyleSheet(DefaultCSS)
    self.RealisateurFilmLine.setStyleSheet(DefaultCSS)
    self.NationaliteLabel.setStyleSheet(DefaultCSS)
    self.NationaliteFilmLine.setStyleSheet(DefaultCSS) 
    self.GenreLabel.setStyleSheet(DefaultCSS)
    self.GenreFilmLine.setStyleSheet(DefaultCSS)
    self.ConfirmButton.setStyleSheet(DefaultCSS)

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
    self.setStyleSheet(BackgroundCSS)
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
    print("269 \t: SELECT * FROM acteur")
    t = self.curseur.fetchall()
    if t == []:                                     # Si la requête ne renvoie rien, mais pas d'erreur sqlite3.OperationError, c'est que la table existe mais est vide
        CloseAll(self.curseur, self.connexion)
        print("273\tIl n'y a pas d'acteur dans la table acteur, Redirection vers le programme d'ajout d'acteur")
        self.EWin = EmergencyWindow(1)
        self.EWin.show()
        return "xacteurfilm"
    self.temp = []
    for i in range(len(t)):
        self.temp.append([t[i][0], t[i][1] + ' ' + t[i][2]])                # La structure de temp sera : [[id_acteur, nom_acteur prenom_acteur], [...], ...]
    self.curseur.execute("SELECT * FROM film ORDER BY titre_film")
    print("281 \t: SELECT * FROM film ORDER BY titre_film")
    t = self.curseur.fetchall()
    self.TabTitreFilm = []
    for i in range(len(t)):
        self.TabTitreFilm.append([t[i][0], t[i][1]])                        # La structure de TabTitreFIlm sera : [[id_film, titre_film], [id_film2, titre_film2], ...]
    self.MenuFilm = QComboBox()                                             # Création d'une menu déroulant
    self.MenuActeur = QComboBox()
    self.MenuFilm.setStyleSheet("height: 150px; width: 200px;")             # Ne sert à rien pck ya des putains d'instructions qui fonctionnent pas mais on le garde en place holder au cas ou
    self.ItemTitreFilm = []
    for i in range(len(self.TabTitreFilm)):                                 # Crée un tableau de la taille du nombre de films, obligé de faire ça car 
        self.ItemTitreFilm.append(' ')                                          # self.ItemTitreFilm = ['' * len(self.TabTitreFilm)] ne semble pas fonctionner
    self.ItemActeur = []
    for i in range(len(self.temp)):
        self.ItemActeur.append(' ')
    self.ModelTitre = QStandardItemModel()                                  # Crée un "modèle" de donnée qui stocke en n°1 l'id de l'acteur/film séléctionné et en n°2 le nom/titre de 
    self.ModelActeur = QStandardItemModel()                                 # Celui ci, on est obligés de faire comme ça au cas ou il y ait 2 titres de film/noms d'acteurs identiques
    for i in range(len(self.TabTitreFilm)):
        self.ItemTitreFilm[i] = QStandardItem(t[i][1])                      # Dans la ligne d'indice i du tableau ItemTitreFilm on dit que le nom de la ligne n°i du menu sera t[i][1]
        self.ItemTitreFilm[i].setData(t[i][0], role=Qt.UserRole)            # Dans la ligne d'indice i du tableau ItemTitreFilm on dit que l'id de la ligne n°i du menu sera t[i][0]
        self.ModelTitre.appendRow(self.ItemTitreFilm[i])                    # Je sais pas à quoi sert le role=Qt.USerRole mais ça avait l'air important sur la doc donc je l'ai laissé ça fait pas de mal je pense pas que ça prenne trop de mémoire
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

    self.TitreLabel.setStyleSheet(DefaultCSS)
    self.ConfirmButton.setStyleSheet(DefaultCSS)
    self.ActeurLabel.setStyleSheet(DefaultCSS)
    self.MenuActeur.setStyleSheet("color: white; font-size: 11px") 
    self.MenuFilm.setStyleSheet("color: white; font-size: 11px")
    
    self.PersonnageExists = True
    self.layout.addWidget(self.TitreLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.MenuFilm, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.ActeurLabel, alignment=Qt.AlignCenter)
    self.layout.addWidget(self.MenuActeur, alignment=Qt.AlignCenter)
    self.curseur.execute("PRAGMA table_info(xacteurfilm)")
    print("330 \t: PRAGMA table_info(xacteurfilm)")
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



class FirstWindow(QWidget):                                 # Ne s'ouvre que quand c'est la première ouverture, les fonctions rudimentaires de cette classe ne sont pas documentées
    def __init__(self):
        super().__init__()
        self.setStyleSheet(BackgroundCSS)
        self.setWindowTitle("Explication")
        self.resize(450, 800)
        self.layout = QVBoxLayout()
        self.label = QLabel(
            '''
            CloseAll()\t\t\t: Ferme simplement une connexion à une base de donnée, fonction créée pour gagner de la place et avoir un code plus simple à comprendre \n
            TableExist()\t\t\t: Permet de savoir si une table existe, évite d'avoir une fatal error dans la console qui ferait crash le programme \n
            ReturnAllTable()\t\t\t: Renvoie une liste de toute les tables qui existent dans la base de donnée \n
            ReturnContentTable(table)\t: Renvoie une liste de la composition d'une table \n
            TableActeur()\t\t\t: Crée les tables xacteurfilm et acteur \n
            AddActeur()\t\t\t: Crée la page qui d'addition d'une entrée à la table acteur \n
            AddRealisateur\t\t\t: Crée la page d'addition d'une entrée à la table realisateur \n
            AddFilm()\t\t\t: Crée la page d'addition d'une entrée dans la table film \n
            AddLink()\t\t\t: Crée la page qui ajoute dans la table XacteurFilm un lien entre les tables acteur et film \n
            BoutonAppuye()\t\t\t: Renvoie soit vers un sous-menu soit vers directement le contenu d'une table \n
            ConfirmedReal()\t\t\t: Ajoute une entrée à la table realisateur \n
            ConfirmedFilm()\t\t\t: Ajoute une entrée à la table Film \n
            ConfirmedXacteurFilm()\t\t: Ajoute le lien entre les tables acteur et film \n
            AddPersonnageXacteurFilm()\t: Ajoute l'attribut personnage_xaf dans la table xacteurfilm \n
            ConfirmedActeur()\t\t: Ajoute une entrée à la table Acteur \n
            AddIdNationaliteActeur()\t\t: Ajoute l'attribut/foreign key id_nationalite_acteur à la table acteur \n
            Window()\t\t\t: Affiche le menu principal \n
            OtherWindow()\t\t\t: Classe qui crée une fenêtre qui affiche un sous menu \n
            LastWindow()\t\t\t: Classe qui crée une fenêtre qui affiche le contenu d'une table \n
            ConfirmedBackToMenu()\t\t: Raffiche le menu principal  \n
            EmergencyWindow()\t\t: Fenêtre qui sert globalement quand c'est la merde, par exemple quand il faut ajouter une entrée dans une table à la volée \n
            ''')
        self.label.setStyleSheet(DefaultCSS)
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.bouton = QPushButton("Fermer cette fenêtre")
        self.bouton.setStyleSheet(DefaultCSS)
        self.bouton.clicked.connect(self.ButtonClose)
        self.layout.addWidget(self.bouton, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)



    def ButtonClose(self):
        self.close()



    def closeEvent(self, event):
        self.Window = Window("Projet NSI", 450, 800)
        self.Window.show()




class Window(QWidget):
    def __init__(self, Title: str, X: int, Y: int, Iteration: int = 0):
        super().__init__()
        self.Iteration = Iteration
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
            self.win = OtherWindow("Ajout {}".format(sender.text().lower()), self.X, self.Y, sender.text().lower(), self.Iteration)
            self.close()
            self.win.show()
        elif sender.text().lower() == "Creer les tables Acteur et XacteurFilm".lower():
            TableActeur()
            self.ActeurWasJustCreated = True                                            # Permet de relancer le programme une seconde fois après la création des tables
            self.close()
        else:
            self.win = LastWindow("Contenu de la table {}".format(sender.text().lower()), self.X, self.Y, sender.text().lower(), self.Iteration)
            self.close()
            self.win.show()



class OtherWindow(QWidget):
    def __init__(self, Title: str, X: int, Y: int, Bouton: str, Iteration: int = 0):
        super().__init__()
        self.Iteration = Iteration
        self.setWindowTitle(Title)
        self.Y, self.X = Y, X
        self.resize(self.Y, self.X)
        self.layout = QVBoxLayout()
        if Bouton == "realisateur":
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
        data = [self.NomRealisateurLine.text().capitalize(), self.PrenomRealisateurLine.text().capitalize(), self.DdnRealisateurLine.text()]
        self.curseur.execute('SELECT * FROM nationalite')
        print("475 \t: SELECT * FROM nationalite")
        b = self.curseur.fetchall()
        self.curseur.execute('SELECT * FROM realisateur')
        print("478 \t: SELECT * FROM realisateur")
        d = self.curseur.fetchall()
        Exist = False
        IsFound = False
        for c in range(len(d)):
            if data[0] + ' ' + data[1] == d[c][1].capitalize() + ' ' + d[c][2].capitalize():                  # Si le nom prenom entré (en minuscule) est égal à l'un présent dans la table realisateur
                print("484\tCe réalisateur existe déjà dans la table, son id est {}".format(d[c][0]))
                Exist = True 
        for c in range(len(b)):
            if self.NationaliteRealisateurLine.text().upper() == b[c][1]:                                                                 # Si la fin du tableau data[], qui contient la nationalité, est identique à l'une des valeurs de la table nationalité (le tableau ressemble à [id, nationalite], [id, nationalite], ...)
                data.append(b[c][0])                                                                        # Alors on affecte à la fin du tableau l'id de la nationalite indiquée par l'utilisateur
                IsFound = True
                break
        if not IsFound:                                                                                             # Si la nationalite n'est pas dans la table    
            try:
                int(self.NationaliteRealisateurLine.text().upper())
            except ValueError:
                if self.NationaliteRealisateurLine.text().upper() != '':
                    self.curseur.execute("INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(self.NationaliteRealisateurLine.text().upper()))     # Créer une nouvelle nationalité sachant que data[len(a) - 1] contient la nationalité entree par l'utilisateur
                    print("497 \t: INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(self.NationaliteRealisateurLine.text().upper()))
                    data.append(len(b) + 1)
            else:
                print("500\tLe nom de la nationalite doit être str")
                return "realisateur"
        if not Exist:
            try:
                int(data[0]), int(data[1])
            except ValueError:
                self.curseur.execute(req, data)
                print("507 \t: INSERT INTO realisateur (nom_realisateur, prenom_realisateur, ddn_realisateur, id_nationalite_realisateur) VALUES ('{}', '{}', {}, {})".format(data[0].capitalize(), data[1].capitalize(), data[2], data[3]))
            else:
                print("509\tERREUR : doit être de type str")
                return "realisateur"
        CloseAll(self.curseur, self.connexion)
        self.w = LastWindow("Contenu de la table Realisateur", self.Y, self.Y, "realisateur", self.Iteration)
        self.close()
        self.w.show()
    


    def ConfirmedFilm(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        req = 'INSERT INTO film (titre_film, annee_film, id_realisateur_film, id_nationalite_film, id_genre_film) VALUES (?, ?, ?, ?, ?)'
        data = [self.TitreFilmLine.text().capitalize(), self.AnneeFilmLine.text(), self.RealisateurFilmLine.text(), self.NationaliteFilmLine.text(), self.GenreFilmLine.text()]
        try:
            int(data[1])
        except ValueError:
            return "film"
        else:
            int(data[1])
            if data[1] == '':
                return "film"
        self.curseur.execute('SELECT * FROM nationalite')
        print("532 \t: SELECT * FROM nationalite")                                                                              #       |
        b = self.curseur.fetchall()                                                                                             #       |
        IsFound = False                                                                                                         #       |
        for c in range(len(b)):                                                                                                 #       |
            if data[len(data) - 2].upper() == b[c][1]:                                                                          #      PASSER D'UNE
                data[len(data) - 2] = b[c][0]                                                                                   #      NATIONALITE A UN ID
                IsFound = True                                                                                                  #       |
                break                                                                                                           #       |
        if not IsFound:                                                                                                         #       |
            try:
                int(data[len(data) - 2])
            except ValueError:
                if data[len(data) - 2] != '':
                    self.curseur.execute("INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(data[len(data) - 2])) #       |
                    print("546 \t: INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(data[len(data) - 2]))                        
                    print("547\tCette nationalité n'était pas dans la table, elle a donc été ajoutée")
                    data[len(data) - 2] = b[len(b) - 1][0] + 1
            else:
                print("550\tLe nom de la nationalite doit être str")
                return "film"
            
        self.curseur.execute('SELECT * FROM genre') 
        print("554 \t: SELECT * FROM genre")                                                                                            #       |
        b = self.curseur.fetchall()                                                                                             #       |
        IsFound = False                                                                                                         #       |
        for c in range(len(b)):                                                                                                 #       |
            if not IsFound and data[len(data) - 1].lower() == b[c][1].lower():                                                  #      PASSER D'UN GENRE A UN ID
                data[len(data) - 1] = b[c][0]                                                                                   #       |
                IsFound = True                                                                                                  #       |
        if not IsFound:                                                                                                         #       |
            try:
                int(data[len(data) - 1])
            except ValueError:
                if data[len(data) - 1] != '':
                    self.curseur.execute("INSERT INTO genre (nom_genre) VALUES ('{}')".format(data[len(data) - 1]))                     #       |
                    print("567 \t: INSERT INTO genre (nom_genre) VALUES ('{}')".format(data[len(data) - 1]))
                    print("568\tCe genre n'était pas dans la table, il a donc été ajouté")
                    data[len(data) - 1] = b[len(b) - 1][0] + 1
            else:
                print("571\tERREUR : doit être de type str")
                return "film"
        self.curseur.execute("SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")
        print("574 \t: SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")                                    #       |
        b = self.curseur.fetchall()                                                                                             #       |
        IsFound = False                                                                                                         #       |
        for c in range(len(b)):                                                                                                 #       |
            ConcD = b[c][1] + ' ' + b[c][2]                                                                                     #      PASSER D'UN NOM/PRENOM A UN ID                                               
            if not IsFound and data[len(data) - 3].lower() == ConcD.lower():                                                    #       |
                data[len(data) - 3] = b[c][0]                                                                                   #       |
                IsFound = True                                                                                                  #       |
        if not IsFound:                                                                                                         #       |
            print("583\tCe réalisateur n'est pas présent dans la table, vous allez être redirigé vers le programme d'ajout de réalisateur")
            CloseAll(self.curseur, self.connexion)
            NomPrenom = self.RealisateurFilmLine.text().split(" ")
            if len(NomPrenom) != 2:
                print("587\tLes prénoms/noms composés doivent être séparés d'un tiret (-)")
                self.close()
                self.EWin = EmergencyWindow(0)
                self.EWin.show()
            else:
                self.EWin = EmergencyWindow(0, NomPrenom[0], NomPrenom[1])
                self.EWin.show()
            self.connexion = sqlite3.connect(database)
            self.curseur = self.connexion.cursor()
            self.curseur.execute("SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")
            print("597 \t: SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")                                #       |
            b = self.curseur.fetchall()                                                                                         #       |
            IsFound = False                                                                                                     #       |
            for c in range(len(b)):                                                                                             #       |
                ConcD = b[c][1] + ' ' + b[c][2]                                                                                 #      PASSER D'UN NOM/PRENOM A UN ID                                               
                if data[len(data) - 3].lower() == ConcD.lower():                                                                #       |
                    data[len(data) - 3] = b[c][0]                                                                               #       |
                    IsFound = True                                                                                              #       |
            if not IsFound:                                                                                                     #       |
                print("606\tCe réalisateur n'est pas présent dans la table, faites attention à taper le même réalisateur dans le programme et dans la sous-programme d'ajout")
                CloseAll(self.curseur, self.connexion)
                return 1
        self.curseur.execute("SELECT titre_film, annee_film, id_realisateur_film, id_nationalite_film, id_genre_film FROM film")
        print("610 \t: SELECT titre_film, annee_film, id_realisateur_film, id_nationalite_film, id_genre_film FROM film")
        a = self.curseur.fetchall()
        Exists = False
        for i in range(len(a)):
            if a[i][0] == data[0] and a[i][1] == data[1] and a[i][2] == data[2] and a[i][3] == data[3] and a[i][4] == data[4]:
                print("615\tCe film est déja dans la table, il se trouve à l'indice {} et son id est {}".format(i, a[i][0]))
                Exists = True
                CloseAll(self.curseur, self.connexion)
                break
        if not Exists:
            try:
                int(data[0]), int(data[1]) , int(data[2])
            except ValueError:
                self.curseur.execute(req, data)
                print("624 \t: ", req, data)    
                CloseAll(self.curseur, self.connexion)
                self.setLayout(self.layout)
            else:
                print("628 \t: L'id du réalisateur doit être un entier et le nom/prenom doit être un str ")                  # ne s'executera normalement jamais car toutes les actions possibles sont couvertes, mais on sait jamais
                return "film"
        self.w = LastWindow("Contenu de la table film", self.X, self.Y, "film", self.Iteration)
        self.close()
        self.w.show()


    def ConfirmedXacteurFilm(self):
        ActeurId = self.MenuActeur.itemData(self.MenuActeur.currentIndex())                                     # Récupère l'id de l'acteur séléctionné
        FilmId = self.MenuFilm.itemData(self.MenuFilm.currentIndex())
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        if not self.PersonnageExists:
            self.curseur.execute("SELECT id_acteur_xaf, id_film_xaf FROM xacteurfilm WHERE id_acteur_xaf = {} AND id_film_xaf = {}".format(ActeurId, FilmId))
            print("642 \t: SELECT id_acteur_xaf, id_film_xaf FROM xacteurfilm WHERE id_acteur_xaf = {} AND id_film_xaf = {}".format(ActeurId, FilmId))
            if self.curseur.fetchall() == []:
                self.curseur.execute("INSERT INTO xacteurfilm (id_acteur_xaf, id_film_xaf) VALUES ({}, {})".format(ActeurId, FilmId))
                print("645 \t: INSERT INTO xacteurfilm (id_acteur_xaf, id_film_xaf) VALUES ({}, {})".format(ActeurId, FilmId))
                CloseAll(self.curseur, self.connexion)
                self.w = LastWindow("Contenu de la table xacteurfilm", self.X, self.Y, "xacteurfilm", self.Iteration)
                self.close()
                self.w.show()
            else:
                print("651 \t: Cet acteur a déjà été lié à ce film")
                CloseAll(self.curseur, self.connexion)
        if self.PersonnageExists:
            self.curseur.execute("SELECT personnage_xaf FROM xacteurfilm WHERE id_acteur_xaf = {} AND id_film_xaf = {}".format(ActeurId, FilmId))       # L'interêt de séléctionner le personnage seulement est qu'on peut séparer un retour "None" et un retour vide, afin de 
            print("655 \t: SELECT personnage_xaf FROM xacteurfilm WHERE id_acteur_xaf = {} AND id_film_xaf = {}".format(ActeurId, FilmId))                      # savoir si on doit ajouter 3 valeurs ou mettre à jour une ligne existante qui n'a pas encore de valeur "Personnage"
            a = self.curseur.fetchall()
            if a == []:                 # Si la ligne n'existe pas 
                try:
                    int(self.XacteurFilmPersonnage.text().capitalize())
                except ValueError:
                    self.curseur.execute("INSERT INTO xacteurfilm (id_acteur_xaf, id_film_xaf, personnage_xaf) VALUES ({}, {}, '{}')".format(ActeurId, FilmId, self.XacteurFilmPersonnage.text().capitalize()))
                    print("662 \t: INSERT INTO xacteurfilm (id_acteur_xaf, id_film_xaf, personnage_xaf) VALUES ({}, {}, '{}')".format(ActeurId, FilmId, self.XacteurFilmPersonnage.text().capitalize()))
                    CloseAll(self.curseur, self.connexion)
                    self.w = LastWindow("Contenu de la table xacteurfilm", self.X, self.Y, "xacteurfilm", self.Iteration)
                    self.close()
                    self.w.show()
                else:
                    print("668 \t: ERREUR : doit être de type str")
                    return "xacteurfilm"
            
            elif a[0][0] == None:       # Si la ligne existe MAIS n'a pas encore de valeur "Personnage" ce qui est possible si l'attribut a été ajouté après ajout d'acteurs
                self.curseur.execute("UPDATE xacteurfilm SET personnage_xaf = '{}' WHERE id_acteur_xaf = {} AND id_film_xaf = {}".format(self.XacteurFilmPersonnage.text().capitalize(), ActeurId, FilmId))
                print("673 \t: UPDATE xacteurfilm SET personnage_xaf = '{}' WHERE id_acteur_xaf = {} AND id_film_xaf = {}".format(self.XacteurFilmPersonnage.text().capitalize(), ActeurId, FilmId))
                CloseAll(self.curseur, self.connexion)
                self.w = LastWindow("Contenu de la table xacteurfilm", self.X, self.Y, "xacteurfilm", self.Iteration)
                self.close()
                self.w.show()
            else:
                print("679 \t: Cet acteur a déjà été lié à ce film")
                CloseAll(self.curseur, self.connexion)


    def AddPersonnageXacteurFilm(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        self.curseur.execute("ALTER TABLE xacteurfilm ADD personnage_xaf TEXT(64)")
        print("687 \t: ALTER TABLE xacteurfilm ADD personnage_xaf TEXT(64)")
        CloseAll(self.curseur, self.connexion)
        self.w = OtherWindow("Choix XacteurFilm", self.X, self.Y, "xacteurfilm", self.Iteration)
        self.close()
        self.w.show()
        

    def ConfirmedActeur(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        self.curseur.execute("PRAGMA table_info(acteur)")
        print("698 \t: PRAGMA table_info(acteur)")
        if len(self.curseur.fetchall()) <= 3:
            req = 'INSERT INTO acteur (nom_acteur, prenom_acteur) VALUES (?, ?)'
            data = [self.NomActeurLine.text().capitalize(), self.PrenomActeurLine.text().capitalize()]
            Exists = False
            self.curseur.execute("SELECT * FROM acteur")
            print("704 \t: SELECT * FROM acteur")
            b = self.curseur.fetchall()
            for i in range(len(b)):
                if data[0] + ' ' + data[1] == b[i][1].capitalize() + ' ' + b[i][2].capitalize():          # Si le nom prenom entré (en minuscule) est égal à l'un présent dans la table
                    print("708 \t: Cet acteur existe déjà dans la table, son id est {}".format(b[i][0]))
                    Exists = True
            if not Exists:
                try:
                    int(data[0]), int(data[1])
                except ValueError:
                   print("714 \t: ", req, data)
                   self.curseur.execute(req, data)
                else:
                    print("717 \t: ERREUR : doit être de type str")
                    return "acteur"
            CloseAll(self.curseur, self.connexion)
            self.w = LastWindow("Contenu de la table acteur", self.X, self.Y, "acteur", self.Iteration)
            self.close()
            self.w.show()
        else:
            req = "INSERT INTO acteur (nom_acteur, prenom_acteur, id_nationalite_acteur) VALUES (?, ?, ?)"
            data = [self.NomActeurLine.text().capitalize(), self.PrenomActeurLine.text().capitalize(), self.NationaliteLine.text().upper()]
            Exists = False
            NationaliteExists = False
            self.curseur.execute("SELECT * FROM acteur")
            print("729 \t: SELECT * FROM acteur")
            b = self.curseur.fetchall()
            self.curseur.execute("SELECT * FROM nationalite")
            print("732 \t: SELECT * FROM nationalite")
            a = self.curseur.fetchall()
            for i in range (len(a)):
                if self.NationaliteLine.text().upper() == a[i][1]:
                    data[2] = a[i][0]
                    NationaliteExists = True
            if not NationaliteExists:
                try:
                    int(self.NationaliteLine.text().upper())
                except ValueError:
                    if self.NationaliteLine.text().upper() != '':
                        self.curseur.execute("INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(self.NationaliteLine.text().upper()))
                        print("744 \t: INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(self.NationaliteLine.text().upper()))
                        data[2] = len(a) + 1
                else:
                    print("747 \t: Le nom de la nationalite doit être str")
                    return "acteur"
            for i in range(len(b)):
                if data[0] + ' ' + data[1] == b[i][1].capitalize() + ' ' + b[i][2].capitalize() and data[2] == b[i][3]:          # Si le nom prenom entré (en minuscule) est égal à l'un présent dans la table
                    print("751 \t: Cet acteur existe déjà dans la table, son id est {}".format(b[i][0]))
                    Exists = True
                if data[0] == b[i][1].capitalize() and data[1] == b[i][2].capitalize() and b[i][3] == None:
                    print("754 \t: UPDATE acteur SET personnage_xaf = '{}' WHERE nom_acteur = '{}' AND prenom_acteur = '{}'".format(data[2], data[0], data[1]))
                    self.curseur.execute("UPDATE acteur SET id_nationalite_acteur = {} WHERE nom_acteur = '{}' AND prenom_acteur = '{}'".format(data[2], data[0], data[1]))
                    Exists = True
            if not Exists:
                try:
                    int(data[0]), int(data[1])
                except ValueError:
                    print("761 \t: ", req, data)
                    self.curseur.execute(req, data) 
                else:
                    print("764 \t: ERREUR : doit être de type str")
                    return "acteur"
            CloseAll(self.curseur, self.connexion)
            self.w = LastWindow("Contenu de la table acteur", self.X, self.Y, "acteur", self.Iteration)
            self.close()
            self.w.show()


    def AddIdNationaliteActeur(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        self.curseur.execute("ALTER TABLE acteur RENAME TO oldacteur")
        print("776 \t: ALTER TABLE acteur RENAME TO oldacteur")
        self.curseur.execute("CREATE TABLE acteur (id_acteur INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nom_acteur TEXT NOT NULL, prenom_acteur TEXT NOT NULL, id_nationalite_acteur INTEGER, FOREIGN KEY(id_nationalite_acteur) REFERENCES nationalite(id_nationalite))")
        print("778 \t: CREATE TABLE acteur (id_acteur INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nom_acteur TEXT NOT NULL, prenom_acteur TEXT NOT NULL, id_nationalite_acteur INTEGER, FOREIGN KEY(id_nationalite_acteur) REFERENCES nationalite(id_nationalite))")
        self.curseur.execute("SELECT * FROM oldacteur")
        print("780 \t: SELECT * FROM oldacteur")
        old = self.curseur.fetchall()
        for i in range (len(old)):
            self.curseur.execute("INSERT INTO acteur (id_acteur, nom_acteur, prenom_acteur) VALUES ({}, '{}', '{}')".format(old[i][0], old[i][1].capitalize(), old[i][2].capitalize()))     # On copie les valeurs de l'ancienne table acteur vers la nouvelle
            print("784 \t: INSERT INTO acteur (id_acteur, nom_acteur, prenom_acteur) VALUES ({}, '{}', '{}')".format(old[i][0], old[i][1].capitalize(), old[i][2].capitalize()))
        self.curseur.execute("DROP TABLE oldacteur")            # Suppression de l'ancienne table acteur, qui ne sert plus à rien
        print("786 \t: DROP TABLE oldacteur")
        CloseAll(self.curseur, self.connexion)
        self.close()
        self.w = OtherWindow("Ajout d'un Acteur", self.X, self.Y, "acteur", self.Iteration)
        self.w.show()



class LastWindow(QWidget):
    def __init__(self, Title: str, X: int, Y: int, Table: str, Iteration: int = 0):
        super().__init__()
        self.Iteration = Iteration
        if Iteration >= Memory:
            self.close()
            self.EW = EmergencyWindow(2)
            self.EW.show()
        else:
            self.setStyleSheet(BackgroundCSS)
            self.setWindowTitle(Title)
            self.resize(Y, X)
            self.X, self.Y = X, Y
            self.Table = Table
            self.Hlayout = QHBoxLayout()
            self.layout = QVBoxLayout()
            self.connexion = sqlite3.connect(database)
            self.curseur = self.connexion.cursor()
            self.curseur.execute("SELECT * FROM {}".format(Table))
            print("813 \t: SELECT * FROM {}".format(Table))
            temp = self.curseur.fetchall()
            if temp == []:                                                  #   Si la table séléctionnée est vide
                self.resize(X, Y)
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
                self.BackToMenuButton = QPushButton("Retourner à l'accueil")
                self.BackToMenuButton.setStyleSheet(DefaultCSS)
                self.BackToMenuButton.clicked.connect(self.ConfirmedBackToMenu)
                self.layout.addWidget(self.BackToMenuButton, alignment=Qt.AlignCenter)
                self.setLayout(self.layout)
                CloseAll(self.curseur, self.connexion)


    def ConfirmedBackToMenu(self):
        self.window = Window("Projet NSI", self.X, self.Y, self.Iteration + 1)
        self.close()
        self.window.show()



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
        elif EmergencyId == 2:
            self.setWindowTitle("Memory Protection")
            self.resize(500, 400)
            self.setStyleSheet(BackgroundCSS)
            self.ErrorLabel = QLabel("En raison d'une erreur de programmation qui provoque\nune fuite de mémoire, Veuillez relancer le programme")
            self.ErrorLabel.setStyleSheet("color: red; font-size: 20px")
            self.layout.addWidget(self.ErrorLabel, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)


    def ConfirmedReal(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        req = 'INSERT INTO realisateur (nom_realisateur, prenom_realisateur, ddn_realisateur, id_nationalite_realisateur) VALUES (?, ?, ?, ?)'
        data = [self.NomRealisateurLine.text().capitalize(), self.PrenomRealisateurLine.text().capitalize(), self.DdnRealisateurLine.text()]
        self.curseur.execute('SELECT * FROM nationalite')
        print("888 \t: SELECT * FROM nationalite")
        b = self.curseur.fetchall()
        self.curseur.execute('SELECT * FROM realisateur')
        print("891 \t: \tSELECT * FROM realisateur")
        d = self.curseur.fetchall()
        Exist = False
        IsFound = False
        for c in range(len(d)):
            # print(data[0].lower() + ' ' + data[1].lower(), d[c][1].lower() + ' ' + d[c][2].lower(), data[0].lower() + ' ' + data[1].lower() == d[c][1].lower() + ' ' + d[c][2].lower())
            if data[0] + ' ' + data[1] == d[c][1].capitalize() + ' ' + d[c][2].capitalize():                  # Si le nom prenom entré (en minuscule) est égal à l'un présent dans la table realisateur
                print("898 \t: Ce réalisateur existe déjà dans la table, son id est {}".format(d[c][0]))
                Exist = True   
        for c in range(len(b)):
            if self.NationaliteRealisateurLine.text().upper() == b[c][1]:                                                                 # Si la fin du tableau data[], qui contient la nationalité, est identique à l'une des valeurs de la table nationalité (le tableau ressemble à [id, nationalite], [id, nationalite], ...)
                data.append(b[c][0])                                                                        # Alors on affecte à la fin du tableau l'id de la nationalite indiquée par l'utilisateur
                IsFound = True
                break
        if not IsFound:  
            try:                                                                                           # Si la nationalite n'est pas dans la table    
                int(self.NationaliteRealisateurLine.text().upper())
            except ValueError:
                if self.NationaliteRealisateurLine.text().upper() != '':
                    self.curseur.execute("INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(self.NationaliteRealisateurLine.text().upper()))     # Créer une nouvelle nationalité sachant que data[len(a) - 1] contient la nationalité entree par l'utilisateur
                    print("911 \t: INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(self.NationaliteRealisateurLine.text().upper()))
                    data.append(len(b) + 1)
            else:
                print("914 \t: Le nom de la nationalite doit être str")
                return "realisateur"
        if not Exist and len(data) == 4:
            try:
                int(data[0]), int(data[1])
            except ValueError:
                print("920 \t: ", req, data)
                self.curseur.execute(req, data)
            else:
                print("923 \t: ERREUR : doit être de type str")
                return "realisateur"
        CloseAll(self.curseur, self.connexion)
        self.close()


    def ConfirmedActeur(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        req = 'INSERT INTO acteur (nom_acteur, prenom_acteur) VALUES (?, ?)'
        data = [self.NomActeurLine.text().capitalize(), self.PrenomActeurLine.text().capitalize()]
        # Vérifier si l'entrée n'existe pas déjà
        Exists = False
        self.curseur.execute("SELECT * FROM acteur")
        print("937 \t: SELECT * FROM acteur")
        b = self.curseur.fetchall()
        for i in range(len(b)):
            if data[0] + ' ' + data[1] == b[i][1].capitalize() + ' ' + b[i][2].capitalize():          # Si le nom prenom entré (en minuscule) est égal à l'un présent dans la table
                print("941 \t: Cet acteur existe déjà dans la table, son id est {}".format(b[i][0]))
                Exists = True
        if not Exists:
            try:
                int(data[0]) , int(data[1])
            except ValueError:
                print("947 \t: ", req, data)
                self.curseur.execute(req, data)
            else:
                print("950 \t: ERREUR : doit être de type str")
                return "acteur"
        CloseAll(self.curseur, self.connexion)
        self.close()


    def AddIdNationaliteActeur(self):
        self.connexion = sqlite3.connect(database)
        self.curseur = self.connexion.cursor()
        self.curseur.execute("ALTER TABLE acteur RENAME TO oldacteur")
        print("960 \t: ALTER TABLE acteur RENAME TO oldacteur")
        self.curseur.execute("CREATE TABLE acteur (id_acteur INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nom_acteur TEXT NOT NULL, prenom_acteur TEXT NOT NULL, id_nationalite_acteur INTEGER, FOREIGN KEY(id_nationalite_acteur) REFERENCES nationalite(id_nationalite))")
        print("962 \t: CREATE TABLE acteur (id_acteur INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nom_acteur TEXT NOT NULL, prenom_acteur TEXT NOT NULL, id_nationalite_acteur INTEGER, FOREIGN KEY(id_nationalite_acteur) REFERENCES nationalite(id_nationalite))")
        self.curseur.execute("SELECT * FROM oldacteur")
        print("964 \t: SELECT * FROM oldacteur")
        old = self.curseur.fetchall()
        for i in range (len(old)):
            self.curseur.execute("INSERT INTO acteur (id_acteur, nom_acteur, prenom_acteur) VALUES ({}, '{}', '{}')".format(old[i][0], old[i][1].capitalize(), old[i][2].capitalize()))
            print("968 \t: INSERT INTO acteur (id_acteur, nom_acteur, prenom_acteur) VALUES ({}, '{}', '{}')".format(old[i][0], old[i][1].capitalize(), old[i][2].capitalize()))
        self.curseur.execute("DROP TABLE oldacteur")
        print("970 \t: DROP TABLE oldacteur")
        CloseAll(self.curseur, self.connexion)
        self.close()
        


app = QApplication.instance() 
if not app:
    app = QApplication([])

with open('settings', 'a+') as fichier:
    fichier.seek(0)        # fseek(SEEK_SET)

    if fichier.readline() == '':
        fichier.write("FirstLaunchFalse")
        FW = FirstWindow()
        FW.show()
        fichier.close()
        app.exec()

    else:
        win = Window("Projet NSI", X, Y)
        win.show()
        app.exec()
        app2 = QApplication.instance() 
        if not app2:
            app2 = QApplication([])
        if win.ActeurWasJustCreated:
            win.close()
            win2 = Window("Projet NSI", X, Y)
            win2.show()
            app2.exec()