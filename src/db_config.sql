-- sqlite

DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS ui_lang;

CREATE TABLE videos(
    video_url TEXT NOT NULL,
    checksum TEXT NOT NULL
);

CREATE TABLE ui_lang(
    ui_element TEXT NOT NULL,
    ui_text TEXT NOT NULL,
    lang TEXT NOT NULL DEFAULT "english"
);

-- English
INSERT INTO ui_lang (ui_element, ui_text) VALUES
    -- Program title
    ("window_title", "YouTube-DL GUI"),

    -- Main window
    ("url_box", "Video URLs"),
    ("dl_button", "Start download"),
    ("quit_button", "Exit"),
    ("dl_complete", "Done downloading, now converting..."),
    ("convert_complete", "Video successfully converted"),

    -- Context menu
    ("rclick_cut", "Cut"),
    ("rclick_copy", "Copy"),
    ("rclick_paste", "Paste"),
    
    -- Toolbar
        -- File menu
        ("tb_file", "File"),
        ("tb_file_cfg", "Settings"),

        -- Help menu
        ("tb_help", "Help"),
        ("tb_help_about", "About"),
        ("tb_help_usage", "Usage"),
        ("tb_help_license", "License"),

    -- Settings window
    ("cfg_title", "YDL Settings"),
    ("cfg_out", "Output (video/audio):"),
    ("cfg_out_vd", "Video"),
    ("cfg_out_aud", "Audio"),
    ("cfg_lang", "GUI Language:"),

    -- "About"-window
    ("about_title", "About"),
    ("about_text", "GUI written by Lari Liuhamo. Runs Youtube-DL under the hood, written by Ricardo Garcia."),
    
    -- Help window
    ("help_title", "Help"),
    ("help_text", "Quick guide\n\n\t1. Copy a YouTube video URL\n\t2. Paste the URL on the text area of this program\n\t3. If you have more than one video to be downloaded, press enter and repeat the steps 1-3 until this is no longer the case\n\t4. Click the download button on the bottom\n\t5. If the program freezes, everything is going well. The moment the URLs disappear all videos have been downloaded (and converted, if you so chose)");


-- Finnish
INSERT INTO ui_lang (ui_element, ui_text, lang) VALUES
    -- Program title
    ("window_title", "YDL-videolataaja"),

    -- Main window
    ("url_box", "Videoiden verkko-osoitteet"),
    ("dl_button", "Lataa videot"),
    ("quit_button", "Sulje"),
    ("dl_complete", "Lataus suoritettu, muutetaan tiedostomuotoa..."),
    ("convert_complete", "Video tallennettu onnistuneesti"),

    -- Context menu
    ("rclick_cut", "Leikkaa"),
    ("rclick_copy", "Kopioi"),
    ("rclick_paste", "Liitä"),
    
    -- Toolbar
        -- File menu
        ("tb_file", "Tiedosto"),
        ("tb_file_cfg", "Asetukset"),

        -- Help menu
        ("tb_help", "Ohje"),
        ("tb_help_about", "Tietoja"),
        ("tb_help_usage", "Käyttöohjeet"),
        ("tb_help_license", "Lisenssi"),

    -- Settings window
    ("cfg_title", "YDL-asetukset"),
    ("cfg_out", "Ladattu tiedostomuoto (video/ääni):"),
    ("cfg_out_vd", "Video"),
    ("cfg_out_aud", "Pelkkä ääni"),
    ("cfg_lang", "Käyttöliittymän kieli:"),

    -- "About"-window
    ("about_title", "Tietoja"),
    ("about_text", "Käyttöliittymän suunnitteli ja teki Lari Liuhamo. Sen alla ohjelman pitää kasassa Ricardo Garcian luoma työkalu Youtube-DL."),
    
    -- Help window
    ("help_title", Käyttöohjeet"),
    ("help_text", "Pikaopas\n\n\t1. Kopioi YouTube-videon verkko-osoite (Ctrl+C tai oikealla hiiren painikkeella)\n\t2. Liitä verkko-osoite tämän ohjelman tekstikenttään (Ctrl+V tai oikealla hiiren painikkeella)\n\t3. Jos haluat ladata useampia videoita, paina enteriä ja toista kohdat 1-3 kunnes kaikki verkko-osoitteet ovat omilla riveillään\n\t4. Klikkaa latausnappia ohjelman vasemmassa alalaidassa\n\t5. Ohjelman pitäisi nyt jäätyä, jos kaikki on kunnossa. Kun verkko-osoitteet katoavat ohjelman syöttökentästä, kaikki videot on ladattu.");
