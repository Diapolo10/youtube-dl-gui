import os
import subprocess
from pathlib import Path

curdir = Path(__file__).parent

try:
    subprocess.call([str(curdir / "pip_auto_update.bat")])
    #os.chdir("..\\src")
    #filepath = os.path.join(os.getcwd(), "..", "src", "main.py")
    filepath = curdir.parent / "src" / "main.py"
    subprocess.call(["python", str(filepath)], cwd=str(filepath.parent))

except Exception as e:
    with open("error.log", 'a') as f:
        f.write(f"{curdir}\n")
        f.write(f"{e}\n")
        f.write(f"\n{'='*20}\n\n")
