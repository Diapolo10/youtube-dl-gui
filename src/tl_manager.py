import tkinter as tk
from functools import partial
from pathlib import Path

from database import Database

class LangManager:
    def __init__(self, parent, home_dir, lang='english'):
        self.parent = parent
        self.parent.language.trace('w', self.update)


        with Database() as db:
            self._text = db.get_localisation(lang)
            self.languages = db.get_languages()

        self.text = {key: tk.StringVar() for key in self._text}

        self.update()

    def update(self, *args):
        lang = self.parent.language.get()

        with Database() as db:
            self._text = db.get_localisation(lang)

        for key, value in self._text.items():
            self.text[key].set(value)

        tk._default_root.title(self.text['window_title'].get()) # set the window title

class LangMenu(tk.Menu):
    '''a new type of Menu that will accept tk.Variables as labels'''
    def __init__(self, master, **kwargs):
        tk.Menu.__init__(self, master, **kwargs)
        self.last_index = -1 if kwargs.get('tearoff') == 0 else 0

    def update_label(self, index, label, *trace_args):
        self.entryconfigure(index, label=label.get())

    def enhance(self, kwargs):
        self.last_index += 1
        label = kwargs.get('label')
        if isinstance(label, tk.Variable):
            label.trace('w', partial(self.update_label, self.last_index, label))
            kwargs['label'] = label.get() # set the initial label text

    def add_command(self, *args, **kwargs):
        self.enhance(kwargs)
        tk.Menu.add_command(self, *args, **kwargs)

    def add_cascade(self, *args, **kwargs):
        self.enhance(kwargs)
        tk.Menu.add_cascade(self, *args, **kwargs)

    def add_checkbutton(self, *args, **kwargs):
        self.enhance(kwargs)
        tk.Menu.add_checkbutton(self, *args, **kwargs)

    def add_radiobutton(self, *args, **kwargs):
        self.enhance(kwargs)
        tk.Menu.add_radiobutton(self, *args, **kwargs)

    def add_separator(self, *args, **kwargs):
        self.last_index += 1
        tk.Menu.add_separator(self, *args, **kwargs)
