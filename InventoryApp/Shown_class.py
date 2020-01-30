# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
import Main
from kivy.core.window import Window



class monacemebi(BoxLayout):
    day = ObjectProperty()
    month = ObjectProperty()
    year = ObjectProperty()
    def __init__(self,gamoidzaxe_row,gamoidzaxe_nomeri,gamoidzaxe_gacema,gamoidzaxe_vada,gamoidzaxe_statusi, **kwargs):
        super(monacemebi, self).__init__(**kwargs)
        Window.bind(on_resize = self.window_size_changed)
        self.size_hint_y = None

        self.number_label = Label(text =gamoidzaxe_nomeri, font_size = Window.width/68.3, size_hint=(None,None))
        self.add_widget(self.number_label)

        self.lbl = Label(text= gamoidzaxe_row, font_name="bpg_arial_2009", font_size = Window.width/68.3)
        self.add_widget(self.lbl)

        self.gacem_date = Label(text =gamoidzaxe_gacema, font_size = Window.width/68.3)
        self.add_widget(self.gacem_date)

        self.vada_lbl = Label(text =gamoidzaxe_vada, font_size = Window.width/68.3)
        self.add_widget(self.vada_lbl)

        self.status_label = Label(markup = True,text= gamoidzaxe_statusi,font_name="bpg_arial_2009", font_size= Window.width/68.3)
        self.add_widget(self.status_label)

        self.delete_button=(Button(background_normal = "ICONS/delete_on.png"
                                   ,size_hint_x = .50))
        self.delete_button.bind(on_release = self.delete)
        self.add_widget(self.delete_button)


    def delete(self, *args):
        self.clear_widgets()
        self.delete_comand = Main.con.execute("delete from Item_list where gacema='%s' and vada='%s'"%(self.gacem_date.text,self.vada_lbl.text))

 
    def window_size_changed(self,window, width,height):
        for child in self.children:
            child.font_size = width/68.3
            
