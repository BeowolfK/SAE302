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


def info_etu(id: int) -> str:
    """
    Cette fonction sélectionne les informations d'un étudiant en utilisant
    l'identifiant de l'étudiant (nom, prénom, sexe et année)
    Args:
        id (int): L'identifiant de l'étudiant pour lequel on veut
        récupérer les informations.
    Returns:
        str : les informations de l'étudiant sous la forme
        "Nom Prenom - AnnéeA"
    """
    try:
        assert isinstance(id, int)
    except AssertionError:
        return
    cur.execute(
        f"SELECT CASE sexe \
        WHEN 'M' THEN CONCAT('Mr', ' ', nom, ' ', prenom) \
        ELSE CONCAT('Mme', ' ', nom, ' ', prenom) END, CONCAT(annee, 'A') \
        FROM etudiant WHERE id_etudiant = {id};"
    )
    info = cur.fetchone()
    return f"{info[0].title()} - {info[1]}"


def info_prof(id: int) -> str:
    """
    Cette fonction sélectionne le nom et prénom d'un enseignant en
    utilisant une jointure entre les tables "enseigne" et "prof" et en
    utilisant un cas pour afficher "Mr" ou "Mme" en fonction du sexe
    de l'enseignant.

    Args:
        id (int): L'identifiant du professeur

    Returns:
        str: chaîne de caractère contenant les informations de l'enseignant
    """

    try:
        assert isinstance(id, int)
    except AssertionError:
        return
    cur.execute(
        f"SELECT CASE sexe \
        WHEN 'M' THEN CONCAT('Mr', ' ', nom, ' ', prenom) \
        ELSE CONCAT('Mme', ' ', nom, ' ', prenom) END \
        FROM prof WHERE id_prof = {id};"
    )
    info = cur.fetchone()
    return f"{info[0].title()}"


def prof_nom(id):
    """
    Cette fonction sélectionne le nom et prénom d'un enseignant en utilisant
    une jointure entre les tables "enseigne" et "prof" et en utilisant un cas
    pour afficher "Mr" ou "Mme" en fonction du sexe de l'enseignant.
    Args:
        id (int): L'identifiant de la matière pour laquelle on veut récupérer
            les informations de l'enseignant
    Returns:
        List[Tuple[str]]: liste contenant les informations de l'enseignant
            (nom et prénom)
    """
    cur.execute(
        f"SELECT CASE prof.sexe \
        WHEN 'M' THEN CONCAT('Mr', ' ', prof.nom, ' ', prof.prenom) \
        ELSE CONCAT('Mme', ' ', prof.nom, ' ', prof.prenom) END \
        FROM enseigne INNER JOIN prof ON enseigne.id_prof = prof.id_prof \
        WHERE id_matiere = {id};"
    )
    return cur.fetchall()


def prof_enseigne(id: int) -> list[str]:
    """
    Cette fonction sélectionne les matières enseignées par un professeur
    en utilisant l'identifiant du professeur.
    Args:
        id (int): L'identifiant du professeur pour lequel
        on veut récupérer les matières enseignées.
    Returns:
        List[str]: liste contenant les noms des matières
        enseignées par le professeur.
    """
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
    try:
        assert isinstance(id, int)
    except AssertionError:
        return
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


def matiere(id: int) -> list[tuple[int, str, str]]:
    """
    Cette fonction sélectionne les matières suivies par un étudiant en
    utilisant l'identifiant de l'étudiant
    (nom de la matière, id de la matière, nom de l'enseignant)
    Args:
        id (int): L'identifiant de l'étudiant pour lequel on veut
            récupérer les matières suivies.
    Returns:
        List[Tuple[int, str, str]] : liste contenant les informations des
            matières suivies par l'étudiant sous la forme
            (id_matiere, nom de la matière, nom de l'enseignant)
            ou [] si l'id n'est pas un entier
    """
    try:
        assert isinstance(id, int)
    except AssertionError:
        return
    cur.execute(
        f"SELECT matiere.id_matiere, matiere.nom FROM etudiant \
        INNER JOIN matiere ON etudiant.annee = matiere.annee \
        WHERE id_etudiant = {id} GROUP BY id_matiere;"
    )
    res = prof_nom(cur.fetchall())
    return res


