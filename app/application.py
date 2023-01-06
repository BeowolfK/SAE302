from login import verify
from management import *
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from etudiant import Etudiant
from kivy.uix.scrollview import ScrollView
from kivy.app import runTouchApp

# CREATION DES CLASS REPRÉSENTANT NOS WINDOWS
class FirstWindow(Screen):
    pass


class StudWindow(Screen):
    pass


class FileChose(Screen):
    def selected(self, filename):

        try:
            self.ids.i_image.source = filename[0]
        except Exception as e:
            print(e)


class TeachWindow(Screen):
    pass


class AdminWindow(Screen):
    pass


class AdminEtuWindow(Screen):
    pass


class AddStudent(Screen):
    pass


class MatiereWindow(Screen):
    pass


class ProfWindow(Screen):
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

    def solo_check3(self):
        if self.root.get_screen("addstudent").ids.ck_1a.active:
            self.root.get_screen("addstudent").ids.ck_1a.active = False

    def solo_check4(self):
        if self.root.get_screen("addstudent").ids.ck_2a.active:
            self.root.get_screen("addstudent").ids.ck_2a.active = False

    def create_lbl(self, texte):
        return Label(text=str(texte), color=(192, 192, 192, 1))

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
                    self.user = Etudiant(verif[1])
                    self.get_stats()
                    return "second"
                if verif[0] == "prof":
                    id = verif [1]
                    info = info_prof(id)
                    self.resetchamp(True)
                    return("teacher")
                    
                if verif[0] == "admin":
                    return "admin"
            else:
                self.resetchamp(False)
            
    
    def get_stud(self):
        liste = liste_etu()
        grid = self.root.get_screen("liste_etu").ids.grid_etu
        
        for etu in liste:
            grid.add_widget(self.create_lbl("photo"))
            grid.add_widget(self.create_lbl(etu[0]))
            grid.add_widget(self.create_lbl(etu[1]))
            grid.add_widget(self.create_lbl(etu[2]))
            grid.add_widget(self.create_lbl(etu[3]))
            grid.add_widget(self.create_lbl(etu[4]))
            if etu[5]:
                btn = Button(
                    text=f"Désactiver {etu[6]}",
                    background_color=(1, 0, 0, 1),
                )
                btn.bind(on_press=self.update_status)
                grid.add_widget(btn)
            else:
                btn = Button(
                    text=f"Activer {etu[6]}",
                    background_color=(0, 1, 0, 1),
                )
                btn.bind(on_press=self.update_status)
                grid.add_widget(btn)

    def clear_stud(self):
        self.root.get_screen("liste_etu").ids.grid_etu.clear_widgets()

    def update_status(self, instance):
        texte, id = instance.text.split()
        if texte == "Désactiver":
            change_status(0, id)
            instance.text = f"Activer {id}"
            instance.background_color = (0, 1, 0, 1)
        elif texte == "Activer":
            change_status(1, id)
            instance.text = f"Désactiver {id}"
            instance.background_color = (1, 0, 0, 1)
        else:
            print("Error")

    def reset_addstudent(self):
        self.root.get_screen("addstudent").ids.t_nom.text = ""
        self.root.get_screen("addstudent").ids.t_prenom.text = ""
        self.root.get_screen("addstudent").ids.i_etu.source = ""
        self.root.get_screen("addstudent").ids.ck_h.active = False
        self.root.get_screen("addstudent").ids.ck_f.active = False
        self.root.get_screen("addstudent").ids.ck_1a.active = False
        self.root.get_screen("addstudent").ids.ck_2a.active = False
        self.root.get_screen("addstudent").ids.t_mdp.text = ""

    def save_image(self, filename):
        try:
            self.root.get_screen("addstudent").ids.i_etu.source = filename[0]
        except Exception as e:
            print(e)

    def add_student(self):
        try:
            filename = self.root.get_screen("addstudent").ids.i_etu.source
            nom = self.root.get_screen("addstudent").ids.t_nom.text
            prenom = self.root.get_screen("addstudent").ids.t_prenom.text
            sexe = "M" if self.root.get_screen("addstudent").ids.ck_h.active \
                else "F"
            annee = 1 if self.root.get_screen("addstudent").ids.ck_1a.active \
                else 2
            mdp = self.root.get_screen("addstudent").ids.t_mdp.text
            res = new_etudiant(nom, prenom, annee, sexe, filename, mdp)
            print(res)
            if not res:
                print("Error")

        except Exception as e:
            print(e)

    def show_to_hide_password(self):
        if self.root.get_screen("addstudent").ids.sh_hd.text == "Show":
            self.root.get_screen("addstudent").ids.t_mdp.password = False
            self.root.get_screen("addstudent").ids.sh_hd.text = "Hide"
        elif self.root.get_screen("addstudent").ids.sh_hd.text == "Hide":
            self.root.get_screen("addstudent").ids.t_mdp.password = True
            self.root.get_screen("addstudent").ids.sh_hd.text = "Show"

    def create_lbl_custom(self, texte, font_s):
        return Label(text=str(texte), color=(192, 192, 192, 1), font_size=(20))

    def get_stats(self):
        id = self.user.get_id()
        
        note = panel_note(id)
        print(note)
        grid = self.root.get_screen("second").ids.grid1
        for grade in note : 
            grid.add_widget(self.create_lbl(grade[0].title()))
            grid.add_widget(self.create_lbl(",".join(grade[1])))
            grid.add_widget(self.create_lbl(grade[2]))
    def clear_note(self):
        self.root.get_screen("second").ids.grid1.clear_widgets()


    def espace_note(self): 
        self.root.add_widget(ScrollView(size_hint=(.3, 2)))

if __name__ == "__main__":
    app = Application()
    app.run()
