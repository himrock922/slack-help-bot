# - *- coding: utf-8 -*
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase, DEFAULT_FONT

resource_add_path('mplus-TESTFLIGHT-061')
LabelBase.register(DEFAULT_FONT, 'mplus-1p-light.ttf')
from kivy.lang import Builder

# TODO my.kvが読み込み出来なかったので直接書く
# 要修正

Builder.load_string('''
<tokenWidget>:
    textinput: textinputwidget
    button: buttonwidget

    #inputtext
    TextInput:
        id: textinputwidget
        font_size: 20
        size: 700,50
        center_x: (root.width/2)
        top: root.top - 100
        multiline: False
    #button
    Button:
        id: buttonwidget
        font_size: 30
        center_x: (root.width/2)
        size: 300,80
        top: root.top-250
        text: "登録"
''')

class tokenWidget(Widget): pass

class TokenInput(App):
  
  def clicked(self, src):
    return self.root.textinput

  def build(self):
    self.root = tokenWidget()
    self.root.button.bind(on_press=self.clicked)
    return self.root
