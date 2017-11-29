import sys
import os
from pathlib import Path
import tkinter as tk

import toml
import youtube_dl

CONFIG_FILE = "settings.toml"

class App(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.init_gui()

    def init_gui(self, *args, **kwargs):

        self.dir = Path(os.path.abspath(__file__)).parent
        self.settings = toml.load(os.path.join(self.dir, CONFIG_FILE))
        self.language = tk.StringVar()
        self.language.set(self.settings['language'].capitalize())
        self.lang = toml.load(
            os.path.join(self.dir, "lang", f"{self.language.get()}.toml")
        )
        self.savepath = self.settings.get('default_save_path')
        if self.savepath == "":
            self.savepath = os.path.join(self.dir, 'dl')
        if not Path(self.savepath).exists():
            os.makedirs(self.savepath)

        self.LANG_OPTIONS = (
            "Suomi",
            "English",
        )

        # App settings
        self.output_type = tk.StringVar()
        self.output_type.set(self.settings.get('output_type', 'video'))
        self.output_type.trace('w', self.config_update)

        self.language.trace('w', self.config_update)

        # Set window title
        self.master.title(self.lang['title'])

        # Create toolbar
        toolbar = tk.Menu(self.master)
        self.master.config(menu=toolbar)

        file_menu = tk.Menu(toolbar)
        file_menu.add_command(label=self.lang['tb_file_cfg'], command=self.config_window)
        file_menu.add_command(label=self.lang['quit_button'], command=self.master.destroy)
        toolbar.add_cascade(label=self.lang['tb_file'], menu=file_menu)

        help_menu = tk.Menu(toolbar)
        help_menu.add_command(label=self.lang['tb_help_about'], command=None)
        help_menu.add_command(label=self.lang['tb_help_usage'], command=None)
        help_menu.add_command(label=self.lang['tb_help_license'], command=None)
        toolbar.add_cascade(label=self.lang['tb_help'], menu=help_menu)


        # Add buttons and text fields
        tk.Label(self.master, text=self.lang['url_box']).grid(row=0)
        self.entry = tk.Text(self.master)
        self.entry.grid(row=0, column=1)

        tk.Button(self.master, text=self.lang['dl_button'], command=self.downloader).grid(row=1, column=0, sticky=tk.W, pady=4)
        tk.Button(self.master, text=self.lang['quit_button'], command=self.master.destroy).grid(row=1, column=1, sticky=tk.W, pady=4)

    def config_window(self):
        t = tk.Toplevel(self)
        t.wm_title(self.lang['cfg_title'])
        t.grid()

        tk.Label(t, text=self.lang['cfg_out']).grid(row=0, column=0)
        tk.Radiobutton(t, text=self.lang['cfg_out_vd'], variable=self.output_type, value='video').grid(row=0, column=1)
        tk.Radiobutton(t, text=self.lang['cfg_out_aud'], variable=self.output_type, value='audio').grid(row=0, column=2)

        tk.Label(t, text=self.lang['cfg_lang']).grid(row=1, column=0)
        #self.temp_lang = tk.StringVar()
        #self.temp_lang.set('English')
        #self.temp_lang.trace('w', self.config_update)
        #tk.OptionMenu(t, variable=self.temp_lang, *self.LANG_OPTIONS).grid(row=1, column=1)
        tk.OptionMenu(t, self.language, *self.LANG_OPTIONS).grid(row=1, column=1)

    def config_update(self, *args, **kwargs):
        #print(args, kwargs)
        #self.settings['language'] = self.LANG_OPTIONS.get(
        #    self.temp_lang.get() if self.temp_lang.get() is not None else 'English',
        #    'en'
        #)
        self.settings['language'] = self.language.get().lower()
        self.settings['output_type'] = self.output_type.get()
        with open(os.path.join(self.dir, CONFIG_FILE), 'w') as f:
            toml.dump(self.settings, f)
        self.init_gui(*args,**kwargs)

    def downloader(self):
        videos = list(filter(None, self.entry.get("1.0", tk.END).splitlines()))
        class MyLogger(object):
            def debug(self, msg):
                print(msg)

            def warning(self, msg):
                print(f"Warning: {msg}")

            def error(self, msg):
                print(f"ERROR: {msg}")


        def my_hook(d):
            if d['status'] == 'finished':
                print(self.lang['dl_complete'])
            if d['status'] == 'downloading':
                print(d['filename'], d['_percent_str'], d['_eta_str'])


        ydl_opts = {
            'format': 'bestaudio/best' if self.output_type.get() == "audio" else 'mp4',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if self.output_type.get() == "audio" else [],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'outtmpl': os.path.join(self.savepath, "%(title)s.%(ext)s"),
            'download_archive': 'downloaded_songs.txt',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(videos)
        if self.output_type.get() == "audio":
            print(self.lang['convert_complete'])
        self.entry.delete('1.0', tk.END)


if __name__ == "__main__":
    App().mainloop()
    sys.exit()
