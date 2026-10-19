import json
from pathlib import Path

class music:
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.active_playlist = None
        self.playlists = []
        self.playlist_index = -1
    
    def scan(self) -> list | str:
        """Rechecks the directory, returns sorted list of playlist paths"""
        index_exists = False
        playlists = []
        for playlist in self.directory.iterdir():
            if not playlist.is_dir():
                if playlist.name != "Index.json":
                    return f"An entry ({playlist.name}) isn't a directory"
                index_exists = True
            else:
                playlists.append(playlist)
        
        if not index_exists:
            return f"Index.json was not found in {self.directory.name}"
        
        with open(self.directory / "Index.json") as f:
            order = json.load(f)
        
        sort = []
        for item in order:
            result = next((p for p in playlists if p.name == item), None)
            if result is None:
                sort = []
                return f"One playlist not in Index.json (Directory Missing)"
            sort.append(result)
        
        if len(sort) != len(playlists):
            return f"One playlist not in Index.json (Reference Missing)"

        self.playlists = sort

        return self.playlists

    def next_playlist(self):
        self.playlist_index += 1
        self.active_playlist = self.playlists[self.playlist_index % len(self.playlists)]
        return
    
    def list_songs(self):
        if not (self.active_playlist / "List.json").is_file():
            return f"{self.active_playlist.name} ({self.active_playlist.absolute()}) Is missing List.json"
        
        with open(self.active_playlist / "List.json") as f:
            return (json.load(f), self.active_playlist)