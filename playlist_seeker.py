import json
from pathlib import Path

class music:
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.playlists = []
    
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

        return len(self.playlists)