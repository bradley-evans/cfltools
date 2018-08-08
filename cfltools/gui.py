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
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

# class ScreenStart(Screen):
#     pass


# class ScreenLogparse(Screen):
#     pass


# class MainMenu(FloatLayout):
#     manager = ObjectProperty(None)


class IncidentListDropDown(DropDown):
    pass
    # def get_incidents(self):
    #     # TODO: implement this
    #     incidents = ['fillerincident1', 'fillerincident2', 'fillerincident3']
    #     return incidents

    # def build_menu(self):
    #     self.incidents = self.get_incidents()
    #     for incident in self.incidents:
    #         button = Button(text=incident, height=20)
    #         self.add_widget(button)
    #     print('hi from build()')


class BrowseForFile(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ScreenLogparse(BoxLayout):
    logfile = ''  # The logfile we want to examine.
    dropdown = IncidentListDropDown()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_browseforfile(self):
        content = BrowseForFile(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title='Browse for Logfile', content=content,
                            size_hint=(0.7, 0.7))
        self._popup.open()

    # def show_incidentiddropdown(self):
    #     self.dropdown = IncidentListDropDown()
    #     self.dropdown.build_menu()
    #     self.dropdown.open(self.ids.incidentid)
    #     self.dropdown.bind(on_select=lambda instance,
    #                        x: setattr(self.ids.incidentid, 'text', x))

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

    def submit(self, filename, incidentid, whois, tor):
        print('Test submission from ScreenLogparse().')
        print(filename)
        print(incidentid)
        if whois:
            print('Whois flag set.')
        if tor:
            print('Tor flag set.')


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
