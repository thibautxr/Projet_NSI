import sqlite3
database = "Film_realisateur_genre_nationalite.db"
print("tapez help(main) pour avoir une explication rapide de chaque fonction")

def main():
    '''
    CloseAll()          : ferme simplement une connexion à une base de donnée, fonction créée pour gagner de la place et avoir un code plus simple à comprendre
    TableExist()        : Permet de savoir si une table existe, évite d'avoir une fatal error dans la console qui ferait crash le programme
    AddRealisateur()    : Ajoute une entrée dans la table Realisateur si elle existe
    AddFilm()           : Ajoute une entrée dans la table film si elle existe
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


def AddRealisateur():
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()
    if not TableExist("nationalite"):
        CloseAll(curseur, connexion)
        return 1
    
    if not TableExist("realisateur"):
        CloseAll(curseur, connexion)
        return 1
 
    req = 'INSERT INTO realisateur (nom_realisateur, prenom_realisateur, ddn_realisateur, id_nationalite_realisateur) VALUES (?, ?, ?, ?)'
    data = []
    curseur.execute('SELECT * FROM nationalite')
    t = curseur.fetchall()
    temp = ''
    for i in t:
        temp = temp + i[1] + ", "
    a = ['Entrez le nom du réalisateur : ', 'Entrez le prénom du réalisateur : ', 'Entrez la ddn du réalisateur (aaaa-mm-jj) : ', 'Entrez la nationalité du realisateur ($) : '] #liste de tous les prompts affichés à l'écran
    for i in range(len(a)):
        a[i] = a[i].replace('$', temp[:-2])
    for i in range(len(a)):                                 # Pour afficher tous les prompt du tableau a[]
        data.append(str(input(a[i])))                       # Ici on ajoute toutes les réponses de l'utilisateur au tableau data[] qui remplaceront les '?' de la requête VALUES (?, ?, ?, ?)
        if i == len(a) - 1:                                 # Quand on a completé tous les champs
            curseur.execute('SELECT * FROM nationalite')
            b = curseur.fetchall()                          # La variable contient les valeurs de la table nationalité, elle est sous la forme : [[id, nationalite], [id, nationalite], ...]
            IsFound = False
            for c in range(len(b)):
                if data[len(a) - 1].upper() == b[c][1]:     # Si la fin du tableau data[], qui contient la nationalité, est identique à l'une des valeurs de la table nationalité (le tableau ressemble à [id, nationalite], [id, nationalite], ...)
                    data[len(a) - 1] = b[c][0]              # Alors on affecte à la fin du tableau l'id de la nationalite indiquée par l'utilisateur
                    IsFound = True
                    break
            if not IsFound:                                 # Si la nationalite n'est pas dans la table    
                curseur.execute("INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(data[len(a) - 1]))     # Créer une nouvelle nationalité sachant que data[len(a) - 1] contient la nationalité entree par l'utilisateur
                data[len(a) - 1] = len(t) + 1

    curseur.execute(req, data)
    curseur.execute("SELECT * FROM realisateur")
    temp = curseur.fetchall()
    CloseAll(curseur, connexion)
    return temp[len(temp) - 1][0]



# Composition de la table film : id_film, titre_film, annee_film, id_realisateur_film, id_nationalite_film, id_genre_film
def AddFilm():
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()

    if not TableExist("film"):
        CloseAll(curseur, connexion)
        return 1

    if not TableExist("nationalite"):
        CloseAll(curseur, connexion)
        return 1

    if not TableExist("genre"):
        CloseAll(curseur, connexion)
        return 1

    if not TableExist("realisateur"):
        CloseAll(curseur, connexion)
        return 1

    curseur.execute('SELECT * FROM nationalite')
    a = curseur.fetchall()
    temp = ''
    for i in a:
        temp = temp + i[1] + ", "
    req = 'INSERT INTO film (titre_film, annee_film, id_realisateur_film, id_nationalite_film, id_genre_film) VALUES (?, ?, ?, ?, ?)'
    data = []
    a = ["Entrez le titre du film : ", "Entrez l'année de sortie du film : ", "Entrez le Nom Prenom du réalisateur : ", "Entrez la nationalité du film ($) : ", "Entrez le genre du film : "]
    for i in range(len(a)):
        a[i] = a[i].replace('$', temp[:-2])                      # On remplace le '$' de la chaine a par toutes les nationalités contenues dans la table
    for i in range (len(a)):
        data.append(str(input(a[i])))
        if i == len(a) - 1:
            curseur.execute('SELECT * FROM nationalite')                                                                #       |
            b = curseur.fetchall()                                                                                      #       |
            IsFound = False                                                                                             #       |
            for c in range(len(b)):                                                                                     #       |
                if data[len(data) - 2].upper() == b[c][1]:                                                              #       |
                    data[len(data) - 2] = b[c][0]                                                                       #       PASSER D'UNE NATIONALITE A UN ID
                    IsFound = True                                                                                      #       |
                    break                                                                                               #       |
            if not IsFound:                                                                                             #       |
                curseur.execute("INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(data[len(data) - 2]))  #       |
                print("Cette nationalité n'était pas dans la table, elle a donc été ajoutée")                           #       |

        

            curseur.execute('SELECT * FROM genre')                                                                      #       |
            b = curseur.fetchall()                                                                                      #       |
            IsFound = False                                                                                             #       |
            for c in range(len(b)):                                                                                     #       |
                if data[len(data) - 1].upper() == b[c][1]:                                                              #       PASSER D'UN
                    data[len(data) - 1] = b[c][0]                                                                       #       GENRE A UN ID
                    IsFound = True                                                                                      #       |
            if not IsFound:                                                                                             #       |
                curseur.execute("INSERT INTO genre (nom_genre) VALUES ('{}')".format(data[len(data) - 1]))              #       |
                print("Ce genre n'était pas dans la table, il a donc été ajouté")                                       #       |
                data[len(data) - 1] = b[len(b) - 1][0]



            curseur.execute("SELECT id_realisateur, nom_realisateur, prenom_realisateur FROM realisateur")              #       |
            b = curseur.fetchall()                                                                                      #       |
            IsFound = False                                                                                             #       |
            for c in range(len(b)):                                                                                     #       |
                ConcD = b[c][1] + b[c][2]                                                                               #       PASSER D'UN NOM/PRENOM A UN ID                                               
                if data[len(data) - 3].upper() == ConcD:                                                                #       |
                    data[len(data) - 3] = b[c][0]                                                                       #       |
                    IsFound = True                                                                                      #       |
            if not IsFound:                                                                                             #       |
                print("Ce réalisateur n'est pas présent dans la table, vous allez être redirigé vers le programme d'ajout de réalisateur")
                CloseAll(curseur, connexion)
                print(req, data)
                data[len(data) - 3] = AddRealisateur()

    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()
    curseur.execute(req, data)
    CloseAll(curseur, connexion)

help(main)