import threading
import time
from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.properties import NumericProperty, StringProperty, ListProperty, DictProperty

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'meiryo.ttc')

class StackArea(Widget):
    start_address = StringProperty()
    end_address = StringProperty()

    def __init__(self, **kwargs):
        super(StackArea, self).__init__(**kwargs)

    def set_address(self, l):
        self.start_address = str(l[0])
        self.end_address = str(l[1])

class HeapArea(Widget):
    start_address = StringProperty()
    end_address = StringProperty()

    def __init__(self, **kwargs):
        super(HeapArea, self).__init__(**kwargs)

class StartMemory(Widget):
    pass

class MemoryRoot(FloatLayout):
    address_dic = DictProperty({})
    def __init__(self, **kwargs):
        super(MemoryRoot, self).__init__(**kwargs)
        self.address_dic = {
            '.text': [],
            '.data': [],
            '.bss': [],
            'heap': [],
            'stack': []
        }
    
    def address_value(self, key):
        return str(self.address_dic[key][0])

    def set_address(self, dic):
        for key in dic:
            self.address_dic[key] = dic[key]
        self.clear_widgets()
        self.add_widget(StartMemory())
        for key in self.address_dic:
            if self.address_dic[key]:
                w = StackArea()
                w.set_address(self.address_dic[key])
                self.add_widget(w)
    def clear(self):
        self.clear_widgets()
    


class MemoryApp(App):
    def __init__(self, **kwargs):
        super(MemoryApp, self).__init__(**kwargs)
        self.title = 'Memory Visualizer'

    def build(self):
        self.widget = MemoryRoot()
        return self.widget

    def clear(self):
        self.widget.clear()
    
    def set_address(self, dic):
        self.widget.set_address(dic)

    
def set_address(app, dic):
    app.set_address(dic)

def clear(app):
    app.clear()

def app_run(app):
    app.run()
