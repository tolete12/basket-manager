import configparser
from tkinter import Listbox, Canvas, Label, Scrollbar, Button, Tk, BOTH, YES, NW, Entry
from tkinter.font import Font
from tkinter.ttk import Treeview

from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

from gui.my_combobox import MyCombobox
from utilities import Utilities
from variables import paths
from variables.constants import LEFT_ARROW, RIGHT_ARROW
from variables.paths import iconsPicsDir


class UtilitiesGui:

    @staticmethod
    def set_center_window(window_width, window_height, pic, title):
        root = Tk()

        def disable_event():
            print("")

        global rescaled_img
        global photo
        root.protocol("WM_DELETE_WINDOW", disable_event)
        root.title(title)
        width_screen, height_screen = UtilitiesGui.get_screen_size()

        original_img = Image.open(pic)
        canvas = Canvas(width=width_screen, height=height_screen, bd=0, highlightthickness=0)
        canvas.pack(fill=BOTH, expand=YES)

        rescaled_img = original_img.resize((window_width, window_height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(rescaled_img)

        root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))

        root.resizable(True, True)

        canvas.create_image(0, 0, image=photo, anchor=NW)

        return root, canvas

    @staticmethod
    def create_photo_image(pic, pic_size_x, pic_size_y):
        img = Image.open(pic)  # PIL solution
        img = img.resize((pic_size_x, pic_size_y), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        img = ImageTk.PhotoImage(img)  # convert to PhotoImage
        return img

    @staticmethod
    def get_screen_size():
        width = 1280
        height = 720
        if Utilities.file_exists(paths.configFile):
            config = configparser.ConfigParser()
            config.read(paths.configFile)
            width = config['General']['WIDTH'] if int(config['General']['WIDTH']) >= 1280 else 1280
            height = config['General']['HEIGHT'] if int(config['General']['HEIGHT']) >= 720 else 720
        return int(width), int(height)

    @staticmethod
    def create_listbox(canvas: Canvas, sf: Font, pos_lst_x: int, pos_lst_y: int, size_lst_x: int,
                       size_lst_y: int, function_on_click) -> Listbox:
        listbox = Listbox(canvas, font=sf)
        listbox.place(x=pos_lst_x, y=pos_lst_y, width=size_lst_x, height=size_lst_y)
        listbox.bind("<<ListboxSelect>>", function_on_click)
        return listbox

    @staticmethod
    def create_label(canvas: Canvas, sf: Font, text: str, pos_lst_x: int, pos_lst_y: int, size_lst_x: int,
                     size_lst_y: int = None, img: PhotoImage = None,
                     style: dict = {'bg': 'black', 'fg': 'white'}) -> Label:
        label = Label(canvas, font=sf, bg=style['bg'], fg=style['fg'], text=text, image=img)
        label.place(x=pos_lst_x, y=pos_lst_y, width=size_lst_x, height=size_lst_y)
        label.widgetName = text
        return label

    @staticmethod
    def create_scrollbar(root, pos_lst_x, pos_lst_y, size_lst_x, size_lst_y) -> Scrollbar:
        scrollbar = Scrollbar(root)
        scrollbar.place(x=pos_lst_x, y=pos_lst_y, height=size_lst_y, width=size_lst_x)
        return scrollbar

    @staticmethod
    def create_button(canvas: Canvas, text: str, sf: Font, function, style: dict, position: dict,
                      image: PhotoImage = None) -> Button:
        but = Button(canvas, text=text, command=function, font=sf, bg=style['bg'], fg=style['fg'], image=image)
        UtilitiesGui.place_button(but, position)
        return but

    @staticmethod
    def place_button(but: Button, position: dict):
        but.place(x=position['pos_x'], y=position['pos_y'], height=position['height'] if 'height' in position else None,
                  width=position['width'] if 'width' in position else None)

    @staticmethod
    def create_combobox(canvas: Canvas, widget_name: str, sf: Font, function, pos_x: int, pos_y: int,
                        values: dict = None, width: int = None, height: int = None):
        combo = MyCombobox(canvas, state='readonly', font=sf, values=values)
        combo.widgetName = widget_name
        combo.place(x=pos_x, y=pos_y, width=width, height=height)
        combo.bind("<<ComboboxSelected>>", function)
        return combo

    @staticmethod
    def create_pic_back_button(size_x: int, size_y: int) -> PhotoImage:
        return UtilitiesGui.create_photo_image(iconsPicsDir + LEFT_ARROW, size_x, size_y)

    @staticmethod
    def create_pic_forward_button(size_x: int, size_y: int) -> PhotoImage:
        return UtilitiesGui.create_photo_image(iconsPicsDir + RIGHT_ARROW, size_x, size_y)

    @staticmethod
    def create_entry(canvas: Canvas, pos_x: int, pos_y: int, size_x: int, size_y: int = None):
        name_entry = Entry(canvas, font=('calibre', 14, 'normal'))
        name_entry.place(x=pos_x, y=pos_y, width=size_x, height=size_y)
        return name_entry

    @staticmethod
    def create_treeview(canvas: Canvas, function, pos_x: int, pos_y: int, size_x: int, size_y: int, columns: list):
        tree = Treeview(canvas, selectmode='browse')
        tree.place(x=pos_x, y=pos_y, width=size_x, height=size_y)

        vsb = Scrollbar(canvas, orient="vertical", command=tree.yview)
        vsb.place(x=pos_x + size_x + 2, y=pos_y, height=size_y)

        tree.configure(yscrollcommand=vsb.set)

        tree['show'] = 'headings'
        tree["columns"] = tuple([str(i + 1) for i in range(len(columns))])

        for i in range(len(columns)):
            tree.column(str(i + 1), width=100, anchor='c')
            tree.heading(str(i + 1), text=columns[i])

        tree.bind('<<TreeviewSelect>>', function)
        return tree


