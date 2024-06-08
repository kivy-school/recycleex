from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

#emoji rendering
# https://www.reddit.com/r/kivy/comments/12l0x8n/any_fix_for_emoji_rendering/

Builder.load_string('''
<SelectableBoxLayout>:
    id: SelectableBoxLayoutID
    orientation: 'horizontal'
    acb: ''
                    
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        id: employee_profileID
        text: 'Employee:' + '\N{grinning face}'
        font_name: 'seguiemj'
        size_hint: (1,1)
        font_size: dp(self.height)*.75
    Label:
        id: employee_number_labelID
        # text: root.employee_number_labelID.text
        # text: root.parent.text2
        text: root.acb
        font_size: dp(self.height)*.75

<RV>:
    viewclass: 'SelectableBoxLayout'
    SelectableRecycleBoxLayout:
        id: RV_ID
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: True
        touch_multiselect: True
''')
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''
class SelectableBoxLayout(RecycleDataViewBehavior, BoxLayout, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)



    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableBoxLayout, self).refresh_view_attrs(
            rv, index, data)
    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
        # import pdb
        # pdb.set_trace()
        # print("??", [x.ids for x in App.get_running_app().root.walk() ])
        # print("aaa", self, self.ids, self.ids['employee_profileID'])
        # print("aaa", self, self.ids, self.ids['employee_profileID'])
        # self.ids['employee_profileID'].text = "????"
    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        # self.data = [{"employee_number_labelID.text":  "abcd"} for x in range(100)]
        # self.data = [{'employee_profileID.text': "ggs"} for x in range(100)]
        # self.data = [{'text': "ggs"} for x in range(100)]
        # self.data = [{'thumb.source': x[0].bigthumb, 'textinfo.text': x[0].title, 'url': x[1], 'pafyobj':x[0] } for x in [[pafy.new(y),y] for y in self.songurls]]
        # self.data = [{"employee_number_labelID.text":  "Employee number: " + str(x*2)} for x in range(100)]
        # self.data = [{'text': str(x), 'active': False} for x in range(10)]
        # self.data = [{'text': str(x), "employee_number_label.text":  "Employee number: " + str(x*2)} for x in range(100)]
        # self.data = [{'text': str(x), "SelectableBoxLayoutID.employee_number_labelID.text":  "Employee number: " + str(x*2)} for x in range(100)]
        # self.data = [{'text': str(x), "SelectableBoxLayoutID.employee_number_labelID.text":  "abcd"} for x in range(100)]
        self.data = [{'text': str(x), "text2":  "abcd", "acb": "bca", "employee_number_labelID.text":  "correcttext"} for x in range(100)]

class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    from kivy.core.window import Window
    #this is to make the Kivy window always on top
    Window.always_on_top = True
    TestApp().run()