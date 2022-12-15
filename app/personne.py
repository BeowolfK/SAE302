class Personne:
    def __init__(self, *args):
        if len(args) > 0:
            print(args[0])
            self.__prenom = args[0]
        else:
            self.__prenom = ""

        if len(args) > 1:
            self.__nom = args[1]
        else:
            self.__nom = ""

        if len(args) > 2:
            self.__email = args[2]
        else:
            self.__email = ""

    def set_prenom(self, x):
        self.__prenom = x

    def get_prenom(self):
        return self.__prenom

    def set_nom(self, x):
        self.__nom = x

    def get_nom(self):
        return self.__nom

    def set_email(self, x):
        self.__email = x

    def get_email(self):
        return self.__email

    def afficher(self):
        return f"{self.__prenom} {self.__nom} {self.__email}"
