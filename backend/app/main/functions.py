from .. import db
from .models import *
from ..settings import settings
import music_tag
import os
import re
import random
import hashlib
import json

def gen_id(base_str):
    h = str(base_str) + str(random.randint(100000, 999999))
    h = hashlib.sha1(h.encode("ascii"))
    return h.hexdigest()

def create_fari_file(song_id):
    # find file in database
    song_row = SongSchema().dump(SongModel.query.get(song_id))
    fari_file_content = {}
    fari_file_content["id"] = song_row["id"]
    fari_file_content["enabled"] = song_row["enabled"]

    # generate fari file path
    song_path = re.sub(r"^/", r"", song_row["path"])
    fari_file_path = os.path.join(settings["media_dir"], song_path) + ".fari"

    # create fari file
    with open(fari_file_path, "w") as file:
        # write file info in json
        file.write(json.dumps(fari_file_content))

    return fari_file_content

def remake_library():
    # delete all songs from database
    SongModel.query.delete()
    db.session.commit()

    # go through all songs, read their tags and write to the database
    # via recursive function
    def recursive_search(current_path):

        # function values
        songs_found = 0
        fari_files_found = 0
        fari_files_created = 0

        # check if current path is a directory (not a file)
        if not os.path.isfile(current_path):
            subfolders = []
            files = []
            dir_content = os.listdir(current_path)

            # get files and subfolders
            for item in dir_content:
                if os.path.isdir(os.path.join(current_path, item)):
                    subfolders.append(item)
                else:
                    if "file_regex" in settings and re.search(settings["file_regex"], item) is not None:
                        files.append(item)

            # files loop
            for file in files:
                file_absolute_path = os.path.join(current_path, file)
                file_tags = music_tag.load_file(file_absolute_path)
                song_id = gen_id(str(file_tags["tracktitle"].value) + str(file_tags["artist"].value))
                song = SongModel(
                    id=song_id,
                    path=os.path.join(current_path, file).replace(settings["media_dir"], "/", 1),
                    enabled=True,
                    tracknumber=file_tags["tracknumber"].value,
                    tracktitle=file_tags["tracktitle"].value,
                    artist=file_tags["artist"].value,
                    album=file_tags["album"].value
                )
                # check for .fari file
                fari_file_absolute_path = file_absolute_path + ".fari"
                fari_file_exists = os.path.exists(fari_file_absolute_path)

                # if .fari file exists, extract info from it
                if fari_file_exists:
                    with open(fari_file_absolute_path, "r") as fari_file:
                        fari_file_content = json.loads(fari_file.read())
                        if "id" in fari_file_content:
                            song_id = fari_file_content["id"]
                            song.id = fari_file_content["id"]
                        if "enabled" in fari_file_content:
                            song.enabled = fari_file_content["enabled"]
                        fari_files_found += 1

                # insert song into the database
                db.session.add(song)
                db.session.commit()
                songs_found += 1

                # if .fari file does not exist, create one
                if not fari_file_exists:
                    create_fari_file(song_id)
                    fari_files_created += 1

            # subfolders loop
            for subfolder in subfolders:
                subfolder_result = recursive_search(os.path.join(current_path, subfolder))
                songs_found += subfolder_result["songs_found"]
                fari_files_found += subfolder_result["fari_files_found"]
                fari_files_created += subfolder_result["fari_files_created"]

        return {
            "songs_found": songs_found,
            "fari_files_found": fari_files_found,
            "fari_files_created": fari_files_created
        }

    media_dir = os.path.join(settings["media_dir"], "")
    result = recursive_search(media_dir)
    return result

