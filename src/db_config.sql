-- sqlite

DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS config;
DROP TABLE IF EXISTS ui_lang;

CREATE TABLE videos(
    video_url TEXT NOT NULL,
    checksum TEXT NOT NULL
);

CREATE TABLE config(
    language TEXT NOT NULL DEFAULT "english",
    video_dir TEXT NOT NULL DEFAULT "",
    output_type INTEGER NOT NULL CHECK (
        output_type IN (
            0, -- "video (MP4)"
            1  -- "audio (MP3)"
        )
    ) DEFAULT 0
);

CREATE TABLE ui_lang(
    ui_element TEXT NOT NULL,
    ui_text TEXT NOT NULL,
    lang TEXT NOT NULL DEFAULT "english"
);

INSERT INTO config VALUES
    ("english", "", 0);

-- English
INSERT INTO ui_lang (ui_element, ui_text) VALUES
    ("window_title", "Something");

-- Finnish
INSERT INTO ui_lang (ui_element, ui_text, lang) VALUES
    ("window_title", "Jotakin", "finnish");