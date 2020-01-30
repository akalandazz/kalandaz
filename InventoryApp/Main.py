# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
import pyodbc
from kivy.config import Config
import kivy
from kivy.uix.image import Image
import Show_layout, Tabbed_class
from kivy.animation import Animation
from kivy.core.window import Window



kivy.require('1.10.1')

#Maximize window
Config.set('graphics', 'window_state', 'maximized')
Config.write()



con = False
try:
    connection = pyodbc.connect(r'akalandia.mdf')
    con = connection
except:
    con = False



class Controller(ScreenManager):
    def __init__(self, **kwargs):
        kwargs.setdefault('size', (Window.width, Window.height))
        super(Controller, self).__init__(**kwargs)
        self.add_widget(Main_screen(name= "Main"))
        self.add_widget(Show_screen(name = "Show"))
        self.add_widget(add_member(name = "register"))
        self.add_widget(about_screen(name="Description"))




class about_screen(Screen):
    def __init__(self, **kwargs):
        super(about_screen,self).__init__(**kwargs)
        self.back_button = Button(size_hint_x=.08, size_hint_y=.10,pos_hint={'x': .02, 'y': .88},
                                  background_normal = "ICONS/Back_on.png",
                                  background_down ="ICONS/Back_off.png" )
        self.back_button.bind(on_release=self.back_button_main)
        self.add_widget(self.back_button)
        self.add_widget(Image(source= "ICONS/logo.png", pos_hint={'x':.38, 'y':.60}, size_hint =(.15,.15)))

        self.add_widget(Label(markup = True, text= "[color=#ff4400]პროგრამის ავტორი: ი-რი ამირან კალანდია\nპროექტის ხელმძღვანელი: მ-რი შალვა გელაძე[/color]",
                              font_name="bpg_arial_2009", font_size = 26, pos_hint = {'x': .30, 'y':.40}, size_hint =(.30, .15)))


    def back_button_main(self, *args):
        self.manager.current = "Main"
        self.manager.transition.direction = "left"


class Main_screen(Screen):
    def __init__(self, **kwargs):
        super(Main_screen,self).__init__(**kwargs)
        Window.bind(on_resize = self.window_size_change)
        self.main_lay = BoxLayout(orientation="vertical",size_hint_x = .208,size_hint_y =.62)
        self.add_widget(self.main_lay)

        self.connection_lbl = Label(markup = True ,font_name="bpg_arial_2009", pos_hint={'x':.32,'y':.40})
        self.add_widget(self.connection_lbl)



        if con:
            self.connection_lbl.text = "[color=#55FB0E]მონაცემთა ბაზასთან დაკავშირებულია[/color]"
            self.add_widget(Image(source='ICONS/on_connection.png',
                                  pos_hint={'x':.46,'y':.40}))



        else:
            self.connection_lbl.text = "[color=#ff0000]მონაცემთა ბაზასთან კავშირი არ არის[/color]"
            self.add_widget(Image(source='ICONS/off_connection.png',
                                  pos_hint={'x':.46,'y':.40}))

        self.search_button = Button(background_normal = "ICONS/on_search.png",
                                 background_down ="ICONS/off_search.png")
        self.search_button.bind(on_release = self.open_info_field)
        self.main_lay.add_widget(self.search_button)





        self.add_button = Button(background_normal = "ICONS/on_add.png",
                                 background_down ="ICONS/off_add.png")
        self.add_button.bind(on_release = self.open_addmember)
        self.main_lay.add_widget(self.add_button)



        self.about_button = Button(background_normal = "ICONS/on_about.png",
                                 background_down ="ICONS/off_about.png",
                                   size_hint=(.202,.31),pos=(900, 10))
        self.about_button.bind(on_release = self.open_about_screen)
        self.add_widget(self.about_button)

        animation1 = Animation(pos=(Window.width/2.85, Window.height/6.53), t='out_bounce', duration=2)
        animation1.start(self.main_lay)


        animation2 = Animation(pos=(Window.width/1.97, Window.height/3.28), t='out_bounce', duration=2)
        animation2.start(self.about_button)


    def open_about_screen(self, *args):
        self.manager.current = "Description"
        self.manager.transition.direction = "right"



    def open_addmember(self, *args):
        self.manager.current = "register"
        self.manager.transition.direction = "up"




    def open_info_field(self, *args):
        self.manager.current = "Show"
        self.manager.transition.direction = "down"


    def window_size_change(self,window,width,height):
        self.main_lay.pos = (width/2.85,Window.height/6.53)
        self.about_button.pos = (width/1.97, height/3.28)







class Show_screen(Screen):
    def __init__(self, **kwargs):
        super(Show_screen, self).__init__(**kwargs)
        self.back_button = Button(size_hint_x=.08, size_hint_y=.10,pos_hint={'x': .02, 'y': .89},
                                  background_normal = "ICONS/Back_on.png",
                                  background_down ="ICONS/Back_off.png" )
        self.back_button.bind(on_release=self.back_button_func)
        self.add_widget(self.back_button)


        self.chveneba=Show_layout.Shown_Mama()
        self.add_widget(self.chveneba)



    def back_button_func(self, *args):
        self.manager.current = "Main"
        self.manager.transition.direction = "up"





class add_member(Screen):
    saxeli = ObjectProperty()
    gvari = ObjectProperty()
    def __init__(self,**kwargs):
        super(add_member, self).__init__(**kwargs)
        self.back_button = Button(size_hint_x=.08, size_hint_y=.10,pos_hint={'x': .02, 'y': .90},
                                  background_normal = "ICONS/Back_on.png",
                                  background_down ="ICONS/Back_off.png")
        self.back_button.bind(on_release=self.back_button_func)
        self.add_widget(self.back_button)
        self.tabb_panel=Tabbed_class.Tab_panel()
        self.add_widget(self.tabb_panel)


    def back_button_func(self, *args):
        self.manager.current = "Main"
        self.manager.transition.direction = "down"







class Test_APP(App):
    def build(self):
        self.title="აღჭურვილობა"
        self.icon = "ICONS/user.png"
        return Controller()

if __name__=='__main__':
    Test_APP().run()
