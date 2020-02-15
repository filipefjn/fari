from .. import db
from .models import *
from ..settings import settings
import music_tag
import os
import re
import random
import hashlib
from base64 import b64decode, b64encode

def gen_id(base_str):
    # TODO improve this
    h = str(base_str) + str(random.randint(100000, 999999))
    h = hashlib.sha1( h.encode("ascii") )
    return b64encode( h.digest() ).decode('ascii')

def hard_remake_library():
    # delete all songs from database
    SongModel.query.delete()
    db.session.commit()

    # go through all songs, read their tags and write to the database
    # via recursive function
    def recursive_search(currentPath):
        if not os.path.isfile(currentPath):
            subfolders = []
            files = []
            dir_content = os.listdir(currentPath)
            for item in dir_content:
                if os.path.isdir(os.path.join(currentPath, item)):
                    subfolders.append(item)
                else:
                    if "file_regex" in settings and re.search(settings["file_regex"], item) is not None:
                        files.append(item)
            songs_found = 0
            for file in files:
                file_absolute_path = os.path.join(currentPath, file)
                file_tags = music_tag.load_file(file_absolute_path)
                song = SongModel(
                    id=gen_id(str(file_tags["tracktitle"].value) + str(file_tags["artist"].value)),
                    path=os.path.join(currentPath, file).replace(settings["media_dir"], "/", 1),
                    enabled=True,
                    tracknumber=file_tags["tracknumber"].value,
                    tracktitle=file_tags["tracktitle"].value,
                    artist=file_tags["artist"].value,
                    album=file_tags["album"].value
                )
                db.session.add(song)
                db.session.commit()
                songs_found += 1
            for subfolder in subfolders:
                songs_found += recursive_search(os.path.join(currentPath, subfolder))
            return songs_found
        return 0

    media_dir = os.path.join(settings["media_dir"], "")
    songs_found = recursive_search(media_dir)

    # return the amount of songs found
    return {
        "songs_found": songs_found
    }

