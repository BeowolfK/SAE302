class Personne:
    def __init__(self, *args):
        if len(args) > 0:
            
            self.__id = args[0]
        else:
            self.__id = None

        if len(args) > 1:
            self.__prenom = args[1]
        else:
            self.__prenom = ""

        if len(args) > 2:
            self.__nom = args[2]
        else:
            self.__nom = ""

    def set_prenom(self, x):
        self.__prenom = x

    def get_prenom(self):
        return self.__prenom

    def set_nom(self, x):
        self.__nom = x

    def get_nom(self):
        return self.__nom

    def set_id(self, x):
        self.__id = x

    def get_id(self):
        return self.__id

    def afficher(self):
        return f"{self.__prenom} {self.__nom} {self.__id}"
