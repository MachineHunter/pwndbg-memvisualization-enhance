import logging
from typing import Dict, List
import numpy
import copy
logging.getLogger("kivy").disabled = True

from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, ListProperty, DictProperty, BooleanProperty, ObjectProperty

class HelpMemory(Widget):
    pass

class HelpMemory(Widget):
    pass

class SectionArea(Widget):
    start_address = StringProperty()
    end_address = StringProperty()
    area_height = NumericProperty()
    text = StringProperty()
    text_color = StringProperty('#ffffff')
    x = NumericProperty(0.5)
    y = NumericProperty()
    pos_x = NumericProperty(0.1)
    top = NumericProperty()
    font_size = StringProperty('24')
    color = StringProperty('#ffffff')
    label_x = NumericProperty(0.65)
    label_size = ListProperty([0.15, 0.02])
    label_font_size = StringProperty('18')
    label_color = StringProperty('#000000')

    def __init__(self, **kwargs):
        super(SectionArea, self).__init__(**kwargs)

    def set_config(self, y, l, text, top, font_size, color, label_size_rate):
        self.y = y
        self.start_address = hex(l[0])
        self.end_address = hex(l[1])
        self.text = text
        self.top = top
        self.font_size = font_size
        self.color = color
        self.label_size[1] = label_size_rate

class RegisterArea(Widget):
    y = NumericProperty(0)
    text = StringProperty()
    label_size = NumericProperty(0.02)
    def __init__(self, **kwargs):
        super(RegisterArea, self).__init__(**kwargs)
    
    def set_point(self, y, text, label_size):
        self.y = y
        self.text = text
        self.label_size = label_size

class StackFrame(Widget):
    y1 = NumericProperty(0)
    y2 = NumericProperty(0)
    text = StringProperty("")
    label_size = NumericProperty(0.02)
    def __init__(self, **kwargs):
        super(StackFrame, self).__init__(**kwargs)
    
    def set_frame(self, y1, y2, text, label_size):
        self.y1 = y1
        self.y2 = y2
        self.text = text
        self.label_size = label_size

class Mark(Widget):
    y = NumericProperty(0)
    text = StringProperty()
    label_size = NumericProperty(0.02)
    def __init__(self, **kwargs):
        super(Mark, self).__init__(**kwargs)
    
    def set_point(self, y, text, label_size):
        self.y = y
        self.text = text
        self.label_size = label_size

class NoneArea(SectionArea):
    memory_height = NumericProperty()
    def __init__(self, **kwargs):
        super(NoneArea, self).__init__(**kwargs)
        self.memory_height = 0.9
        self.top = 0.95
    
    def set_config(self, margin_y, all_y):
        self.memory_height = (all_y - margin_y) / all_y
        self.top = (all_y - margin_y/2) / all_y

class StartMemory(BoxLayout):
    scroll_height = NumericProperty()
    def __init__(self, **kwargs):
        super(StartMemory, self).__init__(**kwargs)
        self.scroll_height = 700

    def set_height(self, height):
        self.scroll_height = height

class SnapMemory(BoxLayout):
    scroll_height = NumericProperty()
    def __init__(self, **kwargs):
        super(SnapMemory, self).__init__(**kwargs)
        self.scroll_height = 700

    def set_height(self, height):
        self.scroll_height = height

