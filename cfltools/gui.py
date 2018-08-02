import kivy

from kivy.app import App
from kivy.uix.label import Label

class TestGui(App):

    def build(self):
        return Label(text='Hello, world!')

def gui():
    print('In gui().')
    TestGui().run()
