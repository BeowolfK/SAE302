from login import verify
from management import *
from management import (
    liste_etu,
    info_etu,
    info_prof,
    change_status,
    new_etudiant,
    panel_note,
    list_mat,
    delete_mat,
    add_mat
)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen
from etudiant import Etudiant
from kivy.uix.gridlayout import GridLayout
from prof import Prof
from functools import partial
from datetime import datetime


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

    def solo_check_1A(self):
        if self.root.get_screen("teacher").ids.ck_1a.active:
            self.root.get_screen("teacher").ids.ck_1a.active = False

    def solo_check_2A(self):
        if self.root.get_screen("teacher").ids.ck_2a.active:
            self.root.get_screen("teacher").ids.ck_2a.active = False

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
                    id = verif[1]
                    info = info_prof(id)
                    info_liste = info.split()

                    self.resetchamp(True)

                    self.user = Prof(
                        id, info_liste[1], info_liste[2], prof_enseigne(id)
                    )

                    return "teacher"

                if verif[0] == "admin":
                    return "admin"
            else:
                self.resetchamp(False)

    def get_stud(self):
        liste = liste_etu()
        grid = self.root.get_screen("liste_etu").ids.grid_etu
        # image path : http://54.37.226.86:8000/<id>-<NOM>-<PRENOM>.png
        for etu in liste:
            pp = AsyncImage(
                source="http://54.37.226.86:8000/{}-{}-{}.png".format(
                    etu[7], etu[1].upper(), etu[2].upper()
                )
            )
            grid.add_widget(pp)
            grid.add_widget(self.create_lbl(etu[0]))
            grid.add_widget(self.create_lbl(etu[1]))
            grid.add_widget(self.create_lbl(etu[2]))
            grid.add_widget(self.create_lbl(etu[3]))
            grid.add_widget(self.create_lbl(etu[4]))
            if etu[5]:
                btn = Button(
                    text="Activé",
                    background_color=(0, 1, 0, 1),
                )
                btn.bind(on_press=partial(self.update_status, etu[6]))
                grid.add_widget(btn)
            else:
                btn = Button(
                    text="Désactivé",
                    background_color=(1, 0, 0, 1),
                )
                btn.bind(on_press=partial(self.update_status, etu[6]))
                grid.add_widget(btn)


    def clear_stud(self):
        self.root.get_screen("liste_etu").ids.grid_etu.clear_widgets()

    def clear_mat(self):
        self.root.get_screen("liste_mat").ids.grid_mat.clear_widgets()

    def update_status(self, id, instance):
        texte = instance.text
        if texte == "Désactivé":
            change_status(1, id)
            instance.text = "Activé"
            instance.background_color = (0, 1, 0, 1)
        elif texte == "Activé":
            change_status(0, id)
            instance.text = "Désactivé"
            instance.background_color = (1, 0, 0, 1)

    def delete_matiere(self, id, instance):
        delete_mat(id)
        self.clear_mat()
        self.get_mat()

    def get_mat(self):
        liste = list_mat()
        grid = self.root.get_screen("liste_mat").ids.grid_mat
        for matiere in liste:
            grid.add_widget(self.create_lbl(matiere[1]))
            grid.add_widget(self.create_lbl("\n".join(matiere[2])))
            grid.add_widget(self.create_lbl(matiere[3]))
            btn = Button(
                    text="Supprimer",
                    background_color=(1, 0, 0, 1),
            )
            btn.bind(on_press=partial(self.delete_matiere, matiere[0]))
            grid.add_widget(btn)

    def reset_matiere(self):
        screen = self.root.get_screen("liste_mat")
        screen.ids.lbl_annee.color = (0, 0, 0, 1)
        screen.ids.lbl_matiere.color = (0, 0, 0, 1)
        screen.ids.ck_1a.active = False
        screen.ids.ck_2a.active = False
        screen.ids.matiere.text = ""

    def add_matiere(self):
        screen = self.root.get_screen("liste_mat")
        nom = screen.ids.matiere.text
        annee = 1 if screen.ids.ck_1a.active else 2
        flag = True
        if not screen.ids.ck_1a.active and not screen.ids.ck_2a.active:
            screen.ids.lbl_annee.color = (1, 0, 0, 1)
            flag = False
        if nom == "":
            screen.ids.lbl_matiere.color = (1, 0, 0, 1)
            flag = False
        if flag:
            add_mat(nom, annee)
            self.reset_matiere()
            self.clear_mat()
            self.get_mat()


    def get_prof(self):
        print("get_prof")

    def reset_addstudent(self):
        screen = self.root.get_screen("addstudent")
        screen.ids.t_nom.text = ""
        screen.ids.t_prenom.text = ""
        screen.ids.i_etu.source = ""
        screen.ids.ck_h.active = False
        screen.ids.ck_f.active = False
        screen.ids.ck_1a.active = False
        screen.ids.ck_2a.active = False
        screen.ids.t_mdp.text = ""

    def save_image(self, filename):
        try:
            self.root.get_screen("addstudent").ids.i_etu.source = filename[0]
        except Exception as e:
            print(e)

    def add_student(self):
        screen = self.root.get_screen("addstudent")
        label_nom = screen.ids.l_nom
        label_prenom = screen.ids.l_prenom
        label_sexe = screen.ids.l_sexe
        label_annee = screen.ids.l_annee
        label_mdp = screen.ids.l_mdp
        label_button = screen.ids.b_filechose
        lbls = [
            label_nom,
            label_prenom,
            label_sexe,
            label_annee,
            label_mdp,
            label_button,
        ]
        for el in lbls:
            el.color = (192, 192, 192, 1)
        try:
            filename = screen.ids.i_etu.source
            nom = screen.ids.t_nom.text
            prenom = screen.ids.t_prenom.text
            sexe = "M" if screen.ids.ck_h.active else "F"
            mdp = screen.ids.t_mdp.text
            if not screen.ids.ck_h.active and not screen.ids.ck_h.active:
                sexe = ""
            annee = 1 if screen.ids.ck_1a.active else 2
            if not screen.ids.ck_1a.active and not screen.ids.ck_2a.active:
                annee = ""
            flag = True
            if filename == "":
                flag = False
                label_button.color = (1, 0, 0, 0.4)
            if nom == "":
                flag = False
                label_nom.color = (1, 0, 0, 0.4)
            if prenom == "":
                flag = False
                label_prenom.color = (1, 0, 0, 0.4)
            if sexe not in ["M", "F"]:
                flag = False
                label_sexe.color = (1, 0, 0, 0.4)
            if annee not in [1, 2]:
                flag = False
                label_annee.color = (1, 0, 0, 0.4)
            if mdp == "":
                flag = False
                label_mdp.color = (1, 0, 0, 0.4)
            if flag:
                self.reset_addstudent()
                res = new_etudiant(nom, prenom, annee, sexe, filename, mdp)
                print(res)
                if not res:
                    print("Error")
            else:
                print("Tous les champs doivent ")

        except Exception as e:
            print(e)

    def show_to_hide_password(self):
        if self.root.get_screen("addstudent").ids.sh_hd.text == "Show":
            self.root.get_screen("addstudent").ids.t_mdp.password = False
            self.root.get_screen("addstudent").ids.sh_hd.text = "Hide"
        elif self.root.get_screen("addstudent").ids.sh_hd.text == "Hide":
            self.root.get_screen("addstudent").ids.t_mdp.password = True
            self.root.get_screen("addstudent").ids.sh_hd.text = "Show"

    def create_lbl_custom(self, texte, size):
        return Label(
            text=str(texte),
            color=(192, 192, 192, 1),
            font_size=(size)
        )

    def get_stats(self):
        id = self.user.get_id()

        note = panel_note(id)
        print(note)
        grid = self.root.get_screen("second").ids.grid1
        for grade in note:
            grid.add_widget(self.create_lbl(grade[0].title()))
            grid.add_widget(self.create_lbl(",".join(grade[1])))
            grid.add_widget(self.create_lbl(grade[2]))

    def clear_note(self):
        self.root.get_screen("second").ids.grid1.clear_widgets()

    def add_button(self, textd, sizee, heightt, police_size, col):
        return Button(
            text=(str(textd)),
            size_hint=(sizee),
            height=(heightt),
            font_size=(police_size),
            background_color=(col),
        )

    def add_button_event(self, textd, sizee, heightt, police_size, col, event):
        return Button(
            text=(str(textd)),
            size_hint=(sizee),
            height=(heightt),
            font_size=(police_size),
            background_color=(col),
            on_release=(event),
        )

    def espace_note(self):
        racine = self.root.get_screen("teacher")
        if racine.ids.ti_find_student_nom.pos_hint == {"x": 0.3, "y": 0.85}:
            self.clear_vie_scolaire()
        racine.ids.s_liste_eleve.size_hint = (0, 0)
        racine.ids.s_liste_eleve.pos_hint = {"x": 1.2, "y": 1.2}
        racine.ids.gl_liste_eleve.clear_widgets()

        if racine.ids.s_espace_note.pos_hint == {"x": 1.2, "y": 1.2}:
            racine.ids.s_espace_note.size_hint = (0.20, 0.15)
            racine.ids.s_espace_note.pos_hint = {"x": 0.2, "y": 0.65}
            for i in self.user.get_enseigne():
                racine.ids.gl_espace_note.add_widget(
                    self.add_button(
                        f"{i}",
                        (0.055, None),
                        35,
                        22,
                        (0, 0, 0, 0)
                    )
                )

        elif racine.ids.s_espace_note.pos_hint == {"x": 0.2, "y": 0.65}:
            racine.ids.s_espace_note.size_hint = (0, 0)
            racine.ids.s_espace_note.pos_hint = {"x": 1.2, "y": 1.2}
            racine.ids.gl_espace_note.clear_widgets()

    def liste_etudiant(self):
        racine = self.root.get_screen("teacher")

        racine.ids.s_espace_note.size_hint = (0, 0)
        racine.ids.s_espace_note.pos_hint = {"x": 1.2, "y": 1.2}
        racine.ids.gl_espace_note.clear_widgets()

        if racine.ids.s_liste_eleve.pos_hint == {"x": 1.2, "y": 1.2}:
            racine.ids.s_liste_eleve.size_hint = (0.20, 0.15)
            racine.ids.s_liste_eleve.pos_hint = {"x": 0.2, "y": 0.55}
            for i in self.user.get_enseigne():
                btn = self.add_button(
                    f"{i}",
                    (0.06, None),
                    35,
                    22,
                    (0, 0, 0, 0)
                )
                btn.bind(on_release=partial(self.show_student_liste, i))
                racine.ids.gl_liste_eleve.add_widget(btn)

        elif racine.ids.s_liste_eleve.pos_hint == {"x": 0.2, "y": 0.55}:
            racine.ids.s_liste_eleve.size_hint = (0, 0)
            racine.ids.s_liste_eleve.pos_hint = {"x": 1.2, "y": 1.2}
            racine.ids.gl_liste_eleve.clear_widgets()

    def show_student_liste(self, *args):
        etudiant = get_student(args[0])
        racine = self.root.get_screen("teacher")
        if racine.ids.ti_find_student_nom.pos_hint == {"x": 0.3, "y": 0.85}:
            self.clear_vie_scolaire()
        racine.ids.gl_write_space.clear_widgets()
        racine.ids.gl_write_space.add_widget(
            self.create_lbl_custom("Nom", 25)
        )
        racine.ids.gl_write_space.add_widget(
            self.create_lbl_custom("Prénom", 25)
        )
        for etu in etudiant:
            racine.ids.gl_write_space.add_widget(self.create_lbl(etu[1]))
            racine.ids.gl_write_space.add_widget(self.create_lbl(etu[2]))

    def vie_scolaire(self):

        racine = self.root.get_screen("teacher")
        if racine.ids.s_liste_eleve.pos_hint == {"x": 0.2, "y": 0.55}:
            racine.ids.s_liste_eleve.size_hint = (0, 0)
            racine.ids.s_liste_eleve.pos_hint = {"x": 1.2, "y": 1.2}
            racine.ids.gl_liste_eleve.clear_widgets()

        elif racine.ids.s_espace_note.pos_hint == {"x": 0.2, "y": 0.65}:
            racine.ids.s_espace_note.size_hint = (0, 0)
            racine.ids.s_espace_note.pos_hint = {"x": 1.2, "y": 1.2}
            racine.ids.gl_espace_note.clear_widgets()

        racine.ids.gl_write_space.clear_widgets()
        racine.ids.gl_write_space.add_widget
        racine.ids.ti_find_student_nom.pos_hint = {"x": 0.3, "y": 0.85}
        racine.ids.ti_find_student_prenom.pos_hint = {"x": 0.51, "y": 0.85}
        racine.ids.box_check.pos_hint = {"x": 0.78, "y": 0.84}
        racine.ids.anne1.pos_hint = {"x": 0.27, "y": 0.376}
        racine.ids.anne2.pos_hint = {"x": 0.336, "y": 0.376}
        racine.ids.recherche.pos_hint = {"x": 0.89, "y": 0.845}

    def clear_vie_scolaire(self):
        racine = self.root.get_screen("teacher")
        racine.ids.ti_find_student_nom.pos_hint = {"x": 3, "y": 85}
        racine.ids.ti_find_student_prenom.pos_hint = {"x": 51, "y": 85}
        racine.ids.box_check.pos_hint = {"x": 78, "y": 84}
        racine.ids.anne1.pos_hint = {"x": 27, "y": 376}
        racine.ids.anne2.pos_hint = {"x": 336, "y": 376}
        racine.ids.recherche.pos_hint = {"x": 89, "y": 845}
        racine.ids.ti_find_student_nom.text = ""
        racine.ids.ti_find_student_prenom.text = ""
        racine.ids.ck_1a.active = False
        racine.ids.ck_2a.active = False
        racine.ids.gl_write_space.spacing = 25
        racine.ids.gl_write_space.padding = 10
        racine.ids.gl_write_space.cols = 2
        racine.ids.gl_write_space.row_force_default = False
        racine.ids.gl_write_space.clear_widgets()

    def recherche_vie_sco(self):
        racine = self.root.get_screen("teacher")
        racine.ids.gl_write_space.clear_widgets()
        if (
            racine.ids.ti_find_student_nom.text != ""
            and racine.ids.ti_find_student_prenom.text != ""
            and (racine.ids.ck_1a.active or racine.ids.ck_2a.active)
        ):
            if racine.ids.ck_1a.active:
                one_stud = get_student_vie_scolaire(
                    racine.ids.ti_find_student_nom.text,
                    racine.ids.ti_find_student_prenom.text,
                    1,
                )
            elif racine.ids.ck_2a.active:
                one_stud = get_student_vie_scolaire(
                    racine.ids.ti_find_student_nom.text,
                    racine.ids.ti_find_student_prenom.text,
                    2,
                )

            for etu in one_stud:

                racine.ids.gl_write_space.cols = 4
                racine.ids.gl_write_space.spacing = 10
                pp = AsyncImage(
                    source="http://54.37.226.86:8000/{}-{}-{}.png".format(
                        etu[0], etu[1].upper(), etu[2].upper()
                    )
                )
                print(pp.source)
                racine.ids.gl_write_space.add_widget(pp)
                racine.ids.gl_write_space.add_widget(self.create_lbl(etu[1]))
                racine.ids.gl_write_space.add_widget(self.create_lbl(etu[2]))
                racine.ids.gl_write_space.add_widget(self.create_lbl(etu[3]))

                btn_a = self.add_button(
                    "Absence", (0.1, None), 35, 15, (0, 0, 0, 0.15)
                )
                btn_a.bind(on_release=partial(self.add_absence, etu))
                racine.ids.gl_write_space.add_widget(btn_a)

                btn_r = self.add_button(
                    "Retard",
                    (0.1, None),
                    35,
                    15,
                    (0, 0, 0, 0.15)
                )
                racine.ids.gl_write_space.add_widget(btn_r)

                btn_e = self.add_button(
                    "Exclusion", (0.1, None), 35, 15, (0, 0, 0, 0.15)
                )

                racine.ids.gl_write_space.add_widget(btn_e)

    def create_text_input(self, message, width):
        return TextInput(
            hint_text=f"{message}",
            halign="center",
            multiline=False,
            font_size=15,
            size_hint=(None, None),
            height=38,
            width=width,
        )

    def add_absence(self, *args):
        racine = self.root.get_screen("teacher")
        etu = args[0]
        racine.ids.gl_write_space.clear_widgets()
        racine.ids.gl_write_space.cols = 1
        layout = GridLayout(cols=4)
        racine.ids.gl_write_space.row_force_default = True

        pp = AsyncImage(
            source="http://54.37.226.86:8000/{}-{}-{}.png".format(
                etu[0], etu[1].upper(), etu[2].upper()
            )
        )
        layout.add_widget(pp)
        layout.add_widget(self.create_lbl(etu[1]))
        layout.add_widget(self.create_lbl(etu[2]))
        layout.add_widget(self.create_lbl(etu[3]))

        racine.ids.gl_write_space.add_widget(layout)

        layout2 = GridLayout(cols=3, spacing=10)
        btn_date = self.create_text_input("Date", 100)

        layout2.add_widget(btn_date)

        btn_heure = self.create_text_input("Heure", 100)
        layout2.add_widget(btn_heure)
        layout2.add_widget(self.create_text_input("Commentaire", 150))

        btn_today = self.add_button(
            "Aujourd'hui", (0.08, None), 35, 15, (0, 0, 0, 0.15)
        )
        btn_today.bind(on_release=partial(self.input_today, btn_date))
        layout2.add_widget(btn_today)

        btn_hours = self.add_button(
            "Heure en cours", (0.08, None), 35, 15, (0, 0, 0, 0.15)
        )
        btn_hours.bind(on_release=partial(self.input_hour, btn_heure))
        layout2.add_widget(btn_hours)

        layout2.add_widget(
            self.add_button("Valider", (0.08, None), 35, 15, (0, 0, 0, 0.15))
        )
        racine.ids.gl_write_space.add_widget(layout2)

    def input_today(self, *args):
        today = datetime.now().date()
        args[0].text = str(today)

    def input_hour(self, *args):
        hours = datetime.now().strftime("%H")
        args[0].text = str(hours)


if __name__ == "__main__":
    app = Application()
    app.run()
