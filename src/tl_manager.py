import tkinter as tk

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