class MemoryRoot(FloatLayout):
    address_dic = DictProperty({})
    other_dic = DictProperty({})
    address_dic_snap = DictProperty({})
    other_dic_snap = DictProperty({})
    areas = ListProperty(['.plt', '.plt.got', '.text', '.got', '.got.plt', '.data', '.bss', 'heap', '︙', 'libc', 'ld', 'stack_unused', 'stack'])
    scroll_height = NumericProperty()
    y_dic = DictProperty({})
    y_rate_dic = DictProperty({})
    top_dic = DictProperty({})
    label_size = NumericProperty()
    base_y = NumericProperty(8)
    base_label_size = NumericProperty(36)
    base_y_pxcel = NumericProperty(50)
    margin_y = NumericProperty(180)
    mapped_y = NumericProperty(360)
    all_y = NumericProperty(0)
    meminfo = ObjectProperty()
    def __init__(self, **kwargs):
        super(MemoryRoot, self).__init__(**kwargs)
    
    def set_memory(self, t):
        self.clear_widgets()
        self.all_y = 0
        self.y_dic = {}
        self.y_rate_dic = {}
        self.top_dic = {}
        if t == 'realtime':
            self.sm = StartMemory()
            address_dic = self.address_dic
        elif t == 'snapshot':
            self.sm = SnapMemory()
            address_dic = self.address_dic_snap
        self.calc_y(t)
        self.calc_top()
        self.label_size = self.base_label_size/self.all_y
        self.sm.set_height(self.all_y)
        self.add_widget(self.sm)
        base = self.sm.ids['base_area']
        address_dic['︙'] = [address_dic['heap'][1], address_dic['libc'][0]]
        for key in address_dic:
            text = key + "(" + str(address_dic[key][1] - address_dic[key][0]) + "bytes)"
            if address_dic[key][0] == address_dic[key][1]:
                continue
            if key == '.plt':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#ffd700', self.label_size)
                base.add_widget(w)
            elif key == '.plt.got':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#ffa500', self.label_size)
                base.add_widget(w)
            elif key == '.text':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#ff8c00', self.label_size)
                base.add_widget(w)
            elif key == '.got':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#f4a460', self.label_size)
                base.add_widget(w)
            elif key == '.got.plt':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#ff7f50', self.label_size)
                base.add_widget(w)
            elif key == '.data':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#ff4500', self.label_size)
                base.add_widget(w)
            elif key == '.bss':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#ff69b4', self.label_size)
                base.add_widget(w)
            elif key == 'heap':
                if address_dic['heap'][1] != address_dic['.bss'][1]:
                    w = SectionArea()
                    w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#ee82ee', self.label_size)
                    base.add_widget(w)
            elif key == '︙':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], "None", self.top_dic[key], '24', '#dcdcdc', self.label_size)
                base.add_widget(w)
            elif key == 'libc':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#191970', self.label_size)
                base.add_widget(w)
            elif key == 'ld':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#00008b', self.label_size)
                base.add_widget(w)
            elif key == 'stack_unused':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#778899', self.label_size)
                base.add_widget(w)
            elif key == 'stack':
                w = SectionArea()
                w.set_config(self.y_rate_dic[key], address_dic[key], text, self.top_dic[key], '24', '#0000cd', self.label_size)
                base.add_widget(w)

    def set_address(self, meminfo):
        self.meminfo = meminfo
        if not App.get_running_app().update_enable:
            return
        self.address_dic, self.other_dic = memInfo_turn_to_dic(meminfo)
        self.set_memory("realtime")
        self.set_regs("realtime")
        self.set_frames("realtime")
        self.set_marks("realtime")
    
    def take_snap(self):
        for k in self.address_dic:
            self.address_dic_snap[k] = copy.deepcopy(self.address_dic[k])
        for k in self.other_dic:
            self.other_dic_snap[k] = copy.deepcopy(self.other_dic[k])

    def set_snap(self):
        if not(self.address_dic_snap) and not(self.other_dic_snap):
            #print("There is no snapshot.")
            pass
        else:
            self.set_memory("snapshot")
            self.set_regs("snapshot")
            self.set_frames("snapshot")
            self.set_marks("snapshot")

    def back(self):
        App.get_running_app().set_mode(True)
        self.set_memory("realtime")
        self.set_regs("realtime")
        self.set_frames("realtime")
        self.set_marks("realtime")

    def on_click_freeze_button(self, type_):
        # stop/playのボタンが押された時に発動する関数
        # playが押されたら、updateを開始/stopなら停止
        # 管理する変数は、appのインスタンスに持たせた.(layoutのupdateでこのインスタンスが消えるかも?と思ったので.kivyのライフサイクルまだよくわかってないもので..)
        # print(App.get_running_app().update_enable, type_)
        if type_ == "play":
            App.get_running_app().set_mode(True)
        else:
            App.get_running_app().set_mode(False)
    
    def update(self):
        self.address_dic, self.other_dic = memInfo_turn_to_dic(self.meminfo)
        self.back()

    def set_regs(self, t):
        if t == 'realtime':
            regs = self.other_dic["regs"]
            address_dic = self.address_dic
        elif t == 'snapshot':
            regs = self.other_dic_snap["regs"]
            address_dic = self.address_dic_snap
        base = self.sm.ids['base_area']
        for k, v in address_dic.items():
            if v[0] <= regs["rip"] and regs["rip"] <= v[1]:
                ra = RegisterArea()
                d_address = regs["rip"] - v[0]
                d_rate = self.top_dic[k] - d_address / (v[1] - v[0]) * self.y_rate_dic[k]
                ra.set_point(d_rate, "rip", self.label_size)
                base.add_widget(ra)
            if v[0] <= regs["rsp"] and regs["rsp"] <= v[1]:
                ra = RegisterArea()
                d_address = regs["rsp"] - v[0]
                d_rate = self.top_dic[k] - d_address / (v[1] - v[0]) * self.y_rate_dic[k]
                ra.set_point(d_rate, "rsp", self.label_size)
                base.add_widget(ra)

    def set_frames(self, t):
        if t == 'realtime':
            frames = self.other_dic["frames"]
            address_dic = self.address_dic
        elif t == 'snapshot':
            frames = self.other_dic_snap["frames"]
            address_dic = self.address_dic_snap
        base = self.sm.ids['base_area']
        stack_start = address_dic['stack'][0]
        stack_end = address_dic['stack'][1]
        stack_size = stack_end - stack_start
        if stack_size == 0:
            return
        for k, v in frames.items():
            sf = StackFrame()
            d1_address = v[0] - stack_start
            d2_address = v[1] - stack_start
            d1_rate = self.top_dic['stack'] - d1_address / stack_size * self.y_rate_dic['stack']
            d2_rate = self.top_dic['stack'] - d2_address / stack_size * self.y_rate_dic['stack']
            sf.set_frame(d1_rate, d2_rate, k, self.label_size)
            base.add_widget(sf)

    def set_marks(self, t):
        if t == 'realtime':
            marks = self.other_dic["marks"]
            address_dic = self.address_dic
        elif t == 'snapshot':
            marks = self.other_dic_snap["marks"]
            address_dic = self.address_dic_snap
        base = self.sm.ids['base_area']
        for i in range(len(marks)):
            for k, v in address_dic.items():
                if v[0] <= marks[i] and marks[i] <= v[1]:
                    m = Mark()
                    d_address = marks[i] - v[0]
                    d_rate = self.top_dic[k] - d_address / (v[1] - v[0]) * self.y_rate_dic[k]
                    m.set_point(d_rate, "mark"+str(i), self.label_size)
                    base.add_widget(m)

    def calc_y(self, t):
        if t == 'realtime':
            address_dic = self.address_dic
        elif t == 'snapshot':
            address_dic = self.address_dic_snap
        for key in address_dic:
            d = address_dic[key][1] - address_dic[key][0]
            pxcel = int(d / self.base_y * self.base_y_pxcel)
            if 50 < pxcel:
                pxcel = int(numpy.tanh((pxcel-50)/10000)*1000 + 50)
            self.y_dic[key] = pxcel
        self.y_dic['︙'] = self.mapped_y
        for key in self.y_dic:
            self.all_y += self.y_dic[key]
        self.all_y += self.margin_y
        self.all_y = int(self.all_y)
        for key in self.y_dic:
            self.y_rate_dic[key] = self.y_dic[key] / self.all_y

    def calc_top(self):
        keys = self.areas
        keys = keys[::-1]
        temp_top = self.margin_y / 2
        for key in keys:
            temp_top += self.y_dic[key]
            self.top_dic[key] = temp_top / self.all_y


