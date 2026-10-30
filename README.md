# Daramulun
<!--Sleep deprived README writing lessgo-->
Daramulun is a local music player for <!--shockingly--> music files. Only Linux <!--the best os--> supported for now.

## Installation:
1. Download the latest <!--or another one i'm not ur boss--> release of Daramulun from <!--you use github you alr know ts--><a href="https://github.com/SurfyGalaxy/Daramulun/releases">the releases tab</a>
2. Extract Daramulun
3. Set up the folder structure as instructed below <!--pls read our schizophrenic file layout-->

## Changing settings
Settings are changed via `settings.json`

## File setup + Adding new playlists/songs
<!--Ahh no I need ASCII skills-->
Immediately after extracting, at the top level, you should have `Daramulun-vx.y.z`, `_internal` and `Assets` <!--if we ship the right thing :sob:-->, with `Assets` containing 2 themes.

To add a playlist, add a directory called `Playlists`, and inside add `Index.json`.

`Index.json` should appear like:

```json
[
    "foo",
    "bar"
]
```

where `foo` and `bar` are both playlists.

Then, inside `Playlists`, add directories with the exact same names as in `Index.json`. At this point you should have

```
(Root directory)
    -> Daramulun-vx.y.z (executable)
    -> Assets (directory)
    -> theme.json
    -> settings.json
    -> _internal (directory)
    -> Playlists (directory)
        -> Index.json (json file)
        -> foo (directory)
        -> bar (directory)
```

Inside your playlist directories (we will use `foo` in these examples), create `List.json`
<!--meow-->
<!--:3-->
`List.json` follows the following schema:

```json
{
    "Image": "<str> path of the album image to use, relative to foo (as if foo was ./), do not add ./. Or null if no image supplied",
    "Songs": [
        {
            "Name": "<str> name of song",
            "Artist": "<str> artist(s)' name",
            "Path": "<str> path of the song, uses same system as image"
        }
    ]
}
```
The `Songs` list can accept infinite songs, and the play order (if without shuffle) is determined by the ordering of songs in the list.
<!--mrrp-->
<!--yes we a furry how'd u tell (also obligatory transfem sounds)-->
Then add your songs to the same directory as `List.json`, leaving you with:

```
(Root directory)
    -> Daramulun-vx.y.z (executable)
    -> Assets (directory)
    -> settings.json
    -> theme.json
    -> _internal (directory)
    -> Playlists (directory)
        -> Index.json
        -> foo (directory)
            -> List.json
            -> some_song.mp3
            -> another_song.mp3
        -> bar (directory)
            -> List.json
            -> cover.png
            -> song_that_is_an_example.mp3
```
<!--yes theme.json and settings.json switch places, no we wont fix it-->
### Example Index.json
```json
[
    "foo",
    "bar"
]
```

### Example List.json
`foo` Playlist:
```json
{
    "Image": null,
    "Songs": [
        {
            "Name": "Some Song",
            "Artist": "Foo",
            "Path": "some_song.mp3"
        },
        {
            "Name": "The song with a different filename",
            "Artist": "Foo",
            "Path": "another_song.mp3"
        }
    ]
}
``` 
<!--Honey wake up The song with a different filename by Foo just dropped on spotify-->
`bar`'s `"Image":` would be `"cover"`

## Making new themes

If you want to give the player a new coat of paint, start by looking inside `theme.json`

Every theme starts with a `Name`, then has `Colours` <!--woah das crazy-->
The colours are used as follows:

<!--Yes this table is horribly aligned, that's the fun (also first time using a table)-->
| Name | Usage |
| - | - |
| Green | The progress bar for time played |
| Base | Background of app |
| Text | Song name + Time display |
| Subtext 0 | Artist name |
| Subtext 1 | Playlist name |
| Overlay 2 | Progress bar background |
<!--we used lolcat names for these-->

Then there is the `Fonts`
This should be fairly simple, as the keys are where they are used.

Once you have updated `theme.json`, you need to go to `Assets`, and create a directory with the same name as the `Name` key in `theme.json`

Inside there, you will need 7 buttons with these exact file names:
- Next Playlist.png
- Pause.png
- Play.png
- Rewind.png
- Shuffle Off.png
- Shuffle On.png
- Skip.png

Once you have that, you have successfully made a new theme which you can use in Daramulun <!--here's a gold star-->

Made with <3 by Ashley

<!-- :3 -->
