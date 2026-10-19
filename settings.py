import tkinter as tk

def run(parent, theme):
    thing = tk.Toplevel(parent, bg=theme["Colours"]["Base"])
    thing.title("Settings")
    thing.grab_set()
    thing.transient(parent)
    thing.geometry("600x800")
    thing.resizable(False, False)

    tk.Label(thing, text="Theme", bg=theme["Colours"]["Base"], fg=theme["Colours"]["Text"], font=("Arial", 24)).grid(row=1, column=1,)