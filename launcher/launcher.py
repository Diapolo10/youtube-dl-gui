import os
import sys
import subprocess
import base64
import requests
from pathlib import Path

curdir = Path(__file__).parent
rootdir = curdir.parent

try:
    # Update all pip packages
    subprocess.call([str(curdir / "pip_auto_update.bat")])

    # Check version
    url = r"https://raw.githubusercontent.com/Diapolo10/youtube-dl-gui/nightly/VERSION"
    req = requests.get(url)
    github_version = req.text.strip()
    with open(rootdir / "VERSION") as f:
        local_version = f.read().strip()

    if local_version == github_version:
        pass
    else:
        pass #TODO: Update repository

    # Launch the program
    filepath = rootdir / "src" / "main.py"
    subprocess.Popen(["python", str(filepath)], cwd=str(filepath.parent))

except Exception as e:
    with open("error.log", 'a') as f:
        f.write(f"{curdir}\n")
        f.write(f"{e}\n")
        f.write(f"\n{'='*20}\n\n")

sys.exit()
