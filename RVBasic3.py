#https://stackoverflow.com/questions/63277704/displaying-different-widget-types-in-recycleview-kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

        # set up the data
        self.data = [
            {'text': 'Some Text', 'image': 'dots.png'},
            {'text': 'more text', 'image': 'tester.png'}
            ]

kv = '''
<MyViewClass@BoxLayout>:
    # define the properties that appear in the data
    text: ''
    image: ''
    
    # define how the data is displayed
    Image:
        source: root.image
    Label:
        text: root.text
RV:
    viewclass: 'MyViewClass'
    RecycleBoxLayout:
        padding: 10, 0, 10, 0
        size_hint_y: None
        height: self.minimum_height
        default_size: None, 40
        default_size_hint: 1, None
        orientation: 'vertical'
        spacing: 3
'''

class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

from kivy.core.window import Window
#this is to make the Kivy window always on top
Window.always_on_top = True
TestApp().run()