import os

from kivy.graphics import Rectangle
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from utilities import Utilities, ImageButton
from variables.paths import parentDir, teamsPicsDir
# to change the kivy default settings we use this module config
from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)


class NewCareer(MDScreen):
    cur_path = os.getcwd()
    separator = Utilities().get_separator()
    Builder.load_file(f"{cur_path}{separator}kv{separator}new_career.kv")
    common_vars = Utilities.get_common_vars()
    country_text = common_vars['utilities'].get_translation(common_vars['translations'], 233,
                                                            common_vars['language_id'])
    league_text = common_vars['utilities'].get_translation(common_vars['translations'], 234,
                                                           common_vars['language_id'])
    conf_text = common_vars['utilities'].get_translation(common_vars['translations'], 235,
                                                         common_vars['language_id'])
    div_text = common_vars['utilities'].get_translation(common_vars['translations'], 236,
                                                        common_vars['language_id'])
    hierarchy = common_vars['sql_helper'].get_sports_hierarchy()[0]
    hierarchy_dict = {}
    for row in hierarchy:
        if row['country_trans_id'] not in hierarchy_dict.keys():
            hierarchy_dict[row['country_trans_id']] = {}
        if row['abbrev_id_leag'] not in hierarchy_dict[row['country_trans_id']].keys():
            hierarchy_dict[row['country_trans_id']][row['abbrev_id_leag']] = {}
        if row['abbrev_id_conf'] not in hierarchy_dict[row['country_trans_id']][row['abbrev_id_leag']].keys():
            hierarchy_dict[row['country_trans_id']][row['abbrev_id_leag']][row['abbrev_id_conf']] = {}
        if row['abbrev_id_div'] not in hierarchy_dict[row['country_trans_id']][row['abbrev_id_leag']][
            row['abbrev_id_conf']].keys():
            hierarchy_dict[row['country_trans_id']][row['abbrev_id_leag']][row['abbrev_id_conf']][
                row['abbrev_id_div']] = []
        if row['team_id'] not in \
                hierarchy_dict[row['country_trans_id']][row['abbrev_id_leag']][row['abbrev_id_conf']][
                    row['abbrev_id_div']]:
            hierarchy_dict[row['country_trans_id']][row['abbrev_id_leag']][row['abbrev_id_conf']][
                row['abbrev_id_div']].append(row['team_id'])
    country_items = []
    for country in hierarchy_dict.keys():
        country_items.append(
            common_vars['utilities'].get_translation(common_vars['translations'], country,
                                                     common_vars['language_id']))
    country_items.sort()

    def go_back(self, button):
        MDApp.get_running_app().root.current = "MainMenu"

    def set_variables(self):

        self.countries_spinner = self.common_vars['utilities'].create_dropdown(self.country_items, {"x": 0, "top": 1},
                                                                               (0.3, 0.3),
                                                                               self.country_text)
        self.league_spinner = self.common_vars['utilities'].create_dropdown([], {"x": 0, "top": 1}, (0.3, 0.3),
                                                                            self.league_text)
        self.conf_spinner = self.common_vars['utilities'].create_dropdown([], {"x": 0, "top": 1}, (0.3, 0.3),
                                                                          self.conf_text)
        self.div_spinner = self.common_vars['utilities'].create_dropdown([], {"x": 0, "top": 1}, (0.3, 0.3),
                                                                         self.div_text)

        self.sel_country = 0
        self.sel_league = 0
        self.sel_conf = 0
        self.sel_div = 0

        self.box_3 = BoxLayout(orientation="horizontal", size_hint=(1, 0.3))

        self.team_lab = Label()
        self.team_lab.font_size = '20sp'
        self.team_lab.markup = True

        self.box_5_2 = BoxLayout(orientation="horizontal", size_hint=(0.4, 1))

    def add_background(self):
        im = Image(orientation='vertical')
        with im.canvas:
            Rectangle(pos=self.pos, size=self.size, source=parentDir + '/resources/backgrounds/court.png')
        self.add_widget(im)

    def on_enter(self, *args):

        self.set_variables()

        self.add_background()

        grid = GridLayout(rows=5, padding=0, spacing=0)
        box_1 = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))

        grid.add_widget(box_1)

        box_2 = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        self.countries_spinner.bind(text=self.update_spinner)
        self.league_spinner.bind(text=self.update_spinner)
        self.conf_spinner.bind(text=self.update_spinner)
        self.div_spinner.bind(text=self.add_teams)
        box_2.add_widget(self.countries_spinner)
        box_2.add_widget(self.league_spinner)
        box_2.add_widget(self.conf_spinner)
        box_2.add_widget(self.div_spinner)
        grid.add_widget(box_2)

        grid.add_widget(self.box_3)

        box_4 = BoxLayout(orientation="horizontal", size_hint=(1, 0.05))
        box_4.add_widget(self.team_lab)
        grid.add_widget(box_4)

        grid_2 = GridLayout(cols=4)
        box_5_1 = BoxLayout(orientation="horizontal", size_hint=(0.1, 1))

        box_5_3 = BoxLayout(orientation="horizontal", size_hint=(0.4, 1))
        box_5_4 = BoxLayout(orientation="horizontal", size_hint=(0.1, 1))

        back_btn = Button(padding=(10, 10),
                          text=self.common_vars['utilities'].get_translation(self.common_vars['translations'], 232,
                                                                             self.common_vars['language_id']),
                          size_hint=(1, 0.2),
                          pos_hint={'bottom': 1})

        back_btn.bind(on_release=self.go_back)

        box_5_1.add_widget(back_btn)

        box_5_4.add_widget(Button(padding=(10, 10),
                                  text=self.common_vars['utilities'].get_translation(self.common_vars['translations'],
                                                                                     237,
                                                                                     self.common_vars['language_id']),
                                  size_hint=(1, 0.2),
                                  pos_hint={'bottom': 1}))
        grid_2.add_widget(box_5_1)
        grid_2.add_widget(self.box_5_2)
        grid_2.add_widget(box_5_3)
        grid_2.add_widget(box_5_4)

        box_5 = BoxLayout(orientation="horizontal", size_hint=(1, 0.35))
        box_5.add_widget(grid_2)
        grid.add_widget(box_5)

        self.add_widget(grid)

        self.ids[self.country_text] = self.countries_spinner
        self.ids[self.league_text] = self.league_spinner
        self.ids[self.conf_text] = self.conf_spinner
        self.ids[self.div_text] = self.div_spinner

        self.countries_spinner.text = self.countries_spinner.values[0]

    def add_teams(self, spinner, text):
        self.box_3.clear_widgets()
        translation_id = self.common_vars['utilities'].get_translation_id_from_text(self.common_vars['translations'],
                                                                                    text,
                                                                                    self.common_vars['language_id'])
        teams = self.hierarchy_dict[self.sel_country][self.sel_league][self.sel_conf][translation_id]
        sep = self.common_vars['utilities'].get_separator()
        grid_teams = GridLayout(rows=2)
        for team in teams:
            team_name = self.common_vars['sql_helper'].get_team_name_by_id(team)
            im = teamsPicsDir + sep + "team" + str(team) + ".png" if self.common_vars['utilities'].file_exists(
                teamsPicsDir + sep + "team" + str(team) + ".png") else teamsPicsDir + sep + "team0.png"
            btn = ImageButton(source=im, on_release=self.print_team, size_hint=(.2, .6),
                              pos_hint={'center_x': 0.5, 'center_y': 0.4})
            btn.team_id = team
            btn.team_name = team_name
            grid_teams.add_widget(btn)
        self.box_3.add_widget(grid_teams)

    def print_team(self, btn):
        self.box_5_2.clear_widgets()
        print(btn.team_id)
        print(btn.team_name)
        self.team_lab.text = '[color=black][b]' + btn.team_name + '[/b][/color]'
        table = MDDataTable(check=True, size_hint=(0.5, 0.5), pos_hint={"left": 1, "top": 1}, use_pagination=True,
                            rows_num=10, pagination_menu_pos='auto', background_color=[1, 0, 0, .5],
                            column_data=[
                                ("First Name", dp(30)),
                                ("Last Name", dp(30)),
                                ("Email Address", dp(30)),
                                ("Phone Number", dp(30)),
                            ],
                            row_data=[
                                ("Yo", "Tambien", "prueba", "123"),
                                ("Yo2", "Tambien2", "prueba2", "1232")
                            ])

        table.bind(on_check_press=self.checked)
        table.bind(on_row_press=self.row_checked)

        self.box_5_2.add_widget(table)

    def checked(self, instance_table, current_row):
        print(instance_table, current_row)

    def row_checked(self, instance_table, instance_row):
        print(instance_table, instance_row)

    def update_spinner(self, spinner, text):
        global to_iterate
        translation_id = self.common_vars['utilities'].get_translation_id_from_text(self.common_vars['translations'],
                                                                                    text,
                                                                                    self.common_vars['language_id'])
        items = []
        if self.ids[self.country_text] == spinner:
            self.sel_country = translation_id
            to_iterate = self.hierarchy_dict[self.sel_country].keys()
        if self.ids[self.league_text] == spinner:
            self.sel_league = translation_id
            to_iterate = self.hierarchy_dict[self.sel_country][self.sel_league].keys()
        if self.ids[self.conf_text] == spinner:
            self.sel_conf = translation_id
            to_iterate = self.hierarchy_dict[self.sel_country][self.sel_league][self.sel_conf].keys()
        if self.ids[self.div_text] == spinner:
            self.sel_div = translation_id

        for country in to_iterate:
            items.append(self.common_vars['utilities'].get_translation(self.common_vars['translations'], country,
                                                                       self.common_vars['language_id']))
        items.sort()
        self.update_spinners(spinner, items)

    def update_spinners(self, spinner, items):
        if self.ids[self.country_text] == spinner:
            self.league_spinner.values = items
            self.league_spinner.text = items[0]
        if self.ids[self.league_text] == spinner:
            self.conf_spinner.values = items
            self.conf_spinner.text = items[0]
        if self.ids[self.conf_text] == spinner:
            self.div_spinner.values = items
            self.div_spinner.text = items[0]
