import subprocess
from pathlib import Path

curdir = Path(__file__).parent

with open(curdir / "error.log", 'a') as f:
    f.write(f"File ran!\n")

try:
    subprocess.call([str(curdir / "pip_auto_update.bat")])
    with open(curdir / "error.log", 'a') as f:
        f.write("Auto-updater found and executed\n")

    filepath = curdir.parent / 'src' / 'main.py'
    with open(curdir / "error.log", 'a') as f:
        f.write(f"{filepath}\n")
    subprocess.call(['python.exe', str(filepath)], cwd=str(filepath.parent))

except Exception as e:
    with open(curdir / "error.log", 'a') as f:
        f.write(f"{e}\n")

with open(curdir / "error.log", 'a') as f:
    f.write(f"\n{'='*20}\n\n")
