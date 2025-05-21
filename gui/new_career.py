import gui.main_class as main_class
from db.createrecords.calendars.create_calendars import CreateCalendars
from utilities import Utilities
from utilities.utilities_gui import UtilitiesGui
from variables.constants import BACKGROUND_PARQUE, INI_DB, SPORTS_TABLE, SPORTS_ID, LEAGUES_ID, LEAGUES_TABLE, \
    CONFERENCES_ID, CONFERENCES_TABLE, DIVISIONS_ID, DIVISIONS_TABLE, TEAM_ID, TEAM_NAME, TEAMS_TABLE, TEAM_LOGO
from variables.paths import backgroundsPicsDir, teamsPicsDir


class NewCareer(main_class.MainClass):
    combo_sports = None
    combo_leagues = None
    combo_conferences = None
    combo_divisions = None
    selected_sport = 0
    selected_league = 0
    selected_conference = 0
    selected_division = 0
    root = None
    canvas = None
    sf = None
    team_label = None
    pos_x_ini_combos = 0
    selected_team_id = 0
    name_entry = None
    players = {}
    tree = None
    selected_player = None
    selected_player_item = None

    def __init__(self, override: bool, save_game: bool, translations: dict):
        super().__init__()
        super().connect_db(INI_DB, override, save_game)
        self.translations = translations
        self.combo_width = int(self.size_x / 4) - 100
        self.pos_x_ini_combos = int((self.size_x - ((self.combo_width * 4) + 60)) / 2)
        self.team_logo_size_x = int(self.size_x / 7)
        self.team_logo_size_y = int((self.team_logo_size_x * 140) / 180)
        self.pos_y_combos = int(self.size_y / 6)
        self.label_width = 400
        self.arrow_buttons_size = 55
        self.label_width = int((self.combo_width * 4) / 3)
        self.label_heigth = 35
        self.interface_new_career()

    def interface_new_career(self):

        pic = backgroundsPicsDir + BACKGROUND_PARQUE
        self.root, self.canvas = UtilitiesGui.set_center_window(self.size_x, self.size_y, pic,
                                                                self.utilities.get_translation(self.translations, 20,
                                                                                               self.option))
        self.sf = font.Font(family='Helvetica', size=14, weight='bold')

        # Back Button
        img = UtilitiesGui.create_pic_back_button(self.arrow_buttons_size, self.arrow_buttons_size)
        UtilitiesGui.create_button(self.canvas, "", self.sf,
                                   self.back_to_main_button, {'bg': 'white', 'fg': 'white'},
                                   {'pos_x': 20, 'pos_y': self.size_y - 70, 'height': self.arrow_buttons_size,
                                    'width': self.arrow_buttons_size}, img)
        # Forward Button
        img2 = UtilitiesGui.create_pic_forward_button(self.arrow_buttons_size, self.arrow_buttons_size)
        UtilitiesGui.create_button(self.canvas, "", self.sf,
                                   self.forward_to_overview, {'bg': 'white', 'fg': 'white'},
                                   {'pos_x': self.size_x - 20 - self.arrow_buttons_size, 'pos_y': self.size_y - 70},
                                   img2)

        self.add_player_controls()
        self.set_tree_players()
        self.load_sports()
        self.set_team_label()
        self.root.mainloop()

    def add_player_controls(self):

        # Label PLayer Name
        UtilitiesGui.create_label(self.canvas, self.sf, self.utilities.get_translation(self.translations, 105, self.option),
                                  int(self.pos_x_ini_combos / 6), int(self.pos_y_combos / 2), self.label_width,
                                  self.label_heigth)
        # Entry Player Name
        self.name_entry = UtilitiesGui.create_entry(self.canvas, int(self.pos_x_ini_combos / 6) + self.label_width + 10,
                                                    int(self.pos_y_combos / 2), self.label_width, self.label_heigth)
        # Button Add Player
        UtilitiesGui.create_button(self.canvas, self.utilities.get_translation(self.translations, 106, self.option), self.sf,
                                   self.add_player, {'bg': 'grey', 'fg': 'white'},
                                   {'pos_x': int(self.pos_x_ini_combos / 6) + self.label_width + 20 + self.label_width
                                       , 'pos_y': int(self.pos_y_combos / 2), 'width': 200})

    def set_tree_players(self):
        columns = [
            self.utilities.get_translation(self.translations, 112, self.option),
            self.utilities.get_translation(self.translations, 113, self.option)
        ]
        tree_pos_y = 10
        tree_pos_x = int(self.pos_x_ini_combos / 6) + self.label_width + 30 + self.label_width + 200
        self.tree = UtilitiesGui.create_treeview(self.canvas, self.on_select, tree_pos_x, tree_pos_y, 200,
                                                 self.pos_y_combos - 20, columns)

        # Button Remove Player
        UtilitiesGui.create_button(self.canvas, self.utilities.get_translation(self.translations, 111, self.option), self.sf,
                                   self.delete_player, {'bg': 'grey', 'fg': 'white'},
                                   {'pos_x': tree_pos_x + 220
                                       , 'pos_y': int(self.pos_y_combos / 2), 'width': 200})

    def delete_player(self):
        if self.selected_player is None:
            messagebox.showinfo(self.utilities.get_translation(self.translations, 107, self.option),
                                self.utilities.get_translation(self.translations, 114, self.option))
        else:
            del self.players[self.selected_player['text']]
            self.tree.delete(self.selected_player_item)
            self.selected_player = None
            self.selected_player_item = None

    def on_select(self, event):
        self.selected_player_item = event.widget.selection()[0]
        self.selected_player = event.widget.item(event.widget.focus())
        # item['text']
        # item['values'] list con los valores de las columnas

    def add_player(self):
        if self.selected_team_id == 0:
            messagebox.showinfo(self.utilities.get_translation(self.translations, 107, self.option),
                                self.utilities.get_translation(self.translations, 104, self.option))
        elif self.name_entry.get() == '':
            messagebox.showinfo(self.utilities.get_translation(self.translations, 107, self.option),
                                self.utilities.get_translation(self.translations, 108, self.option))
        elif self.selected_team_id in self.players.keys():
            messagebox.showinfo(self.utilities.get_translation(self.translations, 107, self.option),
                                self.utilities.get_translation(self.translations, 109, self.option))
        elif self.name_entry.get() in self.players.values():
            messagebox.showinfo(self.utilities.get_translation(self.translations, 107, self.option),
                                self.utilities.get_translation(self.translations, 110, self.option))
        else:
            self.players[self.selected_team_id] = self.name_entry.get()
            self.tree.insert("", 'end', text=self.selected_team_id,
                             values=(self.name_entry.get(), self.team_label.cget("text")))
            self.name_entry.delete(0, 'end')

    def forward_to_overview(self):
        messagebox.showinfo(self.name_entry.get(), self.name_entry.get())
        create_calendars = CreateCalendars(self.sql_helper)
        create_calendars.create_nba_calendar()

    def back_to_main_button(self):
        self.root.destroy()
        from gui.main_menu import MainMenu
        MainMenu(False, False)

    def set_team_label(self):
        self.team_label = UtilitiesGui.create_label(self.canvas, self.sf,
                                                    self.utilities.get_translation(self.translations, 104, self.option),
                                                    int(self.size_x / 2) - int(self.label_width / 2), self.size_y - 60,
                                                    self.label_width, 30)

    def load_sports(self):
        self.combo_sports = UtilitiesGui.create_combobox(self.canvas, 'combo_sports', self.sf, self.reload_combos,
                                                         self.pos_x_ini_combos,
                                                         self.pos_y_combos,
                                                         self.sql_helper.get_single_field_translated(SPORTS_ID,
                                                                                                     SPORTS_TABLE,
                                                                                                     self.option),
                                                         self.combo_width)
        self.combo_sports.current(0)
        self.selected_sport = self.combo_sports.get()
        self.load_leagues()

    def load_leagues(self):
        if self.combo_leagues:
            self.combo_leagues.destroy()
        self.combo_leagues = UtilitiesGui.create_combobox(
            self.canvas, 'combo_leagues', self.sf, self.reload_combos, self.pos_x_ini_combos + self.combo_width + 20,
            self.pos_y_combos,
            self.sql_helper.get_single_field_translated(LEAGUES_ID, LEAGUES_TABLE, self.option,
                                                        SPORTS_ID, self.selected_sport, True), self.combo_width)
        self.combo_leagues.current(0)
        self.selected_league = self.combo_leagues.get()
        self.load_conferences()

    def load_conferences(self):
        if self.combo_conferences:
            self.combo_conferences.destroy()
        self.combo_conferences = UtilitiesGui.create_combobox(
            self.canvas, 'combo_conferences', self.sf, self.reload_combos,
            self.pos_x_ini_combos + (self.combo_width * 2) + 40,
            self.pos_y_combos,
            self.sql_helper.get_single_field_translated(CONFERENCES_ID, CONFERENCES_TABLE, self.option,
                                                        LEAGUES_ID, self.selected_league, True), self.combo_width)
        self.combo_conferences.current(0)
        self.selected_conference = self.combo_conferences.get()
        self.load_divisions()

    def load_divisions(self):
        if self.combo_divisions:
            self.combo_divisions.destroy()
        self.combo_divisions = UtilitiesGui.create_combobox(
            self.canvas, 'combo_divisions', self.sf, self.reload_combos,
            self.pos_x_ini_combos + (self.combo_width * 3) + 60,
            self.pos_y_combos,
            self.sql_helper.get_single_field_translated(DIVISIONS_ID, DIVISIONS_TABLE, self.option,
                                                        CONFERENCES_ID, self.selected_conference, True),
            self.combo_width)
        self.combo_divisions.current(0)
        self.selected_division = self.combo_divisions.get()
        self.load_teams()

    def load_teams(self):
        self.remove_logos()
        rows = self.sql_helper.get_id_and_field(TEAM_ID, TEAM_NAME, TEAMS_TABLE, DIVISIONS_ID, self.selected_division)
        logos_per_row = Utilities.get_logos_per_row(self.size_x, self.team_logo_size_x)
        cur_row = 0
        cur_logo = 1
        for row in rows.keys():
            if cur_logo > logos_per_row:
                cur_logo = 1
                cur_row += 1

            initial_x_pos = Utilities.get_initial_x_pos(logos_per_row, cur_row, len(rows), self.size_x,
                                                        self.team_logo_size_x)

            img = UtilitiesGui.create_photo_image(teamsPicsDir + TEAM_LOGO.format(
                str(row) if Utilities.file_exists(teamsPicsDir + TEAM_LOGO.format(row)) else '0'),
                                                  self.team_logo_size_x,
                                                  self.team_logo_size_y)

            lab = UtilitiesGui.create_label(self.canvas, self.sf, str(row) + "|" + rows[row],
                                            initial_x_pos + ((cur_logo - 1) * self.team_logo_size_x) + (
                                                    (cur_logo - 1) * 20),
                                            (self.pos_y_combos + self.combo_leagues.winfo_reqheight() + 20)
                                            + (self.team_logo_size_y * cur_row) + (cur_row * 20 if cur_row > 0 else 0),
                                            self.team_logo_size_x, self.team_logo_size_y, img,
                                            {'bg': 'white', 'fg': 'white'})
            lab.image = img
            lab.bind("<Button-1>", self.change_team)
            cur_logo += 1

    def remove_logos(self):
        for element in list(self.canvas.children.keys()):
            if isinstance(self.canvas.children[element], Label) and self.canvas.children[element].cget('image'):
                self.canvas.children[element].destroy()

    def change_team(self, event=None):
        self.selected_team_id = event.widget.widgetName.split("|")[0]
        self.team_label.config(text=event.widget.widgetName.split("|")[1])

    def reload_combos(self, event_object):
        if event_object.widget.widgetName == 'combo_sports' and not event_object.widget.get() == self.selected_sport:
            self.selected_sport = event_object.widget.get()
            self.load_leagues()
        if event_object.widget.widgetName == 'combo_leagues' and not event_object.widget.get() == self.selected_league:
            self.selected_league = event_object.widget.get()
            self.load_conferences()
        if event_object.widget.widgetName == 'combo_conferences' \
                and not event_object.widget.get() == self.selected_conference:
            self.selected_conference = event_object.widget.get()
            self.load_divisions()
        if event_object.widget.widgetName == 'combo_divisions' \
                and not event_object.widget.get() == self.selected_division:
            self.selected_division = event_object.widget.get()
            self.load_teams()


if __name__ == '__main__':
    load = NewCareer(False, False)
    load.interface_new_career()
