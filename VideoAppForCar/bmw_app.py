from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
import os
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.checkbox import CheckBox
from kivy.core.audio import SoundLoader
import datetime
from kivy.clock import Clock 
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivymd.toast import toast
from kivymd.uix.list import ILeftBody, OneLineAvatarListItem
import VidePlayer
from kivy.uix.behaviors import ButtonBehavior
from kivy.utils import get_color_from_hex
import RippleMusicClass
import FileChooserPop
from kivy.graphics import Rectangle
from kivy.core.window import Window

class starter_life(FloatLayout):
    def __init__(self,**kwargs):
        super(starter_life,self).__init__(**kwargs)
        self.chemi_lay=animated_lay()
        self.add_widget(self.chemi_lay)
        self.anim=Animation(pos=(300,300),duration=3)+Animation(size=(300,300),duration=3)

        self.anim.bind(on_complete=self.damimate, on_progress = self.change_pos)
        self.anim.start(self.chemi_lay)


        with self.canvas.before:
            self.otxkutxedi = Rectangle()


    def damimate(self,animacia,gilaki):
        self.remove_widget(self.chemi_lay)
        self.add_widget(info_layer())
    def change_pos(self, animacia, gilaki, progess):
        self.otxkutxedi.pos =gilaki.pos
        self.otxkutxedi.size = gilaki.size


class animated_lay(BoxLayout):
    def __init__(self,**kwargs):
        super(animated_lay,self).__init__(**kwargs)


class info_layer(FloatLayout):
    def __init__(self,**kwargs):
        super(info_layer,self).__init__(**kwargs)
        # saatis_machvenebeli_chartos
        # musikis grafashi ro sheval daprintos ro shevedi am velshi
        self.ids.mus_screen.bind(on_enter=self.michvene_roshexvedi)
        # musikis gilakshi shesvlisas daprintos romeli veli davtove
        self.ids.menu_screen.bind(on_leave=self.davtove_screen)
        self.img_flchzr = FileChooserPop.MyPop()
        self.ids.vid_screen.add_widget(VidePlayer.VideoPlayerLayout())



    def machvene_vinvar(self,instance):
        self.ids.menu_screen.manager.current=str(instance.text)
        self.ids.menu_screen.manager.transition.direction="left"

    def michvene_roshexvedi(self,screen):
        print("shevedi",screen)

    def davtove_screen(self,screen):
        print("davtove",screen)


    def update_time(self,*args):
        dro=str(datetime.datetime.today().today().time())
        tarigi=str(datetime.date.today())
        self.ids.timelbl.text='[color=#FFD600]%s \n %s[/color]'%(dro [:8],tarigi)

class MyButt(ButtonBehavior,Label):
    def __init__(self, **kwargs):
        super(MyButt, self).__init__(**kwargs)
        self.font_name='digital-7.ttf'
        self.font_size='50sp'

class MyButtImg(ButtonBehavior,Image):
    def __init__(self, **kwargs):
        super(MyButtImg, self).__init__(**kwargs)

        
class CustomNavigationDrawerIconButton(OneLineAvatarListItem):
    source = StringProperty()

    def _set_active(self, active, nav_drawer):
        pass
class AvatarSampleWidget(ILeftBody, Image):
    pass






class bmw_app(MDApp):
    def __init__(self,**kwargs):
        super(bmw_app,self).__init__(**kwargs)
        self.on_start=self.gamikete
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = '200'
        self.theme_cls.accent_palette = 'LightBlue'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.ripple_color=get_color_from_hex('#ff0000')

    def gamikete(self,*args):
        print("shevedi")

    def build(self):
        return starter_life()


if __name__=='__main__':
    bmw_app().run()
