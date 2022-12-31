from login import verify
from management import info_etu
from kivy.app import App
<<<<<<< HEAD
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
=======

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
>>>>>>> 6fa8d465c570583563adf0fa482c804e0264af4a


# CREATION DES CLASS REPRÉSENTANT NOS WINDOWS
class FirstWindow(Screen):
    pass


class StudWindow(Screen):
    def build(self):
        pass

    def test(self):
        print("test")

class FileChose(Screen):
    def selected(self, filename): 
        
        
        try:
           
            self.ids.i_image.source = filename[0]
       
            print(filename[0])
           
         
        except: 
          
            pass
        
class TeachWindow(Screen):
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

<<<<<<< HEAD
=======
    def solo_check(self): 
        if self.root.get_screen("addstudent").ids.ck_h.active == True:

            self.root.get_screen("addstudent").ids.ck_h.active = False
    def solo_check2(self):    
        if self.root.get_screen("addstudent").ids.ck_f.active == True:
 
            self.root.get_screen("addstudent").ids.ck_f.active = False
>>>>>>> 6fa8d465c570583563adf0fa482c804e0264af4a
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
                    print("prof but no panel")
                if verif[0] == "admin":
                    print("wtf not implement yet, how can you be admin")
            else:
                self.resetchamp(False)

<<<<<<< HEAD
=======
    def reset_addstudent(self): 
        self.root.get_screen("addstudent").ids.t_nom.text = ""
        self.root.get_screen("addstudent").ids.t_prenom.text = ""
        self.root.get_screen("addstudent").ids.i_etu.source = ""
        self.root.get_screen("addstudent").ids.ck_h.active = False
        self.root.get_screen("addstudent").ids.ck_f.active = False
        self.root.get_screen("addstudent").ids.i_year.text = ""
    def save_image(self,filename): 
        try : 
            self.root.get_screen("addstudent").ids.i_etu.source = filename[0]
            print(filename[0])
        except : 
            pass

>>>>>>> 6fa8d465c570583563adf0fa482c804e0264af4a

if __name__ == "__main__":
    app = Application()
    app.run()
