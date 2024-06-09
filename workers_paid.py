from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior, RecycleKVIDsDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout

#emoji rendering
# https://www.reddit.com/r/kivy/comments/12l0x8n/any_fix_for_emoji_rendering/

Builder.load_string('''
#:import pdb pdb
<SelectableBoxLayout>:
    orientation: 'horizontal'
                    
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        id: employee_name_labelID
        # on_press: pdb.set_trace()
        text: "default name"
        font_name: 'seguiemj'
        size_hint: (1,1)
        font_size: dp(self.height)*.75
        
    Label:
        id: employee_number_labelID
        text: "default number"
        font_size: dp(self.height)*.75

<RV>:
    viewclass: 'SelectableBoxLayout'
    id: RV_ID
    data: self.rvdata
    SelectableRecycleBoxLayout:
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
class SelectableBoxLayout(RecycleKVIDsDataViewBehavior, BoxLayout):
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
        # import pdb
        # pdb.set_trace()
        if super(SelectableBoxLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)        
        self.parent.parent.refresh_from_data()
        
    def on_touch_up(self, touch): #touch is laggy because touch up takes a while
        # self.parent.parent.refresh_from_data()
        pass
        
    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            App.get_running_app().root.data[index]['employee_name_labelID.text'] = "Employee: \N{grinning face}"
            print("selection changed to {0}".format(rv.rvdata[index]))
            # App.get_running_app().root.data[index]['employee_name_labelID.color'] = (170,170,170)
            # App.get_running_app().root.data[index]['employee_name_labelID.color'] = (255,0,0)
        else:
            App.get_running_app().root.data[index]['employee_name_labelID.text'] = "Employee: \N{pensive face}"
            print("selection removed for {0}".format(rv.rvdata[index]))
        # this will bug it out, don't always refresh
        print("new rv data", rv.rvdata)
        # rv.refresh_from_data()
        
class RV(RecycleView):
    rvdata = ListProperty() 
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.rvdata = [{"employee_number_labelID.text": "id: "+ str(x*2), 'employee_name_labelID.text': 'Employee:' + '\N{pensive face}'} for x in range(10)]
        

class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    from kivy.core.window import Window
    #this is to make the Kivy window always on top
    Window.always_on_top = True
    TestApp().run()