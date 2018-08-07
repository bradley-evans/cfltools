"""
GUI frontend for cfltools. We use Kivy for the GUI.
Other components are located in a Kivy file in this directory.
"""

import kivy
import os
import pdb

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

# class ScreenStart(Screen):
#     pass


# class ScreenLogparse(Screen):
#     pass


# class MainMenu(FloatLayout):
#     manager = ObjectProperty(None)


class BrowseForFile(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ScreenLogparse(BoxLayout):
    logfile = ''  # The logfile we want to examine.

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_browseforfile(self):
        content = BrowseForFile(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title='Browse for Logfile', content=content,
                            size_hint=(0.7, 0.7))
        self._popup.open()

    def load(self, path, filename):
        if len(filename) > 1:
            # TODO: handle this exception correctly
            print("Error: more than one file selected")
            exit(1)
        try:
            self.logfile = filename[0]
            self.ids.logfile_name.text = self.logfile
        except IndexError as e:
            print(e)
            self.logfile = ''
            self.ids.logfile_name.text = self.logfile
        self.dismiss_popup()


class Manager(BoxLayout):
    sm = ObjectProperty()

    def set_previous_screen(self):
        if self.sm.current != 'start':
            self.sm.transition.direction = 'right'
            self.sm.current = self.sm.previous()


class CFLToolsApp(App):

    def build(self):
        root = Manager()
        return root


def gui():
    print('In gui().')
    CFLToolsApp().run()
