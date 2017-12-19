import tkinter as tk
from functools import partial
from pathlib import Path
import os
import toml

class LangManager:
    def __init__(self, parent, home_dir, lang='english'):
        self.parent = parent
        parent.language.trace('w', self.update)

        self.load(home_dir)

        self.title = tk.StringVar()
        self.url_box = tk.StringVar()
        self.dl_button = tk.StringVar()
        self.quit_button = tk.StringVar()
        self.dl_complete = tk.StringVar()
        self.convert_complete = tk.StringVar()

        self.rclick_cut = tk.StringVar()
        self.rclick_copy = tk.StringVar()
        self.rclick_paste = tk.StringVar()

        self.tb_file = tk.StringVar()
        self.tb_file_cfg = tk.StringVar()

        self.tb_help = tk.StringVar()
        self.tb_help_about = tk.StringVar()
        self.tb_help_usage = tk.StringVar()
        self.tb_help_license = tk.StringVar()

        self.cfg_title = tk.StringVar()

        self.cfg_out = tk.StringVar()
        self.cfg_out_vd = tk.StringVar()
        self.cfg_out_aud = tk.StringVar()

        self.cfg_lang = tk.StringVar()

        self.about_title = tk.StringVar()
        self.about_text = tk.StringVar()

        self.help_title = tk.StringVar()
        self.help_text = tk.StringVar()


        self.update()

    def load(self, home_dir):
        self.languages = {}

        language_pack_dir = os.path.join(home_dir, 'lang')
        for filename in os.listdir(language_pack_dir):
            lang_name = os.path.splitext(filename)[0]
            data = toml.load(os.path.join(language_pack_dir, filename))
            self.languages[lang_name] = data

    def update(self, *args):
        lang = self.parent.language.get()
        for key, value in self.languages[lang].items():
            getattr(self, key).set(value)

        tk._default_root.title(self.title.get()) # set the window title

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
