import mysql.connector
import sys
from os.path import exists

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


def main():
    cur.execute("SELECT * FROM etudiant")
    res = cur.fetchall()
    for people in res:
        filename = "images/{}-{}-{}.png".format(
            people[0], people[1].upper(), people[2].upper()
        )

        if not exists(filename):
            with open(filename, "wb+") as f:
                f.write(people[4])


if __name__ == "__main__":
    main()
