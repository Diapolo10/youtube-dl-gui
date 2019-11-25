import contextlib
import sqlite3
import typing
from pathlib import Path

import ydl_config

DB_NAME = "ydl_db.sqlite"
DB_CONFIG_NAME = "db_config.sql"
DB_CONFIG_PATH = Path(__file__).parent / DB_CONFIG_NAME

def md5(filepath):

    import hashlib
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

with contextlib.closing(sqlite3.connect("test.db")) as db:
    with open("config.sql") as f:
        db.cursor().executescript(f.read())

class Database:
    def __init__(self, db_config_path=DB_CONFIG_PATH, force_rerun_config=False):
        self.db_name = DB_NAME
        self.db_config_file = db_config_path

        run_db_config = force_rerun_config
        
        if not (Path.cwd() / DB_NAME).exists():
            run_db_config = True

        db = sqlite3.connect(DB_NAME)
        self.cur = db.cursor()
        if run_db_config:
            with open(self.db_config_file) as f:
                self.cur.executescript(f.read())

    def get_localisation(self, lang: str):
        self.cur.execute("SELECT ui_element, ui_text, lang FROM ui_lang WHERE lang=?", (lang,))
        db_results: typing.List[typing.Tuple[str, str, str]] = self.cur.fetchall()

        if not db_results:
            raise ValueError(f"No localisation for language '{lang}'")

        results: typing.Dict[str, str] = {}

        for elem, text, lang in db_results:
            results[elem] = text

        return results


    def check_url(self, url: str):
        self.cur.execute("SELECT video_url, checksum FROM videos WHERE video_url=?", (url,))
        video = self.cur.fetchone()

        if not video:
            return False

        if not ydl_config.default_save_path.exists():
            ydl_config.default_save_path.mkdir()
            return False

        for file in ydl_config.default_save_path.iterdir():
            if md5(file) == video[1]:
                return True
        
        return False
        

        

