from login import verify
from management import (
    liste_etu,
    info_etu,
    info_prof,
    change_status,
    new_etudiant,
    panel_note,
    prof_enseigne,
    get_student_vie_scolaire,
    get_student,
    list_mat,
    delete_mat,
    add_mat,
    list_prof,
    delete_prof,
    add_prof,
    all_prof,
    all_mat,
    mat_by_prof,
    assign_mat_prof,
    add_absence_vie_scolaire,
    add_retard_vie_scolaire,
    add_exclusion_vie_scolaire,
    get_id_mat,
    add_note,
)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from prof import Prof
from etudiant import Etudiant
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


class MatiereProfWindow(Screen):
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
        self.reset_matiere()

    def clear_prof(self):
        self.root.get_screen("liste_prof").ids.grid_prof.clear_widgets()
        self.reset_prof()

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
            grid.add_widget(self.create_lbl(matiere[1].title()))
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

    def reset_prof(self):
        screen = self.root.get_screen("liste_prof")
        screen.ids.lbl_nom.color = (0, 0, 0, 1)
        screen.ids.lbl_prenom.color = (0, 0, 0, 1)
        screen.ids.ck_m.active = False
        screen.ids.ck_f.active = False
        screen.ids.nom.text = ""
        screen.ids.prenom.text = ""

    def delete_prof(self, id, instance):
        delete_prof(id)
        self.clear_prof()
        self.get_prof()

    def add_new_prof(self):
        screen = self.root.get_screen("liste_prof")
        nom = screen.ids.nom.text
        prenom = screen.ids.prenom.text
        sexe = "M" if screen.ids.ck_m.active else "F"
        flag = True
        if not screen.ids.ck_m.active and not screen.ids.ck_f.active:
            screen.ids.lbl_annee.color = (1, 0, 0, 1)
            flag = False
        if nom == "":
            screen.ids.lbl_nom.color = (1, 0, 0, 1)
            flag = False
        if prenom == "":
            screen.ids.lbl_prenom.color = (1, 0, 0, 1)
            flag = False
        if flag:
            res = add_prof(nom, prenom, sexe)
            if not res:
                screen.ids.lbl_nom.color = (1, 0, 0, 1)
                screen.ids.lbl_prenom.color = (1, 0, 0, 1)
            self.reset_prof()
            self.clear_prof()
            self.get_prof()

    def get_prof(self):
        liste = list_prof()
        grid = self.root.get_screen("liste_prof").ids.grid_prof
        for prof in liste:
            grid.add_widget(self.create_lbl(prof[1].title()))
            grid.add_widget(self.create_lbl("\n".join(prof[2]).title()))
            btn = Button(
                text="Supprimer",
                background_color=(1, 0, 0, 1),
            )
            btn.bind(on_press=partial(self.delete_prof, prof[0]))
            grid.add_widget(btn)

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

    def reset_mat_prof(self):
        screen = self.root.get_screen("mat_prof")
        screen.ids.grid_prof.clear_widgets()
        screen.ids.grid_mat.clear_widgets()

    def edition_mat(self):
        screen = self.root.get_screen("mat_prof")
        grid = screen.ids.grid_prof
        profs = all_prof()
        for prof in profs:
            btn = Button(
                text=prof[1].title(),
            )
            btn.bind(on_press=partial(self.list_mat_prof, prof[0]))
            grid.add_widget(btn)

    def list_mat_prof(self, id, *args):
        screen = self.root.get_screen("mat_prof")
        grid = screen.ids.grid_mat
        grid.clear_widgets()
        mats = all_mat()
        mat_prof = [mat[0] for mat in mat_by_prof(id)]

        for mat in mats:
            btn = Button(
                text=mat[1].title(),
            )
            btn.bind(on_press=partial(self.edit_mat_prof, mat[0], id))
            if mat[0] in mat_prof:
                btn.background_color = (0, 1, 0, 1)
            else:
                btn.background_color = (1, 0, 0, 1)
            grid.add_widget(btn)

    def edit_mat_prof(self, id_mat, id_prof, instance):
        screen = self.root.get_screen("mat_prof")
        assign_mat_prof(id_prof, id_mat)
        screen.ids.grid_mat.clear_widgets()
        self.list_mat_prof(id_prof)

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
                if not res:
                    print("Error")
            else:
                print("Tous les champs doivent être remplis")

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
        list_note = []

        screen = self.root.get_screen("second")
        grid = screen.ids.grid1

        for grade in note:
            grid.add_widget(self.create_lbl(grade[0].title()))
            grid.add_widget(self.create_lbl(", ".join(grade[1])))
            grid.add_widget(self.create_lbl(grade[2]))
            list_note.append(grade[2])

        mean = round(sum(list_note) / len(list_note), 2)
        screen.ids.lbl_moyenne.text = f"{mean}/20"

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
            on_release=(partial(self.espace_add_note, event)),
        )

    def espace_note(self):
        racine = self.root.get_screen("teacher")

        self.clear_vie_scolaire()
        racine.ids.s_liste_eleve.size_hint = (0, 0)
        racine.ids.s_liste_eleve.pos_hint = {"x": 1.2, "y": 1.2}
        racine.ids.gl_liste_eleve.clear_widgets()

        if racine.ids.s_espace_note.pos_hint == {"x": 1.2, "y": 1.2}:
            racine.ids.s_espace_note.size_hint = (0.20, 0.15)
            racine.ids.s_espace_note.pos_hint = {"x": 0.2, "y": 0.65}
            for i in self.user.get_enseigne():
                racine.ids.gl_espace_note.add_widget(
                    self.add_button_event(
                        f"{i}", (0.055, None), 35, 22, (0, 0, 0, 0), i
                    )
                )

        else:
            racine.ids.s_espace_note.size_hint = (0, 0)
            racine.ids.s_espace_note.pos_hint = {"x": 1.2, "y": 1.2}
            racine.ids.gl_espace_note.clear_widgets()

    def add_note_panel(self, *args):
        id_matiere = args[3]
        etu = args[4]
        racine = self.root.get_screen("teacher")
        racine.ids.gl_write_space.clear_widgets()
        racine.ids.gl_write_space.cols = 1
        racine.ids.gl_write_space.spacing = 10

        layout = GridLayout(cols=4, width=racine.ids.gl_write_space.width)

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

        layout2 = GridLayout(
            cols=3,
            spacing=30,
            padding=30,
            width=racine.ids.gl_write_space.width
        )
        ti_note = self.create_text_input("Note", 100)

        layout2.add_widget(ti_note)

        ti_comment = self.create_text_input("Commentaire", 130)
        layout2.add_widget(ti_comment)

        layout2.add_widget(
            Button(
                text="Valider",
                size_hint=(None, None),
                height=45,
                width=100,
                font_size=25,
                background_color=(0, 0, 0, 0.15),
                on_release=(
                    partial(
                        self.call_add_note,
                        ti_note,
                        ti_comment,
                        id_matiere,
                        etu[0]
                    )
                ),
            )
        )

        racine.ids.gl_write_space.add_widget(layout2)

    def call_add_note(self, *args):
        # racine = self.root.get_screen("teacher")
        flag = True
        note = args[0].text
        if note == "":
            flag = False
            args[0].background_color = (1, 0, 0, 0.3)
        else:
            try:
                note = float(note)
                if not 0 <= note <= 20:
                    flag = False
                    args[0].background_color = (1, 0, 0, 0.3)
            except ValueError:
                flag = False
                args[0].background_color = (1, 0, 0, 0.3)
        comment = args[1].text
        id_matiere = int(args[2][0])
        id_etu = int(args[3])
        if flag:
            add_note(note, comment, id_matiere, id_etu)
            args[0].background_color = (1, 1, 1, 1)
        args[0].text = ""
        args[1].text = ""

    def espace_add_note(self, *args):
        etudiant = get_student(args[0])

        racine = self.root.get_screen("teacher")
        racine.ids.s_espace_note.size_hint = (0, 0)
        racine.ids.s_espace_note.pos_hint = {"x": 1.2, "y": 1.2}
        racine.ids.gl_write_space.clear_widgets()
        racine.ids.gl_write_space.cols = 3
        racine.ids.gl_write_space.spacing = 30
        racine.ids.gl_write_space.add_widget(
            self.create_lbl_custom("Nom", 25)
        )
        racine.ids.gl_write_space.add_widget(
            self.create_lbl_custom("Prénom", 25)
        )
        racine.ids.gl_write_space.add_widget(
            self.create_lbl_custom("Ajouter une note", 25)
        )
        for etu in etudiant:
            racine.ids.gl_write_space.add_widget(self.create_lbl(etu[1]))
            racine.ids.gl_write_space.add_widget(self.create_lbl(etu[2]))
            racine.ids.gl_write_space.add_widget(
                Button(
                    text=("Nouvelle note"),
                    size_hint=(0.1, None),
                    height=45,
                    width=150,
                    font_size=20,
                    background_color=(0, 0, 0, 0.15),
                    on_release=(
                        partial(
                            self.add_note_panel,
                            etu[0],
                            etu[1],
                            etu[2],
                            get_id_mat(args[0]),
                            etu,
                        )
                    ),
                )
            )

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

        else:
            racine.ids.s_liste_eleve.size_hint = (0, 0)
            racine.ids.s_liste_eleve.pos_hint = {"x": 1.2, "y": 1.2}
            racine.ids.gl_liste_eleve.clear_widgets()

    def show_student_liste(self, *args):
        self.clear_vie_scolaire()
        etudiant = get_student(args[0])
        racine = self.root.get_screen("teacher")
        racine.ids.s_liste_eleve.size_hint = (0, 0)
        racine.ids.s_liste_eleve.pos_hint = {"x": 1.2, "y": 1.2}
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
        self.clear_vie_scolaire()
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
                racine.ids.gl_write_space.add_widget(pp)
                racine.ids.gl_write_space.add_widget(self.create_lbl(etu[1]))
                racine.ids.gl_write_space.add_widget(self.create_lbl(etu[2]))
                racine.ids.gl_write_space.add_widget(self.create_lbl(etu[3]))

                btn_a = self.add_button(
                    "Absence",
                    (0.1, None),
                    35,
                    15,
                    (0, 0, 0, 0.15)
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
                btn_r.bind(on_release=partial(self.add_retard, etu))
                racine.ids.gl_write_space.add_widget(btn_r)

                btn_e = self.add_button(
                    "Exclusion", (0.1, None), 35, 15, (0, 0, 0, 0.15)
                )
                btn_e.bind(on_release=partial(self.add_exclusion, etu))
                racine.ids.gl_write_space.add_widget(btn_e)

    def create_text_input(self, message, width):
        return TextInput(
            hint_text=f"{message}",
            halign="center",
            multiline=False,
            font_size=15,
            size_hint_x=0.2,
            height=38,
            width=width,
        )

    def vie_sco_panel(self, args):
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

        layout2 = GridLayout(cols=4, spacing=1)
        ti_date = self.create_text_input("Jour/Mois/Année", 120)

        layout2.add_widget(ti_date)

        ti_heure = self.create_text_input("Heure:Minute", 100)
        layout2.add_widget(ti_heure)

        # hint_text=f"{message}",
        # halign="center",
        # multiline=False,
        # font_size=15,
        # size_hint=(None, None),
        # height=38,
        # width=100,
        matieres = [tup[1].title() for tup in mat_by_prof(self.user.get_id())]
        spinner = Spinner(
            halign="center",
            text="Matière",
            values=matieres,
            height=38,
            width=100,
            size_hint=(None, None)
        )

        layout2.add_widget(spinner)

        ti_commentaire = self.create_text_input("Commentaire/Motif", 120)
        layout2.add_widget(ti_commentaire)

        btn_today = self.add_button(
            "Aujourd'hui", (0.08, None), 35, 15, (0, 0, 0, 0.15)
        )
        btn_today.bind(on_release=partial(self.input_today, ti_date))
        layout2.add_widget(btn_today)

        btn_hours = self.add_button(
            "Heure en cours", (0.08, None), 35, 15, (0, 0, 0, 0.15)
        )
        btn_hours.bind(on_release=partial(self.input_hour_min, ti_heure))
        layout2.add_widget(btn_hours)

        return etu, ti_date, ti_heure, ti_commentaire, spinner, layout2

    def add_absence(self, *args):
        racine = self.root.get_screen("teacher")
        racine = self.root.get_screen("teacher")
        textinput = self.vie_sco_panel(args)
        btn_valider = self.add_button(
            "Valider",
            (0.08, None),
            35,
            15,
            (0, 0, 0, 0.15)
        )
        btn_valider.bind(
            on_release=partial(
                self.send_absence,
                textinput[1],
                textinput[2],
                textinput[3],
                textinput[4],
                textinput[0][0],
            )
        )
        layout2 = textinput[5]
        layout2.add_widget(btn_valider)
        racine.ids.gl_write_space.add_widget(layout2)

    def add_retard(self, *args):
        racine = self.root.get_screen("teacher")
        racine = self.root.get_screen("teacher")
        textinput = self.vie_sco_panel(args)
        btn_valider = self.add_button(
            "Valider",
            (0.08, None),
            35,
            15,
            (0, 0, 0, 0.15)
        )
        btn_valider.bind(
            on_release=partial(
                self.send_retard,
                textinput[1],
                textinput[2],
                textinput[3],
                textinput[4],
                textinput[0][0],
            )
        )
        layout2 = textinput[5]
        layout2.add_widget(btn_valider)
        racine.ids.gl_write_space.add_widget(layout2)

    def add_exclusion(self, *args):
        racine = self.root.get_screen("teacher")
        textinput = self.vie_sco_panel(args)
        btn_valider = self.add_button(
            "Valider",
            (0.08, None),
            35,
            15,
            (0, 0, 0, 0.15)
        )
        btn_valider.bind(
            on_release=partial(
                self.send_exclusion,
                textinput[1],
                textinput[2],
                textinput[3],
                textinput[4],
                textinput[0][0],
            )
        )
        layout2 = textinput[5]
        layout2.add_widget(btn_valider)
        racine.ids.gl_write_space.add_widget(layout2)

    def input_today(self, *args):
        today = datetime.now().date().strftime("%d/%m/%Y")
        args[0].text = str(today)

    def input_hour(self, *args):
        hours = datetime.now().strftime("%H")
        args[0].text = str(hours)

    def input_hour_min(self, *args):
        hours = datetime.now().strftime("%H:%M")
        args[0].text = str(hours)

    def send_absence(self, *args):
        if self.valid_vie_sco(args[:4]):
            date = args[0].text
            heure = args[1].text
            matiere = args[3].text
            comment = args[2].text if args[2] != "" else "Pas de commentaire"
            add_absence_vie_scolaire(
                args[4], self.user.get_id(), matiere, date, heure, comment
            )
        self.reset_vie_sco(args[:4])

    def send_retard(self, *args):
        if self.valid_vie_sco(args[:4]):
            date = args[0].text
            heure = args[1].text
            matiere = args[3].text
            comment = args[2].text if args[2] != "" else "Pas de commentaire"
            add_retard_vie_scolaire(
                args[4], self.user.get_id(), matiere, date, heure, comment
            )
        self.reset_vie_sco(args[:4])

    def send_exclusion(self, *args):
        if self.valid_vie_sco(args[:4]):
            date = args[0].text
            heure = args[1].text
            matiere = args[3].text
            comment = args[2].text if args[2] != "" else "Pas de motif"
            add_exclusion_vie_scolaire(
                args[4], self.user.get_id(), matiere, date, heure, comment
            )
        self.reset_vie_sco(args[:4])

    def valid_vie_sco(self, args):
        flag = True
        for el in args:
            el.background_color = (1, 1, 1, 1)
        if args[0].text == "":
            flag = False
            args[0].background_color = (1, 0, 0, .3)
        if args[1].text == "":
            flag = False
            args[1].background_color = (1, 0, 0, .3)
        if args[3].text == "Matière":
            flag = False
            args[3].background_color = (1, 0, 0, .3)
        return flag

    def reset_vie_sco(self, args):
        args[0].text = ""
        args[1].text = ""
        args[2].text = ""
        args[3].text = "Matière"


if __name__ == "__main__":
    app = Application()
    app.run()
