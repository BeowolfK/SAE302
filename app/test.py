import mysql.connector
from mysql.connector import errorcode
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
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exists")
    else:
        print(err)
    sys.exit(1)

cur = con.cursor()

cur.execute(
    "SELECT username, nom, prenom, annee, sexe, status, id_login \
        FROM login \
        INNER JOIN etudiant ON login.id_personne = etudiant.id_etudiant \
        WHERE login.type = 'etu';"
)
print(cur.fetchall())