class MemoryApp(App):
    update_enable = BooleanProperty(True)
    def __init__(self, **kwargs):
        super(MemoryApp, self).__init__(**kwargs)
        self.title = 'Memory Visualizer'

    def build(self):
        self.rootWidget = MemoryRoot()
        return self.rootWidget

    def set_mode(self, b):
        self.update_enable = b

    def get_mode(self):
        return self.update_enable
    
    def set_address(self, meminfo):
        self.rootWidget.set_address(meminfo)

    
def set_address(app, meminfo):
    app.set_address(meminfo)

def app_run(app):
    app.run()

def memInfo_turn_to_dic(meminfo):
    dic1 = {
        '.plt': copy.deepcopy(meminfo.plt_section),
        '.plt.got': copy.deepcopy(meminfo.pltgot_section),
        '.text': copy.deepcopy(meminfo.text_section),
        '.got': copy.deepcopy(meminfo.got_section),
        '.got.plt': copy.deepcopy(meminfo.gotplt_section),
        '.data': copy.deepcopy(meminfo.data_section),
        '.bss': copy.deepcopy(meminfo.bss_section),
        'heap': copy.deepcopy(meminfo.heap),
        'libc': copy.deepcopy(meminfo.libc),
        'ld': copy.deepcopy(meminfo.ld),
        'stack_unused': copy.deepcopy(meminfo.stack_unused),
        'stack': copy.deepcopy(meminfo.stack_used)
    }
    if dic1['heap'][0] == dic1['heap'][1]:
        dic1['heap'][0] = copy.deepcopy(dic1['.bss'][1])
        dic1['heap'][1] = copy.deepcopy(dic1['.bss'][1])
    dic2 = {
        "regs": copy.deepcopy(meminfo.regs),
        "frames": copy.deepcopy(meminfo.frames),
        "marks": copy.deepcopy(meminfo.marks)
    }
    return dic1, dic2
