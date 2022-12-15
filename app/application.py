import kivy 
from login import * 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


# CREATION DES CLASS REPRESANTANT NOS WINDOWS
class FirstWindow(Screen):
    pass
class StudWindow(Screen): 
    pass 
class TeachWindow(Screen):
    pass
class WindowManager(ScreenManager):
    pass
Builder.load_file("application.kv")

class Application(App): 
    def build(self):
        pass

    def valider(self): 
        """
        Fait une requete pour savoir si c'est un étudiant, un prof, autre et en fonction renvoie la valeur pour switch faire la bonne fenêtre. 
        """
        if self.root.get_screen("hub").ids.identif.text != "" and self.root.get_screen("hub").ids.mdp.text != "":
            identifiant = self.root.get_screen("hub").ids.identif.text
            motdp = self.root.get_screen("hub").ids.mdp.text 
            verif = verify(identifiant, motdp)
            if verif != None : 
                if verif[0] == 'etu':
                    self.root.get_screen("second").ids.nom.text = str(verif[1]) 
                    return "second"
    def resetchamp(self):
        self.root.get_screen("hub").ids.identif.text = "" 
        self.root.get_screen("hub").ids.mdp.text = ""
       
if __name__ == "__main__":
    app = Application()
    app.run()  