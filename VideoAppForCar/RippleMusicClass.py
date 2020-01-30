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

class MusicPlayerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MusicPlayerLayout, self).__init__(**kwargs)
        Window.bind(on_resize = self.show_size)
        self.orientation='vertical'
        self.id = 'plrlay'
        self.opnfilechsrbtn = BrowseButton(on_touch_down = self.on_ripple_touch)
        self.add_widget(self.opnfilechsrbtn)
        self.karuseli = MyCarousel(loop=True, size_hint_y = .90)
        self.sld = MySlider(min =0, on_touch_up = self.on_slider_touch_up, on_touch_down = self.on_slider_touch_down)
        self.panel_but_lay = MyBoxLayout(size_hint_y = .30)
        self.add_widget(self.panel_but_lay)
        self.backbtn = Button(text='previous', on_release = self.load_previous)
        self.panel_but_lay.add_widget(self.backbtn)
        self.pirveli = MyToggleButton(text='play', on_release = self.on_play_pause)
        self.panel_but_lay.add_widget(self.pirveli)
        self.stpbtn = MyButton(text='stop', on_release = self.on_stop)
        self.panel_but_lay.add_widget(self.stpbtn)
        self.nextbtn = MyButton(text='next', on_release = self.load_next)
        self.panel_but_lay.add_widget(self.nextbtn)
        self.app = App.get_running_app()
        self.pop = FileChooserPop.MyPop()
        self.pop.filechooser.bind(on_submit=self.open_music)
        self.check_karuseli()


    def check_karuseli(self):
        if self.karuseli.current_slide is None:
            for bttn in self.panel_but_lay.children:
                bttn.disabled = True
            return True
        else:
            for bttn in self.panel_but_lay.children:
                bttn.disabled =False
            return False
        
    def show_size(self,windwo,width,height):
        if self.pop:
            self.pop.size = (width,height)
            



    

    def on_play_pause(self, instance):
        if instance.state=='down':
            self.karuseli.current_slide.sound.play()
            self.sld.max = int(self.karuseli.current_slide.sound.length)
            Clock.schedule_interval(self.position, 1)
            self.karuseli.current_slide.sound.seek(self.sld.value)
            print(self.sld.max)
        else:
            self.karuseli.current_slide.sound.stop()
            Clock.unschedule(self.position)
            

    def position(self,interval):
        self.sld.value = int(self.karuseli.current_slide.sound.get_pos())
        if self.sld.value == self.sld.max:
            self.load_next(self.nextbtn)
            print('mivedi_bolomde')
        else:
            print('maqsimaluria %s'%self.sld.max)

        print(int(self.karuseli.current_slide.sound.get_pos()))



    def on_stop(self, instance):
        self.karuseli.current_slide.sound.stop()
        Clock.unschedule(self.position)
        self.sld.value = 0
        self.pirveli.state = 'normal'

    def on_slider_touch_down(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            touch.grab(instance)
            instance.size_hint_y = .30


    def on_slider_touch_up(self, instance, touch):
        if touch.grab_current is instance:
            touch.ungrab(instance)
            self.karuseli.current_slide.sound.seek(int(instance.value))
            instance.size_hint_y = .15
            print(int(instance.value))

    def load_next(self, instance):
        if self.pirveli.state =='down':
            self.sld.max = int(self.karuseli.next_slide.sound.length)
            self.karuseli.current_slide.sound.stop()
            self.karuseli.load_next()
            self.karuseli.next_slide.sound.play()
            print('on_nextze %s'%self.sld.max)
        else:
            self.karuseli.load_next()
            self.sld.value = 0
            print(self.sld.value)



    def load_previous(self, instance):
        if self.pirveli.state =='down':
            self.sld.max = int(self.karuseli.previous_slide.sound.length)
            self.karuseli.current_slide.sound.stop()
            self.karuseli.load_previous()
            self.karuseli.previous_slide.sound.play()
            print('on_stopzea %s'%self.sld.max)
        else:
            self.karuseli.load_previous()
            self.sld.value = 0
            print(self.sld.value)


    def open_music(self,function,selected_path,mouse_pos):
        self.pop.myprogress.max = len(function.files)
        self.pop.content = self.pop.myprogress
        Clock.schedule_interval(self.pop.progress_position, 1 / 25) 
        self.clear_widgets()
        self.opnfilechsrbtn.size_hint_y = .18
        self.add_widget(self.opnfilechsrbtn)
        self.add_widget(self.karuseli)
        self.add_widget(self.sld)
        self.add_widget(self.panel_but_lay)
        for mus_number,music in enumerate(os.listdir(function.path)):
            self.karuseli.add_widget(RippleMusic(path=function.path+'/'+music, mus_title = music))
            self.app.root.children[0].ids.scrlbox.add_widget(MyScrollBoxLay(number=mus_number+1,title=music,
             on_touch_down = self.ripple_scroll))

        self.check_karuseli()

    def ripple_scroll(self,instance,touch):
        if instance.collide_point(touch.x, touch.y):
            touch.grab(instance)
            instance.ripple_show(touch)
            #MyScrollBoxLay-shi daprintos childrenebis text
            for slide in self.karuseli.slides:
                if slide.name_label.text == instance.title.text:
                    self.sld.max = int(slide.sound.length)
                    self.karuseli.load_slide(slide)
                    self.karuseli.current_slide.sound.stop()
                    slide.sound.play()
                    Clock.schedule_interval(self.position, 1)
                    self.pirveli.state = 'down'
                    print(self.sld.max)

            return True
        return False
            
            

    def on_ripple_touch(self, instance,touch):
        if instance.collide_point(touch.x, touch.y):
            touch.grab(self)
            instance.ripple_show(touch)
            self.pop.open()
            return True
        return False

class RippleMusic(BoxLayout):
    def __init__(self,path,mus_title,**kwargs):
        super(RippleMusic,self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.sound = SoundLoader.load(filename = str(path))
        self.name_label=(Label(text=str(mus_title), size_hint_y=.10))
        self.add_widget(self.name_label)





class MySlider(Slider):
    def __init__(self, **kwargs):
        super(MySlider,self).__init__(**kwargs)
        self.min = 0
        

    


class MyCarousel(Carousel):
    def __init__(self, **kwargs):
        super(MyCarousel,self).__init__(**kwargs)

class MyButton(Button):
    def __init__(self, **kwargs):
        super(MyButton,self).__init__(**kwargs)

class MyToggleButton(ToggleButton):
    def __init__(self, **kwargs):
        super(MyToggleButton,self).__init__(**kwargs)

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout,self).__init__(**kwargs)

class BrowseButton(TouchRippleBehavior, Label):
    def __init__(self, **kwargs):
        super(BrowseButton,self).__init__(**kwargs)
        self.text = 'Browse'
        self.ripple_color = get_color_from_hex('#074F1C')
      
    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            touch.ungrab(self)
            self.ripple_fade()
            return True
        return False



class MyScrollBoxLay(TouchRippleBehavior,BoxLayout):
    def __init__(self,number,title, **kwargs):
        super(MyScrollBoxLay,self).__init__(**kwargs)
        self.size_hint_y = None
        self.ripple_color = get_color_from_hex('#074F1C')
        self.number = Label(text=str(number),size_hint_x=.10)
        self.add_widget(self.number)
        self.title = Label(text=str(title))
        self.add_widget(self.title)

    def on_touch_up(self,touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()
            return True
        return False
        

    
class MyBubble(Bubble):
    def __init__(self, **kwargs):
        super(MyBubble,self).__init__(**kwargs)


Builder.load_string("""
<RippleMusic>:
    Image:
        size:self.size
        pos:self.pos
        canvas.before:
            Color:
                rgba: 1,1,1,1
            BorderImage:
                source: 'Icons/shadow32.png'
                border: (50,50,50,50)
                size:self.size
                pos:self.pos

<MySlider>:
    size_hint_y:.15
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

<MyScrollBoxLay>:
    canvas:
        Color:
            rgba:get_color_from_hex('#F00B00')
        Line:
            points:self.x, self.y, self.width, self.y
        
<MyBubble>:
    id:bbl
    BubbleButton:
        id:bblbtn
        text: 'TEXT'

"""
)