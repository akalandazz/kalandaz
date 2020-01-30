from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import Functionation_class
import Main
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Line, Color
from kivy.core.window import Window



class Tab_panel(TabbedPanel):
    def __init__(self,**kwargs):
        super(Tab_panel, self).__init__(**kwargs)
        self.pirveli_tab = TabbedPanelItem(text= "შესავსები ბლანკი",font_name="bpg_arial_2009", font_size =20)
        Window.bind(on_resize = self.window_size_changed)
        self.tab_width = Window.width/2.27
        self.tab_height = Window.height/11.76
        self.tab_pos="top_right"
        self.default_tab_text="Registration"
        self.background_image = 'background1.png'
        self.add_widget(self.pirveli_tab)
        self.mama=Mama_lay()


        self.pirovneba = pirovneba_box()
        self.default_tab_content = self.pirovneba
        self.pirveli_tab.add_widget(self.mama)

        self.switch_button= Button(text="შემდეგი", font_name="bpg_arial_2009", font_size =20)
        self.switch_button.bind(on_release=self.next_tab_func)
        self.pirovneba.person_box.add_widget(self.switch_button)



    def next_tab_func(self,*args):
        self.switch_to(self.pirveli_tab, do_scroll=True)
        self.mama.name_text.text = self.pirovneba.name_text.text
        self.mama.surname_text.text = self.pirovneba.surname_text.text
        self.pirovneba.name_text.text = ""
        self.pirovneba.surname_text.text = ""
        self.pirovneba.laptop_text.text = ""

    def window_size_changed(self, window, width, height):
        self.tab_width = width/2.27
        self.tab_height = height/11.76
        self.pirveli_tab.font_size = width/68.3










class pirovneba_box(FloatLayout):
    def __init__(self,**kwargs):
        super(pirovneba_box, self).__init__(**kwargs)
        self.person_box = BoxLayout(orientation = "vertical", spacing=5,size_hint=(.20,.60),pos_hint={'x':.40,'y':.35})
        self.add_widget(self.person_box)





        self.person_image=Image(source="ICONS/user.png",size=(130,130), size_hint=(None,None),pos_hint={'x':.25, 'y':.0})
        self.person_box.add_widget(self.person_image)

        self.name_text = TextInput(hint_text = "სახელი", font_name="bpg_arial_2009", font_size =20,cursor_width = 3.0)
        self.person_box.add_widget(self.name_text)


        self.surname_text = TextInput(hint_text = "გვარი", font_name="bpg_arial_2009", font_size =20,cursor_width = 3.0)
        self.person_box.add_widget(self.surname_text)

        self.laptop_text = TextInput(hint_text = "ლეპტოპის ნომერი", font_name="bpg_arial_2009", font_size =20,
                                     cursor_width = 3.0)
        self.person_box.add_widget(self.laptop_text)

        self.Add_Button = Button(text="დაემატა",font_name="bpg_arial_2009", font_size =20)
        self.Add_Button.bind(on_press = self.dabechde)
        self.person_box.add_widget(self.Add_Button)


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


    def dabechde(self,*args):
        if len(self.name_text.text)==0 or len(self.surname_text.text)==0 or len(self.laptop_text.text)==0:
            self.shecdoma_func()
            self.exception_label.text = "[color=#ff0c00]ველები არ არის შევსებული[/color]"
            self.shecdoma.separator_color = get_color_from_hex('#56f407')
        else:
            command = "insert into Junker_list(Name,Surname,Laptop_Number) values(N'%s',N'%s',N'%s')"%\
                      (self.name_text.text, self.surname_text.text,self.laptop_text.text)
            Main.con.execute(command)
            self.shecdoma_func()
            self.shecdoma.title = "შეტყობინება"
            self.exception_label.text = "[color=#56f407]%s %s[/color] დაემატა"%(self.name_text.text, self.surname_text.text)
            self.shecdoma.separator_color = get_color_from_hex('#56f407')











