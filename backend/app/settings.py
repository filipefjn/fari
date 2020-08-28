
settings = {
    "media_dir": "/srv/library/", # must be an absolute path
    "file_regex": r'((\.mp3)|(\.flac))$',
    "file_tags": [ # TODO remove file_tags
        "tracknumber",
        "tracktitle",
        "album",
        "albumartist",
        "artist",
        "year",
        "discnumber",
        "genre"
    ],
    "metadata_tags": [
        "tracknumber",
        "tracktitle",
        "album",
        "albumartist",
        "artist",
        "year",
        "discnumber",
        "genre"
    ],
    "metadata_tags_to_song_model": {
        "tracknumber": "tracknumber",
        "tracktitle" : "tracktitle",
        "album"      : "album_name",
        "albumartist": "albumartist",
        "artist"     : "artist",
        "year"       : "year",
        "discnumber" : "discnumber",
        "genre"      : "genre"
    }
}
