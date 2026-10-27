import os
import random
import time

from mutagen import File
import pygame

pygame.init()
pygame.mixer.init()
MUSIC_END = pygame.USEREVENT + 1

class AudioPlayer():
    def __init__(self):
        self.queue = ["/home/surfygalaxy/.steam/debian-installation/steamapps/music/Celeste Original Soundtrack/Lena Raine - Celeste Original Soundtrack - 01 Prologue.mp3",
"/home/surfygalaxy/.steam/debian-installation/steamapps/music/Celeste Original Soundtrack/Lena Raine - Celeste Original Soundtrack - 02 First Steps.mp3"]
        self.volume = 0.5
        self.play = True
        self.loop = True
        self.autoplay = True
        self.started = False
        self.shuffle = True
        self.start_time = None
        self.offset = 0
        self.pause_time = None
        self.time = 0
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
                    self.start_time = time.monotonic_ns()
                    if not self.shuffle:
                        self.playing = self.queue.pop(0)
                    else:
                        self.playing = self.queue.pop(random.randrange(len(self.queue)))
                    pygame.mixer.music.load(self.playing)
                    pygame.mixer.music.play()
                    self.duration = File(self.playing).info.length
                    print(f"Playing {self.playing}")
                    self.start_time = time.monotonic_ns()
                    self.offset = 0
                    if self.loop:
                        self.queue.append(self.playing)
                else:
                    print("Already playing music")
    
    def tick(self):
        """Update volume / pause"""
        pygame.mixer.music.set_volume(self.volume)
        if self.play:
            pygame.mixer.music.unpause()
            if self.pause_time is not None:
                self.offset += time.monotonic_ns() - self.pause_time
                self.pause_time = None
        elif not self.play:
            if self.pause_time is None:
                self.pause_time = time.monotonic_ns()
            pygame.mixer.music.pause()
        if self.started and pygame.mixer.music.get_busy():
            if self.offset is not None:
                print(f"""Total: {time.monotonic_ns() - self.start_time - self.offset}
Start: {self.start_time}
Offset: {self.offset}
Time: {time.monotonic_ns()}
""")
                self.time = (time.monotonic_ns() - self.start_time - self.offset) / 1000000000
            else:
                self.time = (time.monotonic_ns() - self.start_time) / 1000000000
    
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
        self.start_time = time.monotonic_ns()