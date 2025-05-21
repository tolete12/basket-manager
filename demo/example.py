from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout


class ClientsTable(Screen):
    def load_table(self):
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            check=True,
            column_data=[
                ("No.", dp(30)),
                ("Column 1", dp(30)),
                ("Column 2", dp(30)),
                ("Column 3", dp(30)),
                ("Column 4", dp(30)),
                ("Column 5", dp(30)), ],
            row_data=[
                (f"{i + 1}", "2.23", "3.65", "44.1", "0.45", "62.5")
                for i in range(50)], )
        self.add_widget(self.data_tables)
        return layout

    def on_enter(self):
        self.load_table()


class LoginPage(Screen):
    username = ObjectProperty()
    password = ObjectProperty()

    def validate_user(self):
        if self.username.text == "m":
            sm.current = "Clientstable"
            self.username.text = ""
            self.password.text = ""
        else:
            print("Not here!")


sm = ScreenManager()


class ExampleApp(MDApp):
    def build(self):
        sm.add_widget(LoginPage(name='Loginpage'))
        sm.add_widget(ClientsTable(name='Clientstable'))
        return sm


if __name__ == "__main__":
    ExampleApp().run()
