import tkinter as tk
from functools import partial

class LangManager:
    def __init__(self, parent, lang='english'):
        self.parent = parent

        self.title = tk.StringVar()
        self.url_box = tk.StringVar()
        self.dl_button = tk.StringVar()
        self.quit_button = tk.StringVar()
        self.dl_complete = tk.StringVar()
        self.convert_complete = tk.StringVar()

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

        self.update(lang)

    def update(self, lang):
        for key, value in self.parent.languages[lang].items():
            getattr(self, key).set(value)

class LangMenu(tk.Menu):
    '''a new type of Menu that will accept tk.Variables as labels'''
    def __init__(self, master, **kwargs):
        tk.Menu.__init__(self, master, **kwargs)
        self.last_index = 0

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

