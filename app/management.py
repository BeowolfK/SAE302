import mysql.connector
import sys
import random
from login import new_account
import re

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


def info_etu(id):
    """Renvoie les informations de l'etudiant

    Args:
        id (int): id de l'etudiant dans la base de données

    Returns:
        list: [Mr/Mme Nom Prenom, annee]
    """
    assert isinstance(id, int)
    cur.execute(
        f"SELECT CASE sexe \
        WHEN 'M' THEN CONCAT('Mr', ' ', nom, ' ', prenom) \
        ELSE CONCAT('Mme', ' ', nom, ' ', prenom) END, CONCAT(annee, 'A') \
        FROM etudiant WHERE id_etudiant = {id};"
    )
    info = cur.fetchone()
    return f"{info[0].title()} - {info[1]}"


def info_prof(id):
    """Renvoie les informations du prof

    Args:
        id (int): id du prof dans la base de données

    Returns:
        list: [Mr/Mme Nom Prenom, annee]
    """
    assert isinstance(id, int)
    cur.execute(
        f"SELECT CASE sexe \
        WHEN 'M' THEN CONCAT('Mr', ' ', nom, ' ', prenom) \
        ELSE CONCAT('Mme', ' ', nom, ' ', prenom) END \
        FROM prof WHERE id_prof = {id};"
    )
    info = cur.fetchone()
    return f"{info[0].title()}"


def prof_nom(res):
    """_summary_

    Args:
        res (list): _description_

    Returns:
        list: _description_
    """
    final = []
    for tup in res:
        cur.execute(
            f"SELECT CASE prof.sexe \
            WHEN 'M' THEN CONCAT('Mr', ' ', prof.nom, ' ', prof.prenom) \
            ELSE CONCAT('Mme', ' ', prof.nom, ' ', prof.prenom) END \
            FROM enseigne INNER JOIN prof ON enseigne.id_prof = prof.id_prof \
            WHERE id_matiere = {tup[0]};"
        )
        list_name = []
        for tuple_name in cur.fetchall():
            list_name.append(tuple_name[0])
        final.append([tup[1], list_name, *tup[2:]])
    return final


def prof_enseigne(id):
    cur.execute(f"Select id_matiere from enseigne where id_prof = {id}")
    matiere = cur.fetchall()
    nom_matiere = []
    for id_mat in matiere:
        cur.execute(f"select nom from matiere where id_matiere = {id_mat[0]}")
        nom_matiere.append(cur.fetchone()[0])
    return nom_matiere


def panel_note(id):
    """Renvoie une liste contenant une liste [matiere, [prof], moyenne]
        list [prof] renvoie une liste de tout les profs enseignant la matiere

    Args:
        id (int): id de l'étudiant

    Returns:
        list: [matiere, [prof], moyenne]
    """
    assert isinstance(id, int)
    cur.execute(
        f"SELECT note.id_matiere, matiere.nom, AVG(NOTE) FROM note \
        INNER JOIN matiere ON note.id_matiere = matiere.id_matiere \
        WHERE note.id_etudiant = {id} GROUP BY note.id_matiere;"
    )
    res = prof_nom(cur.fetchall())
    return res


def matiere(id):
    cur.execute(
        f"SELECT matiere.id_matiere, matiere.nom FROM etudiant \
        INNER JOIN matiere ON etudiant.annee = matiere.annee \
        WHERE id_etudiant = {id} GROUP BY id_matiere;"
    )
    res = prof_nom(cur.fetchall())
    return res


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, "rb") as file:
        binaryData = file.read()
    # Return the binary format
    return binaryData


def generate_username(name):
    first_letter = name[0].lower()
    random_string = "".join(str(random.randint(0, 9)) for _ in range(8))
    final_string = first_letter + random_string
    return final_string


def is_name(name):
    regex = r"^[a-zA-Z-]+$"
    if re.search(regex, name):
        return True
    return


def uniq_username(name):
    uniq = True
    while uniq:
        username = generate_username(name)
        cur.execute(f"SELECT * FROM login WHERE username = '{username}';")
        uniq = cur.fetchone()
    return username


