import sys
import os
from pathlib import Path
import tkinter as tk

import toml
import youtube_dl

from tl_manager import LangManager

CONFIG_FILE = "settings.toml"

def rClicker(e):
    """
    Right click context menu for all tk.Entry and tk.Text widgets
    """

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]

        rmenu = tk.Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        print(' - rClick menu, something wrong')
        pass
    return "break"

def rClickbinder(r):

    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except TclError:
        print(' - rClickbinder, something wrong')
        pass

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(f"Warning: {msg}")

    def error(self, msg):
        print(f"ERROR: {msg}")


class App(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        rClickbinder(self.master)
        self.languages = {}
        self.init_gui(*args, **kwargs)

    def init_gui(self, *args, **kwargs):

        self.dir = Path(os.path.abspath(__file__)).parent
        self.settings = toml.load(os.path.join(self.dir, CONFIG_FILE))
        self.language_packs = os.path.join(self.dir, 'lang')
        self.language = tk.StringVar()
        self.language.set(self.settings['language'])
        #self.lang = toml.load(
        #    os.path.join(self.dir, "lang", f"{self.language.get()}.toml")
        #)
        for filename in os.listdir(self.language_packs):
            self.languages[
                '.'.join(filename.split('.')[:-1])
                ] = toml.load(os.path.join(self.language_packs, filename))
        self.curlang = LangManager(self, self.language.get())
        self.savepath = self.settings.get('default_save_path')
        if self.savepath == "":
            self.savepath = os.path.join(self.dir, 'dl')
        if not Path(self.savepath).exists():
            os.makedirs(self.savepath)

        print(self.languages)
        # App settings
        self.output_type = tk.StringVar()
        self.output_type.set(self.settings.get('output_type', 'video'))
        self.output_type.trace('w', self.config_update)

        self.language.trace('w', self.config_update)

        # Set window title
        self.master.title(
            #self.lang['title']
            self.curlang.title.get()
        )

        # Create toolbar
        toolbar = tk.Menu(self.master)
        self.master.config(menu=toolbar)

        file_menu = tk.Menu(toolbar)
        # file_menu.add_command(label=self.lang['tb_file_cfg'], command=self.config_window)
        # file_menu.add_command(label=self.lang['quit_button'], command=self.master.destroy)
        # toolbar.add_cascade(label=self.lang['tb_file'], menu=file_menu)
        file_menu.add_command(label=self.curlang.tb_file_cfg.get(), command=self.config_window)
        file_menu.add_command(label=self.curlang.quit_button.get(), command=self.master.destroy)
        toolbar.add_cascade(label=self.curlang.tb_file.get(), menu=file_menu)

        help_menu = tk.Menu(toolbar)
        # help_menu.add_command(label=self.lang['tb_help_about'], command=None)
        # help_menu.add_command(label=self.lang['tb_help_usage'], command=None)
        # help_menu.add_command(label=self.lang['tb_help_license'], command=None)
        # toolbar.add_cascade(label=self.lang['tb_help'], menu=help_menu)
        help_menu.add_command(label=self.curlang.tb_help_about.get(), command=None)
        help_menu.add_command(label=self.curlang.tb_help_usage.get(), command=None)
        help_menu.add_command(label=self.curlang.tb_help_license.get(), command=None)
        toolbar.add_cascade(label=self.curlang.tb_help.get(), menu=help_menu)


        # Add buttons and text fields
        # tk.Label(self.master, text=self.lang['url_box']).grid(row=0)
        tk.Label(self.master, textvariable=self.curlang.url_box).grid(row=0)
        self.entry = tk.Text(self.master)
        #self.entry.bind('<Button-3>',rClicker, add='')
        self.entry.grid(row=0, column=1)

        # tk.Button(self.master, text=self.lang['dl_button'], command=self.downloader).grid(row=1, column=0, sticky=tk.W, pady=4)
        # tk.Button(self.master, text=self.lang['quit_button'], command=self.master.destroy).grid(row=1, column=1, sticky=tk.W, pady=4)
        tk.Button(self.master, text=self.curlang.dl_button.get(), command=self.downloader).grid(row=1, column=0, sticky=tk.W, pady=4)
        tk.Button(self.master, text=self.curlang.quit_button.get(), command=self.master.destroy).grid(row=1, column=1, sticky=tk.W, pady=4)

    def config_window(self):
        t = tk.Toplevel(self)
        # t.wm_title(self.lang['cfg_title'])
        t.wm_title(self.curlang.cfg_title.get())
        t.resizable(0, 0)
        t.grid()

        # tk.Label(t, text=self.lang['cfg_out']).grid(row=0, column=0)
        # tk.Radiobutton(t, text=self.lang['cfg_out_vd'], variable=self.output_type, value='video').grid(row=0, column=1)
        # tk.Radiobutton(t, text=self.lang['cfg_out_aud'], variable=self.output_type, value='audio').grid(row=0, column=2)
        tk.Label(t, text=self.curlang.cfg_out.get()).grid(row=0, column=0)
        tk.Radiobutton(t, textvariable=self.curlang.cfg_out_vd, variable=self.output_type, value='video').grid(row=0, column=1)
        tk.Radiobutton(t, textvariable=self.curlang.cfg_out_aud, variable=self.output_type, value='audio').grid(row=0, column=2)

        # tk.Label(t, text=self.lang['cfg_lang']).grid(row=1, column=0)
        tk.Label(t, textvariable=self.curlang.cfg_lang).grid(row=1, column=0)
        #self.temp_lang = tk.StringVar()
        #self.temp_lang.set('English')
        #self.temp_lang.trace('w', self.config_update)
        #tk.OptionMenu(t, variable=self.temp_lang, *self.LANG_OPTIONS).grid(row=1, column=1)
        tk.OptionMenu(t, self.language, *self.languages).grid(row=1, column=1)

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

        ydl_opts = {
            'format': 'bestaudio/best' if self.output_type.get() == "audio" else 'mp4',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if self.output_type.get() == "audio" else [],
            'logger': MyLogger(),
            'progress_hooks': [self.my_hook],
            'outtmpl': os.path.join(self.savepath, "%(title)s.%(ext)s"),
            'download_archive': 'downloaded_songs.txt',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(videos)
        if self.output_type.get() == "audio":
            # print(self.lang['convert_complete'])
            print(self.curlang.convert_complete.get())
        self.entry.delete('1.0', tk.END)

    def my_hook(self, d):
        if d['status'] == 'finished':
            # print(self.lang['dl_complete'])
            print(self.curlang.dl_complete.get())
        if d['status'] == 'downloading':
            print(d['filename'], d['_percent_str'], d['_eta_str'])


if __name__ == "__main__":
    App().mainloop()
    sys.exit()