class Mama_lay(FloatLayout):
    def __init__(self,**kwargs):
        super(Mama_lay, self).__init__(**kwargs)
        Window.bind(on_resize = self.window_size_changed)
        self.sataurebi_lay = BoxLayout(orientation="horizontal", size_hint_x=.85, size_hint_y=.15,
                                       pos_hint={'x': .0, 'y': .80})
        self.add_widget(self.sataurebi_lay)

        self.sataurebi = ["N","დასახელება", "არჩევა", "გაცემის-თარიღი", "საბოლოო ვადა", "მიმდინარე სტატუსი", ]
        for i in self.sataurebi:
            self.sataurebi_lay.add_widget(
                Label(text=str('{}'.format(i)), size_hint_y=None,
                      height=40, font_name="bpg_arial_2009",font_size=20))

        self.pirovneba_box = BoxLayout(size_hint_x = .50, size_hint_y = .06, pos_hint = {'x': .30, 'y':.90})
        self.add_widget(self.pirovneba_box)

        self.name_label = Label(text ="სახელი",font_name="bpg_arial_2009",font_size =24 )
        self.pirovneba_box.add_widget(self.name_label)

        self.name_text = TextInput(hint_text = "სახელი", font_name="bpg_arial_2009", font_size =20 )
        self.name_text.bind(text= self.on_text_name)
        self.pirovneba_box.add_widget(self.name_text)

        self.surname_label = Label(text ="გვარი",font_name="bpg_arial_2009", font_size =24 )
        self.pirovneba_box.add_widget(self.surname_label)

        self.surname_text = TextInput(hint_text = "გვარი", font_name="bpg_arial_2009", font_size =20 )
        self.surname_text.bind(text= self.on_text_surname)
        self.pirovneba_box.add_widget(self.surname_text)

        self.add_widget(Scroll_Boxv2())


    def on_text_name(self,instance,value):
        Functionation_class.person["saxeli"] = value
        print(Functionation_class.person["saxeli"])


    def on_text_surname(self,instance,value):
        Functionation_class.person["gvari"] = value
        print(Functionation_class.person["gvari"])

    def window_size_changed(self, window, width, height):
        for shvilebi in self.sataurebi_lay.children:
            shvilebi.font_size = width/68.3

        for shvilebi in self.pirovneba_box.children:
            shvilebi.font_size = width/68.3








class Scroll_Boxv2(ScrollView):
    def __init__(self,**kwargs):
        super(Scroll_Boxv2, self).__init__(**kwargs)
        self.add_widget(pirovneba_boxv2())
        self.size_hint_y = .80



class pirovneba_boxv2(BoxLayout):
    def __init__(self,**kwargs):
        super(pirovneba_boxv2, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
     


        self.ROWS = ['ზურგჩანთა', 'ფანარი', 'საძილე ტომარა', 'პარალონი', 'მათარა შალითით', 'კარდალა',
                     'მუზარადი', 'მუზარადის შალითა','ქამარი ინდივიდუალური\nაღჭურვილობის','მესანგრის მცირე\nნიჩაბი შალითით',
                     'განტვირთვის ჭილეტი','ქემელბექი', 'სპორტული ზედა ქვედა', 'სპორტული მაისური','სპორტული შორტი','სპორტული ბოტასი',
                     'ქალის საცურაო კოსტუმი','საცურაო შორტი','საცურაო ქუდი','საცურაო სათვალე','აუზის ჩუსტი','ყაზარმის ჩუსტი','ტაქტიკური ზურგჩანთა',
                     'ტაქტიკურო ხელთათმანი','სამუხლე','საიდაყვე','ყურთასმენის დამცავი','ფორმა საველე\n კომუფლირებით','პანამა','ქურთუკი საქარე-გამოსაკრავით',
                     'შარვალი საქარე','პონჩო','ნაქსოვი ზედატანი \n დახურული ყელით','ქუდი ნაქსოვი','კომუფლირებული მაისური','საცვლები თბილი(ზედა ქვედა)',
                     'ხელთათმანი ნახევრად შალის','ფეხსაცმელი მ/ყელიანი','ქამარი წელის','პიჯაკი და შარვალი \n ყოველდღიური','პიჯაკი; შარვალი\n(ქვედაბოლო) ქალის',
                     'წინაფრიანი ქუდი','ბერეტი','ნაქსოვი ზედატანი პულოვერი','ლაბადა გამოსაკრავით \n დათბუნებით','ხელთათმანი ტყავის','პერანგი გ/მ','პრეანგი მ/შ',
                     'პერანგი გრძელი სახელოებით','ჰალსტუხი','ქამარი შარვლის','ფეხსაცმელი დ/ყ','ხელთათმანი თეთრი','პირსახოცი აბანოს','პირსახოცი ხელის',
                     'მაისური ბამბის','ტრუსი ბამბის','წინდა ბამბის','წინდა შალის','სარეცხი ტომარა','კომპასი']


        for self.number, self.i in enumerate(self.ROWS):
            self.add_widget(Functionation_class.Row(gamoidzaxe_row=str(self.i),gamoidzaxe_nomeri=str(self.number+1)))