def new_etudiant(nom, prenom, annee, sexe, filename, mdp):
    """ajoute un étudiant dans la base de données

    Args:
        nom (str): nom de l'étudiant
        prenom (str): prenom de l'étudiant
        annee (int): annee de l'étudiant
        sexe (str): sexe de l'étudiant
        filename (str): chemin d’accès de la photo de l'étudiant
        mdp (str): mdp de l'étudiant
    """
    assert isinstance(nom, str)
    assert isinstance(prenom, str)
    # assert is_name(nom)
    # assert is_name(prenom)
    assert isinstance(annee, int)
    assert annee == 1 or annee == 2
    assert isinstance(sexe, str)
    assert sexe == "M" or sexe == "F"
    photo = convertToBinaryData(filename)
    try:
        cur.execute(
            "INSERT INTO etudiant (nom, prenom, annee, photo, sexe) \
            VALUES (%s, %s, %s, %s, %s)",
            (nom, prenom, annee, photo, sexe),
        )
        con.commit()
    except Exception:
        return
    username = uniq_username(nom)
    cur.execute("SELECT LAST_INSERT_ID();")
    id = int(cur.fetchone()[0])
    res = new_account(username, mdp, "etu", id, 0)
    if res:
        return True
    return


def add_note(note: float, id_matiere: int, id_etu: int):
    """ajoute une note dans la base de données en fonction
    de la matiere et de l'étudiant

    Args:
        note (float): note obtenue par un etudiant dans une matiere
        id_matiere (int): id de la matiere
        id_etu (int): id de l'etudiant
    """
    try:
        cur.execute(
            f"INSERT INTO note (note, id_matiere, id_etudiant) \
            VALUES ({note}, {id_matiere}, {id_etu});"
        )
        con.commit()
    except Exception as e:
        print(e)


def liste_etu():
    cur.execute(
        "SELECT username, nom, prenom, annee, \
        sexe, status, id_login, id_personne \
        FROM login \
        INNER JOIN etudiant ON login.id_personne = etudiant.id_etudiant \
        WHERE login.type = 'etu';"
    )
    return cur.fetchall()


def change_status(status, id):
    cur.execute(f"UPDATE login SET status={status} WHERE id_login = {id};")
    con.commit()


def get_id(nom, prenom):
    """Renvoie l'id correspondant au nom et prénom demandé

    Args:
        nom (str): nom de l'etudiant
        prenom (str): prenom de l'etudiant
    """
    cur.execute(
        f"SELECT id_etudiant from etudiant WHERE nom = '{nom}' and prenom = '{prenom}'"
    )
    id = cur.fetchone()
    return id


# Fonction pannel prof


def get_student(study):

    cur.execute(f"Select annee from matiere where matiere.nom = '{study}' ")
    anne_mat = cur.fetchone()[0]

    cur.execute(
        f"Select etudiant.id_etudiant,etudiant.nom,prenom,etudiant.annee \
        from etudiant \
        inner join matiere \
        where matiere.annee = etudiant.annee and etudiant.annee = {anne_mat} and matiere.nom = '{study}' "
    )
    all_student = cur.fetchall()
    return all_student


def prof_enseigne(id):
    cur.execute(f"Select id_matiere from enseigne where id_prof = {id}")
    matiere = cur.fetchall()
    nom_matiere = []
    for id_mat in matiere:
        cur.execute(f"select nom from matiere where id_matiere = {id_mat[0]}")
        nom_matiere.append(cur.fetchone()[0])
    return nom_matiere


def get_student_vie_scolaire(name, first_name, year):

    cur.execute(
        f"Select * \
        from etudiant \
        inner join matiere \
        where matiere.annee = etudiant.annee and etudiant.nom = '{name}' and etudiant.prenom = '{first_name}' and etudiant.annee = '{year}'"
    )
    all_student = cur.fetchall()
    return all_student


if __name__ == "__main__":
    print(matiere(1))
