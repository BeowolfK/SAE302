from personne import Personne


class Etudiant(Personne):
    def __init__(self, *args):
        Personne.__init__(self, *args)

        if len(args) > 3 and type(int(args[3])) == int:

            self.__annee = int(args[3])
        else:
            self.__annee = 0

        if len(args) > 4:
            self.__matiere = args[4]
        else:
            self.__matiere = ""

        if len(args) > 5:
            self.__moyenne = args[5]
        else:
            self.__moyenne = 0

    def set_annee(self, x):
        self.__annee = x

    def get_annee(self):
        return self.__annee

    def set_matiere(self, x):
        self.__matiere = x

    def get_matiere(self):
        return self.__matiere

    def set_moyenne(self, x):
        self.__moyenne = x

    def get_moyenne(self):
        return self.__moyenne
