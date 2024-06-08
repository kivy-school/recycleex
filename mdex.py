# https://www.reddit.com/r/kivy/comments/19bn3bs/need_some_help_with_recycleview_widgets/
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.recycleview import RecycleView
from kivymd.uix.behaviors import TouchBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    RV:
        id: rv
    Button:
        size_hint_y: None
        height: dp(48)
        text: 'change colors'
        on_release: app.change_colors()
        
<RV>:
    id: rv
    key_viewclass: 'Widget'  # The view class is TwoButtons, defined above.
    scroll_type: ['bars', 'content']
    bar_width: 5
    #do_scroll_y: False
    SelectableRecycleBoxLayout:       
        id: box
        key_size: 'ks'
        key_pos_hint: 'kpos'
        default_size: dp(48), dp(48) 
        default_size_hint: None, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        spacing: sp(10)
        multiselect: True
        touch_multiselect: True

<FolderHolder>:
    id: FolderHolder
    height: 60
    width: 200
    size_hint: None,None
    radius: [10, 10, 10, 10] if self.pos_hint == {'right': 1} else [10, 10, 10, 10]
    # md_bg_color: root.set_color() if app.theme_cls.theme_style == 'Light' else root.set_color() if root.selected else root.set_color() # I have defined it like this as this works like a switch , it helps to change colors on the spot , otherwise app needs to reboot to change colors
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            MDLabel:
                id: name
                text: root.sender
                font_size: 9
                size_hint: None,None
                size: self.texture_size
                pos_hint: {'top': 1, 'right':1}
                bold: True
                text_size: None,None
                color: app.theme_cls.opposite_bg_normal  
            MDBoxLayout:
        MDBoxLayout:
            MDIconButton:
                icon: 'folder'
'''


class RV(RecycleView, TouchBehavior):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout, TouchBehavior):
    ''' Adds selection and focus behaviour to the view. '''


class FolderHolder(ButtonBehavior, MDBoxLayout):
    sender = StringProperty()
    source = StringProperty()
    time = StringProperty()
    type = "folder"
    name = StringProperty()
    important = BooleanProperty(False)
    selected = BooleanProperty(False)


class DataApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        for i in range(10):
            if i % 2 == 0:
                self.root.ids.rv.data.append(
                    {"Widget": 'FolderHolder', 'size': (100, 190), 'ks': (100, 190), 'pos_hint': {'left': 1},
                     'md_bg_color': 'lightgray'})
            else:
                self.root.ids.rv.data.append(
                    {"Widget": 'FolderHolder', 'size': (100, 190), 'ks': (100, 190), 'pos_hint': {'right': 1},
                     'md_bg_color': 'yellow'})

    def change_colors(self):
        rv_datas = self.root.ids.rv.data
        for rv_data in rv_datas:
            if rv_data['pos_hint'] == {'left': 1}:
                rv_data['md_bg_color'] = 'red'
            else:
                rv_data['md_bg_color'] = 'purple'
        self.root.ids.rv.refresh_from_data()


if __name__ == '__main__':
    DataApp().run()