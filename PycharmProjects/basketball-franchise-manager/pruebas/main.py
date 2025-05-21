import self as self
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager


class StartWindow(Screen):
    pass


class PortfolioOverview(Screen):
    pass


class Portfolio(Screen):
    pass


class Market(Screen):
    pass


class Economics(Screen):
    pass


class PortfolioTools(Screen):
    pass


class WindowManager(ScreenManager):
    pass

Builder.load_file("main.kv")


class TestApp(App):
    def build(self):
        return WindowManager()


if __name__ == "__main__":
    TestApp().run()

