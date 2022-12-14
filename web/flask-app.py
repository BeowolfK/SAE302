import mysql.connector
from flask import Flask, render_template, redirect
import sys

"""
Need to improve database select 
website is not dynamic
"""

app = Flask(__name__)

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


@app.route("/")
def home():
    cur.execute(
        "SELECT etudiant.id_etudiant, nom, prenom, sexe, annee, \
        AVG(note) FROM etudiant \
        INNER JOIN note ON etudiant.id_etudiant = note.id_etudiant \
        GROUP BY etudiant.id_etudiant"
    )
    result = cur.fetchall()
    return render_template("home.html", result=result)


@app.route("/etudiant/<etudiant>")
def note_student(etudiant):
    try:
        cur.execute(
            f"SELECT etudiant.nom, etudiant.prenom, etudiant.sexe, \
            matiere.nom, AVG(NOTE) FROM note \
            INNER JOIN matiere ON note.id_matiere = matiere.id_matiere \
            INNER JOIN etudiant ON note.id_etudiant = etudiant.id_etudiant \
            WHERE note.id_etudiant = {etudiant} GROUP BY note.id_matiere;"
        )
        result = cur.fetchall()
        if result == []:
            return redirect("/error404")
        return render_template("etudiant.html", result=result)
    except mysql.connector.errors.ProgrammingError as e:
        print(e)
        return redirect("/error404")


@app.route("/matiere/<matiere>")
def note_matiere(matiere):
    try:
        print(matiere)
        cur.execute(
            f"SELECT etudiant.id_etudiant, matiere.nom, etudiant.nom, \
            etudiant.prenom, etudiant.sexe, AVG(note) FROM matiere \
            INNER JOIN note ON matiere.id_matiere = note.id_matiere \
            INNER JOIN etudiant ON note.id_etudiant = etudiant.id_etudiant \
            WHERE matiere.nom = '{matiere.lower()}' GROUP BY note.id_etudiant \
            ORDER BY AVG(note) DESC;"
        )
        result = cur.fetchall()
        if result == []:
            return redirect("/error404")
        return render_template("matiere.html", result=result)
    except mysql.connector.errors.ProgrammingError as e:
        print(e)
        return redirect("/error404")


@app.route("/error404")
def page404():
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
