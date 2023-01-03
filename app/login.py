import mysql.connector
import sys
import argon2


try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3307",
        password="root",
        database="universite",
    )
except mysql.connector.Error as e:
    print("Exception : ", e)
    sys.exit(1)

cur = con.cursor()
ph = argon2.PasswordHasher()


def new_account(username, password, type, id, status):
    """permet de créer un utilisateur lier a un compte en fonction de l'id
        et du type

    Args:
        username (str): nom d'utilisateur
        password (str): mot de passe
        type (str): only "prof" ou "etu"
        id (str): id de la personne
        status (int): status du compte (0 inactif 1 actif)

    Returns:
        bool: renvoie True seulement quand le compte est créer
    """
    assert isinstance(username, str)
    assert isinstance(password, str)
    assert isinstance(type, str)
    assert isinstance(id, int)
    assert isinstance(status, int)

    cur.execute(f"SELECT type FROM login WHERE id_personne = '{id}'")
    # Il peut y avoir un id prof et un id etudiant identique
    # On vérifie donc que selon le type, il n'y a pas de double compte

    res = cur.fetchall()
    if res != []:
        for i in res:
            if i[0] == type:
                return
    if type == "etu":
        cur.execute(f"SELECT * FROM etudiant WHERE id_etudiant = '{id}'")
        if len(cur.fetchall()) != 1:
            return
    # Pour les étudiants, on vérifie que le compte est bien associé a un élève
    if type == "prof":
        cur.execute(f"SELECT * FROM prof WHERE id_prof= '{id}'")
        if len(cur.fetchall()) != 1:
            return
    # Pareil pour les professeurs on vérifie que c'est bien associé

    hash = ph.hash(password)
    if ph.check_needs_rehash(hash):
        hash = ph.hash(password)
    # On hash le mot de passe, car on ne stocke pas de mot de passe brut
    # dans la base de données. Si il y a besoin d'un rehashage, on refait.

    try:
        cur.execute(
            f"INSERT INTO login \
            (id_login, username, password, type, id_personne, status) \
            VALUES (NULL, '{username}', '{hash}', '{type}', {id}, {status});"
        )
    except mysql.connector.Error:
        return
    con.commit()
    return True
    # On ajoute donc les données d'un nouveau compte et on renvoie True


def verify(username, password):
    assert isinstance(username, str)
    assert isinstance(password, str)

    cur.execute(f"SELECT password FROM login WHERE username = '{username}'")
    user = cur.fetchall()
    if user == []:
        return
    hash = user[0][0]
    try:
        ph.verify(hash, password)
    except argon2.exceptions.VerifyMismatchError:
        return
    # On récupère le hash de l'utilisateur on est vérifie les mot de passes
    # Si les mots de passes sont différent on return

    cur.execute(
        f"SELECT type, id_personne, status FROM login \
        WHERE username = '{username}'"
    )
    id = cur.fetchone()
    if id[2] == 0:
        return
    return id
    # Sinon, on récupère l'ID de l'étudiant qui va nous servir sur le panel


def nom_prenom(type, id):
    assert isinstance(type, str)
    assert isinstance(int(id), int)

    if type == "etu":
        cur.execute(f"SELECT nom,prenom,sexe FROM etudiant \
        WHERE id_etudiant = '{id}'")
    elif type == "prof":
        cur.execute(f"SELECT nom,prenom,sexe FROM prof WHERE id_prof = '{id}'")
    return cur.fetchone()


def create():
    # ack = new_account("prof", "prof", "prof", 1)
    # ack = new_account("etu", "etu", "etu", 3)
    ack = new_account("photo", "photo", "etu", 4, 0)
    if not ack:
        print("Erreur")
    else:
        print("Votre compte a été créé")


if __name__ == "__main__":
    create()
    id = verify("photo", "photo")
    if not id:
        print("mauvais mot de passe")
    else:
        print(id)
