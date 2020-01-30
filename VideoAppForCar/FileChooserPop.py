from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.behaviors import TouchRippleBehavior
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.base import Builder
from kivy.uix.label import Label




class MyPop(Popup):
    def __init__(self, **kwargs):
        super(MyPop, self).__init__(**kwargs)
        self.on_open = self.open_pop
        self.on_dismiss = self.pop_dismiss
        self.title = 'Import Music'
        self.size_hint=(None,None)
        self.pop_cont_lay=BoxLayout(orientation="vertical")
        self.myprogress=MyProgressBar()

        self.filechooser = FileChooserIconView(filters = ['*.mp3'])
        self.pop_cont_lay.add_widget(self.filechooser)
        self.pop_cont_lay.add_widget(Button(text="Close",size_hint_y=.20,on_release=self.dismiss))
        
    def open_pop(self):
    	self.anim = Animation(size=(Window.width, Window.height), duration =0.5,t='in_expo')
    	self.anim.bind(on_complete = self.completed_progress)
    	self.anim.start(self)
    	
    def completed_progress(self,animation, widget):
    	self.content = self.pop_cont_lay
    def progress_position(self,interval):
    	if self.myprogress.value>= self.myprogress.max: 
    		self.dismiss()

    	else:
    		self.myprogress.value += 1
    def pop_dismiss(self):
    	Clock.unschedule(self.progress_position)
    	self.myprogress.value = 0
    	self.anim = Animation(size=(200, 200), duration =0.5,t='in_expo')
    	self.anim.start(self)
    	self.content = self.pop_cont_lay

class MyProgressBar(ProgressBar):
    def __init__(self, **kwargs):
        super(MyProgressBar, self).__init__(**kwargs)
 
Builder.load_string("""
<MyProgressBar>:
""")