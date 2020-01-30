# -*- coding: utf-8 -*-
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
import datetime
import Main
import Shown_class
from kivy.uix.dropdown import DropDown
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.graphics import Line, Color
from kivy.core.window import Window



class Shown_Mama(FloatLayout):
    def __init__(self,**kwargs):
        super(Shown_Mama, self).__init__(**kwargs)
        Window.bind(on_resize=self.window_size_changed)
        self.chveneba_klasi = Shown_Scroll()
        self.pirovneba_klasi = Pirovneba_box1()
        self.add_widget(self.chveneba_klasi)
        self.add_widget(self.pirovneba_klasi)



        self.dropdown = DropDown()  # Create the dropdown once and keep a reference to it
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.button, 'text', x))


        self.button = Button(text='იუნკერთა სია', font_size=20, size_hint=(.15,.10),font_name="bpg_arial_2009",
                             pos_hint= {'x':.0,'y':.80},background_color = get_color_from_hex("#ff680a"),on_release=self.refresh_dopdown)
        self.add_widget(self.button)

        self.items_klasi = Shown_Box()
        self.chveneba_klasi.add_widget(self.items_klasi)

        self.sataurebi_lay = sataurebi_layout()
        self.add_widget(self.sataurebi_lay)
        

        self.refres_btn = Button(text = "ძებნა",font_name="bpg_arial_2009", font_size=20)
        self.refres_btn.bind(on_release = self.refresh)
        self.pirovneba_klasi.add_widget(self.refres_btn)

        self.delete_btn = Button(text = "წაშლა",font_name="bpg_arial_2009", font_size=20)
        self.delete_btn.bind(on_release = self.delete_junker)
        self.pirovneba_klasi.add_widget(self.delete_btn)

    def window_size_changed(self,window, width,height):
        self.button.font_size = width/68.3
        self.dropdown.font_size = width/68.3


    def delete_junker(self,*args):
        Main.con.execute("delete from Junker_list where Name = N'%s'and Surname=N'%s'"%(self.pirovneba_klasi.kaci_teqst.text,
                                                                                        self.pirovneba_klasi.kaci_gvari_teqst.text))
        self.pirovneba_klasi.name_text.text = "უცნობია"
        self.pirovneba_klasi.surname_text.text = "უცნობია"
        self.pirovneba_klasi.laptop_serial_result.text = "უცნობია"
        self.button.text = "იუნკერთა სია"
        self.pirovneba_klasi.kaci_teqst.text = ""
        self.pirovneba_klasi.kaci_gvari_teqst.text = ""
        self.items_klasi.clear_widgets()

    def refresh_dopdown(self,*args):
        self.dropdown.open(self.button)
        self.dropdown.clear_widgets()
        for index in self.junker_list():
            btn = Button(text='Value %s %s' % (index[2],index[2]), size_hint_y=None, height=44,font_name="bpg_arial_2009",
                         on_release=lambda btn: self.command2(name=btn.text))  # bind every btn to a print statement
            btn.text = '%s %s' % (index[1],index[2])
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)




    def info_container(self):
        self.command= Main.con.execute("select Name,Surname,dasaxeleba,gacema,vada,Laptop_number from Junker_list, Item_list "
                                   "where Junker_list.Jun_ID = Item_list.junker_id and Name = N'%s'and Surname=N'%s' "
                                   "order by name"%(self.pirovneba_klasi.kaci_teqst.text,self.pirovneba_klasi.kaci_gvari_teqst.text))
        for items in self.command:
            yield items


    def junker_list(self):
        self.junker_fetch = Main.con.execute("select * from Junker_list")
        for junker in self.junker_fetch:
            yield junker


    def command2(self,name):
        self.dakofili = name.split(' ')
        self.pirovneba_klasi.kaci_teqst.text = self.dakofili[0]
        self.pirovneba_klasi.kaci_gvari_teqst.text = self.dakofili[1]
        self.refresh()




    def refresh(self,*args):
        self.items_klasi.clear_widgets()
        for self.number, self.item in enumerate(self.info_container()):
            self.pirovneba_klasi.name_text.text = self.item[0]
            self.pirovneba_klasi.surname_text.text = self.item[1]
            self.pirovneba_klasi.laptop_serial_result.text = self.item[5]
            self.a = self.item[4].split("-")
            self.vada_list = [int(g) for g in self.a]
            self.mimdinare_dro = datetime.datetime(int(self.vada_list[0]),int(self.vada_list[1]),int(self.vada_list[2])) - datetime.datetime.today()
            self.strig_converted = str(self.mimdinare_dro)

            if self.mimdinare_dro.days >= 60:
                self.items_klasi.add_widget(Shown_class.monacemebi(gamoidzaxe_row=str(self.item[2]),gamoidzaxe_nomeri=str(self.number+1),
                                              gamoidzaxe_gacema=str(self.item[3]),gamoidzaxe_vada=self.item[4],
                                              gamoidzaxe_statusi="[color=#55FB0E]%s დღე - %s სთ[/color]"%(self.strig_converted[:5],self.strig_converted[10:19])))
            elif self.mimdinare_dro.days < 60 and self.mimdinare_dro.days > 30:
                self.items_klasi.add_widget(Shown_class.monacemebi(gamoidzaxe_row=str(self.item[2]),gamoidzaxe_nomeri=str(self.number+1),
                                              gamoidzaxe_gacema=str(self.item[3]),gamoidzaxe_vada=self.item[4],
                                              gamoidzaxe_statusi="[color=#ffff14]%s დღე - %s სთ[/color]"%(self.strig_converted[:5],self.strig_converted[10:19])))
            elif self.mimdinare_dro.days <=30:
                self.items_klasi.add_widget(Shown_class.monacemebi(gamoidzaxe_row=str(self.item[2]),gamoidzaxe_nomeri=str(self.number+1),
                                              gamoidzaxe_gacema=str(self.item[3]),gamoidzaxe_vada=self.item[4],
                                              gamoidzaxe_statusi="[color=#ff2914]%s დღე - %s სთ[/color]"%(self.strig_converted[:5],self.strig_converted[10:19])))






