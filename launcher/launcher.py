import subprocess
import requests
from pathlib import Path

curdir = Path(__file__).parent
rootdir = curdir.parent

try:
    # Update all pip packages
    subprocess.call([str(curdir / "pip_auto_update.bat")])

    # Check version
    url = r"https://raw.githubusercontent.com/Diapolo10/youtube-dl-gui/gramps/VERSION"
    req = requests.get(url)
    github_version = req.text.strip()
    with open(rootdir / "VERSION") as f:
        local_version = f.read().strip()

    if local_version == github_version:
        print("Using latest version")
    else:
        subprocess.call(["git clone -b gramps --single-branch 'https://github.com/Diapolo10/youtube-dl-gui'"], cwd=str(rootdir.parent))

    # Launch the program
    filepath = rootdir / "src" / "main.pyw"
    subprocess.Popen(["pythonw", str(filepath)], cwd=str(filepath.parent))

except Exception as e:
    with open("error.log", 'a') as f:
        f.write(f"{curdir}\n")
        f.write(f"{e}\n")
        f.write(f"\n{'='*20}\n\n")

