import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


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

        if (
            self.root.get_screen("hub").ids.identif.text != ""
            and self.root.get_screen("hub").ids.mdp.text != ""
        ):
            identifiant = self.root.get_screen("hub").ids.identif.text
            motdp = self.root.get_screen("hub").ids.mdp.text

            return "second"


if __name__ == "__main__":
    app = Application()
    app.run()
