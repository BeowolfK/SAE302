import mysql.connector
import sys

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
    return binaryData


def new_etudiant(nom, prenom, annee, sexe, filename):
    assert isinstance(nom, str)
    assert isinstance(prenom, str)
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
    except Exception as e:
        print(e)


def add_note(note, id_matiere, id_etu):
    try :
        cur.execute(
            f"INSERT INTO note (note, id_matiere, id_etudiant) \
            VALUES ({note}, {id_matiere}, {id_etu});"
        )
        con.commit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # new_etudiant(
    #     "photo",
    #     "photo",
    #     1,
    #     "F",
    #     r"C:\Users\Sarah\Kenan\SIMCom GPS DEMO V1.07\Image\log1.png",
    # )
    add_note(13, 2, 1)
