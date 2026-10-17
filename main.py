import tkinter as tk

import helpers
import audio
import playlist_seeker

main = tk.Tk()
main.geometry("600x300")
main.resizable(False, False)

playlists = playlist_seeker.music("./Playlists").scan()

main.mainloop()