def convertToBinaryData(filename: str) -> bytes:
    """
    Cette fonction convertit les données d'un fichier en données binaires
    Args:
        filename (str): le nom du fichier dont on veut récupérer les données
    Returns:
        bytes : les données binaires du fichier
    """
    try:
        with open(filename, "rb") as file:
            binaryData = file.read()
        return binaryData
    except Exception:
        return


def is_name(name: str) -> bool:
    """
    Cette fonction vérifie si une chaîne de caractères est un nom valide
    en utilisant une expression régulière
    Args:
        name (str): la chaîne de caractères à vérifier
    Returns:
        bool : True si la chaîne est un nom valide, False sinon
    """
    regex = r"^[a-zA-Z-]+$"
    if re.search(regex, name):
        return True
    return


def generate_username(name: str) -> str:
    """
    Cette fonction génère un nom d'utilisateur pour un nom donné
    Args:
        name (str): le nom pour lequel on veut générer un nom d'utilisateur.
    Returns:
        str : le nom d'utilisateur généré sous la forme
            "Première lettre du nom + 8 chiffres aléatoires"
    """
    try:
        assert is_name(name)
    except AssertionError:
        return
    first_letter = name[0].lower()
    random_string = "".join(str(random.randint(0, 9)) for _ in range(8))
    final_string = first_letter + random_string
    return final_string


def uniq_username(name: str) -> str:
    """
    Cette fonction génère un nom d'utilisateur unique pour un nom donné en
    vérifiant que le nom d'utilisateur généré n'est pas déjà utilisé dans
    la base de données
    Args:
        name (str): le nom pour lequel on veut générer
            un nom d'utilisateur unique.
    Returns:
        str : le nom d'utilisateur unique généré sous la forme
            "Première lettre du nom + 8 chiffres aléatoires"
    """
    uniq = True
    while uniq:
        username = generate_username(name)
        cur.execute(f"SELECT * FROM login WHERE username = '{username}';")
        uniq = cur.fetchone()
    return username


def new_etudiant(nom: str,
                 prenom: str,
                 annee: int,
                 sexe: str,
                 filename: str,
                 mdp: str) -> bool:
    """
    Cette fonction permet d'ajouter un étudiant dans la base de données avec
    les informations données (nom, prénom, année, sexe, photo, mdp)
    Args:
        nom (str): nom de l'étudiant
        prenom (str): prénom de l'étudiant
        annee (int): année de l'étudiant
        sexe (str): sexe de l'étudiant
        filename (str): le nom du fichier contenant la photo de l'étudiant
        mdp (str): mot de passe de l'étudiant
    Returns:
        bool : True si l'étudiant est ajouté avec succès
    """
    try:
        assert isinstance(nom, str)
        assert isinstance(prenom, str)
        assert is_name(nom)
        assert is_name(prenom)
        assert isinstance(annee, int)
        assert annee == 1 or annee == 2
        assert isinstance(sexe, str)
        assert sexe == "M" or sexe == "F"
    except AssertionError:
        return
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
        print("="*50, username, "="*50, sep="\n")
        return True
    return


def add_note(note: float, comm: str, id_matiere: int, id_etu: int) -> None:
    """
    Cette fonction permet d'ajouter une note dans la base de données pour un
    étudiant donné pour une matière donnée
    Args:
        note (float): la note à ajouter
        comm (str): commentaire associé à la note
        id_matiere (int): l'identifiant de la matière pour
            laquelle on ajoute la note
        id_etu (int): l'identifiant de l'étudiant
            pour lequel on ajoute la note
    Returns:
        None
    """
    try:
        cur.execute(
            f"INSERT INTO note (note, commentaire, id_matiere, id_etudiant) \
            VALUES ({note}, '{comm}' ,{id_matiere}, {id_etu});"
        )
        con.commit()
    except Exception as e:
        print(e)


def liste_etu() -> list[tuple[str, str, str, int, str, str, int, int]]:
    """
    Cette fonction récupère la liste de tous les étudiants
    Returns:
        List[Tuple[str,str,str,int,str,str,int,int]] : une liste de tuples
            contenant les informations
            (username, nom, prenom, annee, sexe, status, id_login, id_personne)
            des étudiants
    """

    cur.execute(
        "SELECT username, nom, prenom, annee, \
        sexe, status, id_login, id_personne \
        FROM login \
        INNER JOIN etudiant ON login.id_personne = etudiant.id_etudiant \
        WHERE login.type = 'etu'\
        ORDER BY nom ASC;"
    )
    return cur.fetchall()


