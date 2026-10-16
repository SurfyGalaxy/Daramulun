import os
import time

from mutagen import File
import pygame

import helpers

pygame.init()
pygame.mixer.init()
MUSIC_END = pygame.USEREVENT + 1

class AudioPlayer():
    def __init__(self):
        self.queue = ["/home/surfygalaxy/.steam/debian-installation/steamapps/music/Celeste Original Soundtrack/Lena Raine - Celeste Original Soundtrack - 01 Prologue.mp3",
"/home/surfygalaxy/.steam/debian-installation/steamapps/music/Celeste Original Soundtrack/Lena Raine - Celeste Original Soundtrack - 02 First Steps.mp3"]
        self.volume = 0.5
        self.play = True
        self.loop = False
        self.autoplay = True
        self.started = False
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.set_endevent(MUSIC_END)

    def new_song(self):
        """Play the next song in the queue"""
        if not self.queue:
            print("Nothing to play")
            return (False, 1)
            
        elif not pygame.mixer.music.get_busy():
            self.started = True
            if os.path.isfile(self.queue[0]) and self.queue[0].endswith(".mp3"):
                if not pygame.mixer.music.get_busy():
                    self.playing = self.queue.pop(0)
                    pygame.mixer.music.load(self.playing)
                    pygame.mixer.music.play()
                    print(f"Playing {self.playing}")
                    self.duration = File(self.playing).info.length
                    if self.loop:
                        self.queue.append(self.playing)
                else:
                    print("Already playing music")
    
    def tick(self):
        """Update volume / pause"""
        pygame.mixer.music.set_volume(self.volume)
        if self.play:
            pygame.mixer.music.unpause()
        elif not self.play:
            pygame.mixer.music.pause()
        if self.started:
            self.time = pygame.mixer.music.get_pos() / 1000
    
    def query(self) -> dict:
        """Get info about what's playing"""
        return {
            "File": self.playing,
            "Time": self.time,
            "Volume": self.volume,
            "Paused": not self.play,
            "Duration": self.duration,
            "Queue": self.queue
        }
    
    def add_queue(self, path: str, position: int | None = None) -> int:
        """Add a song to the queue
        
        Returns a 1-indexed queue position"""
        if position is None:
            self.queue.append(path)
            print(f"Adding {path} ({len(self.queue)} in queue)")
            return len(self.queue)
        else:
            self.queue.insert(position, path)
            print(f"Adding {path} to position {position}")
            return position + 1
    
    def skip(self):
        print("Skipping")
        pygame.mixer.music.stop()
        if not self.autoplay:
            self.new_song()
    
    def rewind(self):
        print("Restarting song")
        pygame.mixer.music.rewind()

player = AudioPlayer()
player.new_song()

while True:
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            if player.autoplay:
                player.new_song()
    player.tick()
    print(player.query())
    time.sleep(1)