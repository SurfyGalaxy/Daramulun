import json
import sys
import tkinter as tk
from pathlib import Path

import audio
import helpers
import playlist_seeker

def crash():
    import crashed
    crashed.crash_window(main, crash_messages)
    sys.exit(1)

main = tk.Tk()
main.geometry("600x300")
main.resizable(False, False)
crash_messages = []

playlists = playlist_seeker.music("./Playlists").scan()

if not Path("./settings.json").is_file():
    crash_messages.append("Missing settings.json (is it in the same directory level?)")
if not Path("./theme.json").is_file():
    crash_messages.append("Couldn't find theme.json")

if crash_messages:
    crash()

with open("theme.json") as f:
    themes = json.load(f)
with open("settings.json") as f:
    settings = json.load(f)

if not any(theme["Name"] == settings["Theme"] for theme in themes):
    crash_messages.append(f"Theme '{settings["Theme"]}' not found in theme.json")
    crash()

main.mainloop()