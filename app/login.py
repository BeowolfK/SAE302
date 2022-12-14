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
else:
    print("Connexion réussie")

cur = con.cursor()
ph = argon2.PasswordHasher()


def new_account(username, password, type, id):
    assert isinstance(username, str)
    assert isinstance(password, str)
    assert isinstance(type, str)
    assert isinstance(id, int)

    cur.execute(f"SELECT type FROM login WHERE id_personne = '{id}'")
    res = cur.fetchall()
    if res != []:
        for i in res:
            if i[0] == type:
                return
    if type == "etu":
        cur.execute(f"SELECT * FROM etudiant WHERE id_etudiant = '{id}'")
        if len(cur.fetchall()) != 1:
            return
    if type == "prof":
        cur.execute(f"SELECT * FROM prof WHERE id_prof= '{id}'")
        if len(cur.fetchall()) != 1:
            return

    hash = ph.hash(password)
    if ph.check_needs_rehash(hash):
        hash = ph.hash(password)

    try:
        cur.execute(
            f"INSERT INTO `login` \
            (`id_login`, `username`, `password`, `type`, `id_personne`) \
            VALUES (NULL, '{username}', '{hash}', '{type}', '{id}'); "
        )
    except mysql.connector.Error:
        return
    con.commit()
    return True


def verify(username, password):
    assert isinstance(username, str)
    assert isinstance(password, str)

    cur.execute(f"SELECT password FROM login WHERE username = '{username}'")
    hash = cur.fetchone()[0]
    try:
        ph.verify(hash, password)
    except argon2.exceptions.VerifyMismatchError:
        return

    cur.execute(
        f"SELECT type, id_personne FROM login WHERE username = '{username}'"
        )
    id = cur.fetchone()
    return id


def create():
    # ack = new_account("prof", "prof", "prof", 1)
    ack = new_account("etu", "etu", "etu", 3)
    if not ack:
        print("Erreur")
    else:
        print("Votre compte a été créé")


if __name__ == "__main__":
    # create()
    id = verify("etu", "etu")
    if not id:
        print("mauvais mot de passe")
    else:
        print(id)
