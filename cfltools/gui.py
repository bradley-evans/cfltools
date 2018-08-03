import kivy

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty


# class ScreenStart(Screen):
#     pass


# class ScreenLogparse(Screen):
#     pass


# class MainMenu(FloatLayout):
#     manager = ObjectProperty(None)


class Manager(BoxLayout):

    sm = ObjectProperty()

    def set_previous_screen(self):
        if self.sm.current != 'start':
            self.sm.transition.direction = 'right'
            self.sm.current = self.sm.previous()


class CFLToolsApp(App):

    def build(self):
        return Manager()


def gui():
    print('In gui().')
    CFLToolsApp().run()
