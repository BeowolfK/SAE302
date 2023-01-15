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


def prof_nom(id):
    cur.execute(
        f"SELECT CASE prof.sexe \
        WHEN 'M' THEN CONCAT('Mr', ' ', prof.nom, ' ', prof.prenom) \
        ELSE CONCAT('Mme', ' ', prof.nom, ' ', prof.prenom) END \
        FROM enseigne INNER JOIN prof ON enseigne.id_prof = prof.id_prof \
        WHERE id_matiere = {id};"
    )
    return cur.fetchall()


def prof_enseigne(id):
    cur.execute(f"SELECT id_matiere FROM enseigne WHERE id_prof = {id}")
    matiere = cur.fetchall()
    nom_matiere = []
    for id_mat in matiere:
        cur.execute(f"SELECT nom FROM matiere WHERE id_matiere = {id_mat[0]}")
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
    res = cur.fetchall()
    final = []
    for tup in res:
        noms = prof_nom(tup[0])
        list_name = []
        for tuple_name in noms:
            list_name.append(tuple_name[0])
        final.append([tup[1], list_name, *tup[2:]])
    return final


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


def add_note(note: float, commentaire: str, id_matiere: int, id_etu: int):
    """ajoute une note dans la base de données en fonction
    de la matiere et de l'étudiant

    Args:
        note (float): note obtenue par un etudiant dans une matiere
        id_matiere (int): id de la matiere
        id_etu (int): id de l'etudiant
    """
    try:
        cur.execute(
            f"INSERT INTO note (note, commentaire, id_matiere, id_etudiant) \
            VALUES ({note}, '{commentaire}' ,{id_matiere}, {id_etu});"
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
    """Renvoie l'id correspondant au nom et prénom demANDé

    Args:
        nom (str): nom de l'etudiant
        prenom (str): prenom de l'etudiant
    """
    cur.execute(
        f"SELECT id_etudiant FROM etudiant \
        WHERE nom = '{nom}' AND prenom = '{prenom}'"
    )
    id = cur.fetchone()
    return id


def get_student(study):
    cur.execute(f"SELECT annee FROM matiere WHERE matiere.nom = '{study}' ")
    annee_mat = cur.fetchone()[0]

    cur.execute(
        f"SELECT etudiant.id_etudiant,etudiant.nom,prenom,etudiant.annee \
        FROM etudiant \
        INNER JOIN matiere \
        WHERE matiere.annee = etudiant.annee \
        AND etudiant.annee = {annee_mat} \
        AND matiere.nom = '{study}' "
    )
    all_student = cur.fetchall()
    return all_student


def get_student_vie_scolaire(name, first_name, year):
    cur.execute(
        f"SELECT * FROM etudiant INNER JOIN matiere \
        WHERE matiere.annee = etudiant.annee \
        AND etudiant.nom = '{name}' \
        AND etudiant.prenom = '{first_name}' \
        AND etudiant.annee = '{year}'"
    )
    return cur.fetchall()


def add_absence_vie_scolaire(id_etu, id_teacher, mat, dates, hour, comment):
    """Fait une requête pour insérer des données dans la table absence"""
    cur.execute(
        f"INSERT INTO absence \
        (id_etudiant, id_prof, matiere, date, heure, commentaire) \
        VALUES \
        ({id_etu}, {id_teacher},'{mat}','{dates}','{hour}','{comment}');"
    )
    con.commit()


def add_retard_vie_scolaire(id_etu, id_teacher, mat, dates, hour, comment):
    cur.execute(
        f"INSERT INTO retard \
        (id_etudiant, id_prof, matiere, date, heure,raison) \
        VALUES \
        ({id_etu}, {id_teacher},'{mat}','{dates}','{hour}','{comment}');"
    )
    con.commit()


def add_exclusion_vie_scolaire(id_etu, id_teacher, mat, dates, hour, comment):
    cur.execute(
        f"INSERT INTO exclusion \
        (id_etudiant, id_prof, matiere, date, heure,raison) \
        VALUES \
        ({id_etu}, {id_teacher},'{mat}','{dates}','{hour}','{comment}');"
    )
    con.commit()


def get_id_mat(nom_mat):
    cur.execute(f"SELECT id_matiere from matiere where nom = '{nom_mat}'")
    return cur.fetchone()


def list_mat():
    cur.execute("SELECT * FROM matiere")
    matiere = []
    for id in cur.fetchall():
        noms = [tup[0].title() for tup in prof_nom(id[0])]
        matiere.append([id[0], id[1], noms, id[2]])
    return matiere


def add_mat(name, annee):
    cur.execute(
        f"INSERT INTO matiere (nom, annee) \
        VALUES ('{name}', '{annee}')"
    )
    con.commit()


def delete_mat(id, *args):
    cur.execute(f"DELETE FROM matiere WHERE id_matiere = {id}")
    con.commit()


def mat_by_prof(id):
    cur.execute(
        f"SELECT matiere.id_matiere, matiere.nom FROM matiere \
        INNER JOIN enseigne ON matiere.id_matiere = enseigne.id_matiere \
        WHERE enseigne.id_prof = {id};"
    )
    return cur.fetchall()


def all_prof():
    cur.execute(
        "SELECT id_prof, \
        CASE prof.sexe \
        WHEN 'M' THEN CONCAT('Mr', ' ', prof.nom, ' ', prof.prenom) \
        ELSE CONCAT('Mme', ' ', prof.nom, ' ', prof.prenom) \
        END \
        FROM prof;"
    )
    return cur.fetchall()


def list_prof():
    res = all_prof()
    prof = []
    for id in res:
        mat = mat_by_prof(id[0])
        prof.append([id[0], id[1], [nom[1].title() for nom in mat]])
    return prof


def delete_prof(id, *args):
    cur.execute(f"DELETE FROM prof WHERE id_prof = {id}")
    con.commit()


def add_prof(nom, prenom, sexe):
    try:
        cur.execute(
            f"INSERT INTO prof (nom, prenom, sexe) \
            VALUES ('{nom}', '{prenom}', '{sexe}')"
        )
    except Exception:
        return False
    else:
        return True


def all_mat():
    cur.execute("SELECT * FROM matiere")
    return cur.fetchall()


def assign_mat_prof(id_prof, id_mat):
    cur.execute(f"SELECT id_prof FROM enseigne WHERE id_matiere = {id_mat}")
    res = [id[0] for id in cur.fetchall()]
    if id_prof in res:
        cur.execute(
            f"DELETE FROM enseigne \
            WHERE id_prof = {id_prof} \
            AND id_matiere = {id_mat}"
        )
    else:
        cur.execute(
            f"INSERT INTO enseigne (id_prof, id_matiere) \
            VALUES ({id_prof}, {id_mat})"
        )
    con.commit()


if __name__ == "__main__":
    print(mat_by_prof(1))
