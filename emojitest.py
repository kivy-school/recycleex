#emoji rendering
# https://www.reddit.com/r/kivy/comments/12l0x8n/any_fix_for_emoji_rendering/

from kivy.app import App
from kivy.lang import Builder

kv = """
BoxLayout:
    Label:
        text: 'Test Emoji:' + '\N{grinning face}'
        font_name: 'seguiemj'
        font_size: 40
"""


class EmojiApp(App):
    def build(self):
        return Builder.load_string(kv)


EmojiApp().run()