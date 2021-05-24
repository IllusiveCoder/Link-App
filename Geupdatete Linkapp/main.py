from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.core.window import Window
from kivy.lang.builder import Builder
import webbrowser
import json
import time
import kivy.uix.widget
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty
from kivy.clock import Clock
from functools import partial

class speicher():
    
    dictionary = {}
    schlüssel = {}
    dictlänge = 0 
    data = None
    counter = 0
    neuepos = 0
    update = False
    
class storage_system():
        
    def suche_schluessel(self, value):
        for schluessel, wert in speicher.schlüssel.items():
            if value == wert:
                return schluessel
        return None
            
        
    def aktualisieren(self):
        with open("storage.json", "w") as file:
            json.dump(speicher.dictionary, file, indent = 4)
        
        with open("storage.json", "r") as myfile:
            speicher.data = myfile.read()
            speicher.dictionary = json.loads(speicher.data)
            speicher.dictlänge = len(speicher.dictionary)
        
        with open("key_names.json", "w") as file:
            json.dump(speicher.schlüssel, file, indent = 4)
        
        with open("key_names.json", "r") as file:
            speicher.data = file.read()
            speicher.schlüssel = json.loads(speicher.data)
        
        speicher.update = True
        
            
    def add(self, eingabe1, eingabe2):
        speicher.dictlänge += 1
        speicher.dictionary[str(speicher.dictlänge)] = str(eingabe1)
        speicher.schlüssel[str(speicher.dictlänge)] =  str(eingabe2)
        storage_system.aktualisieren(self)
            
    def loeschen(self, eingabe_zahl, eingabe_name):
        try:
            speicher.counter = int(storage_system.suche_schluessel(self,eingabe_name))
        except:  
            speicher.counter = int(eingabe_zahl)

        try:
            if speicher.counter and  speicher.dictlänge == 1 or speicher.counter == speicher.dictlänge:
                speicher.schlüssel.pop(str(speicher.counter))
                speicher.dictionary.pop(str(speicher.counter))
                storage_system.aktualisieren(self)
            elif speicher.counter <= speicher.dictlänge:
                while speicher.counter <= speicher.dictlänge:
                    speicher.dictlänge = len(speicher.dictionary)
                    speicher.neuepos = speicher.counter
                    speicher.counter += 1
                    speicher.schlüssel[str(speicher.neuepos)] = speicher.schlüssel.pop(str(speicher.counter))
                    speicher.dictionary[str(speicher.neuepos)] = speicher.dictionary.pop(str(speicher.counter))
                    storage_system.aktualisieren(self)
        except:
            speicher.dictlänge = len(speicher.dictionary)

with open("storage.json", "r") as myfile:
    speicher.data = myfile.read()
    speicher.dictionary = json.loads(speicher.data)
    if  len(speicher.dictionary) > 0:
        speicher.dictlänge = len(speicher.dictionary)
    elif len(speicher.dictionary) == 0:
        speicher.dictlänge = 0
        
with open("key_names.json", "r") as keyfile:
    speicher.data = keyfile.read()
    speicher.schlüssel = json.loads(speicher.data)

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        Clock.schedule_interval(self.prüfen, 1.2)
        if speicher.dictlänge == 0:
            self.data = []
        elif speicher.dictlänge > 0:
            self.data = [{'text': str(x) + ": " + str(speicher.schlüssel[str(x)]), 'on_release': partial(self.oeffnen, x)} for x in range(1,speicher.dictlänge+1)]
    
    def prüfen(self, no_need):
        if speicher.update == True:
            self.erneuern()
            speicher.update = False
            
    def erneuern(self):
        self.data = [{'text': str(x) + ": " + str(speicher.schlüssel[str(x)]), 'on_release': partial(self.oeffnen, x)} for x in range(1,speicher.dictlänge+1)]
        
        
    def oeffnen(self, x):
        webbrowser.open(str(speicher.dictionary[str(x)]))
                         
class Startscreen(Screen):
        
    def change_to_mainscreen(self, *args):
        self.manager.current = "mainscreen"
        self.ids.starten.background_color = (1,1,1,0.05)
        
    def end_screen(self, *args):
        hauptgui().stop()
        
    def starten(self):
        # Erste Animation
        animate = Animation( background_color = (1,1,1,1), duration = 0.5)
        # Zweite Animation
        animate += Animation( background_color = (0,0,0,0), duration = 0.5)
        # Binden von Methode
        animate.bind(on_complete = self.change_to_mainscreen)
        # Starte Animation
        animate.start(self.ids.starten)
        
    def beenden(self):
        # Erste Animation
        animate = Animation( background_color = (1,1,1,1), duration = 0.5)
        # Zweite Animation
        animate += Animation( background_color = (0,0,0,0), duration = 0.5)
        # Binden von Methode
        animate.bind(on_complete = self.end_screen)
        # Starte Animation
        animate.start(self.ids.beenden)
                
class Mainscreen(Screen):
    pass
        
class Addscreen(Screen):
    
    def add(self):
        try:
            storage_system.add(self, self.ids.add_inhalt.text,self.ids.add_text.text)
            self.ids.add_text.text = ""
            self.ids.add_inhalt.text = ""
        except:
            self.ids.add_text.text = "Fehler"
            self.ids.add_inhalt.text = "Fehler"
            time.sleep(1.5)
            self.ids.add_text.text = ""
            self.ids.add_inhalt.text = ""
        
class Deletescreen(Screen):
    
    def delete(self):
        try:
            self.ids.status_label.text = "Status: wird gelöscht..."
            storage_system.loeschen(self,self.ids.nummer_loeschen.text, self.ids.name_loeschen.text)
            self.ids.nummer_loeschen.text = ""
            self.ids.name_loeschen.text = ""
        except:
            self.ids.status_label.text = "Status: Fehler"
            time.sleep(2)
            self.ids.nummer_loeschen.text = ""
            self.ids.name_loeschen.text = ""
            self.ids.status_label.text = "Status: ----"
            
           
class Wmanager(ScreenManager):
    pass

class hauptgui(App):
    def build(self):
        with open("guicode.kv", encoding="utf8") as file:
            guidesign = Builder.load_string(file.read())
            return guidesign

if __name__ == "__main__":
    hauptgui().run()

