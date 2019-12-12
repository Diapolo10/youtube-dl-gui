import sys
import tkinter as tk
import webbrowser
from pathlib import Path

import youtube_dl

from tl_manager import LangManager, LangMenu
import ydl_config

DESKTOP_PATH = Path.home() / 'Desktop'
HOME_DIR = Path(__file__).parent


# right click management; should probably be in it's own file since it's logically unrelated to anything here

class RightClickMenu(LangMenu):
    def __init__(self, lang, *args, **kwargs):
        LangMenu.__init__(self, None, tearoff=0, takefocus=0, **kwargs)

        self.add_command(label=lang.text['rclick_cut'], command=self.rClick_Cut)
        self.add_command(label=lang.text['rclick_copy'], command=self.rClick_Copy)
        self.add_command(label=lang.text['rclick_paste'], command=self.rClick_Paste)

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
        self.settings_file = ydl_config.DEFAULT_SAVE_PATH

        self.language = tk.StringVar(value=ydl_config.LANGUAGE)
        self.language.trace('w', self.config_update)

        self.curlang = LangManager(self, HOME_DIR)
        RightClickMenu(self.curlang)

        #self.grid()

        self.savepath = ydl_config.DEFAULT_SAVE_PATH
        
        if not self.savepath.exists():
            self.savepath.mkdir()

        # App settings
        self.output_type = tk.StringVar(value=ydl_config.OUTPUT_TYPE)
        self.output_type.trace('w', self.config_update)

        # Create toolbar
        toolbar = LangMenu(self.master)
        self.master.config(menu=toolbar)

        file_menu = LangMenu(toolbar)
        file_menu.add_command(label=self.curlang.text['tb_file_cfg'], command=self.config_window)
        file_menu.add_command(label=self.curlang.text['quit_button'], command=self.master.destroy)
        toolbar.add_cascade(label=self.curlang.text['tb_file'], menu=file_menu)

        help_menu = LangMenu(toolbar)
        help_menu.add_command(label=self.curlang.text['tb_help_about'], command=self.about_window)
        help_menu.add_command(label=self.curlang.text['tb_help_usage'], command=self.help_window)
        help_menu.add_command(label=self.curlang.text['tb_help_license'], command=lambda: webbrowser.open_new(r'https://github.com/Diapolo10/youtube-dl-gui/blob/gramps/LICENSE'))
        toolbar.add_cascade(label=self.curlang.text['tb_help'], menu=help_menu)

        lbl = tk.Label(self, textvariable=self.curlang.text['url_box'])
        lbl.pack(anchor=tk.W, side=tk.LEFT)
        #lbl.grid(row=0, column=0)

        self.entry = tk.Text(self)
        self.entry.pack()
        #self.entry.grid(row=0, column=1)

        subframe = tk.Frame(self)
        btn_dl = tk.Button(subframe, textvariable=self.curlang.text['dl_button'], command=self.downloader)
        btn_dl.pack(side=tk.LEFT)
        #btn_dl.grid(row=1, column=0)
        btn_close = tk.Button(subframe, textvariable=self.curlang.text['quit_button'], command=self.master.destroy)
        btn_close.pack(side=tk.LEFT)
        #btn_close.grid(row=1, column=1)
        subframe.pack(anchor=tk.W)

    def config_window(self):
        t = tk.Toplevel(self)
        t.wm_title(self.curlang.text['cfg_title'].get())
        t.resizable(0, 0)
        t.grid()

        tk.Label(t, textvariable=self.curlang.text['cfg_out']).grid(row=0, column=0)
        tk.Radiobutton(t, textvariable=self.curlang.text['cfg_out_vd'], variable=self.output_type, value='video').grid(row=0, column=1)
        tk.Radiobutton(t, textvariable=self.curlang.text['cfg_out_aud'], variable=self.output_type, value='audio').grid(row=0, column=2)

        tk.Label(t, textvariable=self.curlang.text['cfg_lang']).grid(row=1, column=0)
        tk.OptionMenu(t, self.language, *self.curlang.languages).grid(row=1, column=1)

    def about_window(self):
        window = tk.Toplevel(self)
        window.wm_title(self.curlang.text['about_title'].get())
        window.resizable(0, 0)

        tk.Label(window, textvariable=self.curlang.text['about_text']).pack()

    def help_window(self):
        window = tk.Toplevel(self)
        window.wm_title(self.curlang.text['help_title'].get())
        window.resizable(0, 0)

        tk.Label(window, textvariable=self.curlang.text['help_text']).pack()


    def config_update(self, *args):
        self.language = self.language.get().lower()
        self.output_type = self.output_type.get()
        # with open(self.settings_file, 'w') as f:
        #     toml.dump(self.settings, f)

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
            print(self.curlang.text['convert_complete'].get())
        self.entry.delete('1.0', tk.END)

    def my_hook(self, d):
        if d['status'] == 'finished':
            print(self.curlang.text['dl_complete'].get())
        if d['status'] == 'downloading':
            print(d['filename'], d['_percent_str'], d['_eta_str'])


if __name__ == "__main__":
    try:
        root = tk.Tk()
        win = App(root)
        win.pack()
        root.mainloop()
    except Exception as e:
        import time
        print(e)
        time.sleep(1000)
