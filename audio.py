import time

from mutagen import File
import pygame

import helpers

pygame.init()
pygame.mixer.init()
MUSIC_END = pygame.USEREVENT + 1

class Player():
    def __init__(self):
        self.queue = []
        self.volume = 0.5
        self.play = True
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.set_endevent(MUSIC_END)

    def new_song(self):
        """Play the next song in the queue"""
        if not self.queue:
            print("Nothing to play")
            return (False, 1)
        elif not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.queue[0])
            pygame.mixer.music.play()
            print(f"Playing {self.queue[0]}")
            self.playing = self.queue.pop(0)
            self.duration = File(self.playing).info.length
        else:
            print("Already playing music")
    
    def tick(self):
        """Update volume / pause"""
        pygame.mixer.music.set_volume(self.volume)
        if self.play:
            pygame.mixer.music.unpause()
        elif not self.play:
            pygame.mixer.music.pause()
        self.time = pygame.mixer.music.get_pos() / 1000
    
    def query(self) -> dict:
        """Get info about what's playing"""
        return {
            "File": self.playing,
            "Played": self.time,
            "Volume": self.volume,
            "Paused": not self.play,
            "Duration": self.duration
        }