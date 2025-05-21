from tkinter import ttk


class MyCombobox(ttk.Combobox):

    def __init__(self, master=None, cnf={}, **options):

        self.dict = None

        # get dictionary from options and put list of keys
        if 'values' in options and isinstance(options.get('values'), dict):
            self.dict = options.get('values')
            options['values'] = sorted(self.dict.keys())

        # combobox constructor with list of keys
        ttk.Combobox.__init__(self, **options)

        # assign some function
        self.bind('<<ComboboxSelected>>', self.on_select)

    def on_select(self, event):
        print(self.get(), self.get_key(), self.get_value())

    # overwrite `get()` to return `value` instead of `key`
    def get(self):
        if self.dict:
            return self.dict[ttk.Combobox.get(self)]
        else:
            return ttk.Combobox.get(self)

    def get_key(self):
        return ttk.Combobox.get(self)

    def get_value(self):
        return self.get()
