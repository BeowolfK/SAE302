import mysql.connector
import sys
import argon2


try:
    con = mysql.connector.connect(
        host="54.37.226.86",
        user="sae_kivy",
        port="3306",
        password="Sae302!client",
        database="universite",
        auth_plugin="mysql_native_password",
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
        if len(cur.fetchall()) >= 1:
            return
    # Pour les étudiants, on vérifie que le compte est bien associé a un élève
    if type == "prof":
        cur.execute(f"SELECT * FROM prof WHERE id_prof= '{id}'")
        if len(cur.fetchall()) >= 1:
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
    except mysql.connector.Error as e:
        print(e)
        return
    con.commit()
    return True
    # On ajoute donc les données d'un nouveau compte et on renvoie True


def verify(username, password):
    """Vérifie les identifiants d'un utilisateur

    Args:
        username (str): nom d'utilisateur
        password (str): mot de passe

    Returns:
        tuple: renvoie un tuple avec le type de compte, l'id de la personne et
        le status du compte
    """
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


def nom_prenom(type: str, id: int) -> tuple:
    """
    Args:
        type (str): type de la personne (etu ou prof)
        id (int): id de la personne

    Returns:
        tuple: tuple contenant le nom, le prénom et le sexe de la personne
    """
    assert isinstance(type, str)
    assert isinstance(int(id), int)

    if type == "etu":
        cur.execute(
            f"SELECT nom,prenom,sexe FROM etudiant \
        WHERE id_etudiant = '{id}'"
        )
    elif type == "prof":
        cur.execute(f"SELECT nom,prenom,sexe FROM prof WHERE id_prof = '{id}'")
    return cur.fetchone()


if __name__ == "__main__":
    id = verify("etu", "etu")
    if not id:
        print("mauvais mot de passe")
    else:

        print(id)
