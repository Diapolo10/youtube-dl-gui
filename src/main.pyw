import sys
import webbrowser
from pathlib import Path
import tkinter as tk
from win32com.shell import shell, shellcon

import toml
import youtube_dl

from tl_manager import LangManager, LangMenu

CONFIG_FILE = "settings.toml"
DESKTOP_PATH = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)


'''
* why are you laying everything out in self.master? The whole point of subclassing a Frame is to layout in self.
* your rClickbinder function binds to the Text (good) and Entry, Listbox and Label class (why???)
* try not to use names of built in function as variable names, like "dir"
* I'm glad to see that you can split lines apart to make code more readable, but it's often better to make variables instead
* use instance variables when you need to share data between methods, and not anywhere else
* why toml and not a built in serialzer like json?
'''


# right click management; should probably be in it's own file since it's logically unrelated to anything here

class RightClickMenu(LangMenu):
    def __init__(self, lang, *args, **kwargs):
        LangMenu.__init__(self, None, tearoff=0, takefocus=0, **kwargs)

        self.add_command(label=lang.rclick_cut, command=self.rClick_Cut)
        self.add_command(label=lang.rclick_copy, command=self.rClick_Copy)
        self.add_command(label=lang.rclick_paste, command=self.rClick_Paste)

        self.bind_class("Text", sequence='<Button-3>', func=self.popup, add='')
        self.event = None

    def popup(self, event):
        self.event = event
        self.event.widget.focus() # not really sure why this is needed.
        self.tk_popup(event.x_root+40, event.y_root+10, entry="0")

    def rClick_Copy(self):
        self.event.widget.event_generate('<Control-c>')

    def rClick_Cut(self):
        self.event.widget.event_generate('<Control-x>')

    def rClick_Paste(self):
        self.event.widget.event_generate('<Control-v>')

# end right click management code

class MyLogger:
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(f"Warning: {msg}")

    def error(self, msg):
        print(f"ERROR: {msg}")

class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # GUI init code here (no need for a method)
        home_dir = Path(__file__).parent
        self.settings_file = home_dir / CONFIG_FILE
        self.settings = toml.load(self.settings_file)

        self.language = tk.StringVar(value=self.settings['language'])
        self.language.trace('w', self.config_update)

        self.curlang = LangManager(self, home_dir)
        RightClickMenu(self.curlang)

        #self.grid()

        self.savepath = self.settings.get('default_save_path')
        if self.savepath == "":
            self.savepath = Path(DESKTOP_PATH) / "ladatut_videot"
        else:
            self.savepath = Path(self.savepath)
        if not self.savepath.exists():
            self.savepath.mkdir()

        # App settings
        self.output_type = tk.StringVar(value = self.settings.get('output_type', 'video'))
        self.output_type.trace('w', self.config_update)

        # Create toolbar
        toolbar = LangMenu(self.master)
        self.master.config(menu=toolbar)

        file_menu = LangMenu(toolbar)
        file_menu.add_command(label=self.curlang.tb_file_cfg, command=self.config_window)
        file_menu.add_command(label=self.curlang.quit_button, command=self.master.destroy)
        toolbar.add_cascade(label=self.curlang.tb_file, menu=file_menu)

        help_menu = LangMenu(toolbar)
        help_menu.add_command(label=self.curlang.tb_help_about, command=self.about_window)
        help_menu.add_command(label=self.curlang.tb_help_usage, command=self.help_window)
        help_menu.add_command(label=self.curlang.tb_help_license, command=lambda: webbrowser.open_new(r'https://github.com/Diapolo10/youtube-dl-gui/blob/gramps/LICENSE'))
        toolbar.add_cascade(label=self.curlang.tb_help, menu=help_menu)

        lbl = tk.Label(self, textvariable=self.curlang.url_box)
        lbl.pack(anchor=tk.W, side=tk.LEFT)
        #lbl.grid(row=0, column=0)

        self.entry = tk.Text(self)
        self.entry.pack()
        #self.entry.grid(row=0, column=1)

        subframe = tk.Frame(self)
        btn_dl = tk.Button(subframe, textvariable=self.curlang.dl_button, command=self.downloader)
        btn_dl.pack(side=tk.LEFT)
        #btn_dl.grid(row=1, column=0)
        btn_close = tk.Button(subframe, textvariable=self.curlang.quit_button, command=self.master.destroy)
        btn_close.pack(side=tk.LEFT)
        #btn_close.grid(row=1, column=1)
        subframe.pack(anchor=tk.W)

    def config_window(self):
        t = tk.Toplevel(self)
        t.wm_title(self.curlang.cfg_title.get())
        t.resizable(0, 0)
        t.grid()

        tk.Label(t, textvariable=self.curlang.cfg_out).grid(row=0, column=0)
        tk.Radiobutton(t, textvariable=self.curlang.cfg_out_vd, variable=self.output_type, value='video').grid(row=0, column=1)
        tk.Radiobutton(t, textvariable=self.curlang.cfg_out_aud, variable=self.output_type, value='audio').grid(row=0, column=2)

        tk.Label(t, textvariable=self.curlang.cfg_lang).grid(row=1, column=0)
        tk.OptionMenu(t, self.language, *self.curlang.languages).grid(row=1, column=1)

    def about_window(self):
        window = tk.Toplevel(self)
        window.wm_title(self.curlang.about_title.get())
        window.resizable(0, 0)

        tk.Label(window, textvariable=self.curlang.about_text).pack()

    def help_window(self):
        window = tk.Toplevel(self)
        window.wm_title(self.curlang.help_title.get())
        window.resizable(0, 0)

        tk.Label(window, textvariable=self.curlang.help_text).pack()


    def config_update(self, *args):
        self.settings['language'] = self.language.get().lower()
        self.settings['output_type'] = self.output_type.get()
        with open(self.settings_file, 'w') as f:
            toml.dump(self.settings, f)

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
            'outtmpl': str(self.savepath / "%(title)s.%(ext)s"),
            'download_archive': 'downloaded_songs.txt',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(videos)
        if self.output_type.get() == "audio":
            print(self.curlang.convert_complete.get())
        self.entry.delete('1.0', tk.END)

    def my_hook(self, d):
        if d['status'] == 'finished':
            print(self.curlang.dl_complete.get())
        if d['status'] == 'downloading':
            print(d['filename'], d['_percent_str'], d['_eta_str'])


if __name__ == "__main__":
    root = tk.Tk()
    win = App(root)
    win.pack()
    root.mainloop()
