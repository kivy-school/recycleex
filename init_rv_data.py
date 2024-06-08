# https://stackoverflow.com/questions/49935190/kivy-how-to-initialize-the-viewclass-of-the-recycleview-dynamically

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock

kv = """
<Row>:
    id: row
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Rectangle:
            size: self.size
            pos: self.pos


<Test>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    orientation: 'vertical'
    GridLayout:
        cols: 3
        rows: 2
        size_hint_y: None
        height: dp(108)
        padding: dp(8)
        spacing: dp(16)
        Button:
            text: 'Update list'
            on_press: root.update()
    RecycleView:
        id: rvlist
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(10)
        viewclass: 'Row'
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(2)
"""

Builder.load_string(kv)

class Row(BoxLayout):
    row_content = ObjectProperty()


    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.finish_init,0)
# it delays the end of the initialization to the next frame, once the widget are already created
# and the properties properly initialized

    def finish_init(self, dt):
        for elt in self.row_content:
            self.add_widget(Label(text = elt))
            # now, this works properly as the widget is already defined
        self.bind(row_content = self.update_row)


    def update_row(self, *args):
        # right now the update is rough, I delete all the widget and re-add them. Something more subtle
        # like only replacing the label which have changed
        print(args)
        # because of the binding, the value which have changed are passed as a positional argument.
        # I use it to set the new value of the labels.
        self.clear_widgets()
        for elt in args[1]:
            self.add_widget(Label(text = elt))


class Test(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.rvlist.data = [{'row_content': [str(i) for i in range(5)]} for x in range(15)]

    def update(self):
        self.ids.rvlist.data[0]['row_content'] =  [str(10*i) for i in range(5)]
        self.ids.rvlist.refresh_from_data()

class TestApp(App):
    def build(self):
        return Test()

if __name__ == '__main__':
    from kivy.core.window import Window
    #this is to make the Kivy window always on top
    Window.always_on_top = True
    TestApp().run()