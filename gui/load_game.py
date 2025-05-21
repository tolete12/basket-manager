from tkinter import END, messagebox
import gui.main_class as main_class
from db.sql_lite_handler import SQLiteHandler
from db.sql_lite_helper import SQLLiteHelper
from utilities.utilities_gui import UtilitiesGui
from variables.constants import BACKGROUND_PARQUE, INI_DB
from variables.paths import backgroundsPicsDir, parentDir
import tkinter.font as font


class LoadGame(main_class.MainClass):
    selected_game = ""
    root = None

    def __init__(self, override: bool, save_game: bool, translations: dict):
        super().__init__()
        super().connect_db(INI_DB, override, save_game)
        self.translations = translations
        self.arrow_buttons_size = 55
        self.interface_load_game()

    def on_simple_click(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            self.selected_game = widget.get(selection[0])

    def load_game(self):
        messagebox.showinfo(self.selected_game, self.selected_game)

    def delete_game(self):
        messagebox.showinfo(self.selected_game, self.selected_game)

    def fill_save_games(self, listbox):
        for file in self.utilities.list_files(parentDir, "py"):
            listbox.insert(END, file)

    def back_to_main_button(self):
        self.root.destroy()
        from gui.main_menu import MainMenu
        MainMenu(False, False)

    def interface_load_game(self):
        pic = backgroundsPicsDir + BACKGROUND_PARQUE
        self.root, canvas = UtilitiesGui.set_center_window(self.size_x, self.size_y, pic,
                                                           self.utilities.get_translation(self.translations,
                                                                                          20, self.option))

        sf = font.Font(family='Helvetica', size=20, weight='bold')
        size_lst_x = int(self.size_x / 2)
        size_lst_y = int(self.size_y / 2)
        pos_lst_x = int(self.size_x / 2) - int(self.size_x / 4)
        pos_lst_y = int(self.size_y / 2) - int(self.size_y / 4)

        listbox = UtilitiesGui.create_listbox(canvas, sf, pos_lst_x, pos_lst_y, size_lst_x, size_lst_y,
                                              self.on_simple_click)
        UtilitiesGui.create_label(canvas, sf, self.utilities.get_translation(self.translations, 26, self.option),
                                  pos_lst_x,
                                  int(pos_lst_y / 4), size_lst_x)
        scrollbar = UtilitiesGui.create_scrollbar(canvas, pos_lst_x + size_lst_x + 1, pos_lst_y, 20, size_lst_y)

        self.fill_save_games(listbox)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        img = UtilitiesGui.create_pic_back_button(self.arrow_buttons_size, self.arrow_buttons_size)

        UtilitiesGui.create_button(canvas, "", sf,
                                   self.back_to_main_button, {'bg': 'white', 'fg': 'white'},
                                   {'pos_x': 20, 'pos_y': self.size_y - 100}, img)

        UtilitiesGui.create_button(canvas, self.utilities.get_translation(self.translations, 20, self.option), sf,
                                   self.load_game, {'bg': 'blue', 'fg': 'white'},
                                   {'pos_x': pos_lst_x, 'pos_y': pos_lst_y + size_lst_y + 20})
        but_del_career = UtilitiesGui.create_button(canvas,
                                                    self.utilities.get_translation(self.translations, 27, self.option),
                                                    sf,
                                                    self.delete_game, {'bg': 'blue', 'fg': 'white'},
                                                    {'pos_x': 0, 'pos_y': 0})
        canvas.update()
        UtilitiesGui.place_button(but_del_career, {'pos_x': pos_lst_x + size_lst_x - but_del_career.winfo_width(),
                                                   'pos_y': pos_lst_y + size_lst_y + 20})
        self.root.mainloop()


if __name__ == '__main__':
    db_obj = SQLiteHandler(INI_DB, override=False, save_game=False)
    sql_helper = SQLLiteHelper(db_obj)
    translations_out = sql_helper.get_all_translations()
    load = LoadGame(False, False, translations_out)
    load.interface_load_game()