def change_status(status: int, id: int) -> None:
    """
    Cette fonction permet de changer le status d'un utilisateur
    Args:
        status (int): le status (0 ou 1)
        id (int): l'identifiant de l'utilisateur
    Returns:
        None
    """
    try:
        assert isinstance(status, int)
        assert isinstance(id, int)
        assert status == 0 or status == 1
    except AssertionError:
        return
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


def get_student(study: str) -> list[tuple[int, str, str, int]]:
    """
    Cette fonction permet de récupérer la liste des étudiants inscrits
    dans une matière donnée
    Args:
        study (str): le nom de la matière pour laquelle
            on veut récupérer les étudiants
    Returns:
        Union[None, List[Tuple[int,str,str,int]]] : une liste de tuples
            contenant les informations (id_etudiant, nom, prenom, annee)
            des étudiants inscrits dans la matière donnée
    """
    try:
        cur.execute(
            f"SELECT annee FROM matiere WHERE matiere.nom = '{study}';"
        )
        annee_mat = cur.fetchone()[0]
    except IndexError:
        return

    cur.execute(
        f"SELECT etudiant.id_etudiant,etudiant.nom,prenom,etudiant.annee \
        FROM etudiant \
        INNER JOIN matiere \
        WHERE matiere.annee = etudiant.annee \
        AND etudiant.annee = {annee_mat} \
        AND matiere.nom = '{study}' \
        ORDER BY etudiant.nom ASC;"
    )
    all_student = cur.fetchall()
    return all_student


def get_student_vie_scolaire(name: str,
                             first_name: str,
                             year: int) -> list[tuple]:
    """
    Cette fonction permet de récupérer les informations d'un étudiant donné
    Args:
        name (str): le nom de l'étudiant
        first_name (str): le prénom de l'étudiant
        year (int): l'année de l'étudiant
    Returns:
        List[Tuple] : liste de tuples contenant les informations de l'étudiant
    """
    cur.execute(
        f"SELECT * FROM etudiant INNER JOIN matiere \
        WHERE matiere.annee = etudiant.annee \
        AND etudiant.nom = '{name}' \
        AND etudiant.prenom = '{first_name}' \
        AND etudiant.annee = '{year}' \
        ORDER BY etudiant.nom ASC;"
    )
    return cur.fetchall()


def add_absence_vie_scolaire(id_etu: int,
                             id_teacher: int,
                             mat: str,
                             dates: str,
                             hour: str,
                             comment: str) -> None:
    """
    Cette fonction permet d'ajouter une absence dans la base de données
    Args:
        id_etu (int): l'identifiant de l'étudiant
        id_teacher (int): l'identifiant du professeur
        mat (str): la matière de l'absence
        dates (str): la date de l'absence
        hour (str): l'heure de l'absence
        comment (str): un commentaire (facultatif) sur l'absence
    Returns:
        None
    """
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


def add_exclusion_vie_scolaire(id_etu: int,
                               id_teacher: int,
                               mat: str,
                               dates: str,
                               hour: str,
                               comment: str) -> None:
    """
    Cette fonction permet d'ajouter un retard dans la base de données
    Args:
        id_etu (int): l'identifiant de l'étudiant
        id_teacher (int): l'identifiant du professeur
        mat (str): la matière du retard
        dates (str): la date du retard
        hour (str): l'heure du retard
        comment (str): une raison (facultative) de l'exclusion
    Returns:
        None
    """
    cur.execute(
        f"INSERT INTO exclusion \
        (id_etudiant, id_prof, matiere, date, heure,raison) \
        VALUES \
        ({id_etu}, {id_teacher},'{mat}','{dates}','{hour}','{comment}');"
    )
    con.commit()


def get_id_mat(nom_mat: str) -> tuple:
    """
    Cette fonction permet de récupérer l'identifiant d'une matière donnée
    Args:
        nom_mat (str): le nom de la matière
    Returns:
        Tuple : un tuple contenant l'identifiant de la matière
    """
    cur.execute(f"SELECT id_matiere from matiere where nom = '{nom_mat}'")
    return cur.fetchone()


