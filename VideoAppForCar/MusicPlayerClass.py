from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.behaviors import TouchRippleBehavior
from kivy.utils import get_color_from_hex
from kivy.uix.bubble import Bubble
import FileChooserPop
from kivy.uix.image import Image
from kivy.base import Builder
import os
from kivymd.uix.card import MDCardPost
from kivy.uix.floatlayout import FloatLayout
class MusicPlayerLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MusicPlayerLayout, self).__init__(**kwargs)
        print(self.ids.but)
        self.mus_pop =MyMusPop()

class MyMusPop(Popup):
    def __init__(self, **kwargs):
        super(MyMusPop, self).__init__(**kwargs)
        self.size_hint=None,None
        self.on_open = self.open_pop
        self.on_dismiss = self.pop_dismiss
        self.myfile = FileChooserIconView(filters = ['*.mp4','*.MOV','*.mpg'])
        self.pop_lay= BoxLayout(orientation = 'vertical')
        self.pop_lay.add_widget(self.myfile)
        self.pop_lay.add_widget(Button(text='Close',on_press = self.dismiss, size_hint_y=.10))
        

    def open_pop(self):
        self.anim = Animation(size=(Window.width, Window.height), duration =0.5,t='in_expo')
        self.anim.bind(on_complete = self.completed_progress)
        self.anim.start(self)
        
    def completed_progress(self,animation, widget):
        self.content = self.pop_lay

    def pop_dismiss(self):
        self.anim = Animation(size=(200, 200), duration =0.5,t='in_expo')
        self.anim.start(self)
Builder.load_string("""
<MusicPlayerLayout>:
    
    BoxLayout:
        orientation:'vertical'
        spacing:20
        padding:15
        Carousel:
            id:mus_karuseli
            Button:
        Slider:
            size_hint_y:.20
            id:mus_slider

        BoxLayout:     
            size_hint_y:.30
            canvas.before:
                Line:
                    rectangle:self.x,self.y, self.width, self.height
            Label:
                text:str(int(mus_slider.value))
                text_size:self.size
                valign:'top'
            Label:
                text:'text1'
                text_size:self.size
                valign:'top'
                halign:'right'
        BoxLayout: 
            canvas.before:
                Line:
                    rectangle:self.x,self.y, self.width, self.height
            size_hint_y:.25
            spacing:10
            Button:
                text:'shuffle'
            Button:
                id:but
                text:'back'
            ToggleButton:
                text:'pause/play'
            Button:
                text:'next'
            Button:
                text:'rotation'
        BoxLayout:
            canvas.before:
                Line:
                    rectangle:self.x,self.y, self.width, self.height
            size_hint_y:.20
            Label:
                text:'vol_down'
            Slider:
                id:vol_slider
            Label:
                text:'max'
        BoxLayout:
            size_hint_y:.20
            Button:
                text:'Pla'
"""
)

class app(App):
    def __init__(self, **kwargs):
        super(app, self).__init__(**kwargs)
    def build(self):
        return MusicPlayerLayout()


app().run()