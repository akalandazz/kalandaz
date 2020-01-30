from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.video import Video
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.behaviors import TouchRippleBehavior, ToggleButtonBehavior
from kivy.utils import get_color_from_hex
from kivy.uix.bubble import Bubble
import FileChooserPop
from kivy.uix.image import Image
from kivy.base import Builder
import os
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp

class VideoPlayerLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(VideoPlayerLayout, self).__init__(**kwargs)
        self.pop = MyVidPop()
        self.pop.myfile.bind(on_submit = self.open_music)
        self.pane_box =MyBox(id='panbox')

    def open_music(self,function,selected_path,mouse_pos):
        self.pop.dismiss()
        for video in function.files[1:]:
            self.ids.vid_karuseli.add_widget(MyVideo(source='IMG_0827.png', video_path=video, on_touch_down= self.touch_down))

    def touch_down (self,instance,touch):
        self.anim=Animation(height=150,duration=0.1)
        if instance.collide_point(touch.x,touch.y):
            self.remove_widget(self.pane_box)
            self.pane_box.height = 0
            self.add_widget(self.pane_box)
            self.anim.start(self.pane_box)
            Clock.schedule_interval(instance.time, 1)
            print('started')
            return True
        return False





class MyVidPop(Popup):
    def __init__(self, **kwargs):
        super(MyVidPop, self).__init__(**kwargs)
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


class MyBox(BoxLayout):
    def __init__(self,**kwargs):
        super(MyBox, self).__init__(**kwargs)
        self.height = 0


class MyVideo(Video):
    def __init__(self, video_path,**kwargs):
        super(MyVideo, self).__init__(**kwargs)
        self.video = video_path
        self.current_time = 0
        self.app =App.get_running_app()


    def time(self,timer):
        self.current_time += 1
        if self.current_time == 5:
            self.app.root.children[0].ids.vid_screen.children[0].remove_widget(
                self.app.root.children[0].ids.vid_screen.children[0].pane_box)
            Clock.unschedule(self.time)
            self.current_time = 0
 


class AnimBut(TouchRippleBehavior,Image):
    def __init__(self,**kwargs):
        super(AnimBut, self).__init__(**kwargs)
        self.ripple_color = get_color_from_hex('#ff0000')
        self.ripple_duration_in = 0.1
        self.ripple_duration_out= 0.9
    def on_touch_down(self, touch):
        if self.collide_point(touch.x,touch.y):
            touch.grab(self)
            self.ripple_show(touch)
            return True
        return False

    def on_touch_up(self,touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()
            return True
        return False

class AnimTogBut(ToggleButtonBehavior,Image):
    pass


    

      


Builder.load_string("""
#:import Window kivy.core.window.Window
<VideoPlayerLayout>:
    BoxLayout:
        orientation:'vertical'
        Button:
            size_hint_y:.15
            text:'Browse'
            on_press:root.pop.open()

        TabbedPanel:
            do_default_tab: False
            tab_pos:'top_mid'
            tab_width:self.width/2
            TabbedPanelItem:
                text:'Library'

                Carousel:
                    id:vid_karuseli
            TabbedPanelItem:
                text:'VideoList'
    

<MyBox>:
    size_hint_y:None
    orientation:'vertical'
    spacing:15
    BoxLayout:
        Slider:
            size_hint_y:None
            height:self.parent.height
            on_touch_down:
                if self.collide_point(*Window.mouse_pos):self.height = 300
            on_touch_up:
                if self.collide_point(*Window.mouse_pos):self.height = self.parent.height
            canvas:
                Clear
                Color:
                    rgb: (0.2, 0.2, 0.2)
                Rectangle:
                    pos: self.pos
                    size: self.width, self.height
                Color:
                    rgb: (1, 0, 0)
                Rectangle:
                    pos: self.pos
                    size: self.width * (self.value_normalized if self.orientation == 'horizontal' else 1),\
                    self.height * (self.value_normalized if self.orientation == 'vertical' else 1)
                    
        Image:
            source:'Icons/muted.png' if vl_sld.value==0 else 'Icons/medium.png' if vl_sld.value<50 else 'Icons/high.png'
            size_hint_x:.15
        Slider:
            id:vl_sld
            min:0
            max:100
            size_hint_y:None
            height:self.parent.height
            size_hint_x:.30
            on_touch_down:
                if self.collide_point(*Window.mouse_pos):self.height = 300
            on_touch_up:
                if self.collide_point(*Window.mouse_pos):self.height = self.parent.height
            canvas:
                Clear
                Color:
                    rgb: (0.2, 0.2, 0.2)
                Rectangle:
                    pos: self.pos
                    size: self.width, self.height
                Color:
                    rgb: (1, 0, 0)
                Rectangle:
                    pos: self.pos
                    size: self.width * (self.value_normalized if self.orientation == 'horizontal' else 1),\
                    self.height * (self.value_normalized if self.orientation == 'vertical' else 1)
    BoxLayout:
        size_hint_x:.40
        pos_hint:{'x':.30,'y':0}
        canvas:
            Color:
                rgba: 0.88,0.88,0.88,1
            RoundedRectangle:
                size: self.size
                pos: self.pos

        AnimBut:
            source:'Icons/back.png'
            on_touch_down: if self.collide_point(*Window.mouse_pos): print('BACK')
        AnimBut:
            source:'Icons/stop.png'
            on_touch_down: if self.collide_point(*Window.mouse_pos): root.parent.ids.vid_karuseli.current_slide.state='stop';\
            root.parent.ids.vid_karuseli.current_slide.source='IMG_0827.png';\
            strtbtn.state='normal'
                

        AnimTogBut:
            id:strtbtn
            source:'Icons/pause.png' if self.state=='down' else 'Icons/next.png'

            on_state:
                root.parent.ids.vid_karuseli.current_slide.source = root.parent.ids.vid_karuseli.current_slide.video;\
                root.parent.ids.vid_karuseli.current_slide.state='play' if self.state=='down' else 'pause'
        AnimBut:
            source:'Icons/next.png'
            on_touch_down: if self.collide_point(*Window.mouse_pos): print('NEXT')

""")
