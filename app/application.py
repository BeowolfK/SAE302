import kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
Builder.load_file("application.kv")

class Application(App): 
    def build(self):
        pass

if __name__ == "__main__":
    app = Application()
    app.run()  