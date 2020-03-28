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
    fari_file_content["tags"] = []
    for tag in song_row["tags"]:
        fari_file_content["tags"].append(tag["name"])

    # generate fari file path
    song_path = re.sub(r"^/", r"", song_row["path"])
    fari_file_path = os.path.join(settings["media_dir"], song_path) + ".fari"

    # create fari file
    with open(fari_file_path, "w") as file:
        # write file info in json
        file.write(json.dumps(fari_file_content))

    return fari_file_content

def get_or_create_tag(tag_name):
    # check if the tag already exists
    queried_tag = TagModel.query.filter(TagModel.name == tag_name).first()
    if queried_tag:
        return queried_tag
    else:
        created_tag = TagModel(
            name=tag_name
        )
        db.session.add(created_tag)
        db.session.commit()
        return created_tag

def delete_artists_and_albums():
    # set all songs' album to null
    SongModel.query.update({"album_id": None})
    db.session.commit()
    # delete all artists and albums from database
    AlbumModel.query.delete()
    ArtistModel.query.delete()
    db.session.commit()


def remake_artists_and_albums():
    delete_artists_and_albums()

    artists_found = 0
    albums_found = 0

    for song in SongModel.query.all():
        # get song's artist name
        song_artist_name = song.albumartist
        if not song_artist_name:
            song_artist_name = song.artist
        if not song_artist_name:
            song_artist_name = "Unknown artist"

        # look for artist
        song_artist = ArtistModel.query.filter(ArtistModel.name.ilike(song_artist_name)).first()
        if not song_artist:
            # create a new artist
            song_artist = ArtistModel(
                name=song_artist_name
            )
            db.session.add(song_artist)
            db.session.commit()
            artists_found += 1

        # get song's album name
        song_album_name = song.album_name
        if not song_album_name:
            song_album_name = "Unknown album"

        # check if album exists
        found_album = False
        for album in song_artist.albums:
            if album.name.lower() == song_album_name.lower():
                found_album = True
                song.album = album
                db.session.commit()
                break

        # if does not, create it
        if not found_album:
            song_album = AlbumModel(
                name=song_album_name,
                artist=song_artist,
                year=song.year
            )
            song.album = song_album
            db.session.commit()
            albums_found += 1

    return {
        "artists_found": artists_found,
        "albums_found": albums_found
    }


def remake_library():
    # delete all songs and tags from database
    for song in SongModel.query.all():
        db.session.delete(song)
    for tag in TagModel.query.all():
        db.session.delete(tag)
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
                    albumartist=file_tags["albumartist"].value,
                    artist=file_tags["artist"].value,
                    album_name=file_tags["album"].value,
                    year=file_tags["year"].value
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
                        if "tags" in fari_file_content:
                            tag_list = []
                            for tag_name in fari_file_content["tags"]:
                                song.tags.append(get_or_create_tag(tag_name))
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

