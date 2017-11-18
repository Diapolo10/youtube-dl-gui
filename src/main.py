import sys
import os
from pathlib import Path
import tkinter as tk

import toml
import youtube_dl



class App:
    def __init__(self):
        self.root = tk.Tk()
        self.dir = Path(os.path.abspath(__file__)).parent
        self.settings = toml.load(os.path.join(self.dir, "settings.toml"))
        self.lang = toml.load(
            os.path.join(self.dir, "lang", f"{self.settings['language']}.toml")
        )
        self.savepath = self.settings.get('default_save_path')
        if self.savepath == "":
            self.savepath = os.path.join(self.dir, 'dl')
        if not Path(self.savepath).exists():
            os.makedirs(self.savepath)
            
        self.root.title(self.lang['title'])

        # Add buttons and text fields
        tk.Label(self.root, text=self.lang['url_box']).grid(row=0)
        self.entry = tk.Text(self.root)
        self.entry.grid(row=0, column=1)

        tk.Button(self.root, text=self.lang['dl_button'], command=self.downloader).grid(row=1, column=0, sticky=tk.W, pady=4)
        tk.Button(self.root, text=self.lang['quit_button'], command=self.root.destroy).grid(row=1, column=1, sticky=tk.W, pady=4)


    def downloader(self):
        videos = self.entry.get("1.0", tk.END).splitlines()
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


        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'outtmpl': os.path.join(self.savepath, "%(title)s.%(ext)s"),
            'download_archive': 'downloaded_songs.txt',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(videos)
        print(self.lang['convert_complete'])
        self.entry.delete('1.0', tk.END)


if __name__ == "__main__":
    App().root.mainloop()
    sys.exit()
