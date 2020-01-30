# -*- coding: utf-8 -*-
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import datetime
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
import Main,Tabbed_class
from kivy.core.window import Window



person={"saxeli":"--", "gvari":"--"}


class Row(BoxLayout):
    day = ObjectProperty()
    month = ObjectProperty()
    year = ObjectProperty()
    def __init__(self,gamoidzaxe_row,gamoidzaxe_nomeri,**kwargs):
        super(Row, self).__init__(**kwargs)
        Window.bind(on_resize = self.window_size_changed)
        self.size_hint = (None,None)
        self.size = (Window.width,Window.height/7.6)
        self.x = 20


        self.number_label = Label(text =gamoidzaxe_nomeri ,font_size=20)
        self.add_widget(self.number_label)

        self.lbl = Label(text= gamoidzaxe_row, font_name="bpg_arial_2009",font_size=20)
        self.add_widget(self.lbl)

        self.chk = CheckBox(active = False)
        self.chk.bind(active = self.charte)
        self.add_widget(self.chk)

        self.gacem_date = Label(text ="No Info", font_size=20)
        self.add_widget(self.gacem_date)


        self.teqsti_day = TextInput(hint_text= "დღე", size_hint_x = .50, size_hint_y = .50, pos_hint= {'x':.01, 'y':.25}, font_name="bpg_arial_2009",font_size =24)
        self.teqsti_day.bind(text= self.text)
        self.add_widget(self.teqsti_day)
        self.teqsti_day.disabled = True


        self.teqsti_month = TextInput(hint_text= "თვე" , size_hint_x = .50, size_hint_y = .50, pos_hint= {'x':.01, 'y':.25}, font_name="bpg_arial_2009",font_size =24)
        self.teqsti_month.bind(text= self.text)
        self.add_widget(self.teqsti_month)
        self.teqsti_month.disabled = True

        self.teqsti_year = TextInput(hint_text= "წელი", size_hint_x = .50, size_hint_y = .50, pos_hint= {'x':.01, 'y':.25}, font_name="bpg_arial_2009",font_size =24)
        self.teqsti_year.bind(text= self.text)
        self.add_widget(self.teqsti_year)
        self.teqsti_year.disabled = True

        self.status_label = Label(text= "Unknown", font_size=20, font_name="bpg_arial_2009")
        self.add_widget(self.status_label)


        self.btn = Button(text= "შენახვა", font_name="bpg_arial_2009", font_size=20)
        self.btn.bind(on_release = self.dabechde)
        self.add_widget(self.btn)
        self.btn.disabled = True

        self.jun_id  = 0






    def charte(self, instance, value):
        if value:
            self.teqsti_day.disabled = False
            self.teqsti_month.disabled = False
            self.teqsti_year.disabled = False
            self.btn.disabled = False
            self.teqsti_day.bind(text= self.teqst_func)
            self.gacem_date.text = str(datetime.date.today())
            self.lbl.color = (0, 0.255, 42, 1)
            print('chartulia')
        else:
            self.teqsti_day.disabled = True
            self.teqsti_month.disabled = True
            self.teqsti_year.disabled = True
            self.btn.disabled = True
            self.gacem_date.text = "No info"
            self.lbl.color = (1,1,1,1)



    def teqst_func(self, instance, value):
        print(value)



    def text(self,instance,value):
        if len(value) == 2:
            self.teqsti_day._keyboard_released()
            self.teqsti_month._keyboard_released()
        elif len(value) == 4:
            self.teqsti_year._keyboard_released()

    def shecdoma_func(self):
        self.shecdoma = Popup(title="შეცდომა",size_hint=(None, None), size=(500, 200), title_font="bpg_arial_2009")
        self.shecdoma_lay = BoxLayout(orientation = "vertical")
        self.shecdoma.add_widget(self.shecdoma_lay)
        self.close_button = Button(text= "დახურვა", font_name = "bpg_arial_2009")
        self.close_button.bind(on_release= self.shecdoma.dismiss)
        self.exception_label=Label(font_name = "bpg_arial_2009",markup = True)
        self.shecdoma_lay.add_widget(self.exception_label)
        self.shecdoma_lay.add_widget(self.close_button)
        self.shecdoma.open()



    def dabechde(self, *args):
        self.day = self.teqsti_day.text
        self.month = self.teqsti_month.text
        self.year = self.teqsti_year.text
        print(person["saxeli"])
        if person["saxeli"]=="" and person["gvari"]=="":
                self.shecdoma_func()
                self.exception_label.text = "პიროვნების სახელი და გვარი არ არის არჩეული!"
                self.shecdoma.separator_color = get_color_from_hex('#ff0c00')


        else:
            try:
                self.find_junker = "select * from Junker_list where Name = N'%s' and Surname = N'%s'"%(person["saxeli"],person["gvari"])
                for i in Main.con.execute(self.find_junker):
                    self.jun_id = i[0]
                print(self.jun_id)
                self.tarigi = datetime.date(int(self.year), int(self.month),int(self.day))
                self.status_label.text ="{}-დღე".format(str((self.tarigi - datetime.date.today()).days))
                print(self.gacem_date.text, self.tarigi)
                command = "insert into Item_list(dasaxeleba,gacema,vada,junker_id) values(N'%s',N'%s',N'%s',N'%s')"%(self.lbl.text,self.gacem_date.text, self.tarigi,self.jun_id)
                Main.con.execute(command)
                self.shecdoma_func()
                self.exception_label.text = "[color=#56f407]{}[/color] დაემატა მონაცემთა ბაზას".format(self.lbl.text)
                self.shecdoma.title = "შეტყობინება"
                self.shecdoma.separator_color = get_color_from_hex('#56f407')

            except:
                self.shecdoma_func()
                self.exception_label.text = "[color=#ff0c00]{}[/color]-ს საბოლოო ვადა არ არის შეყვანილი".format(self.lbl.text)
                self.shecdoma.separator_color = get_color_from_hex('#ff0c00')

    def window_size_changed(self, window, width, height):
        self.size = (width,height/7.6)
        for shvilebi in self.children:
            shvilebi.font_size = width/68.3
