# https://stackoverflow.com/questions/73622792/kivy-recycleview-with-custom-widget

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.recycleview import RecycleView

Builder.load_string('''
<MyObject>:
    size_hint_y: None
    height: 100
    Label:
        id: label
        text: root.text  # uses the text StringProperty
        size_hint: None, None
        size: 200, 100
<RV>:
    viewclass: 'MyObject'
    RecycleBoxLayout:
        default_size: None, 100
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')


class MyObject(BoxLayout):
    show = ObjectProperty(None)
    text = StringProperty('Abba')

    def on_show(self, instance, new_obj):
        # handle the ObjectProperty named show
        if new_obj.parent:
            # remove this obj from any other MyObject instance
            new_obj.parent.remove_widget(new_obj)
        for ch in self.children:
            if isinstance(ch, Image):
                # remove any previous obj instances
                self.remove_widget(ch)
                break
        # add the new obj to this MyObject instance
        self.add_widget(new_obj)


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x),
                      'show': Image(source='tester.png', size_hint=(None, None), size=(100, 100),
                                    allow_stretch=True, keep_ratio=True)}
                     for x in range(100)]


class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    from kivy.core.window import Window
    #this is to make the Kivy window always on top
    Window.always_on_top = True
    TestApp().run()