import subprocess
import sys

try:
    if sys.platform == "darwin":
        subprocess.Popen(["open", "-a", "Calculator"])
        print("[RCE] macOS Calculator opened!")
    elif sys.platform == "win32":
        subprocess.Popen(["calc.exe"])
        print("[RCE] Windows Calculator opened!")
    else:
        subprocess.Popen(["gnome-calculator"])
        print("[RCE] Linux Calculator opened!")
except Exception as e:
    print(f"Error: {e}")
