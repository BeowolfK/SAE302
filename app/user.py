"""
Ce fichier ne nous sert qu'as ajouter automatiquement tous les étudiants
de notre promo a la base de données
"""

from login import new_account
from management import convertToBinaryData
import os
import mysql.connector
import sys


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
dir = "../photo/"
for filename in os.listdir(dir):
    print(filename)
    prenom, nom, username = filename.split("_")
    filename = os.path.join(dir, filename)
    username = nom[0].lower() + username.split(".")[0]
    photo = convertToBinaryData(filename)
    try:
        cur.execute(
            "INSERT INTO etudiant (nom, prenom, annee, photo, sexe) \
            VALUES (%s, %s, %s, %s, %s)",
            (nom, prenom, 2, photo, 'M'),
        )
        con.commit()
    except Exception as e:
        print(e)
    cur.execute("SELECT LAST_INSERT_ID();")
    id = int(cur.fetchone()[0])
    res = new_account(username, "etu", "etu", id, 1)
    print(res)