def list_mat() -> list[list]:
    """
    Cette fonction permet de récupérer la liste de toutes les matières
    Returns:
        List[List] : informations des matières avec le nom des professeurs
            qui enseigne la matiere
    """
    cur.execute("SELECT * FROM matiere")
    matiere = []
    for id in cur.fetchall():
        noms = [tup[0].title() for tup in prof_nom(id[0])]
        matiere.append([id[0], id[1], noms, id[2]])
    return matiere


def add_mat(name: str, annee: int) -> None:
    """
    Cette fonction permet d'ajouter une matière dans la base de données
    Args:
        name (str): le nom de la matière
        annee (int): l'année de la matière
    Returns:
        None
    """
    cur.execute(
        f"INSERT INTO matiere (nom, annee) \
        VALUES ('{name}', '{annee}')"
    )
    con.commit()


def delete_mat(id: int, *args) -> None:
    """
    Cette fonction permet de supprimer une matière de la base de données
    Args:
        id (int): l'identifiant de la matière à supprimer
    Returns:
        None
    """
    cur.execute(f"DELETE FROM matiere WHERE id_matiere = {id}")
    con.commit()


def mat_by_prof(id: int) -> list[tuple]:
    """
    Cette fonction permet de récupérer les matières enseignées
    par un professeur
    Args:
        id (int): l'identifiant du professeur
    Returns:
        List[Tuple]: une liste de tuples contenant les informations
            des matières enseignées par le professeur
    """
    cur.execute(
        f"SELECT matiere.id_matiere, matiere.nom FROM matiere \
        INNER JOIN enseigne ON matiere.id_matiere = enseigne.id_matiere \
        WHERE enseigne.id_prof = {id};"
    )
    return cur.fetchall()


def all_prof() -> list[tuple]:
    """
    Cette fonction permet de récupérer la liste de tous les professeurs
    Returns:
        List[Tuple]: une liste de tuples contenant les informations
        des professeurs
    """
    cur.execute(
        "SELECT id_prof, \
        CASE prof.sexe \
        WHEN 'M' THEN CONCAT('Mr', ' ', prof.nom, ' ', prof.prenom) \
        ELSE CONCAT('Mme', ' ', prof.nom, ' ', prof.prenom) \
        END \
        FROM prof;"
    )
    return cur.fetchall()


def list_prof() -> list[list]:
    """
    Cette fonction permet de récupérer la liste des professeurs avec
    les matières qu'ils enseignent
    Returns:
        List[List]: une liste contenant les informations de chaque professeur
    """
    res = all_prof()
    prof = []
    for id in res:
        mat = mat_by_prof(id[0])
        prof.append([id[0], id[1], [nom[1].title() for nom in mat]])
    return prof


def delete_prof(id: int, *args) -> None:
    """
    Cette fonction permet de supprimer un professeur de la base de données
    Args:
        id (int): l'identifiant du professeur à supprimer
    Returns:
        None
    """
    cur.execute(f"DELETE FROM prof WHERE id_prof = {id}")
    con.commit()


def add_prof(nom: str, prenom: str, sexe: str) -> bool:
    """
    Cette fonction permet d'ajouter un professeur à la base de données
    Args:
        nom (str): le nom du professeur
        prenom (str): le prenom du professeur
        sexe (str): le sexe du professeur
    Returns:
        bool: True si l'ajout a été effectué avec succès, False sinon
    """
    try:
        cur.execute(
            f"INSERT INTO prof (nom, prenom, sexe) \
            VALUES ('{nom}', '{prenom}', '{sexe}')"
        )
        con.commit()
    except Exception:
        return False
    else:
        cur.execute("SELECT LAST_INSERT_ID();")
        id = int(cur.fetchone()[0])
        res = new_account(nom, "prof", "prof", id, 1)
        return res


def all_mat() -> list:
    """
    Cette fonction permet de récupérer la liste de toutes les matières
    Returns:
        List: une liste contenant les informations de chaque matière
    """
    cur.execute("SELECT * FROM matiere")
    return cur.fetchall()


def assign_mat_prof(id_prof: int, id_mat: int) -> None:
    """Permet d'assigner un professeur à une matière pour savoir ensuite
    lesquels il enseigne

    Args:
        id_prof (int): ID du professeur
        id_mat (int): ID de la matière
    Returns:
        None
    """
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
