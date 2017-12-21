import os
import subprocess

with open("error.log", 'a') as f:
        f.write(f"{os.getcwd()}\n")

try:
    subprocess.call(["pip_auto_update.bat"])
    with open("error.log", 'a') as f:
        f.write("Auto-updater found and executed\n")
    #os.chdir("..\\src")
    filepath = os.path.join(os.getcwd(), "..", "src", "main.py")
    subprocess.call([filepath])
    
except Exception as e:
    with open("error.log", 'a') as f:
        f.write(f"{e}\n")
        
with open("error.log", 'a') as f:
    f.write(f"\n{'='*20}\n\n")
    
