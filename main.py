import json
import sys
import tkinter as tk
from pathlib import Path

import pygame

import audio
import helpers
import playlist_seeker
import images

val = []
def new_playlist(assets):
    global val
    data = scheduler.list_songs()
    if isinstance(data, str):
        crash_messages = [data]
        crash()
    
    songs = data[0]
    if songs["Image"] is not None:
        image = images.process(data[1] / songs["Image"], 180)
    else:
        image = images.process(Path("./Assets/Placeholder.png"), 180)
    val.append(image)
    
    assets["Image"].config(image=image)

    return assets

def pause():
    if player.play:
        player.play = False
        assets["Play"].config(image=images.process(Path("./Assets/" + active_theme["Name"] + "/Play.png"), 90))
    else:
        player.play = True
        assets["Play"].config(image=images.process(Path("./Assets/" + active_theme["Name"] + "/Pause.png"), 90))

def skip():
    player.skip()

def crash():
    import crashed
    crashed.crash_window(main, crash_messages)
    sys.exit(1)

main = tk.Tk()
main.geometry("600x300")
main.resizable(False, False)
crash_messages = []

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

active_theme = next((theme for theme in themes if theme["Name"] == settings["Theme"]), f"Theme '{settings["Theme"]}' not found in theme.json")

if isinstance(active_theme, str):
    crash_messages = [active_theme]
    crash()

scheduler = playlist_seeker.music(settings["Music Directory"])
scanned = scheduler.scan()
if isinstance(scanned, str):
    crash_messages = [scanned]
    crash()

main.config(bg=active_theme["Colours"]["Base"])
assets = {
    "Image": tk.Label(main),
    "Canvas": tk.Canvas(main, width=390, height=10, bg=active_theme["Colours"]["Overlay 2"]),
    "Song Name": tk.Label(main, bg=active_theme["Colours"]["Base"], fg=active_theme["Colours"]["Text"], font=(active_theme["Fonts"]["Title"], 28), text="AAAAAAAAAAAAA"), 
    "Artist Name": tk.Label(main, bg=active_theme["Colours"]["Base"], fg=active_theme["Colours"]["Subtext 0"], font=(active_theme["Fonts"]["Artist"], 16), text="AAAAAAAAAA"),
    "Playlist Name": tk.Label(main, bg=active_theme["Colours"]["Base"], fg=active_theme["Colours"]["Subtext 1"], font=(active_theme["Fonts"]["Playlist"], 14), text="AAAAAAA"),
    "Time": tk.Label(main, bg=active_theme["Colours"]["Base"], fg=active_theme["Colours"]["Text"], font=(active_theme["Fonts"]["Time"]), text="XX:XX / XX:XX"),
    "Play": tk.Button(main, image=images.process(Path("./Assets/" + active_theme["Name"] + "/Pause.png"), 90), command=pause),
    "Skip": tk.Button(main, image=images.process(Path("./Assets/" + active_theme["Name"] + "/Skip.png"), 90), command=skip),
    "New Playlist": tk.Button(main, image=images.process(Path("./Assets/" + active_theme["Name"] + "/Next Playlist.png"), 90), command=lambda: playlists_new(assets)),
    "Shuffle": tk.Button(main, image=images.process(("./Assets/" + active_theme["Name"] + "/Shuffle On.png"), 90), command=shuffle)
}
percent_left = 0.0
assets["Progress bar"] = assets["Canvas"].create_rectangle(0, 0, int(percent_left * 390), 11, fill=active_theme["Colours"]["Green"])

assets["Image"].place(x=10, y=10)

assets["Canvas"].place(x=200, y=140)

assets["Song Name"].place(x=200, y=10)
assets["Artist Name"].place(x=200, y=60)
assets["Playlist Name"].place(x=200, y=94)
assets["Time"].place(x=395 - assets["Time"].winfo_reqwidth() / 2, y=160)
assets["Play"].place(x=132, y=200)
assets["Skip"].place(x=255, y=200)
assets["New Playlist"].place(x=500, y=200)

def playlists_new(assets):
    scheduler.next_playlist()
    data = scheduler.list_songs()
    assets = new_playlist(assets)
    return (assets, data)

assets, data = playlists_new(assets)

assets["Playlist Name"].config(text=str(data[1]).split('/')[1])

queue = []
for song in data[0]["Songs"]:
    queue.append("./" + str(data[1]) + '/' + song["Path"])

player = audio.AudioPlayer()

player.queue = queue

player.new_song()

def tick():
    global percent_left
    for event in pygame.event.get():
        if event.type == audio.MUSIC_END:
            if player.autoplay:
                player.new_song()
    
    player.tick()
    update = player.query()

    assets["Time"].config(text=helpers.fmt(update["Time"]) + " / " + helpers.fmt(update["Duration"]))
    percent_left = update["Time"] / update["Duration"]

    assets["Canvas"].coords(assets["Progress bar"], 0, 0, int(percent_left * 390), 11,)
    
    

    for song in data[0]["Songs"]:
        if song["Path"] == update["File"].split('/')[-1]:
            meta = song
            break
    
    assets["Song Name"].config(text=meta["Name"])
    assets["Artist Name"].config(text=meta["Artist"])

    main.after(1, tick)

tick()

main.mainloop()