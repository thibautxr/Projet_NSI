import sqlite3
database = "Film_realisateur_genre_nationalite.db"
 
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

    curseur.close()
    connexion.commit()
    connexion.close()
    return boool


def add_realisateur():
    connexion = sqlite3.connect(database)
    curseur = connexion.cursor()
    if not TableExist("nationalite"):
        curseur.close()
        connexion.commit()
        connexion.close()
        return 1
    
    if not TableExist("realisateur"):
        curseur.close()
        connexion.commit()
        connexion.close()
        return 1
 
    req = 'INSERT INTO realisateur (nom_realisateur, prenom_realisateur, ddn_realisateur, id_nationalite_realisateur) VALUES (?, ?, ?, ?)'
    data = []
    a = ['Entrez le nom du réalisateur : ', 'Entrez le prénom du réalisateur : ', 'Entrez la ddn du réalisateur (aaaa-mm-jj) : ', 'Entrez la nationalité du realisateur (FR, US, GB) : '] #liste de tous les prompts affichés à l'écran
    for i in range(len(a)):                                 # Pour afficher tous les prompt du tableau a[]
        print(a[i])
        data.append(str(input()))                           # Ici on ajoute toutes les réponses de l'utilisateur au tableau data[] qui remplaceront les '?' de la requête VALUES (?, ?, ?, ?)
        if i == len(a) - 1:                                 # Quand on a completé tous les champs
            curseur.execute('SELECT * FROM nationalite')
            b = curseur.fetchall()                          # La variable contient les valeurs de la table nationalité, elle est sous la forme : [[id, nationalite], [id, nationalite], ...]
            IsFound = False
            for c in range(len(b)):
                if data[len(a) - 1] == b[c][1]:             # Si la fin du tableau data[], qui contient la nationalité, est identique à l'une des valeurs de la table nationalité (le tableau ressemble à [id, nationalite], [id, nationalite], ...)
                    data[len(a) - 1] = b[c][0]              # Alors on affecte à la fin du tableau l'id de la nationalite indiquée par l'utilisateur
                    IsFound = True
            if not IsFound:                                 # Si la nationalite n'est pas dans la table    
                curseur.execute("INSERT INTO nationalite (nom_nationalite) VALUES ('{}')".format(data[len(a) - 1]))     # Créer une nouvelle nationalité sachant que data[len(a) - 1] contient la nationalité entree par l'utilisateur


    curseur.execute(req, data)
    curseur.execute("SELECT * FROM realisateur")
    temp = curseur.fetchall()
    print("Contenu de la table \"realisateur\" : ")
    for row in temp:
        print(row)


    curseur.close()
    connexion.commit()
    connexion.close()