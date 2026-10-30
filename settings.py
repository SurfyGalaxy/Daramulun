import json
import tkinter as tk
from tktooltip import ToolTip

def answers():
    pass

def undo():
    thing.destroy()

def run(parent, theme):
    thing = tk.Toplevel(parent)
    thing.title("Settings")
    thing.grab_set()
    thing.transient(parent)

    theme_label = tk.Label(thing, text="Theme")
    theme_label.grid(row=0, column=0)
    ToolTip(theme_label, msg="The colour theme to use for the player")
    
    with open("theme.json") as f:
        themes = json.load(f)
    theme_list = [theme["Name"] for theme in themes]
    print(theme_list)

    theme_answer = tk.StringVar()
    theme_answer.set(theme["Name"])
    theme_selector = tk.OptionMenu(thing, theme_answer, *theme_list)
    theme_selector.grid(row=0, column=3)

    cancel = tk.Button(thing, text="Cancel", command=undo)
    submit = tk.Button(thing, text="Apply", command=answers)
    submit.grid(row=5, column=1)
    cancel.grid(row=5, column=2)