class Shown_Scroll(ScrollView):
    def __init__(self,**kwargs):
        super(Shown_Scroll, self).__init__(**kwargs)
        self.size_hint=(.85,.78)
        self.pos_hint={'x':.15,'y':0}





class Pirovneba_box1(BoxLayout):
    def __init__(self,**kwargs):
        super(Pirovneba_box1, self).__init__(**kwargs)
        Window.bind(on_resize=self.window_size_changed)
        self.size_hint=(.90,.06)
        self.pos_hint = {'x': .10, 'y':.917}
        self.add_widget(Image(source="ICONS/person.png",size=(50,50),size_hint= (None,None)))
        self.name_text = Label(text= "უცნობია",font_name="bpg_arial_2009", font_size= 24)
        self.add_widget(self.name_text)

        self.surname_text = Label(text ="უცნობია",font_name="bpg_arial_2009",font_size= 24)
        self.add_widget(self.surname_text)


        self.add_widget(Image(source="ICONS/laptop.png",size=(50,50),size_hint= (None,None)))

        self.laptop_serial_result = Label(text = "უცნობია",font_name="bpg_arial_2009",font_size= 24)
        self.add_widget(self.laptop_serial_result)

        self.kaci_teqst = TextInput(hint_text= "სახელი",font_name ="bpg_arial_2009" ,font_size=20)
        self.add_widget(self.kaci_teqst)

        self.kaci_gvari_teqst = TextInput(hint_text= "გვარი",font_name ="bpg_arial_2009", font_size=20 )
        self.add_widget(self.kaci_gvari_teqst)



        self.sataurebi_lay = BoxLayout(orientation="horizontal",  size_hint=(.85,.75), pos_hint={'x':.15,'y':.80})
        self.add_widget(self.sataurebi_lay)

    def window_size_changed(self,window, width,height):
        for child in self.children:
            child.font_size = width/68.3





class Shown_Box(BoxLayout):
    def __init__(self,**kwargs):
        super(Shown_Box, self).__init__(**kwargs)
        Window.bind(on_resize=self.window_size_changed)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.spacing = 5
        self.bind(minimum_height=self.setter('height'))

    def window_size_changed(self,window, width,height):
        for child in self.children:
            child.font_size = width/68.3



class sataurebi_layout(BoxLayout):
    def __init__(self,**kwargs):
        super(sataurebi_layout, self).__init__(**kwargs)
        Window.bind(on_resize=self.window_size_changed)
        self.size_hint=(.842,.10)
        self.pos_hint={'x':.155,'y':.80}
        self.add_widget(Label(text="N",size_hint_x= None,font_size=20))
        self.sataurebi = ["დასახელება", "გაცემის თარიღი", "საბოლოო ვადა", "მიმდინარე სტატუსი","წაშლა" ]
        for i in self.sataurebi:
            self.add_widget(Label(font_size=20,text=str('{}'.format(i)),
                       font_name="bpg_arial_2009",size_hint_x=None, width= 220))

    def window_size_changed(self,window, width,height):
        for child in self.children:
            child.font_size = width/68.3
            child.width = width/6.20









