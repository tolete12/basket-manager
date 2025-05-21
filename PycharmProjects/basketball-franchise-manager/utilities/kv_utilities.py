from kivy.core.window import Window
from kivy.graphics import RoundedRectangle, Color, Line
from kivy.lang import Builder
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock
from kivy.uix.widget import Widget
from utilities import Utilities
from kivymd.uix.label import MDLabel
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from itertools import chain
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.utils import get_color_from_hex

Builder.load_string('''
#: import Utilities utilities.utilities.Utilities
<ConfirmPopup>:
    id: confirm
    cols:1
	Label:
		text: root.text
	GridLayout:
		cols: 2
		size_hint_y: None
		height: '44sp'
		Button:
			text: Utilities.get_translation(app.translations, 228, app.language_id)
			on_release: app.stop()
		Button:
			text: Utilities.get_translation(app.translations, 229, app.language_id)
			on_release: root.dispatch('on_answer', 'No')
''')

Builder.load_string('''
<CommonComponentLabel>
    halign: "center"


<MobileView>
    CommonComponentLabel:
        text: "Mobile"


<TabletView>
    CommonComponentLabel:
        text: "Table"


<DesktopView>
    CommonComponentLabel:
        text: "Desktop"
<ResponsiveView>:
''')


class ConfirmPopup(GridLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup, self).__init__(**kwargs)

    def on_answer(self, *args):
        print(*args)


class MyPopUp(GridLayout):
    text = StringProperty()

    def __init__(self, translations=None, language_id=0, **kwargs):
        super().__init__(**kwargs)
        if translations is None:
            translations = {}
        self.popup = None
        self.translations = translations
        self.language_id = language_id

    def close_popup(self):
        self.popup_window.dismiss()

    def show_popup(self, **kwargs):
        content = ConfirmPopup(text=kwargs['text'])
        content.bind(on_answer=self._on_answer)
        self.popup = Popup(title=kwargs['title'],
                           content=content,
                           size_hint=(None, None),
                           size=(480, 400),
                           auto_dismiss=False)
        self.popup.open()

    def _on_answer(self, instance, answer):
        print(repr(answer))
        print(instance)
        print(answer)
        if answer == Utilities.get_translation(self.translations, 229, self.language_id):
            self.popup.dismiss()


class OneLineListItemAligned(OneLineListItem):
    halign = StringProperty()
    id = StringProperty()
    text = StringProperty()
    bg_color = ColorProperty()
    # x = NumericProperty(0)
    # y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(OneLineListItemAligned, self).__init__(**kwargs)
        Clock.schedule_once(self.on_start)

    def on_start(self, *args):
        self.ids._lbl_primary.halign = self.halign
        self.ids._lbl_primary.id = self.id
        self.ids._lbl_primary.text = self.text
        self.ids._lbl_primary.bg_color = self.bg_color
        self.ids._lbl_primary.size_hint = (0.9, 0.9)
       
class CommonComponentLabel(MDLabel):
    pass
 
class MobileView(MDScreen):
    pass


class TabletView(MDScreen):
    pass

class DesktopView(MDScreen):
    pass

class ResponsiveView(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MobileView()
        self.tablet_view = TabletView()
        self.desktop_view = DesktopView()
        
class Gradient(object):

    @staticmethod
    def horizontal(*args):
        texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def vertical(*args):
        texture = Texture.create(size=(1, len(args)), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

class LayoutGradient(BoxLayout):
    def __init__(self, **args):
        self.size=(800, 800)
        self.pos=(0,0)
        super(LayoutGradient, self).__init__(**args)
        self.texture = Texture.create(size=(2, 1), colorfmt='rgb')

        color1 = 0
        color2 = 255

        buf = ''.join(map(chr, [color1, color2])).encode('utf-8')

        self.texture.blit_buffer(buf)

        self.canvas.add(Rectangle(pos=self.pos, size=self.size, texture=self.texture))
            
        self.bind(size=self.update_rect)
        self.bind(pos=self.update_rect)

    def update_rect(self, *args):
        for children in self.canvas.children:
            if isinstance(children, Rectangle):
                children.size = self.size
                children.pos = self.pos

    # def __init__(self, **args):
    #     super(LayoutGradient, self).__init__(**args)

    #     self.texture = Texture.create(size=(2, 1), colorfmt='rgb')

    #     color1 = 0
    #     color2 = 255

    #     buf = ''.join(map(chr, [color1, color2])).encode('utf-8')

    #     self.texture.blit_buffer(buf)

    #     with self.canvas:
    #         Rectangle(pos=self.pos, size=self.size, texture=self.texture)
            
    #     self.bind(size=self.update_rect)
    #     self.bind(pos=self.update_rect)

    # def update_rect(self, *args):
    #     for children in self.canvas.children:
    #         if isinstance(children, Rectangle):
    #             children.size = self.size
    #             children.pos = self.pos


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Invisible background color to regular button
        self.background_normal = ''
        self.kwargs = kwargs
        self.halign = "left"
        self.bold=True
        self.color=get_color_from_hex("#1952ffff")
        with self.canvas.before:
            self.shape_color = Color(rgba=kwargs['normal_color'] if 'normal_color' in kwargs else get_color_from_hex('#ff7f32ff'))
            self.shape = RoundedRectangle(pos=self.pos, size=self.size, radius=kwargs['radius'] if 'radius' in kwargs else [18])
            self.bind(pos=self.update_shape, size=self.update_shape)
        
        self.size_hint = kwargs['size_hint'] if 'size_hint' in kwargs else (0.8, 0.5)
        self.pos_hint = {"center_x": kwargs['center_x'] if 'center_x' in kwargs else 0.5,
                         "center_y": kwargs['center_y'] if 'center_y' in kwargs else 0.5}

    def update_shape(self, *args):
        self.shape.pos = self.pos
        self.shape.size = self.size

    def on_press(self, *args):
        if self.last_touch.button == 'left':
            self.shape_color.rgba = self.kwargs['press_color'] if 'press_color' in self.kwargs else (206, 0, 0, 0.8)
            print('pressed')
            print(self.shape_color.rgba)

    def on_release(self, *args):
        if self.last_touch.button == 'left':
            self.shape_color.rgba = self.kwargs['normal_color'] if 'normal_color' in self.kwargs else get_color_from_hex('#ff7f32ff')
            print(self.shape_color.rgba)

