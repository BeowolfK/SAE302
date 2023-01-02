from login import verify, new_account
from management import info_etu, liste_etu
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen


# CREATION DES CLASS REPRÉSENTANT NOS WINDOWS
class FirstWindow(Screen):
    pass


class StudWindow(Screen):
    pass


class FileChose(Screen):
    def selected(self, filename):

        try:
            self.ids.i_image.source = filename[0]
            print(filename[0])
        except Exception as e:
            print(e)


class TeachWindow(Screen):
    pass


class AdminWindow(Screen):
    pass


class AddStudent(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class Application(App):
    def build(self):
        pass

    def resetchamp(self, verif):
        mdp_box = self.root.get_screen("hub").ids.mdp
        lbl = self.root.get_screen("hub").ids.mdp_lbl
        mdp_box.text = ""
        if not verif:
            lbl.color = (1, 0, 0, 1)
            lbl.underline = True
        else:
            lbl.color = (192, 192, 192, 1)
            lbl.underline = False

    def solo_check(self):
        if self.root.get_screen("addstudent").ids.ck_h.active:
            self.root.get_screen("addstudent").ids.ck_h.active = False

    def solo_check2(self):
        if self.root.get_screen("addstudent").ids.ck_f.active:
            self.root.get_screen("addstudent").ids.ck_f.active = False

    def valider(self):
        """Fait une requête pour savoir si c'est un étudiant, un prof, autre et
        en fonction renvoie la valeur pour switch faire la bonne fenêtre.

        Returns:
            str: nom du prochain écran
        """

        if (
            self.root.get_screen("hub").ids.identif.text != ""
            and self.root.get_screen("hub").ids.mdp.text != ""
        ):
            identifiant = self.root.get_screen("hub").ids.identif.text
            motdp = self.root.get_screen("hub").ids.mdp.text
            verif = verify(identifiant, motdp)
            if verif:
                if verif[0] == "etu":
                    id = verif[1]
                    info = info_etu(id)
                    pres = f"{id}) {info}"
                    self.root.get_screen("second").ids.nom.text = pres
                    self.resetchamp(True)
                    return "second"
                if verif[0] == "prof":
                    print(verif)
                if verif[0] == "admin":
                    liste = liste_etu()
                    grid = self.root.get_screen("admin").ids.grid_etu
                    # for etu in liste:
                    #     print(etu)
                    #     grid.add_widget(Label(text="photo", color=(192, 192, 192, 1)))
                    #     grid.add_widget(Label(text=etu[0], color=(192, 192, 192, 1)))
                    #     grid.add_widget(Label(text=etu[1], color=(192, 192, 192, 1)))
                    #     grid.add_widget(
                    #         Label(text=str(etu[2]), color=(192, 192, 192, 1))
                    #     )
                    #     grid.add_widget(Label(text=etu[3], color=(192, 192, 192, 1)))
                    #     grid.add_widget(
                    #         Label(text=str(etu[4]), color=(192, 192, 192, 1))
                    #     )
                    return "admin"
            else:
                self.resetchamp(False)


    def reset_addstudent(self):
        self.root.get_screen("addstudent").ids.t_nom.text = ""
        self.root.get_screen("addstudent").ids.t_prenom.text = ""
        self.root.get_screen("addstudent").ids.i_etu.source = ""
        self.root.get_screen("addstudent").ids.ck_h.active = False
        self.root.get_screen("addstudent").ids.ck_f.active = False
        self.root.get_screen("addstudent").ids.i_year.text = ""
        mdp = self.root.get_screen("addstudent").ids.t_mdp.text = ""

    def save_image(self, filename):
        try:
            self.root.get_screen("addstudent").ids.i_etu.source = filename[0]
            photo = filename[0]
            nom = self.root.get_screen("addstudent").ids.t_nom.text
            prenom = self.root.get_screen("addstudent").ids.t_prenom.text
            sexe = 'M' if self.root.get_screen("addstudent").ids.ck_h.active else 'F'
            annee =  self.root.get_screen("addstudent").ids.i_year.text
            mdp = self.root.get_screen("addstudent").ids.t_mdp.text
            
            
        except Exception as e:
            print(e)
    """
    def show_to_hide_password(self):
        if self.root.get_screen("addstudent").ids.sh_hd.text == "Show" : 
            print(self.root.get_screen("addstudent").ids.sh_hd.text)
            self.root.get_screen("addstudent").ids.t_mdp.password = False
            self.root.get_screen("addstudent").ids.sh_hd.text = "Hide"  
            print(self.root.get_screen("addstudent").ids.sh_hd.text )
        if self.root.get_screen("addstudent").ids.sh_hd.text == "Hide" :
            self.root.get_screen("addstudent").ids.t_mdp.password = True
            self.root.get_screen("addstudent").ids.sh_hd.text = "Show"
    """
if __name__ == "__main__":
    app = Application()
    app.run()
